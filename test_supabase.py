import os
import sys
import sqlite3
from dotenv import load_dotenv

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment
load_dotenv(".env.local", override=True)
load_dotenv(".env", override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = (
    os.getenv("SUPABASE_KEY", "") or
    os.getenv("SUPABASE_ANON_KEY", "") or
    os.getenv("SUPABASE_PUBLISHABLE_KEY", "") or
    os.getenv("SUPABASE_SERVICE_ROLE_KEY", "") or
    os.getenv("SUPABASE_SECRET_KEY", "")
)

print("=" * 60)
print("[STARK-X AgriPirate] Supabase Cloud Diagnostics")
print("=" * 60)
print(f"Supabase Endpoint: {SUPABASE_URL}")
print(f"Key Prefix:        {SUPABASE_KEY[:16]}..." if SUPABASE_KEY else "No key found")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\n[ERROR] SUPABASE_URL or SUPABASE_KEY missing in .env or .env.local")
    exit(1)

try:
    from supabase import create_client
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("\n[OK] Supabase Client initialized successfully!")
except Exception as e:
    print(f"\n[FAIL] Client initialization failed: {e}")
    exit(1)

# Check sos_tickets table
print("\n[CHECK] Querying 'public.sos_tickets' table in Supabase...")
try:
    res = sb.table("sos_tickets").select("*").limit(5).execute()
    print("[SUCCESS] 'public.sos_tickets' table exists and is connected in Supabase!")
    print(f"   Found {len(res.data)} existing records in cloud:")
    for r in res.data:
        f_name = r.get('farmer_name') or r.get('name') or "Farmer"
        v_name = r.get('village') or "Erode"
        cat = r.get('issue_type') or r.get('category') or "General"
        desc = r.get('description') or ""
        ts = r.get('created_at') or r.get('timestamp') or ""
        print(f"   - [{ts[:19]}] {f_name} ({v_name}): {cat} - {desc[:60]}...")
        
except Exception as e:
    err_str = str(e)
    if "PGRST205" in err_str or "schema cache" in err_str or "not found" in err_str.lower():
        print("\n[ATTENTION] Table 'public.sos_tickets' has NOT been created yet in Supabase!")
    else:
        print(f"\n[WARNING] Query notice: {e}")

# Check marketplace_crops table
print("\n[CHECK] Querying 'public.marketplace_crops' table in Supabase...")
try:
    c_res = sb.table("marketplace_crops").select("*").limit(5).execute()
    print("[SUCCESS] 'public.marketplace_crops' table exists and is connected in Supabase!")
    print(f"   Found {len(c_res.data)} existing listings in cloud:")
    for c in c_res.data:
        c_crop = c.get('crop_name') or "Crop"
        c_farmer = c.get('farmer_name') or "Farmer"
        c_qty = c.get('quantity_kg') or 0
        c_price = c.get('price_per_kg') or 0
        c_phone = c.get('phone') or c.get('phone_whatsapp') or ""
        print(f"   - {c_crop} ({c_qty} kg @ ₹{c_price}/kg) listed by {c_farmer} [{c_phone}]")
except Exception as e:
    print(f"\n[WARNING] Marketplace query notice: {e}")

print("\n" + "=" * 60)
