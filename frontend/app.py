
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
from gtts import gTTS
import tempfile


def contains_offensive_language(text):
    offensive_words = [
        "badword1", "badword2", "idiot", "stupid", "hate", "urât", "prost", "jignire"
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in offensive_words)

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



# Toggle for offensive language filter
filter_enabled = st.checkbox("Block offensive language", value=True)
# Toggle for GPT safety prompt
gpt_safety_enabled = st.checkbox("Instruct GPT to refuse inappropriate requests", value=True)

query = st.text_input("Ce temă sau context te interesează?")

if query:
    if filter_enabled and contains_offensive_language(query):
        st.error("Vă rugăm să folosiți un limbaj adecvat. Recomandările nu pot fi generate pentru mesaje ofensatoare.")
        st.stop()
    with st.spinner("Caut recomandări..."):
        recommendations = retriever.semantic_search(query)
        if not recommendations:
            st.warning("Nu am găsit recomandări pentru această temă.")
        else:
            prompt = "Recomandă o carte pe baza următoarelor rezultate:\n"
            for rec in recommendations:
                prompt += f"- {rec['title']}: {', '.join(rec['themes'])}\n"
            prompt += f"\nUtilizatorul caută: {query}\nRăspunde conversațional, cu titlul propus."
            if gpt_safety_enabled:
                prompt += "\nDacă mesajul utilizatorului conține limbaj ofensator sau nepotrivit, răspunde politicos că nu poți oferi recomandări."

            # Inject block message if offensive and filter is enabled
            if filter_enabled and contains_offensive_language(prompt):
                st.error("Request blocked due to offensive content. [ERR_CODE: OFFENSIVE]")
                st.stop()

            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.subheader("Recomandare AI:")
            st.write(answer)

            recommended_title = recommendations[0]["title"]
            summary = chatbot.get_summary_by_title(recommended_title)
            st.subheader(f"Rezumat complet pentru '{recommended_title}':")
            st.write(summary)

            # Text-to-speech button
            tts_text = f"Recomandare: {answer}\nRezumat: {summary}"
            if st.button("Ascultă recomandarea și rezumatul"):
                tts = gTTS(tts_text, lang='ro')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, format='audio/mp3')
