# PowerShell script to automate project setup and run all steps
# Save as run_all.ps1 and run in the project root

# Step 1: Create and activate venv, install dependencies
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Step 2: Check for API key
if (!(Test-Path backend/OPENAI_API_KEY)) {
    Write-Host "Please add your OpenAI API key to backend/OPENAI_API_KEY before continuing."
    exit 1
}

# Step 3: Populate vector database
python backend/load_books_to_chromadb.py

# Step 4: Run chatbot CLI (optional)
python backend/chatbot.py

# Step 5: Start frontend (Streamlit)
streamlit run frontend/app.py

Write-Host "Setup complete. Interact with the AI librarian in your browser (http://localhost:8501)."
