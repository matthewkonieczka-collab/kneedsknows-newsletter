"""
Newsletter signup backend.

Run locally:
    uvicorn landing-page.subscribe:app --reload --port 8000

Deploy to Render/Railway:
    uvicorn landing-page.subscribe:app --host 0.0.0.0 --port $PORT
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Newsletter Signup")

# Allow CORS for Squarespace embedding + local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.kneedsknows.com",
        "https://kneedsknows.com",
        "https://parrotfish-hyperboloid-rngt.squarespace.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

LANDING_DIR = Path(__file__).parent
DATA_FILE = LANDING_DIR / "data" / "subscribers.json"


class SubscribeRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str = ""


def _load_subscribers() -> list[dict]:
    DATA_FILE.parent.mkdir(exist_ok=True)
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def _save_subscribers(subs: list[dict]):
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(subs, indent=2, ensure_ascii=False), encoding="utf-8")


@app.post("/api/subscribe")
async def subscribe(req: SubscribeRequest):
    subs = _load_subscribers()

    # Check for duplicate email
    if any(s["email"].lower() == req.email.lower() for s in subs):
        return {"message": "You're already subscribed! Check your inbox this Sunday."}

    subs.append({
        "first_name": req.first_name,
        "last_name": req.last_name,
        "email": req.email,
        "phone": req.phone,
        "subscribed_at": datetime.now(timezone.utc).isoformat(),
    })
    _save_subscribers(subs)

    return {"message": "Subscribed successfully! Your first newsletter arrives this Sunday."}


@app.get("/api/subscribers/count")
async def subscriber_count():
    subs = _load_subscribers()
    return {"count": len(subs)}


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def index():
    return FileResponse(LANDING_DIR / "index.html")


# Clean-URL routes for each page (extensionless paths -> .html files).
# These must be declared BEFORE the StaticFiles mount.
_PAGES = ["subscribe", "store", "deals", "newsletter", "book"]


def _make_page_route(name: str):
    async def _route():
        return FileResponse(LANDING_DIR / f"{name}.html")
    _route.__name__ = f"page_{name}"
    return _route


for _page in _PAGES:
    app.add_api_route(f"/{_page}", _make_page_route(_page), methods=["GET"])


# Serve static files (CSS, etc.)
app.mount("/", StaticFiles(directory=str(LANDING_DIR)), name="static")
