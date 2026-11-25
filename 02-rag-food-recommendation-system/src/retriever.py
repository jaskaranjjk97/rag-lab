"""Retrieve relevant food records from ChromaDB."""

from src.config import TOP_K
from src.vector_store import get_collection

def retrieve_semantic_foods(
        query,
        top_k=TOP_K,
        cuisine=None,
        max_calories=None,
        dietary_type=None,
):
    """Retrieve relevant foods with optional metadata filters."""
    if not isinstance(query,str) or not query.strip():
        raise ValueError("Search Query text can not be empty.")

    if top_k < 1 :
        raise ValueError("Top_k value should be atleast 1.")

    allowed_types = {"vegetarian", "non_vegetarian", "unknown"}

    if dietary_type is not None and dietary_type not in allowed_types:
        raise ValueError(
            f"dietary_type must be one of {allowed_types}"
        )

    collection=get_collection()

    conditions=[]

    if cuisine:
        conditions.append(
            {
                "cuisine_type":{"$eq":cuisine}
            }
        )

    if max_calories is not None:
        if max_calories < 0:
            raise ValueError("Maximum calories can not be negative")
        
        conditions.append(
            {
                "calories":{"$lte":float(max_calories)}
            }
        )

    if dietary_type:
        conditions.append({
            "dietary_type": {"$eq": dietary_type}
        })


    # Combine filters when multiple conditions exist
    where = None

    if len(conditions) == 1:
        where=conditions[0]

    elif len(conditions) > 1:
        where={"$and":conditions}

    results=collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where,
        include=["documents","metadatas","distances"],
    )

    foods=[]
    for document,metadata,distance in zip(results['documents'][0],results['metadatas'][0],results['distances'][0]):
        foods.append({
            "document": document,
            "metadata": metadata,
            "distance": distance
        })

    return foods

    