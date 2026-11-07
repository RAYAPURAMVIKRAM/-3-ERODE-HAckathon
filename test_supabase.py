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
        print(f"   - [{r.get('timestamp')}] {r.get('name')} ({r.get('village')}): {r.get('category')} - {r.get('description')}")
        
except Exception as e:
    err_str = str(e)
    if "PGRST205" in err_str or "schema cache" in err_str or "not found" in err_str.lower():
        print("\n[ATTENTION] Table 'public.sos_tickets' has NOT been created yet in Supabase!")
        print("\n--> ACTION REQUIRED (Takes only 15 seconds):")
        print("   1. Open: https://supabase.com/dashboard/project/rhomwvtmmkwepclzaiuu/sql")
        print("   2. Open the file 'supabase_setup.sql' in your project root")
        print("   3. Paste into the SQL Editor and click the green 'RUN' button.")
        print("   4. Re-run this test script: python test_supabase.py")
        print("\n[NOTE] Don't worry! AgriPirate's built-in Demo Fallback system is active, so the app is fully functional with live demo data.")
    else:
        print(f"\n[WARNING] Query notice: {e}")

print("\n" + "=" * 60)
