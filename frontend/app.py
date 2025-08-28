import streamlit as st
from backend.retriever import semantic_search
from backend.chatbot import get_summary_by_title
from openai import OpenAI

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

st.title("Smart Librarian – AI Book Recommender")
st.write("Caută cărți după temă/context și primește recomandări AI!")

query = st.text_input("Ce temă sau context te interesează?")

if query:
    with st.spinner("Caut recomandări..."):
        recommendations = semantic_search(query)
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
            st.write(get_summary_by_title(recommended_title))
