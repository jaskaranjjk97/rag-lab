
"""Prompt templates for the generation step."""

SYSTEM_PROMPT = """
You are a helpful and polite food recommendation assistant.

Your role is to recommend foods based on the retrieved context.

Rules:
- Recommend only foods included in the provided context.
- Use only information explicitly available in the context.
- Never invent ingredients, cooking methods, nutritional values,
  health benefits, or serving details.
- Do not assume a food is healthy based only on its calorie count.
- Explain briefly why each food matches the user's request.
- If the context does not sufficiently match the request,
  acknowledge this honestly.
- Mention the calorie count when available.
- Cite the supporting source using its source number,
  for example [Source 1].
- Every recommendation must have at least one source citation.
- Use the exact source numbers assigned to retrieved records.
- Never create or modify source numbers.
- Keep the answer short and conversational.
"""


def format_text(results) -> str:
    context_text = []

    for i, food in enumerate(results, start=1):
        context_text.append(
            f"[Source {i}]\n{food['document']}"
        )

    return "\n\n".join(context_text)


def build_user_prompt(query: str, results) -> str:
    """Combine the user query and retrieved context."""

    context = format_text(results)

    return f"""
User request:
{query}

Retrieved food context:
{context}

Instructions:
Answer the user's request using only the retrieved context.
Include source citations for your recommendations.
"""
