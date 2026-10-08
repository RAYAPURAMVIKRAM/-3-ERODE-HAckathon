import os
import sqlite3
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

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
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
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
    """Inserts an emergency SOS ticket to Supabase and local SQLite."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
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
    """Fetches tickets from Supabase if table exists, or falls back to local SQLite."""
    client = get_supabase_client()
    if client:
        try:
            res = client.table("sos_tickets").select("*").order("id", desc=True).execute()
            if res.data and len(res.data) > 0:
                import pandas as pd
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
    return df
