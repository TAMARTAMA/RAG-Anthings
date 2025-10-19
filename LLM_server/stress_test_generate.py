import asyncio, time, argparse, json
import aiohttp

def pct(vals, p):
    """Return the p-th percentile of a numeric list (e.g., p=0.95)."""
    if not vals:
        return 0.0
    vals = sorted(vals)
    k = max(0, min(len(vals) - 1, int(p * (len(vals) - 1))))
    return vals[k]

async def one_call(session, url, payload, sem):
    t0 = time.perf_counter()
    async with sem:
        try:
            async with session.post(url, json=payload, timeout=120) as resp:
                await resp.read()
                ok = (resp.status == 200)
        except Exception:
            ok = False
    return ok, time.perf_counter() - t0  # seconds

async def warmup(session, url, payload, n=3):
    for _ in range(n):
        try:
            async with session.post(url, json=payload, timeout=120) as r:
                await r.read()
        except Exception:
            pass

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8013/generate")
    ap.add_argument("--rate", type=int, default=100, help="target requests/sec")
    ap.add_argument("--seconds", type=int, default=20)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--max-new-tokens", type=int, default=4)
    ap.add_argument("--warmup", type=int, default=3)
    args = ap.parse_args()

    # payload aligned with server: messages + minimal generation
    payload = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": "Reply with exactly: OK"}]}
        ],
        "max_new_tokens": args.max_new_tokens,
        "temperature": 0.0001,  # >0 to satisfy transformers validation
    }

    sem = asyncio.Semaphore(args.concurrency)
    latencies = []
    sent = 0
    ok_count = 0
    tasks = []

    async with aiohttp.ClientSession() as session:
        if args.warmup > 0:
            await warmup(session, args.url, payload, n=args.warmup)

        start = time.perf_counter()
        end = start + args.seconds

        async def fire():
            nonlocal ok_count
            ok, dt = await one_call(session, args.url, payload, sem)
            if ok:
                ok_count += 1
                latencies.append(dt)

        # Launch at target rate (best-effort)
        while time.perf_counter() < end:
            tasks.append(asyncio.create_task(fire()))
            sent += 1
            await asyncio.sleep(1 / max(1, args.rate))

        # Wait for all scheduled tasks to finish
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    dur = time.perf_counter() - start
    rps = ok_count / dur if dur > 0 else 0.0

    result = {
        "target_qps": args.rate,
        "duration_sec": round(dur, 3),
        "sent": sent,
        "ok": ok_count,
        "errors": sent - ok_count,
        "observed_rps": round(rps, 3),
        "p50_s": round(pct(latencies, 0.50), 3),
        "p95_s": round(pct(latencies, 0.95), 3),
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

