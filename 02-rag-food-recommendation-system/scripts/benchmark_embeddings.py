import statistics
import time

from src.config import EMBEDDING_PROVIDER, collection_name
from src.retriever import retrieve_semantic_foods

QUERIES = [
    "I want something sweet and chocolatey",
    "Suggest a traditional Indian vegetarian meal",
    "Recommend a healthy snack with nuts and dried fruits",
    "I want a rich and filling meal",
]

# Manually labelled relevant food names for this test dataset.
EXPECTED_RELEVANT = {
    QUERIES[0]: {
        "Chocolate Syrup",
        "Chocolate Cake",
        "Classic Chocolate Cake",
        "Chocolate Lava Cake",
    },
    QUERIES[1]: {
        "Vegetable Korma",
        "Chickpea Curry",
        "Lentil Dhal",
    },
    QUERIES[2]: {
        "Salted Roasted Mixed Nuts and Dried Fruits",
        "Salted Roasted Mixed Nuts",
        "Salted Roasted Cashew Nuts",
        "Salted Cashews",
    },
    QUERIES[3]: {
        "Beef Stew",
        "Chicken Dum Biryani",
        "Lentil Dhal",
        "Chickpea Curry",
    },
}


TOP_K = 5
REPEATS = 3

def get_food_names(results):
    return [item['metadata'].get('food_name','Unknown') for item in results]

def calculate_relevance(food_names, expected_names):
    retrieved_names=set(food_names)

    relevant_found=retrieved_names.intersection(expected_names)
    print(f"Relevant foods found: {len(relevant_found)}")


    precision=(len(relevant_found)/len(food_names) if food_names else 0)
    recall=(len(relevant_found)/len(expected_names)  if expected_names else 0)

    return precision, recall

def benchmark_query(query):
    timings = []

    for _ in range(REPEATS):
        start = time.perf_counter()
        results = retrieve_semantic_foods(query, top_k=TOP_K)
        timings.append(time.perf_counter() - start)

    food_names = get_food_names(results)

    precision, recall = calculate_relevance(
        food_names,
        EXPECTED_RELEVANT[query],
    )

    return  {
        "median_time": statistics.median(timings),
        "mean_time": statistics.mean(timings),
        "food_names": food_names,
        "precision":precision,
        "recall":recall
    }

def main():
    print("\nEMBEDDING BENCHMARK")
    print("=" * 55)
    print(f"Provider   : {EMBEDDING_PROVIDER}")
    print(f"Collection : {collection_name()}")
    print(f"Top K      : {TOP_K}")
    print(f"Repeats    : {REPEATS}")

    # Measure cold start only once, in this process.
    print("\nMeasuring cold start...")
    start = time.perf_counter()
    retrieve_semantic_foods(QUERIES[0], top_k=TOP_K)
    cold_time = time.perf_counter() - start

    print(f"Cold-start retrieval: {cold_time:.4f} seconds")
    
    warm_times = []
    precision_scores = []
    recall_scores = []

    for index, query in enumerate(QUERIES, start=1):
        result = benchmark_query(query)

        warm_times.append(result["median_time"])
        precision_scores.append(result["precision"])
        recall_scores.append(result["recall"])

        print(f"\nQuery {index}: {query}")
        print(f"Median retrieval: {result['median_time']:.4f} seconds")
        print(f"Mean retrieval  : {result['mean_time']:.4f} seconds")

        print("Retrieved Foods:")
        for rank, name in enumerate(result["food_names"], start=1):
            print(f"  {rank}. {name}")

        print(f"\nPrecision@{TOP_K}: {result['precision']:.2f}")
        print(f"Recall@{TOP_K}   : {result['recall']:.2f}")

    print("\n" + "=" * 55)
    print("BENCHMARK SUMMARY")
    print(f"Cold-start retrieval : {cold_time:.4f} seconds")
    print(f"Average warm time for retrieval:{statistics.mean(warm_times):.4f} seconds")
    print(f"Average Precision@{TOP_K}: {statistics.mean(precision_scores):.2f}")
    print(f"Average Recall@{TOP_K}   : {statistics.mean(recall_scores):.2f}")

if __name__=="__main__":
    main()