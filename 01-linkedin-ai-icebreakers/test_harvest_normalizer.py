
import json
import config

from modules.data_preprocessing import normalize_harvestapi_profile
from modules.data_preprocessing import split_profile_data

with open(config.HARVEST_API_MOCK, "r", encoding="utf-8") as file:
    raw_data = json.load(file)

# HarvestAPI returns a list of profile objects
raw_profile = raw_data[0] if isinstance(raw_data, list) else raw_data

normalized = normalize_harvestapi_profile(raw_profile)

print("Name:", normalized["full_name"])
print("Experience records:", len(normalized["position_groups"]))
print("Education records:", len(normalized["educations"]))
print("Skills:", len(normalized["skills"]))
print("Certifications:", len(normalized["certifications"]))

nodes = split_profile_data(normalized)

print("\nTotal nodes created:", len(nodes))

for i, node in enumerate(nodes, 1):
    print(
        f"Node {i}: "
        f"{node.metadata.get('section')} | "
        f"{len(node.text)} characters"
    )

# Verify important information survived preprocessing
all_text = "\n".join(node.text for node in nodes)

keywords = [
    "$3.2B",
    "2030 strategic plan",
    "GenAI",
    "20+ Deloitte Member Firms",
    "40% reduction",
]

print("\n========== DATA PRESERVATION CHECK ==========")

for keyword in keywords:
    found = keyword.lower() in all_text.lower()
    print(f"{keyword}: {'PASS' if found else 'FAIL'}")



from modules.data_preprocessing import create_vector_database

index = create_vector_database(nodes)

if index is None:
    raise RuntimeError("Vector index creation failed")


retriever = index.as_retriever(similarity_top_k=10)

questions = [
    "What degrees and qualifications did Bharat complete?",
    "What GenAI initiatives did Bharat work on at Deloitte?"
]

for question in questions:
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    retrieved_nodes = retriever.retrieve(question)

    for i, result in enumerate(retrieved_nodes, 1):
        print(f"\n--- Result {i} ---")
        print("Score:", round(result.score, 4))
        print("Section:", result.node.metadata.get("section"))
        print("Content:\n", result.node.text)