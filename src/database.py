import os
import json
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "sports_facts.json")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)


def setup_and_populate_db(json_file_path=DATA_FILE):
    client = get_chroma_client()

    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    if collection.count() > 0:
        print(f"Database already contains {collection.count()} facts.")
        return collection

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Missing file: {json_file_path}")

    with open(json_file_path, "r", encoding="utf-8") as f:
        facts = json.load(f)

    documents = []
    metadatas = []
    ids = []

    for i, item in enumerate(facts):
        documents.append(item["fact"])
        metadatas.append({"sport": item["sport"]})
        ids.append(f"fact_{i}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Inserted {len(documents)} facts into ChromaDB.")

    return collection


def query_historic_facts(sport, query_text, n_results=2):
    client = get_chroma_client()

    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"sport": sport}
    )

    return results.get("documents", [[]])[0]


if __name__ == "__main__":
    setup_and_populate_db()
    print("Database ready.")