# Offensive language filter for CLI
# Add this function to backend/chatbot.py and use before sending prompt to LLM

def contains_offensive_language(text):
    # Simple list, can be extended
    offensive_words = [
        "badword1", "badword2", "idiot", "stupid", "hate", "urât", "prost", "jignire"
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in offensive_words)

# In CLI pipeline, before semantic_search and LLM prompt:
if __name__ == "__main__":
    OPENAI_API_KEY = read_api_key()
    query = input("Ce temă sau context te interesează? ")
    if contains_offensive_language(query):
        print("Vă rugăm să folosiți un limbaj adecvat. Recomandările nu pot fi generate pentru mesaje ofensatoare.")
        sys.exit(0)
    recommendations = semantic_search(query)
    # ...existing code...
