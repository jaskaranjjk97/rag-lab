"""Test semantic retrieval and metadata filters."""

from src.retriever import retrieve_semantic_foods

def display_results(title, results):
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    if not results:
        print("No matching foods found.")
        return

    for index, item in enumerate(results, start=1):
        metadata=item['metadata']

        print(
            f"{index}. {metadata['food_name']} | "
            f"Cuisine: {metadata['cuisine_type']} | "
            f"Calories: {metadata['calories']} | "
            f"Distance: {item['distance']:.4f}"
        )

def main():
    # Test 1: Semantic retrieval
    results = retrieve_semantic_foods(
        query="Something sweet and chocolatey",
        top_k=5
    )
    display_results("Test 1: Semantic retrieval", results)
    assert len(results) > 0, "Semantic retrieval returned no results."

    # Test 2 :Cuisine filtering
    results = retrieve_semantic_foods(
        query="A Delicious meal",
        cuisine="Indian",
        top_k=5,
    )
    display_results(title="Indian Cuisine",results=results)
    assert len(results) > 0, "No Indian food records found."

    assert all(
        item["metadata"]["cuisine_type"] == "Indian"
        for item in results
    ),"Cuisine filter failed"

    # Test 3: Calorie Filtering

    results=retrieve_semantic_foods(
        query="something Nutritious.",
        top_k=5,
        max_calories=300
    )

    display_results(title="Maximum 300 calories",results=results)
    assert len(results) > 0 , "No food with calorie less than equal to 300 found "

    assert all(item['metadata']['calories']<=300
           for item in results ), "Calorie filter failed."

    # Test 4: Combined filtering
    results = retrieve_semantic_foods(
        query="A healthy meal",
        cuisine="Indian",
        max_calories=500,
        top_k=5
    )
    display_results("Test 4: Indian food under 500 calories", results)
    assert len(results) > 0, "No Indian foods found under 500 calories."

    assert all(item['metadata']['cuisine_type'] == 'Indian'
               and item['metadata']['calories']<=500   for item in results),"Combined filters failed"

    print("\nAll retrieval tests passed!")


if __name__ == "__main__":
    main()


