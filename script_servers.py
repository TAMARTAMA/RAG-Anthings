import subprocess
import threading

servers = [
    ("Server 1", "cd ~/SERVER_shared/B/data/KG/search && uvicorn app.main:app --host 0.0.0.0 --port 8003"),
    ("Server 2", "cd /srv/python_envs/shared_env/B/code/SERVER/Server && uvicorn app.main:app --reload --host 0.0.0.0 --port 8002"),
    ("Server 3", "cd B && uvicorn Moptimizer.LLM_server.server:app --host 0.0.0.0 --port 8013")
]

def stream_output(name, process):
    """מאזין לפלט ומדפיס עם תיוג השרת"""
    for line in iter(process.stdout.readline, b''):
        print(f"[{name}] {line.decode().rstrip()}")
    process.stdout.close()

processes = []
for name, cmd in servers:
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    t = threading.Thread(target=stream_output, args=(name, p), daemon=True)
    t.start()
    processes.append(p)

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\n[INFO] סוגר את כל השרתים...")
    for p in processes:
        p.terminate()
