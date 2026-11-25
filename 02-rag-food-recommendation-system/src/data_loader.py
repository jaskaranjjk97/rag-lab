import json
import re

from src.config import FOOD_FILE

def load_food_data():
    """Loads food data from JSON file."""
    if not FOOD_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {FOOD_FILE}")

    with open(FOOD_FILE,"r",encoding="utf-8") as file:
        foods=json.load(file)

    if not foods:
        raise ValueError(f"No data found in location:{FOOD_FILE}")

    if not isinstance(foods, list):
        raise ValueError("Expected the food dataset to contain a list.")

    return foods

def format_mapping(data):
    """Convert dictionary into text"""

    if not isinstance(data,dict):
        return str(data)

    return "\n".join(f"{key}:{value}" for key ,value in data.items())

def create_food_document(food):
    """Convert one food record into embedding-friendly text."""

    ingredients=",".join(food['food_ingredients'])

    document=f"""
Food Name: {food['food_name']}

Description: {food['food_description']}

Cuisine: {food['cuisine_type']}

Ingredients: {ingredients}

Cooking Method: {food['cooking_method']}

Calories per Serving: {food['food_calories_per_serving']}

Nutritional Factors:
{format_mapping(food['food_nutritional_factors'])}

Health Benefits: {food['food_health_benefits']}

Food Features:
{format_mapping(food['food_features'])}
"""

    return document.strip()

def contains_term(text, terms):
    return any(
        re.search(r"\b" + re.escape(term) + r"\b", text)
        for term in terms
    )

def classify_dietary_type(food):

    ingredients = food.get("food_ingredients",[])
    if not ingredients:
        return "unknown"

    text = " ".join(str(item).lower() for item in ingredients)

    non_vegetarian_terms = [
        "chicken", "beef", "pork", "lamb", "mutton", "goat",
        "fish", "shrimp", "prawn", "crab", "lobster", "anchovy",
        "bacon", "ham", "pepperoni", "pancetta", "turkey",
        "duck", "sausage", "meat", "seafood"
    ]
    ambiguous_terms = [
        "gelatin", "dashi", "broth", "stock", "rennet",
        "caesar dressing"
    ]

    if contains_term(text,non_vegetarian_terms):
        return "non_vegetarian"

    if contains_term(text,ambiguous_terms):
        return "unknown"

    # Detect a conflict between the food name and its ingredients.
    name = food.get("food_name", "").lower()

    if contains_term(name, non_vegetarian_terms):
        return "unknown"

    return "vegetarian"

def get_dietary_tags(food):
    """Identify dietary components explicitly listed in ingredients."""

    ingredients = " ".join(
        str(item).lower()
        for item in food.get("food_ingredients", [])
    )

    tags = []

    ingredient_groups = {
        "contains_dairy": [
            "milk", "butter", "cheese", "cream", "yogurt",
            "yoghurt", "paneer", "whey", "ghee", "mascarpone",
            "mozzarella", "ricotta"
        ],
        "contains_eggs": ["egg"],
        "contains_gluten": [
            "wheat", "flour", "barley", "rye", "bread",
            "pasta", "spaghetti", "breadcrumbs"
        ],
        "contains_nuts": [
            "almond", "cashew", "peanut", "walnut", "pecan",
            "pistachio", "hazelnut", "macadamia", "brazil nut"
        ],
        "contains_soy": ["soy", "tofu", "edamame", "miso"]
    }

    for tag, terms in ingredient_groups.items():
        if contains_term(ingredients, terms):
            tags.append(tag)

    return tags



def prepare_food_records(foods):
    """Prepare documents, metadata, and unique IDs for ChromaDB."""
    documents=[]
    metadatas=[]
    ids=[]

    id_counts={}
    seen_records=set()

    for food in foods:

        record_signature=json.dumps({key:value for key,value in food.items() if key!="food_id"},sort_keys=True)

        if record_signature in seen_records:
            continue
        seen_records.add(record_signature)

        # Normalize the original ID to a string
        original_id=str(food['food_id'])

        # Resolve duplicate IDs without losing any records
        id_counts[original_id]=id_counts.get(original_id,0) + 1

        if id_counts[original_id]==1:
            unique_id=original_id
        else:
            unique_id=f"{original_id}_{id_counts[original_id]}"

        document=create_food_document(food)

        metadata={
            "food_id": original_id,
            "food_name": str(food["food_name"]),
            "cuisine_type": str(food["cuisine_type"]),
            "cooking_method": str(food["cooking_method"]),
            "calories": float(food["food_calories_per_serving"]),
            "dietary_type":classify_dietary_type(food),
            "dietary_tags":get_dietary_tags(food) or ["no_known_tags"],
        }

        ids.append(unique_id)
        documents.append(document)
        metadatas.append(metadata)

    return documents, metadatas, ids


        
