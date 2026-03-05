# Discord Release Viewer — api.evanblokender.org/mm

FastAPI backend that proxies Discord API calls server-side (token never exposed to browser).

## Files
```
main.py          ← FastAPI app
index.html       ← Discord-style frontend
requirements.txt
.env.example     ← copy to .env and fill in
Procfile         ← for Render / Railway
```

## Local dev
```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env with your token
uvicorn main:app --reload --port 8000
# open http://localhost:8000/mm
```

## Deploy on Render
1. Push this folder to a GitHub repo
2. New Web Service → connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `DISCORD_TOKEN=your_token`
6. Deploy

## Cloudflare setup (api.evanblokender.org)
Add a CNAME record:
```
Type: CNAME
Name: api
Target: your-render-app.onrender.com
Proxy: ON (orange cloud)
```

Add a Cloudflare Page Rule for `api.evanblokender.org/mm*`:
- Cache Level: Bypass  (so messages are always fresh)

## Endpoints
| Route | Description |
|---|---|
| GET /mm | Serves the viewer HTML |
| GET /mm/api/channel | Channel info (name, topic) |
| GET /mm/api/messages?limit=100&before=ID | Paginated messages |
