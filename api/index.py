from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>STARK-X | AgriPirate - 3-ERODE Hackathon</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
      background: linear-gradient(135deg, #09130b 0%, #102616 100%);
      color: #f1f5f9;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .card {
      max-width: 640px;
      width: 100%;
      background: rgba(18, 41, 23, 0.85);
      border: 1px solid #22c55e;
      border-radius: 20px;
      padding: 40px 32px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      text-align: center;
      backdrop-filter: blur(12px);
    }
    .badge {
      display: inline-block;
      background: #14532d;
      color: #4ade80;
      font-size: 13px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 50px;
      margin-bottom: 18px;
      letter-spacing: 0.5px;
    }
    h1 {
      font-size: 32px;
      color: #4ade80;
      margin-bottom: 12px;
      font-weight: 800;
    }
    p {
      color: #cbd5e1;
      font-size: 16px;
      line-height: 1.6;
      margin-bottom: 24px;
    }
    .features {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 28px;
      text-align: left;
    }
    .feature-item {
      background: rgba(0, 0, 0, 0.25);
      padding: 12px 16px;
      border-radius: 10px;
      border-left: 3px solid #22c55e;
      font-size: 14px;
      color: #e2e8f0;
    }
    .btn {
      display: inline-block;
      background: #22c55e;
      color: #052e16;
      padding: 14px 28px;
      border-radius: 10px;
      text-decoration: none;
      font-weight: 700;
      font-size: 15px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(34, 197, 94, 0.4);
    }
    .btn:hover {
      background: #16a34a;
      transform: translateY(-2px);
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">🚜 3-ERODE HACKATHON PROJECT</div>
    <h1>🌾 STARK-X | AgriPirate</h1>
    <p>Autonomous Precision Agronomy & FinTech Intelligence Platform calibrated for Kongu Nadu smallholder farmers.</p>
    
    <div class="features">
      <div class="feature-item">💬 <b>Agri-Chat:</b> WhatsApp-style Trilingual Advisory</div>
      <div class="feature-item">📸 <b>Crop Vision:</b> Google Gemini Leaf Pathology</div>
      <div class="feature-item">🌾 <b>Optimizer:</b> NPK & Soil Recommendation Engine</div>
      <div class="feature-item">📈 <b>Market & SOS:</b> FinTech Mandi & Supabase Helpdesk</div>
    </div>

    <a class="btn" href="https://github.com/RAYAPURAMVIKRAM/-3-ERODE-HAckathon" target="_blank">
      🚀 View GitHub Source Code
    </a>
  </div>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))
        return
