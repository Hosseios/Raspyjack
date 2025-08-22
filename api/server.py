#!/usr/bin/env python3

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
except Exception as e:  # FastAPI not installed on the device
    raise SystemExit(f"FastAPI import failed: {e}. Install with: pip3 install fastapi uvicorn[standard]")

import os
import time
from typing import Iterator
from fastapi.responses import StreamingResponse

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
_current_payload_name = None
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

    global _is_running, _current_payload_name
    if _run_lock is None:
        # Fallback: run inline (not recommended)
        EXEC_PAYLOAD(name)
        return {"status": "finished", "name": name}

    with _run_lock:
        if _is_running:
            raise HTTPException(status_code=409, detail="Another payload is running")
        _is_running = True
        _current_payload_name = name

    def _worker():
        global _is_running, _current_payload_name
        try:
            EXEC_PAYLOAD(name)
        finally:
            if _run_lock:
                with _run_lock:
                    _is_running = False
                    _current_payload_name = None
            else:
                _is_running = False
                _current_payload_name = None

    threading.Thread(target=_worker, daemon=True).start()
    return {"status": "started", "name": name}


@app.get("/api/status")
def api_status():
    if _run_lock:
        with _run_lock:
            return {"running": _is_running, "name": _current_payload_name}
    return {"running": _is_running, "name": _current_payload_name}


@app.get("/api/logs/tail")
def api_tail_logs(from_start: bool = False) -> StreamingResponse:
    """Stream loot/payload.log lines as they are written."""
    log_path = "/root/Raspyjack/loot/payload.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    open(log_path, "ab").close()  # ensure file exists

    def _iter() -> Iterator[bytes]:
        with open(log_path, "rb", buffering=0) as f:
            if not from_start:
                try:
                    f.seek(0, os.SEEK_END)
                except Exception:
                    pass
            while True:
                chunk = f.readline()
                if chunk:
                    yield chunk
                else:
                    time.sleep(0.2)

    return StreamingResponse(_iter(), media_type="text/plain")


