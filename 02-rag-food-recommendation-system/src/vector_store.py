"""ChromaDB persistence: create the collection and index the food dataset."""

import chromadb

from src import config

from src.data_loader import load_food_data,prepare_food_records
from src.embeddings import get_embedding_function

BATCH_SIZE = 500

def get_client():
    config.CHROMA_DIR.mkdir(parents=True,exist_ok=True)
    client=chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return client

def get_collection():
    client=get_client()
    return client.get_or_create_collection(
        name=config.collection_name(),
        embedding_function=get_embedding_function(),
        configuration={
            "hnsw":
            {"space":"cosine",
             "ef_construction":120,
             "ef_search":120,
             "max_neighbors":20},
        }
    )

def build_index(rebuild: bool = False):
    """Return the food collection, indexing the dataset if it is empty.

    rebuild=True drops the collection first (use after editing the dataset
    or changing how documents are built).
    """
    client=get_client()
    if rebuild:
        try:
            client.delete_collection(config.collection_name())
        except Exception :
            pass # to handle initial index creation

    collection=get_collection()

    if collection.count() == 0:
        foods=load_food_data()
        documents,metadatas,ids=prepare_food_records(foods=foods)

        for start in range(0,len(documents),BATCH_SIZE):
            collection.upsert(
                ids=ids[start:start + BATCH_SIZE],
                documents=documents[start:start + BATCH_SIZE],
                metadatas=metadatas[start:start + BATCH_SIZE]
            )
    return collection

