from modules.data_extraction import extract_linkedin_profile
from modules.data_preprocessing import (
    split_profile_data,
    create_vector_database
)
from modules.llm_interface import (
    create_openai_llm,
    create_openai_embedding,
)

from modules.query_engine import (
    generate_initial_facts,
    answer_user_query
)

import config

# Test profile extraction
profile = extract_linkedin_profile(
    "https://www.linkedin.com/in/sundeep-kumar-associate-manager-ta-gspann-technologies/"
)

print("\nProfile:", profile.get("full_name"))

# Test profile Preprocessing 
nodes = split_profile_data(profile)

print("Nodes created:", len(nodes))

# Test vector index
index = create_vector_database(nodes)

if index is None:
    raise RuntimeError("Vector index creation failed.")

print("\nVector index created successfully.")

# Test Initial Facts 
initial_facts=generate_initial_facts(index)

print("\nInitial facts:")
print(initial_facts)

# Test question answering
question = "What companies has this person worked for?"

answer = answer_user_query(index, question)

print("\nQuestion:", question)
print("Answer:", answer)