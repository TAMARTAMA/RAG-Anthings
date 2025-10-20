import LLM_server.server as server
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
        ],
        "temperature": 1.0
    }

def test_probabilities_basic_shape(client):
    r = client.post("/probabilities", json=_basic_payload())
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and isinstance(data["items"], list)
    assert server._tok is not None
    head_size = server._model.get_output_embeddings().weight.shape[0]
    assert len(data["items"]) == head_size
    first = data["items"][0]
    assert "token" in first and "prob" in first
    assert isinstance(first["token"], str)
    assert isinstance(first["prob"], float)

def test_probabilities_sum_and_bounds(client):
    r = client.post("/probabilities", json=_basic_payload())
    assert r.status_code == 200
    probs = [it["prob"] for it in r.json()["items"]]
    # sum ~ 1
    s = sum(probs)
    assert abs(s - 1.0) < 1e-5
    # bounds and finiteness
    assert all((p >= 0.0 and p <= 1.0 and math.isfinite(p)) for p in probs)

def test_probabilities_empty_messages_400(client):
    r = client.post("/probabilities", json={"messages": []})
    assert r.status_code == 400

def test_probabilities_temperature_zero_is_safe(client):
    payload = _basic_payload()
    payload["temperature"] = 0.0  # triggers safeguard inside the API
    r = client.post("/probabilities", json=payload)
    assert r.status_code == 200
    probs = [it["prob"] for it in r.json()["items"]]
    # still a valid distribution
    assert abs(sum(probs) - 1.0) < 1e-5
