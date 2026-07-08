"""
test_api.py — Simple API test script for Me And Mauki.

Run with the backend already running:
    python test_api.py
"""

import sys
import requests

BASE_URL = "http://localhost:8000"
ASK_TIMEOUT = 400  # seconds — local CPU inference can be slow


def test_health():
    print("\n[TEST] GET /health")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=10)
    except requests.exceptions.ConnectionError:
        print("  FAIL: Could not connect to backend. Is uvicorn running?")
        return False

    if r.status_code == 200:
        print(f"  PASS: {r.status_code} -> {r.json()}")
        return True
    else:
        print(f"  WARN: {r.status_code} -> {r.json()} (model may not be running)")
        return False


def test_ask_valid():
    print(f"\n[TEST] POST /ask with a valid question (timeout={ASK_TIMEOUT}s, be patient)")
    payload = {"question": "How do I register for courses this semester?"}
    try:
        r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=ASK_TIMEOUT)
    except requests.exceptions.Timeout:
        print(f"  FAIL: Client-side timeout after {ASK_TIMEOUT}s. Model is slower than that.")
        return False
    except requests.exceptions.ConnectionError:
        print("  FAIL: Could not connect to backend.")
        return False

    if r.status_code == 200:
        data = r.json()
        assert "answer" in data
        print(f"  PASS: {r.status_code}")
        print(f"  Answer (truncated): {data['answer'][:150]}...")
        print(f"  Response time: {data['response_time_seconds']}s")
        return True
    else:
        print(f"  FAIL: {r.status_code} -> {r.text}")
        return False


def test_ask_empty_question():
    print("\n[TEST] POST /ask with an empty question (should be rejected)")
    payload = {"question": "   "}
    r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=10)

    if r.status_code == 422:
        print(f"  PASS: correctly rejected with {r.status_code}")
        return True
    else:
        print(f"  FAIL: expected 422, got {r.status_code} -> {r.text}")
        return False


def test_ask_missing_field():
    print("\n[TEST] POST /ask with missing 'question' field")
    r = requests.post(f"{BASE_URL}/ask", json={}, timeout=10)

    if r.status_code == 422:
        print(f"  PASS: correctly rejected with {r.status_code}")
        return True
    else:
        print(f"  FAIL: expected 422, got {r.status_code} -> {r.text}")
        return False


if __name__ == "__main__":
    results = {
        "health": test_health(),
        "ask_valid": test_ask_valid(),
        "ask_empty_question": test_ask_empty_question(),
        "ask_missing_field": test_ask_missing_field(),
    }

    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    for name, passed in results.items():
        print(f"  {name}: {'PASS' if passed else 'FAIL'}")

    if all(results.values()):
        print("\nAll tests passed.")
        sys.exit(0)
    else:
        print("\nSome tests failed or returned warnings — check output above.")
        sys.exit(1)