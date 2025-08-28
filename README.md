# Smart Librarian – AI with RAG + Tool Completion

This project provides an AI chatbot that recommends books based on themes and context, using a database of summaries, semantic search (RAG), and GPT integration.

## Structure
- `backend/` – Code for processing, RAG, chatbot, and book summaries database
- `frontend/` – Streamlit interface for user interaction


## How to Run (Step-by-Step)
1. Create and activate the virtual environment, then install dependencies:
	- Run `setup.ps1` in PowerShell, or manually:
	  ```powershell
	  python -m venv venv
	  .\venv\Scripts\Activate.ps1
	  pip install -r requirements.txt
	  ```
2. Add your OpenAI API key to a file named `OPENAI_API_KEY` in the `backend` folder.
3. Populate the vector database:
	```powershell
	python backend/load_books_to_chromadb.py
	```
4. Run the chatbot in CLI (optional):
	```powershell
	python backend/chatbot.py
	```
5. Start the frontend (Streamlit web app):
	```powershell
	streamlit run frontend/app.py
	```
6. Interact with the AI librarian in your browser (usually at http://localhost:8501).

## Key Files
- `backend/book_summaries.json` – Book summaries and key themes
- `backend/chatbot.py` – RAG + GPT + tool pipeline
- `frontend/app.py` – Web interface

## Requirements
- Python 3.8+
- OpenAI API key

## Author
lukapopovici
