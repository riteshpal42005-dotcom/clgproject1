
# services/llm.py

import os
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_URL = os.getenv(
    "OPENROUTER_URL",
    "https://openrouter.ai/api/v1",
)


def get_llm():
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing in .env")

    if not OPENROUTER_MODEL:
        raise ValueError("OPENROUTER_MODEL is missing in .env")

    model_name = OPENROUTER_MODEL

    if not model_name.startswith("openrouter/"):
        model_name = f"openrouter/{model_name}"

    return LitellmModel(
        model=model_name,
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_URL,
    )
