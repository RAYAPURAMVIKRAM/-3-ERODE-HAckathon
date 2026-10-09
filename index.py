import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the STARK-X index.html web application
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"STARK-X Autonomous Agriculture Engine is Online.")

# Standalone execution for local testing
if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(("0.0.0.0", 3000), handler)
    print("Serving on http://localhost:3000")
    server.serve_forever()
