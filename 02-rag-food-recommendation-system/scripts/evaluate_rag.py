"""Evaluate retrieval quality, metadata filters, and RAG generation."""

import re 

from src.data_loader import prepare_food_records,load_food_data
from src.retriever import retrieve_semantic_foods
from src.rag_pipeline import rag_pipeline

def test_semantic_retrieval():

    results=retrieve_semantic_foods(
        query="something sweet and chocolatey",
        top_k=5
    )

    food_names=[item['metadata']['food_name'] for item in results]

    expected_names={
        "Chocolate Syrup",
        "Chocolate Lava Cake"
    }

    assert results,"No Food results retrieved"
    assert expected_names.issubset(set(food_names)), (
        f"Expected chocolate foods not found. Retrieved: {food_names}"
    )

def test_cuisine_filter():
    results=retrieve_semantic_foods(
        query="Suggest a traditional meal",
        cuisine="Indian",
        top_k=5,
    )

    assert results, "No Indian foods retrieved."
    assert all(
        item["metadata"]["cuisine_type"] == "Indian"
        for item in results
    ), "Cuisine filter returned non-Indian foods."

def test_calorie_filter():
    results=retrieve_semantic_foods(
        query="Suggest a nutritious snack",
        max_calories=300,
        top_k=5,
    )

    assert results,"No nutritious food within 300 calories"
    assert all(
        item['metadata']['calories'] <= 300 
        for item in results
    ),"Calorie filter returned foods above the limit."


def test_dietary_filter():
    results = retrieve_semantic_foods(
        query="Suggest a vegetarian Indian meal",
        dietary_type="vegetarian",
        top_k=10,
    )

    assert results, "No vegetarian foods retrieved."

    assert all(
        item["metadata"]["dietary_type"] == "vegetarian"
        for item in results
    ), "Dietary filter returned an incorrectly classified food."




def test_combined_filters():
    results = retrieve_semantic_foods(
        query="Suggest a vegetarian Indian meal",
        cuisine="Indian",
        max_calories=500,
        dietary_type="vegetarian",
        top_k=10,
    )

    assert results, "No matching Indian vegetarian foods found."

    assert all(
        item["metadata"]["cuisine_type"] == "Indian"
        and item["metadata"]["calories"] <= 500
        and item["metadata"]["dietary_type"] == "vegetarian"
        for item in results
    ), "Combined metadata filters failed."


def test_duplicate_records():
    foods=load_food_data()

    documents, metadatas, ids = prepare_food_records(foods)

    assert len(ids)==len(set(ids)),"Duplicate ChromaDB IDs found."
    assert len(documents)==len(set(documents)),"Duplicate food documents found."
    assert len(documents)==len(metadatas)==len(ids),"Documents, metadata and IDs have different lengths."
    allowed_types = {"vegetarian", "non_vegetarian", "unknown"}

    assert all(
    item["dietary_type"] in allowed_types
    for item in metadatas
    )


def test_generation_and_citations():
    top_k = 3
    answer = rag_pipeline(
        query="Something sweet and chocolatey",
        top_k=top_k
    )

    assert answer and answer.strip(), "LLM returned an empty answer."

    citations = re.findall(
    r"\[Source\s+(\d+)\]",
    answer)

    assert citations, "No source citations found."

    assert all(
        1 <= int(source) <= top_k
        for source in citations
    ), "Answer contains an invalid source reference."

def run_test(name, test_function):
    """Execute one evaluation test and display its result."""
    print(f"\nRunning: {name}")

    try:
        test_function()
        print(f"PASS: {name}")
        return True

    except Exception as error:
        print(f"FAIL: {name}")
        print(f"Reason: {error}")
        return False

def main():
    print("\n========================================")
    print("       VANILLA RAG EVALUATION")
    print("========================================")

    tests = [
        ("Semantic retrieval relevance", test_semantic_retrieval),
        ("Indian cuisine filtering", test_cuisine_filter),
        ("Maximum calorie filtering", test_calorie_filter),
        ("Dietary type filtering", test_dietary_filter),
        ("Combined metadata filtering", test_combined_filters),
        ("Duplicate record detection", test_duplicate_records),
        ("LLM generation and citations", test_generation_and_citations),
    ]

    passed = 0

    for name, test_function in tests:
        result = run_test(name, test_function)
        if result:
            passed+=1

    failed = len(tests) - passed

    print("\n========================================")
    print("          EVALUATION SUMMARY")
    print("========================================")
    print(f"Total tests : {len(tests)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("========================================")

    if failed:
        raise SystemExit(1)

if __name__=="__main__":
    main()
