import types
import torch
import importlib
from fastapi.testclient import TestClient

# We import the server module and then monkeypatch its global 'model' and 'tok'.
server = importlib.import_module("server")

class FakeOut:
    def __init__(self, logits):
        self.logits = logits

class FakeModel:
    def __call__(self, input_ids):
        # Return logits with shape [1, T=3, V=5]; we only use the last position for top-k.
        # Last row probabilities (after softmax) will favor token 3 > token 1 > others.
        last = torch.tensor([[0.1, 2.0, -1.0, 3.0, 0.0]])    # [1, 5]
        logits = torch.cat([last, last, last], dim=0).unsqueeze(0)  # [1, 3, 5]
        return FakeOut(logits)

    def eval(self):
        return self

class FakeTokenizer:
    pad_token_id = 0

    def apply_chat_template(self, messages, add_generation_prompt=True, return_tensors="pt"):
        # We just need *some* tensor; content is irrelevant for the fake model.
        return torch.tensor([[1, 2, 3]])

    def decode(self, token_tensor):
        tid = int(token_tensor.item())
        return f"<T{tid}>"

# Monkeypatch globals
server.model = FakeModel().eval()
server.tok = FakeTokenizer()

client = TestClient(server.app)

def test_next_token_topk_core():
    res = server.next_token_topk("hello", 3)
    assert "top_k" in res and "vocab_size" in res
    assert res["vocab_size"] == 5
    # top-1 should be token 3 according to our fake logits
    assert res["top_k"][0]["token_id"] == 3
    assert res["top_k"][0]["token"] == "<T3>"
    assert 0.0 <= res["top_k"][0]["prob"] <= 1.0

def test_api_next_token_probs():
    r = client.post("/next_token_probs", json={"question": "hello", "top_k": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["vocab_size"] == 5
    assert len(body["top_k"]) == 2
    assert body["top_k"][0]["token_id"] == 3
