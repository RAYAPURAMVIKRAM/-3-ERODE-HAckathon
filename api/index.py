"""
api/index.py
Vercel Serverless Function entrypoint for STARK-X AgriPirate.
Provides FastAPI ASGI routing with zero-404 middleware fix.
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

# Add root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

app = FastAPI(title="STARK-X AgriPirate API", version="2.0.0")

# Vercel matched path rewrite middleware to prevent 404s on rewritten routes
@app.middleware("http")
async def fix_vercel_matched_path(request: Request, call_next):
    matched = (
        request.headers.get("x-matched-path") or
        request.headers.get("x-vercel-matched-path") or
        request.headers.get("x-original-uri")
    )
    if matched:
        request.scope["path"] = matched
    else:
        path = request.scope.get("path", "")
        for prefix in ["/api/index.py", "/api/index"]:
            if path.startswith(prefix):
                new_path = path[len(prefix):] or "/"
                request.scope["path"] = new_path
                break
    return await call_next(request)

def get_index_html_content() -> str:
    html_path = ROOT_DIR / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>STARK-X Agriculture Engine is Online.</h1>"

@app.get("/health")
@app.get("/api/health")
@app.get("/api")
async def health_check():
    return {
        "status": "online",
        "platform": "STARK-X Agriculture OS",
        "version": "2.0.0",
        "hackathon": "3-ERODE-Hackathon",
        "engine": "Autonomous Precision Agronomy"
    }

@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def serve_index():
    return HTMLResponse(content=get_index_html_content())

@app.get("/api/index.py")
@app.get("/api/index")
async def vercel_inspect(request: Request):
    # If hit directly without path rewrite, serve index or gateway info
    return HTMLResponse(content=get_index_html_content())

# Catch-all route to serve the Single Page Application for any subpaths
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_spa(full_path: str):
    if full_path in ["health", "api/health", "api"]:
        return JSONResponse({
            "status": "online",
            "platform": "STARK-X Agriculture OS",
            "version": "2.0.0",
            "hackathon": "3-ERODE-Hackathon",
            "engine": "Autonomous Precision Agronomy"
        })
    return HTMLResponse(content=get_index_html_content())
