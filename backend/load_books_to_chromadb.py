import json
import os
import sys
from chromadb import Client
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

summaries_path = os.path.join(os.path.dirname(__file__), "book_summaries.json")
with open(summaries_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    books = data["books"]
texts = []
metadatas = []
for book in books:
    text = f"{book['title']}: {book['summary']}\nTeme: {', '.join(book['themes'])}"
    texts.append(text)
    metadatas.append({"title": book["title"], "themes": book["themes"]})
openai_client = OpenAI(api_key=read_api_key())
embeddings = openai_client.embeddings.create(
    input=texts,
    model="text-embedding-3-small"
).data
vectors = [e.embedding for e in embeddings]
chroma_client = Client()
collection = chroma_client.create_collection(name="books")
collection.add(
    embeddings=vectors,
    documents=texts,
    metadatas=metadatas
)
print("Book summaries loaded and embedded in ChromaDB.")
