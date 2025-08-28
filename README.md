# Smart Librarian – AI with RAG + Tool Completion

This project provides an AI chatbot that recommends books based on themes and context, using a database of summaries, semantic search (RAG), and GPT integration.

## Structure
- `backend/` – Code for processing, RAG, chatbot, and book summaries database
- `frontend/` – Streamlit interface for user interaction

## How to Run
1. Install dependencies: `openai`, `chromadb`, `streamlit`
2. Add your OpenAI key in the code or as an environment variable
3. Run the backend to populate the database
4. Start the frontend with `streamlit run frontend/app.py`

## Key Files
- `backend/book_summaries.json` – Book summaries and key themes
- `backend/chatbot.py` – RAG + GPT + tool pipeline
- `frontend/app.py` – Web interface

## Requirements
- Python 3.8+
- OpenAI API key

## Author
lukapopovici
