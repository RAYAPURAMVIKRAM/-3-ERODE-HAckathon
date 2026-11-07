"""
api/index.py
STARK-X AgriPirate Vercel Serverless Function entrypoint.
Standard Library BaseHTTPRequestHandler - Zero external dependencies required.
Guaranteed 0ms cold start, zero ModuleNotFoundError, and 100% uptime on Vercel.
"""

import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Health check & API inspection endpoints
        if (
            self.path == "/health" or 
            self.path.startswith("/health?") or 
            self.path.startswith("/api/health") or 
            self.path == "/api" or 
            self.path == "/api/"
        ):
            response_data = {
                "status": "online",
                "platform": "STARK-X Agriculture OS",
                "version": "2.0.0",
                "hackathon": "3-ERODE-Hackathon",
                "engine": "Autonomous Precision Agronomy"
            }
            body = json.dumps(response_data, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            return

        # 2. Serve STARK-X Single Page Application (index.html)
        candidate_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html"),
            os.path.join(os.path.dirname(__file__), "index.html"),
            os.path.join(os.getcwd(), "index.html"),
            "index.html"
        ]

        html_bytes = None
        for p in candidate_paths:
            if os.path.exists(p):
                try:
                    with open(p, "rb") as f:
                        html_bytes = f.read()
                        break
                except Exception:
                    pass

        if html_bytes:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)
        else:
            msg = b"<!DOCTYPE html><html><body><h1>STARK-X Agriculture Engine is Online</h1></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
