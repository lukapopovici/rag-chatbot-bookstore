

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


def semantic_search(query, top_k=3):
    api_key = read_api_key()
    openai_client = OpenAI(api_key=api_key)
    embedding = openai_client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    ).data[0].embedding
    chroma_client = Client()
    collection = chroma_client.get_collection(name="books")
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    recommendations = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        recommendations.append({
            "title": meta["title"],
            "themes": meta["themes"],
            "text": doc
        })
    return recommendations

if __name__ == "__main__":
    query = input("Ce temă sau context te interesează? ")
    recs = semantic_search(query)
    for i, rec in enumerate(recs, 1):
        print(f"{i}. {rec['title']}\n   {rec['text']}")
