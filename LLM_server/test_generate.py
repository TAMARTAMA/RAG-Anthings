from pathlib import Path
from fastapi.testclient import TestClient
import concurrent.futures as futures
import pytest

from .server import app, MODEL_DIR

# validate model path
pytestmark = pytest.mark.skipif(
    not Path(MODEL_DIR).exists(),
    reason=f"model_dir not found: {MODEL_DIR}",
)

# client אחד לכל הסשן – מעלה את המודל פעם אחת (startup) וסוגר בסוף
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_generate_basic(client):
    r = client.post(
        "/generate",
        json={"prompt": "Say hi in one word", "max_new_tokens": 4, "temperature": 0.0},
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["text"], str) and len(data["text"]) > 0
    assert data["tokens"] >= 1
    assert isinstance(data["duration_ms"], int)

def test_generate_empty_prompt_400(client):
    r = client.post("/generate", json={"prompt": "   "})
    assert r.status_code == 400

def test_generate_small_concurrency(client):
    # little stress
    def one(i):
        return client.post(
            "/generate",
            json={"prompt": f"Echo {i} in one word", "max_new_tokens": 4, "temperature": 0.0},
        )

    with futures.ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(one, range(3)))

    assert all(r.status_code == 200 for r in results)

    #run
    #PYTHONPATH=. pytest -q servers/Moptimizer/LLM_server/test_generate.py

