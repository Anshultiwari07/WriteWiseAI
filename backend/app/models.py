import os
import requests
from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
import language_tool_python

# ===============================
# ENV VARS
# ===============================
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY not set in .env")
if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY not set in .env")

# ===============================
# HUGGINGFACE ROUTER SETTINGS
# ===============================
HF_BASE_URL = "https://router.huggingface.co/hf-inference/models"

# You can change these later if you want to try other models
AGENT1_MODEL_ID = "google/flan-t5-large"                 # Planner
AGENT2_MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"     # Writer
AGENT3_MODEL_ID = "google/flan-t5-large"                 # Polisher


def _hf_generate(
    model_id: str,
    prompt: str,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
    """
    Low-level helper that calls Hugging Face Router for text generation.
    Works for both FLAN-T5 and Phi-3 style models.
    """
    url = f"{HF_BASE_URL}/{model_id}"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "return_full_text": False,
        },
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=60)

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        # Surface a clean error in FastAPI logs
        raise RuntimeError(
            f"HuggingFace API error for {model_id}: "
            f"{resp.status_code} {resp.text}"
        ) from e

    data = resp.json()

    # HF router usually returns: [ { "generated_text": "..." } ]
    text: str | None = None

    if isinstance(data, list) and data:
        item = data[0]
        if isinstance(item, dict):
            text = item.get("generated_text") or item.get("text")
    elif isinstance(data, dict):
        text = data.get("generated_text") or data.get("text")

    if not text:
        # Fallback – in case format changes, at least return something
        text = str(data)

    return text.strip()


# ===============================
# AGENT-SPECIFIC HELPERS
# ===============================

def agent1_generate(prompt: str) -> str:
    """Agent-1 (Planner) – FLAN-T5-Large."""
    return _hf_generate(
        AGENT1_MODEL_ID,
        prompt,
        max_new_tokens=512,
        temperature=0.4,
    )


def agent2_generate(prompt: str) -> str:
    """Agent-2 (Writer) – Phi-3 Mini."""
    return _hf_generate(
        AGENT2_MODEL_ID,
        prompt,
        max_new_tokens=1024,
        temperature=0.8,
    )


def agent3_generate(prompt: str) -> str:
    """Agent-3 (Polisher) – FLAN-T5-Large."""
    return _hf_generate(
        AGENT3_MODEL_ID,
        prompt,
        max_new_tokens=512,
        temperature=0.4,
    )


# ===============================
# TOOLS: SEARCH + GRAMMAR
# ===============================

# Web search via SerpAPI (used by Agent-1)
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

# Local grammar checker (used before Agent-3)
grammar_tool = language_tool_python.LanguageTool("en-US")


