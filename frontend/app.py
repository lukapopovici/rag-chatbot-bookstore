
import streamlit as st
import os
import sys

# Dynamically add backend folder to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)


import retriever
import chatbot
from openai import OpenAI


def read_api_key():
    key_path = os.path.join(backend_path, "OPENAI_API_KEY")
    try:
        with open(key_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        st.error(f"Error reading OpenAI API key: {e}")
        return None

OPENAI_API_KEY = read_api_key()

st.title("Smart Librarian – AI Book Recommender")
st.write("Caută cărți după temă/context și primește recomandări AI!")

query = st.text_input("Ce temă sau context te interesează?")

if query:
    with st.spinner("Caut recomandări..."):
        recommendations = retriever.semantic_search(query)
        if not recommendations:
            st.warning("Nu am găsit recomandări pentru această temă.")
        else:
            prompt = "Recomandă o carte pe baza următoarelor rezultate:\n"
            for rec in recommendations:
                prompt += f"- {rec['title']}: {', '.join(rec['themes'])}\n"
            prompt += f"\nUtilizatorul caută: {query}\nRăspunde conversațional, cu titlul propus."

            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.subheader("Recomandare AI:")
            st.write(answer)

            recommended_title = recommendations[0]["title"]
            st.subheader(f"Rezumat complet pentru '{recommended_title}':")
            st.write(chatbot.get_summary_by_title(recommended_title))
