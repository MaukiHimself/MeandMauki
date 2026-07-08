# Me And Mauki — Technical Report

*(Convert this to PDF for final submission. Fill in the [bracketed] parts.)*

## 1. Introduction

[Brief intro: what this project is, why you built it solo, course context (IS 365).]

## 2. System Use Case

Me And Mauki is a University Student Support Assistant for CoICT / UDSM
students, answering questions on course registration, examination rules,
library services, ICT support, hostel applications, fee payment, the
academic calendar, and student conduct.

## 3. Tools and Technologies Used

- OS: Kali Linux
- Language: Python 3.x
- Virtual environment: `venv`
- Local LLM serving: Ollama, model `llama3.2:1b`
- Backend: FastAPI + Uvicorn
- Frontend: Streamlit
- Testing: custom Python script (`tests/test_api.py`)
- Version control: Git/GitHub

## 4. System Architecture

```
User → Streamlit frontend → FastAPI backend → Ollama (llama3.2:1b) → response
```

[Insert your architecture diagram/screenshot here if you make one.]

## 5. Implementation Steps

[Describe, in your own words, how you set up venv → Ollama → backend →
frontend → tests. Reference screenshots in docs/screenshots/.]

## 6. Testing and Results

[Paste/describe test_api.py output. Screenshot the terminal run.]

## 7. Challenges Encountered

[E.g. model response latency on limited hardware, tuning the system prompt,
handling Ollama connection errors gracefully, etc.]

## 8. Production Readiness Discussion

[Pull from Task 9 reflection below — expand on what's missing for real
deployment: auth, rate limiting, monitoring, HTTPS, data retention policy.]

## 9. Conclusion

[Summarize what you built and what you learned about the full LLM
deployment pipeline.]

## 10. Appendix: Screenshots and Code Snippets

[Insert screenshots from docs/screenshots/ here, referenced in order:
venv activated → model pulled/running → API response → FastAPI running →
/docs → /health → /ask → frontend → Q&A → test output → log file.]

---

## Task 6: Prompt Engineering — Before & After

**Original prompt (naive):**
```
You are a helpful assistant. Answer the student's question.
```

**Improved prompt (used in `backend/config.py` as `SYSTEM_PROMPT`):**
```
You are 'Me And Mauki', a helpful, concise assistant for university
students at CoICT, University of Dar es Salaam. You answer questions
about course registration, examination rules, library services, ICT
support, hostel application, fee payment, the academic calendar, and
student conduct. If a question is outside these topics, politely say
so and redirect the student to the right office. Keep answers short,
clear, and practical — use numbered steps when explaining a process.
Do not invent policies, deadlines, or fees you are not sure about;
instead tell the student to confirm with the relevant university office.
```

**Comparison (fill in with a real example after testing):**

| Question | Response (original prompt) | Response (improved prompt) |
|---|---|---|
| "How do I register for courses?" | [generic, possibly vague] | [scoped, step-by-step, CoICT-specific tone] |

[Note what changed: specificity, tone, refusal of out-of-scope questions,
willingness to say "I'm not sure, check with the registrar" instead of
inventing an answer.]

---

## Task 9: Industry Production Reflection

1. **Main components:** Streamlit frontend, FastAPI backend
   (`main.py`, `llm_client.py`, `config.py`), Ollama serving `llama3.2:1b`
   locally, file-based logging, a Python test script.

2. **Why FastAPI:** [async support, automatic Swagger docs at /docs,
   built-in request validation via Pydantic, easy to extend.]

3. **Role of the LLM model:** [interprets the student's natural-language
   question and generates a relevant answer based on the system prompt.]

4. **Role of the frontend:** [gives students a simple chat interface,
   handles empty-input and connection-error cases before they reach the
   backend, shows loading state during generation.]

5. **Local model vs external API:** [local = full data privacy, no
   per-request cost, but limited by local hardware and model size;
   external API = stronger models, no infra to manage, but data leaves
   your machine and costs scale with usage.]

6. **Security risks in an organisational deployment:** [no auth on
   endpoints currently, no rate limiting, logs store raw questions which
   could contain personal data, CORS wide open (`*`), no HTTPS.]

7. **Improvements needed before production:** [add authentication/API
   keys, rate limiting, HTTPS via reverse proxy, restrict CORS, log
   redaction/rotation, containerization (Docker), health monitoring/alerts,
   input sanitization, model output moderation.]

8. **Monitoring in real-world use:** [structured logs shipped to a
   central system, uptime checks on /health, response-time metrics,
   error-rate alerting.]

9. **Protecting sensitive student info:** [avoid logging full question
   text if it may contain personal identifiers, encrypt logs at rest,
   restrict log file access, define a retention/deletion policy, don't
   send data to third-party APIs without consent.]

10. **Challenges faced:** [fill in honestly — e.g. Ollama response
    latency, tuning timeouts, handling empty/slow requests gracefully,
    working solo through all 7 roles.]
