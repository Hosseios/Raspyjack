#!/usr/bin/env python3

try:
    from fastapi import FastAPI
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


