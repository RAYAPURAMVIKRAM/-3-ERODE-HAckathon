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
    "DEFAULT_DEMO_TICKETS",
    "DEFAULT_DEMO_CROPS",
]

# Rich pre-seeded fallback data for AgriPirate
DEFAULT_DEMO_TICKETS = [
    {
        "Date": "2026-11-07 10:15",
        "Farmer": "Murugan K.",
        "Location": "Perundurai, Erode",
        "Emergency": "Water Scarcity / Borewell Failure",
        "Details": "Groundwater table dropped below 680ft; urgent geophysics survey needed for community borewell."
    },
    {
        "Date": "2026-11-07 11:30",
        "Farmer": "Selvam P.",
        "Location": "Bhavani River Basin",
        "Emergency": "Crop Disease Outbreak",
        "Details": "Severe Rhizome Rot (Pythium) noticed across 2.5 acres of turmeric crop following unexpected rainfall."
    },
    {
        "Date": "2026-11-07 12:45",
        "Farmer": "Arumugam S.",
        "Location": "Gobichettipalayam",
        "Emergency": "Mandi Fraud / Price Rigging",
        "Details": "Regulated market commission agent deducting 8% illegal handling fee on CO-86032 sugarcane cane weight."
    },
    {
        "Date": "2026-11-07 14:10",
        "Farmer": "Kavitha M.",
        "Location": "Sathyamangalam",
        "Emergency": "Crop Disease Outbreak",
        "Details": "Whitefly attack spreading rapidly on hybrid cotton (MCU-5); leaves showing upward curling."
    },
    {
        "Date": "2026-11-07 15:20",
        "Farmer": "Dhandapani R.",
        "Location": "Kodumudi",
        "Emergency": "Water Scarcity / Borewell Failure",
        "Details": "Lower Bhavani Project (LBP) branch canal sluice jammed with silt; 40 acres paddy fields dried out."
    }
]

