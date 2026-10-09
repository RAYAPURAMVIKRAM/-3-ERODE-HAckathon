import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # API Health and Info endpoint
        if self.path.startswith("/api/health") or self.path == "/api":
            response_data = {
                "status": "online",
                "platform": "STARK-X Agriculture OS",
                "version": "2.0.0",
                "hackathon": "3-ERODE-Hackathon",
                "engine": "Autonomous Precision Agronomy"
            }
            body = json.dumps(response_data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Serve index.html if requested directly through API handler
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            msg = b"STARK-X Agriculture Engine is Online."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
