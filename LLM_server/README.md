# 📘 Gemma 3 LLM Server & Stress Test

## 📁 Directory Structure
```

└── Moptimizer/
    └── LLM_server/
        ├── server.py              # FastAPI server serving the Gemma model
        ├── config.json            # Configuration file for model path & parameters
        ├── test_generate.py       # Unit tests for the API
        ├── stress_generate.py     # Load/Stress testing script
```

---

## 🚀 Run the Server

1. Make sure `config.json` points to the correct local model path:
   ```json
   {
     "model_dir": "/home/ruth/SERVER_shared/Models/gemma-3-4b-it",
     "dtype": "float32",
     "device_map": "cpu",
     "system_prompt": "You are a helpful assistant.",
     "default_max_new_tokens": 200,
     "default_temperature": 0.2
   }
   ```

2. Start the FastAPI server:
   ```bash
   cd ~/SERVER_shared
   uvicorn servers.Moptimizer.LLM_server.server:app --host 0.0.0.0 --port 8013
   ```

3. Quick API check:
   ```bash
   curl -s http://127.0.0.1:8013/health
   curl -s -X POST http://127.0.0.1:8013/generate \
     -H 'Content-Type: application/json' \
     -d '{"prompt":"Say hi in one word","max_new_tokens":4,"temperature":0.0}'
   ```

---

## 🧪 Unit Tests

To verify the API endpoints without running the server separately:

```bash
PYTHONPATH=. pytest -q servers/Moptimizer/LLM_server/test_generate.py
```

✅ Expected output example:
```
.... [100%]
```

> Note: The `@app.on_event("startup")` deprecation warning is harmless for now.

---

## ⚡ Stress Test (Performance Benchmark)

### Run the Test
In a new terminal (with the server running):

```bash
python servers/Moptimizer/LLM_server/stress_generate.py \
  --url http://127.0.0.1:8013/generate \
  --rate 100 \
  --seconds 20 \
  --concurrency 16 \
  --max-new-tokens 4
```

### What It Does
- Sends hundreds/thousands of `POST /generate` requests at a fixed rate.
- Measures how many succeed (`status 200`), response latencies, and actual throughput.

---

## 📊 Stress Test Metrics Explained

| Field | Meaning | Interpretation |
|--------|----------|----------------|
| **target_qps** | Desired request rate (Queries Per Second) | How many requests per second we attempted to send |
| **duration_sec** | Total test duration | Should be close to `--seconds` |
| **sent** | Total number of requests sent | Includes both successful and failed |
| **ok** | Successful requests (`HTTP 200`) | Should be nearly equal to `sent` |
| **errors** | Failed or timed-out requests | If high → indicates overload or network issues |
| **observed_rps** | Actual achieved QPS | If much lower than target → bottleneck (CPU/GPU/Network) |
| **p50_ms** | Median latency (50%) | Typical response time (good if <300–400 ms) |
| **p95_ms** | 95th percentile latency | Shows tail latency — how slow the worst 5% are (good if <1000 ms) |

---

## 📈 Example Output
```json
{
  "target_qps": 100,
  "duration_sec": 20.1,
  "sent": 2000,
  "ok": 1978,
  "errors": 22,
  "observed_rps": 98.3,
  "p50_ms": 280,
  "p95_ms": 610
}
```

### Interpretation
- The server handled ~100 requests/sec successfully.
- Most responses are quick (~0.28 s median).
- Only 1–2% failed (expected at high load).
- If `p95_ms` grows or `errors` increase → system saturation.

---

## 🧠 Best Practices

- **Shorter tests for quick checks:**
  ```bash
  python stress_generate.py --seconds 5 --rate 20
  ```
- **Gradually increase rate:**
  Start low (10 QPS) → 50 → 100 → until you find breaking point.
- **For GPU use:**
  Set `"device_map": "auto"` and `"dtype": "bfloat16"` or `"float16"` in `config.json`.
- **Monitor system load:**
  ```bash
  htop
  nvidia-smi
  ```

---

## ✅ Summary

| Step | Purpose | Command |
|------|----------|----------|
| 🧱 Load model | Verify configuration | `uvicorn ...` |
| ✅ Unit test | Check API correctness | `pytest` |
| ⚡ Stress test | Measure performance | `python stress_generate.py` |

---


**Author:** Ruth @ ETA  
**Date:** 2025-10-15  
**Project:** Moptimizer – Gemma LLM API & Benchmark Tools
