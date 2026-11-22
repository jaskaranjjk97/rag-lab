"""Module for querying indexed LinkedIn profile data."""

import logging
from typing import Any
from llama_index.core import VectorStoreIndex,PromptTemplate

from modules.llm_interface import create_openai_llm
import config

logger=logging.getLogger(__name__)

def generate_initial_facts(
        vector_index: VectorStoreIndex
)->str:
    """Generates interesting facts about the person's career or education.
    Args:
        index: VectorStoreIndex containing the LinkedIn profile data.    
        Returns: String containing interesting facts about the person.
    """
    try:
        openai_llm=create_openai_llm(
            temperature=0.0,
            max_new_tokens=500
        )
        prompt=PromptTemplate(template=config.INITIAL_FACTS_TEMPLATE)
        query_engine=vector_index.as_query_engine(
            llm=openai_llm,
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            text_qa_template=prompt,
        )
        query = "Provide three interesting facts about this person's career or education."
        response=query_engine.query(query)
        return str(response)
    except Exception as e:
        logger.error(f"Error in generate_initial_facts: {e}")
        return "Failed to generate initial facts."

def answer_user_query(vector_index: VectorStoreIndex, user_query: str) -> Any:
    """Answers the user's question using the vector database and the LLM.    
    Args:
        index: VectorStoreIndex containing the LinkedIn profile data.
        user_query: The user's question.    
    Returns:
        Response object containing the answer to the user's question.
    """
    try:
        openai_llm=create_openai_llm(
            temperature=0.0,
            max_new_tokens=500
        )
        question_prompt=PromptTemplate(template=config.USER_QUESTION_TEMPLATE)
        query_engine=vector_index.as_query_engine(
            llm=openai_llm,
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            text_qa_template=question_prompt,
        )
        response=query_engine.query(user_query)
        return str(response)
    except Exception:
        logger.exception("Error in answer_user_query")
        return "Failed to answer the question."