"""Single place which decides which embedding model to use

Chroma calls this embedding function for both documents (on add/upsert) and
queries (on query), so the two can never be embedded with different models.
Swap providers with EMBEDDING_PROVIDER in .env - nothing else changes.
"""

from functools import lru_cache
from src import config

from chromadb.utils import embedding_functions

@lru_cache(maxsize=1)
def get_embedding_function():
    if config.EMBEDDING_PROVIDER == "local":
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.LOCAL_EMBEDDING_MODEL
        )
    if config.EMBEDDING_PROVIDER == "openai":
        config.validate_config()
        return embedding_functions.OpenAIEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL,
            api_key=config.OPENAI_API_KEY,
        )
    raise ValueError(f"Unknown Embedding provider '{config.EMBEDDING_PROVIDER}', use 'local' or 'openai' .")
