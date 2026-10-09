import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
import streamlit as st
from dotenv import load_dotenv

# Ensure root directory is on sys.path
_ROOT_DIR = str(Path(__file__).resolve().parent)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

# IST timezone setup
IST = timezone(timedelta(hours=5, minutes=30))

__all__ = [
    "IST",
    "get_ist_now",
    "format_to_ist",
    "sign_up_farmer",
    "sign_in_farmer",
    "quick_demo_login",
    "sign_out_farmer",
    "get_current_user",
    "is_supabase_connected",
    "insert_sos_ticket",
    "get_sos_tickets",
    "fetch_marketplace_crops",
    "add_marketplace_crop",
    "get_supabase_client",
]

def get_ist_now() -> str:
    """Returns current timestamp formatted in Indian Standard Time (IST)."""
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M")

def format_to_ist(ts_val) -> str:
    """Converts any timestamp (ISO string, UTC string, or standard string) into IST formatted string."""
    if not ts_val:
        return ""
    ts_str = str(ts_val).strip()
    try:
        if "T" in ts_str or "+" in ts_str or ts_str.endswith("Z"):
            cleaned = ts_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(cleaned)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(IST).strftime("%Y-%m-%d %H:%M")
        return ts_str
    except Exception:
        return ts_str

# Load fresh environment variables from both .env.local and .env
load_dotenv(".env.local", override=True)
load_dotenv(".env", override=True)
SUPABASE_URL = (os.getenv("SUPABASE_URL", "") or os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")).strip(' "\'')
SUPABASE_KEY = (os.getenv("SUPABASE_KEY", "") or os.getenv("SUPABASE_PUBLISHABLE_KEY", "") or os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY", "")).strip(' "\'')

# Initialize SQLite local database for offline / fallback mode
LOCAL_DB_PATH = "agripirate.db"

def init_local_db():
    conn = sqlite3.connect(LOCAL_DB_PATH)
    c = conn.cursor()
    # Farmers table for local auth
    c.execute('''CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        name TEXT,
        village TEXT,
        created_at TEXT
    )''')
    # SOS tickets table
    c.execute('''CREATE TABLE IF NOT EXISTS sos_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        village TEXT,
        category TEXT,
        description TEXT,
        timestamp TEXT
    )''')
    # Marketplace crops table
    c.execute('''CREATE TABLE IF NOT EXISTS marketplace_crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_name TEXT,
        phone_whatsapp TEXT,
        crop_name TEXT,
        quantity_kg REAL,
        price_per_kg REAL,
        location TEXT,
        created_at TEXT
    )''')
    
    # Seed initial demo crops if table is empty
    c.execute("SELECT COUNT(*) FROM marketplace_crops")
    if c.fetchone()[0] == 0:
        seed_data = [
            ('Murugan K.', '+919876543210', 'Erode Organic Turmeric (Finger)', 500.0, 145.0, 'Perundurai, Erode', '2026-10-09 09:30'),
            ('Selvam P.', '+919443218765', 'Sugarcane (CO-86032)', 1200.0, 32.0, 'Bhavani, Erode', '2026-10-09 08:15'),
            ('Vignesh R.', '+919842155678', 'Pearl Millet (Kambu / Bajra)', 350.0, 42.0, 'Sathyamangalam', '2026-10-09 07:45')
        ]
        c.executemany("""INSERT INTO marketplace_crops 
                         (farmer_name, phone_whatsapp, crop_name, quantity_kg, price_per_kg, location, created_at) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)""", seed_data)
                         
    conn.commit()
    conn.close()

init_local_db()

@st.cache_resource
def get_supabase_client():
    """Initializes and caches the Supabase client if keys are present."""
    if not SUPABASE_URL or not SUPABASE_KEY or "your-project" in SUPABASE_URL:
        return None
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase initialization error: {e}")
        return None

def is_supabase_connected() -> bool:
    """Checks if Supabase credentials are configured."""
    return get_supabase_client() is not None

# ================= AUTHENTICATION FUNCTIONS =================

def sign_up_farmer(email: str, password: str, name: str, village: str):
    """Registers a new farmer with Supabase or fallback local database."""
    client = get_supabase_client()
    
    # 1. Supabase Cloud Sign Up
    if client:
        try:
            res = client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name,
                        "village": village
                    }
                }
            })
            if res.user:
                user_data = {
                    "id": res.user.id,
                    "email": email,
                    "name": name,
                    "village": village,
                    "provider": "supabase"
                }
                st.session_state["user"] = user_data
                return True, "Farmer account registered with Supabase!"
        except Exception as e:
            return False, f"Supabase Registration Error: {str(e)}"
            
    # 2. Local Fallback Database Sign Up
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        now = get_ist_now()
        c.execute("INSERT INTO farmers (email, password, name, village, created_at) VALUES (?, ?, ?, ?, ?)",
                  (email, password, name, village, now))
        conn.commit()
        conn.close()
        
        user_data = {
            "email": email,
            "name": name,
            "village": village,
            "provider": "local"
        }
        st.session_state["user"] = user_data
        return True, "Account registered successfully (Local Database)!"
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception as e:
        return False, f"Registration Error: {str(e)}"

