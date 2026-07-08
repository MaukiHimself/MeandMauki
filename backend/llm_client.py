"""
llm_client.py — Handles all communication with the locally hosted
Ollama model. Kept separate from main.py so the FastAPI layer doesn't
need to know anything about Ollama's request/response format.
"""

import logging
import requests

from config import OLLAMA_BASE_URL, MODEL_NAME, LLM_TIMEOUT_SECONDS, SYSTEM_PROMPT

logger = logging.getLogger("meandmauki")


class LLMConnectionError(Exception):
    """Raised when Ollama cannot be reached at all (not running / wrong port)."""
    pass


class LLMResponseError(Exception):
    """Raised when Ollama is reachable but returns an error or bad response."""
    pass


def ask_llm(question: str) -> str:
    """
    Sends a question to the local Ollama model and returns the answer text.

    Raises:
        LLMConnectionError: Ollama isn't running / unreachable.
        LLMResponseError: Ollama responded with an error or unexpected payload.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "system": SYSTEM_PROMPT,
        "stream": False,
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=LLM_TIMEOUT_SECONDS,
        )
    except requests.exceptions.ConnectionError as exc:
        logger.error(f"Could not connect to Ollama at {OLLAMA_BASE_URL}: {exc}")
        raise LLMConnectionError(
            f"Could not connect to Ollama at {OLLAMA_BASE_URL}. "
            "Is 'ollama serve' running?"
        ) from exc
    except requests.exceptions.Timeout as exc:
        logger.error(f"Ollama request timed out after {LLM_TIMEOUT_SECONDS}s: {exc}")
        raise LLMResponseError(
            f"The model took too long to respond (timeout {LLM_TIMEOUT_SECONDS}s)."
        ) from exc

    if response.status_code != 200:
        logger.error(f"Ollama returned status {response.status_code}: {response.text}")
        raise LLMResponseError(
            f"Ollama returned an error (status {response.status_code}). "
            f"Is model '{MODEL_NAME}' pulled? Try: ollama pull {MODEL_NAME}"
        )

    data = response.json()
    answer = data.get("response")

    if not answer:
        logger.error(f"Ollama response missing 'response' field: {data}")
        raise LLMResponseError("Ollama returned an empty or malformed response.")

    return answer.strip()


def check_ollama_health() -> bool:
    """
    Lightweight check used by /health to confirm Ollama is up
    (doesn't run a full generation, just pings the base endpoint).
    """
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
