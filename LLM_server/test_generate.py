from pathlib import Path
from fastapi.testclient import TestClient
import pytest

from .server import app, MODEL_DIR

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_generate_basic(client):
    payload = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": "Say hi in one word."}]}
        ],
        "max_new_tokens": 8,
        "temperature": 1.0
    }
    r = client.post("/generate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["text"], str) and len(data["text"]) > 0
    assert data["tokens"] >= 1
    assert isinstance(data["duration_s"], float)

def test_generate_empty_messages_400(client):
    r = client.post("/generate", json={"messages": []})
    assert r.status_code == 400

def test_generate_echo_minimal(client):
    # check output
    target = "42-ABC"
    payload = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": f"Reply with exactly: {target}"}]}
        ],
        "max_new_tokens": 8,
        "temperature": 0.0001
    }
    r = client.post("/generate", json=payload)
    assert r.status_code == 200
    txt = r.json()["text"].strip()
    norm = txt.strip().strip('"').strip("'")
    assert target in norm
