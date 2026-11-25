"""RAG pipeline that connects vector index to prompt augmentation and LLM generation"""

import time
from openai import OpenAI

from src.retriever import retrieve_semantic_foods
from src.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    TOP_K,
    validate_config
)
from src.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt
)
from src.logging_config import logger

def rag_pipeline(
        query:str,
        top_k=TOP_K,
        cuisine: str | None = None,
        max_calories: float | None=None,
        dietary_type: str | None = None,
        ):

    request_start=time.perf_counter()

    logger.info("RAG request started.")

    try:
        validate_config()
        client=OpenAI(api_key=OPENAI_API_KEY)

        retrieval_request=time.perf_counter()

        results=retrieve_semantic_foods(
            query=query,
            top_k=top_k,
            cuisine=cuisine,
            max_calories=max_calories,
            dietary_type=dietary_type,
        )

        retrieval_time = time.perf_counter() - retrieval_request
        logger.info(
            "Retrieval completed | Documents: %d | Time: %.2f seconds",
            len(results),
            retrieval_time
        )

        if not results:
            logger.warning("No matching food records found")
            return "I couldn't find any matching food for your request"
        
        user_prompt=build_user_prompt(query,results)

        generation_start = time.perf_counter()
        response=client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":user_prompt}
            ],
        )
        generation_time=time.perf_counter() - generation_start

        logger.info(
            "LLM generation completed | Time: %.2f seconds",
            generation_time
        )
        answer=response.choices[0].message.content

        return answer or "I couldn't generate a recommendation."
    except Exception:
        logger.exception("RAG request failed")
        raise
    finally:
        total_time = time.perf_counter() - request_start

        logger.info(
            "RAG request finished | Total time: %.2f seconds",
            total_time
        )