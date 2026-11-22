import os 
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# Apify Api key 

APIFY_API_TOKEN=os.getenv("APIFY_API_TOKEN")
APIFY_API_ENDPOINT = (
    "https://api.apify.com/v2/acts/"
    "harvestapi~linkedin-profile-scraper/run-sync-get-dataset-items"
)

# Mock data 
MOCK_DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "mock_profile.json"
)

HARVEST_API_MOCK = os.path.join(os.path.dirname(__file__),"harvest_api.json")

SIMILARITY_TOP_K = 10
TEMPERATURE = 0.2
MAX_NEW_TOKENS = 500
CHUNK_SIZE = 500

# LLM prompt templates
INITIAL_FACTS_TEMPLATE = """
You are an AI assistant analyzing a LinkedIn profile.

Context information:
---------------------
{context_str}
---------------------

Identify exactly 3 interesting facts about this person's
career or education.

For each fact:
1. Provide a short heading.
2. Explain the fact using the available profile information.
3. Mention relevant companies, roles, or institutions when available.

Use only the provided context.
Do not invent achievements, dates, or qualifications.
If the context does not contain enough information for 3 facts,
provide only the facts that can be supported.
"""

USER_QUESTION_TEMPLATE = """
You are an AI assistant that provides detailed answers to questions
based on the provided context.

Context information is below:

{context_str}

Question: {query_str}

Answer the user's question directly and concisely.

Use only the provided context.
Include relevant details such as dates, organizations, roles,
and figures when available.

Do not include unrelated information.
If the answer is not available in the context,
say "I don't know. The information is not available on the LinkedIn page."""

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing from .env")