DEFAULT_DEMO_CROPS = [
    {
        "id": 1,
        "farmer_name": "Murugan K.",
        "phone_whatsapp": "+919876543210",
        "crop_name": "Erode Organic Turmeric (Finger)",
        "quantity_kg": 500.0,
        "price_per_kg": 145.0,
        "location": "Perundurai, Erode",
        "created_at": "2026-11-07 09:30"
    },
    {
        "id": 2,
        "farmer_name": "Selvam P.",
        "phone_whatsapp": "+919443218765",
        "crop_name": "Sugarcane (CO-86032)",
        "quantity_kg": 1200.0,
        "price_per_kg": 32.0,
        "location": "Bhavani River Basin",
        "created_at": "2026-11-07 10:00"
    },
    {
        "id": 3,
        "farmer_name": "Vignesh R.",
        "phone_whatsapp": "+919842155678",
        "crop_name": "Pearl Millet (Kambu / Bajra)",
        "quantity_kg": 350.0,
        "price_per_kg": 42.0,
        "location": "Sathyamangalam Foothills",
        "created_at": "2026-11-07 11:20"
    },
    {
        "id": 4,
        "farmer_name": "Kavitha M.",
        "phone_whatsapp": "+919789123456",
        "crop_name": "Hybrid Long Staple Cotton (MCU-5)",
        "quantity_kg": 800.0,
        "price_per_kg": 78.0,
        "location": "Gobichettipalayam",
        "created_at": "2026-11-07 12:40"
    },
    {
        "id": 5,
        "farmer_name": "Arumugam S.",
        "phone_whatsapp": "+919442098765",
        "crop_name": "Country Red Shallots (Small Onion)",
        "quantity_kg": 600.0,
        "price_per_kg": 58.0,
        "location": "Chennimalai Belt",
        "created_at": "2026-11-07 13:15"
    },
    {
        "id": 6,
        "farmer_name": "Dhandapani R.",
        "phone_whatsapp": "+919943567890",
        "crop_name": "Robusta Banana (Pachainadan)",
        "quantity_kg": 1500.0,
        "price_per_kg": 24.0,
        "location": "Kodumudi Riverbed",
        "created_at": "2026-11-07 14:00"
    }
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

# Load environment variables
load_dotenv(".env.local", override=True)
load_dotenv(".env", override=True)

# Master Supabase Production Constants (Guaranteed fallback for Streamlit Cloud & local runs)
_MASTER_SUPABASE_URL = "https://rhomwvtmmkwepclzaiuu.supabase.co"
_MASTER_SUPABASE_KEY = "sb_publishable_OJUn4OSw4PYcDmlIjCntNQ_qGeFBWFO"

def _get_config(key: str, default: str = "") -> str:
    """Safely retrieves config from env vars or st.secrets without throwing StreamlitSecretNotFoundError."""
    val = os.getenv(key, "")
    if val:
        return val.strip(' "\'')
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip(' "\'')
    except Exception:
        pass
    return default

SUPABASE_URL = (
    _get_config("SUPABASE_URL") or
    _get_config("NEXT_PUBLIC_SUPABASE_URL") or
    _MASTER_SUPABASE_URL
)

# Support new format keys: sb_publishable_ and sb_secret_
SUPABASE_KEY = (
    _get_config("SUPABASE_KEY") or
    _get_config("SUPABASE_ANON_KEY") or
    _get_config("SUPABASE_PUBLISHABLE_KEY") or
    _get_config("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY") or
    _get_config("SUPABASE_SERVICE_ROLE_KEY") or
    _get_config("SUPABASE_SECRET_KEY") or
    _MASTER_SUPABASE_KEY
)

# Initialize SQLite local database for offline / fallback mode
LOCAL_DB_PATH = os.path.join(_ROOT_DIR, "agripirate.db")

def init_local_db():
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            name TEXT,
            village TEXT,
            created_at TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS sos_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            village TEXT,
            category TEXT,
            description TEXT,
            timestamp TEXT
        )''')
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

        # Seed local SOS tickets if empty
        c.execute("SELECT COUNT(*) FROM sos_tickets")
        if c.fetchone()[0] == 0:
            ticket_seeds = [
                (t["Farmer"], t["Location"], t["Emergency"], t["Details"], t["Date"])
                for t in DEFAULT_DEMO_TICKETS
            ]
            c.executemany("INSERT INTO sos_tickets (name, village, category, description, timestamp) VALUES (?, ?, ?, ?, ?)", ticket_seeds)

        # Seed initial demo crops if table is empty
        c.execute("SELECT COUNT(*) FROM marketplace_crops")
        if c.fetchone()[0] == 0:
            crop_seeds = [
                (c["farmer_name"], c["phone_whatsapp"], c["crop_name"], c["quantity_kg"], c["price_per_kg"], c["location"], c["created_at"])
                for c in DEFAULT_DEMO_CROPS
            ]
            c.executemany("""INSERT INTO marketplace_crops 
                             (farmer_name, phone_whatsapp, crop_name, quantity_kg, price_per_kg, location, created_at) 
                             VALUES (?, ?, ?, ?, ?, ?, ?)""", crop_seeds)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"init_local_db warning: {e}")

init_local_db()

@st.cache_resource
def get_supabase_client():
    """Initializes and caches the Supabase client if valid credentials are present."""
    if not SUPABASE_URL or not SUPABASE_KEY or "your-project" in SUPABASE_URL:
        return None
    try:
        from supabase import create_client, ClientOptions
        options = ClientOptions(postgrest_client_timeout=4)
        return create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
    except Exception as e:
        print(f"Supabase client initialization exception: {e}")
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
            # Non-blocking fallback to local DB on network/auth error
            print(f"Supabase Sign-Up notice: {e}")

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
        return True, "Account registered successfully (Local Fallback Database)!"
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
            print(f"Supabase login notice: {e}")

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
            # If not in local db, provide demo user bypass for presentation
            if email in ["murugan.erode@agripirate.org", "demo@agripirate.org"]:
                return quick_demo_login(), "Demo Farmer login verified!"
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

def insert_sos_ticket(farmer_name: str, village: str, category: str, description: str, phone: str = "+91 98427 11204", district: str = "Erode", severity: str = "HIGH"):
    """Inserts an emergency SOS ticket to Supabase (using live schema columns) and local SQLite in IST."""
    now = get_ist_now()

    # 1. Always save to local SQLite first for zero-latency guarantee
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO sos_tickets (name, village, category, description, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (farmer_name, village, category, description, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Local ticket save error: {e}")

    # 2. Also save to Supabase if connected
    client = get_supabase_client()
    if client:
        try:
            # Primary: Live Master Supabase schema (farmer_name, phone, village, district, issue_type, severity, description, status)
            client.table("sos_tickets").insert({
                "farmer_name": farmer_name,
                "phone": phone if phone else "+91 98427 11204",
                "village": village,
                "district": district if district else "Erode",
                "issue_type": category,
                "severity": severity if severity else "HIGH",
                "description": description,
                "status": "OPEN - TNAU DISPATCHED"
            }).execute()
        except Exception as e:
            # Secondary fallback attempt with legacy column names
            try:
                client.table("sos_tickets").insert({
                    "name": farmer_name,
                    "village": village,
                    "category": category,
                    "description": description,
                    "timestamp": now
                }).execute()
            except Exception as e2:
                print(f"Supabase ticket insert notice: {e} / {e2}")

def get_sos_tickets():
    """Fetches tickets from Supabase if table exists, or falls back to local SQLite/in-memory data."""
    import pandas as pd

    client = get_supabase_client()
    if client:
        try:
            res = client.table("sos_tickets").select("*").order("created_at" if "created_at" in (client.table("sos_tickets").schema if hasattr(client.table("sos_tickets"), "schema") else "") else "id", desc=True).execute()
            if res.data and len(res.data) > 0:
                normalized = []
                for row in res.data:
                    ts = row.get("created_at") or row.get("timestamp") or ""
                    farmer = row.get("farmer_name") or row.get("name") or "Farmer"
                    vil = row.get("village", "")
                    dist = row.get("district", "")
                    loc = f"{vil}, {dist}".strip(', ') if dist and dist != vil else vil or "Erode, Tamil Nadu"
                    issue = row.get("issue_type") or row.get("category") or "General Emergency"
                    details = row.get("description") or ""
                    normalized.append({
                        "Date": format_to_ist(ts) if ts else get_ist_now(),
                        "Farmer": farmer,
                        "Location": loc,
                        "Emergency": issue,
                        "Details": details
                    })
                df = pd.DataFrame(normalized)
                return df
        except Exception as e:
            print(f"Supabase get_sos_tickets fallback: {e}")

    # Fallback to SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        df = pd.read_sql_query("SELECT timestamp as Date, name as Farmer, village as Location, category as Emergency, description as Details FROM sos_tickets ORDER BY id DESC", conn)
        conn.close()
        if not df.empty:
            if "Date" in df.columns:
                df["Date"] = df["Date"].apply(format_to_ist)
            return df
    except Exception as e:
        print(f"Local SQLite fallback notice: {e}")

    # In-memory guaranteed demo tickets
    return pd.DataFrame(DEFAULT_DEMO_TICKETS)

# ================= MARKETPLACE FUNCTIONS =================

def fetch_marketplace_crops():
    """Fetches marketplace crop listings from Supabase or SQLite fallback, never empty."""
    client = get_supabase_client()
    if client:
        try:
            res = client.table("marketplace_crops").select("*").order("id", desc=True).execute()
            if res.data and len(res.data) > 0:
                for item in res.data:
                    if "created_at" in item:
                        item["created_at"] = format_to_ist(item.get("created_at"))
                    # Normalize phone keys so both phone and phone_whatsapp work everywhere
                    ph = item.get("phone") or item.get("phone_whatsapp") or "+919876543210"
                    item["phone"] = ph
                    item["phone_whatsapp"] = ph
                return res.data
        except Exception as e:
            print(f"Supabase fetch_marketplace_crops fallback: {e}")

    # Fallback to local SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, farmer_name, phone_whatsapp, crop_name, quantity_kg, price_per_kg, location, created_at FROM marketplace_crops ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        if rows and len(rows) > 0:
            return [
                {
                    "id": r[0],
                    "farmer_name": r[1],
                    "phone": r[2],
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
        print(f"Local SQLite fetch_marketplace_crops notice: {e}")

    # In-memory guaranteed fallback
    return list(DEFAULT_DEMO_CROPS)

def add_marketplace_crop(farmer: str, phone: str, crop: str, qty: float, price: float, loc: str, variety: str = "Standard High-Yield"):
    """Adds a new crop listing to Supabase (using live columns) and SQLite fallback in IST."""
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
        print(f"Local SQLite add_marketplace_crop notice: {e}")

    # 2. Sync to Supabase with live Master Supabase columns
    client = get_supabase_client()
    if client:
        try:
            # Primary: Live table schema (farmer_name, phone, location, crop_name, variety, quantity_kg, price_per_kg, mandi_price_per_kg, organic_certified, available)
            client.table("marketplace_crops").insert({
                "farmer_name": farmer,
                "phone": phone,
                "location": loc,
                "crop_name": crop,
                "variety": variety or "Standard Commercial",
                "quantity_kg": float(qty),
                "price_per_kg": float(price),
                "mandi_price_per_kg": round(float(price) * 0.92, 1),
                "organic_certified": True,
                "available": True
            }).execute()
        except Exception as e:
            # Secondary fallback with legacy columns
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
            except Exception as e2:
                print(f"Supabase add_marketplace_crop notice: {e} / {e2}")

    return True
