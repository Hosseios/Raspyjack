#!/usr/bin/env python3

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
except Exception as e:  # FastAPI not installed on the device
    raise SystemExit(f"FastAPI import failed: {e}. Install with: pip3 install fastapi uvicorn[standard]")


app = FastAPI(title="RaspyJack API", version="0.1.0")

# CORS – adjust origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# --- Bridge to RaspyJack runtime (set from raspyjack.py) --------------------
EXEC_PAYLOAD = None
LIST_PAYLOADS = None

_is_running = False
try:
    import threading
    _run_lock = threading.Lock()
except Exception:
    _run_lock = None


def attach_raspyjack(exec_payload_fn, list_payloads_fn):
    global EXEC_PAYLOAD, LIST_PAYLOADS
    EXEC_PAYLOAD = exec_payload_fn
    LIST_PAYLOADS = list_payloads_fn


@app.get("/api/payloads")
def api_list_payloads():
    names = LIST_PAYLOADS() if LIST_PAYLOADS else []
    return {"payloads": [{"name": n} for n in names]}


@app.post("/api/payloads/{name}/run")
def api_run_payload(name: str):
    if EXEC_PAYLOAD is None:
        raise HTTPException(status_code=503, detail="Payload runner unavailable")

    if not name.endswith(".py"):
        name = name + ".py"

    allowed = LIST_PAYLOADS() if LIST_PAYLOADS else []
    if name not in allowed:
        raise HTTPException(status_code=404, detail="Payload not found")

    global _is_running
    if _run_lock is None:
        # Fallback: run inline (not recommended)
        EXEC_PAYLOAD(name)
        return {"status": "finished", "name": name}

    with _run_lock:
        if _is_running:
            raise HTTPException(status_code=409, detail="Another payload is running")
        _is_running = True

    def _worker():
        global _is_running
        try:
            EXEC_PAYLOAD(name)
        finally:
            if _run_lock:
                with _run_lock:
                    _is_running = False
            else:
                _is_running = False

    threading.Thread(target=_worker, daemon=True).start()
    return {"status": "started", "name": name}


