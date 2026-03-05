import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

TOKEN   = os.getenv("DISCORD_TOKEN", "")
GUILD   = os.getenv("GUILD_ID",   "1093281735137054752")
CHANNEL = os.getenv("CHANNEL_ID", "1450312141750931457")

DISCORD_API = "https://discord.com/api/v10"
HEADERS = {"Authorization": TOKEN}

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://evanblokender.org", "https://api.evanblokender.org"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── HTML (token injected server-side, never exposed to client) ──────────────
HTML = open("index.html", encoding="utf-8").read().replace("__DISCORD_TOKEN__", "PROXIED")

@app.get("/mm", response_class=HTMLResponse)
async def serve_viewer():
    return HTMLResponse(content=HTML)


# ── Proxy: channel info ──────────────────────────────────────────────────────
@app.get("/mm/api/channel")
async def get_channel():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{DISCORD_API}/channels/{CHANNEL}", headers=HEADERS)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()


# ── Proxy: messages ──────────────────────────────────────────────────────────
@app.get("/mm/api/messages")
async def get_messages(
    limit: int = Query(default=100, ge=1, le=100),
    before: str = Query(default=None),
):
    params = {"limit": limit}
    if before:
        params["before"] = before

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{DISCORD_API}/channels/{CHANNEL}/messages",
            headers=HEADERS,
            params=params,
        )
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return JSONResponse(content=r.json())
