from chromadb import Client
from openai import OpenAI

def semantic_search(query, top_k=3):
    """
    Return top_k book recommendations based on semantic similarity to the query.
    """
    # Generate embedding for query
    openai_client = OpenAI()
    embedding = openai_client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    ).data[0].embedding

    # Search in ChromaDB
    chroma_client = Client()
    collection = chroma_client.get_collection(name="books")
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    # Return list of dicts: title, summary, themes
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
