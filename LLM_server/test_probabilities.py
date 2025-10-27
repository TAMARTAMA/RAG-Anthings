import Moptimizer.LLM_server.server as server
from fastapi.testclient import TestClient
import pytest
import math

@pytest.fixture(scope="session")
def client():
    with TestClient(server.app) as c:
        yield c

def _basic_payload():
    return {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": "Say hi in one word."}]}
        ]
    }

def test_probabilities_basic_shape(client):
    r = client.post("/probabilities", json=_basic_payload())
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and isinstance(data["items"], list)
    assert len(data["items"]) > 0
    first = data["items"][0]
    assert "token" in first and "prob" in first
    assert isinstance(first["token"], str)
    assert isinstance(first["prob"], float)

def test_probabilities_sum_and_bounds(client):
    r = client.post("/probabilities", json=_basic_payload())
    assert r.status_code == 200
    probs = [it["prob"] for it in r.json()["items"]]
    s = sum(probs)
    assert abs(s - 1.0) < 1e-5
    assert all((p >= 0.0 and p <= 1.0 and math.isfinite(p)) for p in probs)

def test_probabilities_empty_messages_400(client):
    r = client.post("/probabilities", json={"messages": []})
    assert r.status_code == 400

def test_probabilities_functional_argmax_is_reasonable(client):
    payload = {
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Reply with exactly: 1"}
            ]}
        ]
    }
    r = client.post("/probabilities", json=payload)
    assert r.status_code == 200
    items = r.json()["items"]
    argmax_idx = max(range(len(items)), key=lambda i: items[i]["prob"])
    top_token = items[argmax_idx]["token"]
    assert "1" in top_token
