import json
from chromadb import Client
from openai import OpenAI

# Load book summaries
with open("book_summaries.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    books = data["books"]

# Prepare documents and metadata
texts = []
metadatas = []
for book in books:
    text = f"{book['title']}: {book['summary']}\nTeme: {', '.join(book['themes'])}"
    texts.append(text)
    metadatas.append({"title": book["title"], "themes": book["themes"]})

# Generate embeddings with OpenAI
openai_client = OpenAI()
embeddings = openai_client.embeddings.create(
    input=texts,
    model="text-embedding-3-small"
).data
vectors = [e.embedding for e in embeddings]

# Store in ChromaDB
chroma_client = Client()
collection = chroma_client.create_collection(name="books")
collection.add(
    embeddings=vectors,
    documents=texts,
    metadatas=metadatas
)

print("Book summaries loaded and embedded in ChromaDB.")
