"""
main.py — FastAPI backend for "Me And Mauki", a University Student
Support Assistant powered by a locally hosted LLM via Ollama.

Endpoints:
    GET  /health  -> checks that Ollama is reachable
    POST /ask     -> sends a student's question to the LLM and returns the answer

Run with:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

import logging
import os
import time
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from config import LOG_DIR, LOG_FILE, MODEL_NAME, APP_HOST, APP_PORT
from llm_client import ask_llm, check_ollama_health, LLMConnectionError, LLMResponseError

# --- Logging setup (Task 8) ---
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),  # also print to console while developing
    ],
)
logger = logging.getLogger("meandmauki")

app = FastAPI(
    title="Me And Mauki",
    description="A self-hosted LLM-powered University Student Support Assistant.",
    version="1.0.0",
)

# Allow the Streamlit frontend (different port) to call this API in local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Question cannot be empty.")
        return value.strip()


class AskResponse(BaseModel):
    answer: str
    model: str
    response_time_seconds: float


@app.get("/health")
def health_check():
    """
    Confirms the backend is up AND that Ollama is reachable.
    Task 3 + Task 7 (model not running -> clear backend error).
    """
    ollama_up = check_ollama_health()
    status = "ok" if ollama_up else "degraded"

    logger.info(f"Health check | ollama_reachable={ollama_up}")

    if not ollama_up:
        raise HTTPException(
            status_code=503,
            detail={
                "status": status,
                "message": "Backend is running, but Ollama is not reachable. "
                            "Start it with: ollama serve",
            },
        )

    return {"status": status, "model": MODEL_NAME}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """
    Receives a student's question, forwards it to the local LLM,
    logs the interaction, and returns the answer.
    """
    question = request.question
    timestamp = datetime.now().isoformat()
    start = time.time()

    logger.info(f"Question received | time={timestamp} | question=\"{question}\"")

    try:
        answer = ask_llm(question)
    except LLMConnectionError as exc:
        logger.error(f"LLM connection error | time={timestamp} | error={exc}")
        raise HTTPException(status_code=503, detail=str(exc))
    except LLMResponseError as exc:
        logger.error(f"LLM response error | time={timestamp} | error={exc}")
        raise HTTPException(status_code=502, detail=str(exc))

    elapsed = round(time.time() - start, 2)

    logger.info(
        f"Answer generated | time={timestamp} | elapsed={elapsed}s | "
        f"answer=\"{answer[:200]}\""
    )

    return AskResponse(answer=answer, model=MODEL_NAME, response_time_seconds=elapsed)


@app.get("/")
def root():
    return {"message": "Me And Mauki backend is running. Visit /docs for the API UI."}
