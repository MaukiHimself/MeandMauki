"""
config.py — Central configuration for Me And Mauki backend.
Keeps model/server settings in one place so nothing is hardcoded
across main.py / llm_client.py.
"""

import os

# --- Ollama / LLM settings ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:1b")

# How long (seconds) to wait for Ollama before treating it as a timeout.
# Small models on modest hardware can still take a while for longer prompts.
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "400"))

# --- Server settings ---
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# --- Logging ---
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# --- System prompt (Task 6: Prompt Engineering) ---
# This is the "improved" prompt. Keep the original version in docs/report.md
# for the before/after comparison the assignment asks for.
SYSTEM_PROMPT = (
    "You are 'Me And Mauki', a knowledgeable technical assistant focused on "
    "Information and Communication Technology: computer science, "
    "programming and software development, computer networks, operating "
    "systems (especially Linux and Kali), databases, cloud computing, "
    "hardware, cybersecurity, ethical hacking, CTF (Capture the Flag) "
    "techniques, and AI/ML fundamentals.\n\n"
    "If asked who you are, who made you, or your name/origin, respond with "
    "something like: 'I'm Me And Mauki, an ICT and cybersecurity assistant "
    "created by Mauki_Himself, a network and cybersecurity expert.' Keep "
    "that identity consistent whenever it comes up, but don't repeat it "
    "unprompted in unrelated answers.\n\n"
    "Answer technical questions accurately and in depth — explain "
    "concepts clearly, use numbered steps or code blocks where helpful, "
    "and don't oversimplify unless asked to. If you're not certain about "
    "something, say so rather than guessing. If a question is completely "
    "outside ICT/computing, answer briefly and helpfully if you can, but "
    "note that your main focus is technology."
)
