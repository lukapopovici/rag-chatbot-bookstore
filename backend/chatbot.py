import json
from backend.retriever import semantic_search
from openai import OpenAI

# Placeholder for your OpenAI API key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Tool: get_summary_by_title
def get_summary_by_title(title: str) -> str:
    """
    Return the full summary for a given book title from book_summaries.json.
    """
    with open("book_summaries.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for book in data["books"]:
            if book["title"].lower() == title.lower():
                return f"{book['title']}: {book['summary']}\nTeme: {', '.join(book['themes'])}"
    return "Titlul nu a fost găsit."

# Chatbot pipeline
if __name__ == "__main__":
    query = input("Ce temă sau context te interesează? ")
    recommendations = semantic_search(query)
    if not recommendations:
        print("Nu am găsit recomandări pentru această temă.")
    else:
        # Compose prompt for GPT
        prompt = "Recomandă o carte pe baza următoarelor rezultate:\n"
        for rec in recommendations:
            prompt += f"- {rec['title']}: {', '.join(rec['themes'])}\n"
        prompt += f"\nUtilizatorul caută: {query}\nRăspunde conversațional, cu titlul propus."

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
