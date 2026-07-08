# Me And Mauki 🎓

A self-hosted LLM-powered University Student Support Assistant, built for
IS 365 (Full-Stack Pipeline for Deploying a Self-Hosted LLM Application).

It answers CoICT / UDSM student questions about course registration, exams,
library services, ICT support, hostel applications, fee payment, the
academic calendar, and student conduct — using a locally hosted model
(`llama3.2:1b`) served by Ollama, a FastAPI backend, and a Streamlit frontend.

## Architecture

```
User → Streamlit frontend → FastAPI backend → Ollama (llama3.2:1b) → response
```

## Project structure

```
MeandMauki/
├── backend/
│   ├── main.py         # FastAPI app: /health, /ask
│   ├── llm_client.py    # Talks to Ollama's /api/generate
│   ├── config.py        # Settings + system prompt
│   └── logs/
│       └── app.log      # Created automatically on first run
├── frontend/
│   └── app.py            # Streamlit chat UI
├── tests/
│   └── test_api.py       # API test script
├── docs/
│   ├── screenshots/
│   └── report.md
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/MaukiHimself/MeandMauki.git
cd MeandMauki
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and run Ollama, pull the model

```bash
# If Ollama isn't installed yet:
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull llama3.2:1b

# Start Ollama's server (leave this running in its own terminal)
ollama serve
```

## Running the app

You'll need **three terminals** (all inside the activated venv where relevant):

**Terminal 1 — Ollama**
```bash
ollama serve
```

**Terminal 2 — Backend**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Terminal 3 — Frontend**
```bash
cd frontend
streamlit run app.py
```
- Opens at: http://localhost:8501

## Testing

With the backend (and Ollama) running:

```bash
cd tests
python test_api.py
```

## Configuration

Environment variables (all optional, sensible defaults in `backend/config.py`):

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Where Ollama is listening |
| `MODEL_NAME` | `llama3.2:1b` | Model to query |
| `LLM_TIMEOUT_SECONDS` | `60` | Timeout before giving up on a response |
| `APP_HOST` / `APP_PORT` | `0.0.0.0` / `8000` | FastAPI bind address |

## Error handling

| Situation | Behaviour |
|---|---|
| Backend not running | Frontend sidebar shows "Backend unreachable" + fix instructions |
| Model not running | Backend returns `503` with a clear message; frontend surfaces it |
| Empty question | Rejected client-side (Streamlit) and server-side (`422` via Pydantic validation) |
| Slow response | Frontend shows a spinner ("Me And Mauki is thinking...") while waiting |

## Logging

`backend/logs/app.log` records, with timestamps: received questions,
generated answers, and any errors (connection failures, timeouts, bad
responses from Ollama).

## Author

Mauki — BSc Computer Science, CoICT, University of Dar es Salaam.
