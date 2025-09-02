# Smart Librarian – AI Book Recommender

## Project Structure

- `backend/` – Python Flask API server
  - `server.py` – main Flask server
  - `retriever.py`, `chatbot.py` – core logic
  - `book_summaries.json` – book data
- `frontend/` – HTML + JS frontend
  - `index.html` – main web interface
  - `style.css` – styles

## Setup & Run

1. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key:**
   - Place your key in a file named `OPENAI_API_KEY` in the project root.

4. **Run the Flask backend:**
   ```powershell
   python backend/server.py
   ```
   - The API will be available at `http://localhost:5000`

5. **Serve the frontend:**
   ```powershell
   cd frontend
   python -m http.server 8080
   ```
   - Open [http://localhost:8080](http://localhost:8080) in your browser.

## Usage

- Enter a theme/context or use the microphone button to speak your query.
- Click "Get Recommendation" to receive a book suggestion.
- View the summary and optionally listen to the recommendation via TTS.

## Endpoints

- `POST /recommend` – Get book recommendations
- `GET /summary?title=...` – Get full summary for a book
- `POST /tts` – Get TTS audio for recommendation/summary

## Requirements

See `requirements.txt` for all dependencies.
