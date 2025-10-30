import math
import pytest
from fastapi.testclient import TestClient
import Moptimizer.LLM_server.server as server

@pytest.fixture(scope="session")
def client():
    # השרת טוען מודל ב-startup; ודאי שהמודל נגיש במסלול שב-config.json
    with TestClient(server.app) as c:
        yield c

def _payload(prompt: str):
    return {"prompt": prompt}

def test_probabilities_basic_shape(client):
    r = client.post("/probabilities", json=_payload("Hello"))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and isinstance(data["items"], list)
    assert len(data["items"]) > 0
    first = data["items"][0]
    assert "token" in first and "prob" in first
    assert isinstance(first["token"], str)
    assert isinstance(first["prob"], float)

def test_probabilities_sum_and_bounds(client):
    r = client.post("/probabilities", json=_payload("Hello"))
    assert r.status_code == 200
    probs = [it["prob"] for it in r.json()["items"]]
    s = sum(probs)
    assert abs(s - 1.0) < 1e-5
    assert all((0.0 <= p <= 1.0 and math.isfinite(p)) for p in probs)

def test_probabilities_empty_prompt_400(client):
    r1 = client.post("/probabilities", json={"prompt": ""})
    r2 = client.post("/probabilities", json={"prompt": "   "})
    assert r1.status_code == 400
    assert r2.status_code == 400

def test_probabilities_functional_argmax_is_reasonable(client):
    prompt = "Reply with exactly: 1"
    r = client.post("/probabilities", json=_payload(prompt))
    assert r.status_code == 200
    items = r.json()["items"]
    assert len(items) > 0
    argmax_idx = max(range(len(items)), key=lambda i: items[i]["prob"])
    top_token = items[argmax_idx]["token"]
    assert "1" in top_token