def sign_in_farmer(email: str, password: str):
    """Signs in farmer with Supabase or fallback local database."""
    client = get_supabase_client()
    
    # 1. Supabase Cloud Sign In
    if client:
        try:
            res = client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if res.user:
                meta = res.user.user_metadata or {}
                user_data = {
                    "id": res.user.id,
                    "email": email,
                    "name": meta.get("name", email.split("@")[0]),
                    "village": meta.get("village", "Tamil Nadu"),
                    "provider": "supabase"
                }
                st.session_state["user"] = user_data
                return True, "Login successful with Supabase!"
        except Exception as e:
            return False, f"Supabase Login Error: {str(e)}"
            
    # 2. Local Fallback Database Sign In
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name, village FROM farmers WHERE email = ? AND password = ?", (email, password))
        row = c.fetchone()
        conn.close()
        
        if row:
            user_data = {
                "email": email,
                "name": row[0],
                "village": row[1],
                "provider": "local"
            }
            st.session_state["user"] = user_data
            return True, "Login successful!"
        else:
            return False, "Invalid email or password."
    except Exception as e:
        return False, f"Login Error: {str(e)}"

def quick_demo_login():
    """Instant login as verified farmer for demo / hackathon presentation."""
    demo_user = {
        "email": "murugan.erode@agripirate.org",
        "name": "Murugan K.",
        "village": "Perundurai, Erode (TN)",
        "provider": "demo"
    }
    st.session_state["user"] = demo_user
    return True

def sign_out_farmer():
    """Signs out current farmer session."""
    client = get_supabase_client()
    if client:
        try:
            client.auth.sign_out()
        except Exception:
            pass
    if "user" in st.session_state:
        del st.session_state["user"]

def get_current_user():
    """Returns current logged-in farmer data or None."""
    return st.session_state.get("user")

# ================= DATABASE DATA FUNCTIONS =================

def insert_sos_ticket(farmer_name: str, village: str, category: str, description: str):
    """Inserts an emergency SOS ticket to Supabase and local SQLite in IST."""
    now = get_ist_now()
    
    # Always save to local SQLite first for instant responsiveness
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sos_tickets (name, village, category, description, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (farmer_name, village, category, description, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Local ticket save error: {e}")
        
    # Also save to Supabase if connected
    client = get_supabase_client()
    if client:
        try:
            client.table("sos_tickets").insert({
                "name": farmer_name,
                "village": village,
                "category": category,
                "description": description,
                "timestamp": now
            }).execute()
        except Exception as e:
            print(f"Supabase ticket insert error (table may not be created yet): {e}")

def get_sos_tickets():
    """Fetches tickets from Supabase if table exists, or falls back to local SQLite, formatted in IST."""
    client = get_supabase_client()
    if client:
        try:
            res = client.table("sos_tickets").select("*").order("id", desc=True).execute()
            if res.data and len(res.data) > 0:
                import pandas as pd
                for row in res.data:
                    if "timestamp" in row:
                        row["timestamp"] = format_to_ist(row.get("timestamp"))
                df = pd.DataFrame(res.data)
                # Map column names nicely
                col_map = {
                    "timestamp": "Date",
                    "name": "Farmer",
                    "village": "Location",
                    "category": "Emergency",
                    "description": "Details"
                }
                return df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
        except Exception as e:
            print(f"Supabase fetch fallback to SQLite: {e}")
            
    # Fallback to SQLite
    import pandas as pd
    conn = sqlite3.connect(LOCAL_DB_PATH)
    df = pd.read_sql_query("SELECT timestamp as Date, name as Farmer, village as Location, category as Emergency, description as Details FROM sos_tickets ORDER BY id DESC", conn)
    conn.close()
    if not df.empty and "Date" in df.columns:
        df["Date"] = df["Date"].apply(format_to_ist)
    return df

# ================= MARKETPLACE FUNCTIONS =================

def fetch_marketplace_crops():
    """Fetches marketplace crop listings from Supabase or SQLite fallback, formatted in IST."""
    client = get_supabase_client()
    if client:
        try:
            response = client.table("marketplace_crops").select("*").order("id", desc=True).execute()
            if response.data is not None and len(response.data) > 0:
                for item in response.data:
                    if "created_at" in item:
                        item["created_at"] = format_to_ist(item.get("created_at"))
                return response.data
        except Exception as e:
            print(f"Supabase fetch_marketplace_crops fallback to SQLite: {e}")

    # Fallback to local SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, farmer_name, phone_whatsapp, crop_name, quantity_kg, price_per_kg, location, created_at FROM marketplace_crops ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return [
            {
                "id": r[0],
                "farmer_name": r[1],
                "phone_whatsapp": r[2],
                "crop_name": r[3],
                "quantity_kg": r[4],
                "price_per_kg": r[5],
                "location": r[6],
                "created_at": format_to_ist(r[7])
            }
            for r in rows
        ]
    except Exception as e:
        print(f"Local SQLite fetch_marketplace_crops error: {e}")
        return []

def add_marketplace_crop(farmer, phone, crop, qty, price, loc):
    """Adds a new crop listing to Supabase and SQLite fallback in IST."""
    now = get_ist_now()
    
    # 1. Save locally first for guaranteed zero-downtime
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO marketplace_crops 
                     (farmer_name, phone_whatsapp, crop_name, quantity_kg, price_per_kg, location, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (farmer, phone, crop, qty, price, loc, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Local SQLite add_marketplace_crop error: {e}")

    # 2. Sync to Supabase with explicit created_at timestamp in IST
    client = get_supabase_client()
    if client:
        try:
            client.table("marketplace_crops").insert({
                "farmer_name": farmer,
                "phone_whatsapp": phone,
                "crop_name": crop,
                "quantity_kg": qty,
                "price_per_kg": price,
                "location": loc,
                "created_at": now
            }).execute()
            return True
        except Exception as e:
            print(f"Supabase add_marketplace_crop error: {e}")
            return True
            
    return True

