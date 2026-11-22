"""Module for interfacing with OpenAI LLMs and embedding models."""

import logging 

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import config

logger=logging.getLogger(__name__)

def create_openai_embedding()->OpenAIEmbedding:
    """Create an OpenAI embedding model for vector representation."""
    embedding_model=OpenAIEmbedding(
        model=config.EMBEDDING_MODEL,
        api_key=config.OPENAI_API_KEY,
    )
    logger.info(f"Created OpenAI embedding model: {config.EMBEDDING_MODEL}")
    return embedding_model

def create_openai_llm(
    max_new_tokens: int = config.MAX_NEW_TOKENS,
    temperature = None,
) -> OpenAI:
    """Create an OpenAI LLM for generating responses."""

    if temperature is None:
        temperature=config.TEMPERATURE
    llm = OpenAI(
        model=config.LLM_MODEL,
        max_tokens=max_new_tokens,
        api_key=config.OPENAI_API_KEY,
        temperature=temperature,
    )

    logger.info(f"Created OpenAI LLM: {config.LLM_MODEL}")

    return llm

def change_llm_model(new_model_id: str) -> None:
    """Change the LLM model used by the application."""

    config.LLM_MODEL=new_model_id

    logger.info(f"LLM model changed to: {new_model_id}")







