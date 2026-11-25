
import os
from pathlib import Path
from dotenv import load_dotenv
import re

# Project root directory
ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from project root
load_dotenv(ROOT / ".env")

# Dataset paths
DATA_DIR = ROOT / "data"
FOOD_FILE = DATA_DIR / "food_dataset.json"
CHROMA_DIR=ROOT/"chromadb"

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM_MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")

EMBEDDING_PROVIDER=os.getenv("EMBEDDING_PROVIDER","local")
LOCAL_EMBEDDING_MODEL=os.getenv("LOCAL_EMBEDDING_MODEL","all-MiniLM-L6-v2")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","text-embedding-3-small")

TOP_K=int(os.getenv("TOP_K",3))

def collection_name() -> str:
    """One collection per embedding setup, so vectors of different sizes never mix."""
    model= EMBEDDING_MODEL if EMBEDDING_PROVIDER =="openai" else LOCAL_EMBEDDING_MODEL
    slug=re.sub(r"[^A-Za-z0-9.-_]","-",model)
    return f"food_{EMBEDDING_PROVIDER}_{slug}"

def llm_available() -> bool:
    return bool(OPENAI_API_KEY)


def validate_config():
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is missing. Check your .env file."
        )
