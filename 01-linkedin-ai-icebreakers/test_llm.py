from modules.llm_interface import (
    create_openai_embedding,
    create_openai_llm,
)

llm = create_openai_llm()
embedding = create_openai_embedding()

response = llm.complete("Explain RAG in one sentence.")

print("LLM response:", response.text)

vector = embedding.get_text_embedding("What is RAG?")

print("Embedding dimensions:", len(vector))