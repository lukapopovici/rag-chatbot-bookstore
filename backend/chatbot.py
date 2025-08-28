
import json
import os
import sys
from retriever import semantic_search
from openai import OpenAI

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def read_api_key():
    key_path = os.path.join(get_project_root(), "OPENAI_API_KEY")
    try:
        with open(key_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading OpenAI API key: {e}")
        sys.exit(1)


# Tool: get_summary_by_title
def get_summary_by_title(title: str) -> str:
    summaries_path = os.path.join(os.path.dirname(__file__), "book_summaries.json")
    with open(summaries_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for book in data["books"]:
            if book["title"].lower() == title.lower():
                return f"{book['title']}: {book['summary']}\nTeme: {', '.join(book['themes'])}"
    return "Titlul nu a fost găsit."

# Chatbot pipeline
    offensive_words = [
        "badword1", "badword2", "idiot", "stupid", "hate", "urât", "prost", "jignire"
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in offensive_words)

if __name__ == "__main__":
    OPENAI_API_KEY = read_api_key()
    print("(Type 'safe' for GPT safety prompt, or 'unsafe' to skip)")
    gpt_safety = input("Enable GPT safety prompt? (safe/unsafe): ").strip().lower() == "safe"
    query = input("Ce temă sau context te interesează? ")
    if contains_offensive_language(query):
        print("Vă rugăm să folosiți un limbaj adecvat. Recomandările nu pot fi generate pentru mesaje ofensatoare.")
        sys.exit(0)
    recommendations = semantic_search(query)
    if not recommendations:
        print("Nu am găsit recomandări pentru această temă.")
    else:
        # Compose prompt for GPT
        prompt = "Recomandă o carte pe baza următoarelor rezultate:\n"
        for rec in recommendations:
            prompt += f"- {rec['title']}: {', '.join(rec['themes'])}\n"
        prompt += f"\nUtilizatorul caută: {query}\nRăspunde conversațional, cu titlul propus."
        if gpt_safety:
            prompt += "\nDacă mesajul utilizatorului conține limbaj ofensator sau nepotrivit, răspunde politicos că nu poți oferi recomandări."

        # Call GPT (OpenAI Chat API)
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        print("\nRecomandare AI:")
        print(answer)

        # Extract recommended title (simple heuristic: first title in answer)
        recommended_title = recommendations[0]["title"]
        print("\nRezumat complet:")
        print(get_summary_by_title(recommended_title))
