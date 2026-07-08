"""
app.py — Streamlit frontend for "Me And Mauki".

Run with:
    streamlit run app.py
"""

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Me And Mauki", page_icon="🎓")

st.title("🎓 Me And Mauki")
st.caption("Your ICT & cybersecurity assistant — networking, programming, Linux, "
           "CTF, and everything in between. Created by Mauki_Himself.")

# --- Backend connectivity check (Task 7: backend not running) ---
def backend_is_up() -> bool:
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.RequestException:
        return False


with st.sidebar:
    st.subheader("System status")
    if backend_is_up():
        st.success("Backend + model: online")
    else:
        st.error("Backend unreachable. Is FastAPI running?\n\n"
                 "Start it with:\nuvicorn main:app --reload")

# --- Chat state ---
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question about university services...")

if question is not None:
    # Task 7: empty question handling
    if not question.strip():
        st.warning("Please enter a question before submitting.")
    else:
        st.session_state.history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            # Task 7: slow response -> loading/spinner message
            with st.spinner("Me And Mauki is thinking..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={"question": question},
                        timeout=400,
                    )
                except requests.exceptions.ConnectionError:
                    st.error(
                        "⚠️ Could not connect to the backend. "
                        "Make sure FastAPI is running (uvicorn main:app --reload)."
                    )
                    st.stop()
                except requests.exceptions.Timeout:
                    st.error("⚠️ The request timed out. The model may be overloaded.")
                    st.stop()

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    st.write(answer)
                    st.caption(f"Model: {data['model']} · {data['response_time_seconds']}s")
                    st.session_state.history.append({"role": "assistant", "content": answer})
                elif response.status_code == 503:
                    st.error("⚠️ The model isn't running. Try: ollama serve")
                elif response.status_code == 422:
                    st.warning("Please enter a valid question.")
                else:
                    detail = response.json().get("detail", "Unknown error.")
                    st.error(f"⚠️ Backend error: {detail}")
