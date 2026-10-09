import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path
_ROOT_DIR = str(Path(__file__).resolve().parent)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

import streamlit as st
from locales import t, TRANSLATIONS
from supabase_client import (
    sign_in_farmer,
    sign_up_farmer,
    quick_demo_login,
    sign_out_farmer,
    get_current_user,
    is_supabase_connected
)

def render_auth_sidebar():
    """Renders persistent language selector, user authentication and profile status in the sidebar."""
    st.sidebar.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1.5px solid #cbd5e1 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #0f172a !important;
        }
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1.5px solid #94a3b8 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] button {
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: 0 3px 8px rgba(5, 150, 105, 0.25) !important;
        }
        section[data-testid="stSidebar"] button * {
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] [data-testid="stExpander"] {
            background: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 0. SYNCHRONIZED APP LANGUAGE SELECTOR VIA st.session_state["lang"]
    if "lang" not in st.session_state:
        st.session_state["lang"] = st.session_state.get("selected_lang", "English")
    st.session_state["selected_lang"] = st.session_state["lang"]
        
    langs = ["English", "Tamil (தமிழ்)", "Telugu (తెలుగు)"]
    curr_lang = st.session_state.get("lang", "English")
    curr_idx = langs.index(curr_lang) if curr_lang in langs else 0
    
    # Styled Language Badges with Vivid Text Colors
    st.sidebar.markdown("""
    <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px 12px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
        <div style="font-size: 13px; font-weight: 700; margin-bottom: 8px; color: #1e293b;">
            🌐 Language / மொழி / భాష
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <span style="color: #2563eb; font-weight: 800; font-size: 12px; background: #eff6ff; padding: 3px 8px; border-radius: 6px; border: 1px solid #bfdbfe;">
                🇬🇧 English
            </span>
            <span style="color: #16a34a; font-weight: 800; font-size: 12px; background: #f0fdf4; padding: 3px 8px; border-radius: 6px; border: 1px solid #bbf7d0;">
                🌾 தமிழ்
            </span>
            <span style="color: #ea580c; font-weight: 800; font-size: 12px; background: #fff7ed; padding: 3px 8px; border-radius: 6px; border: 1px solid #fed7aa;">
                ☀️ తెలుగు
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    chosen = st.sidebar.selectbox(
        "Choose App Language",
        langs,
        index=curr_idx,
        key="global_sidebar_lang_selector",
        label_visibility="collapsed"
    )
    if chosen != st.session_state["lang"]:
        st.session_state["lang"] = chosen
        st.session_state["selected_lang"] = chosen
        st.rerun()

    user = get_current_user()
    st.sidebar.markdown("---")
    
    # 1. LOGGED IN STATE
    if user:
        provider_badge = "🟢 Supabase Cloud" if user.get("provider") == "supabase" else "🟡 Local Session"
        st.sidebar.markdown(f"""
        <div style="background-color: #f0fdf4; border: 1px solid #86efac; padding: 12px; border-radius: 12px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🧑‍🌾</span>
                <div>
                    <strong style="color: #166534; font-size: 15px;">{user.get('name', 'Farmer')}</strong><br/>
                    <small style="color: #4b5563;">📍 {user.get('village', 'Tamil Nadu')}</small>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 11px; color: #15803d; font-weight: 600;">
                {provider_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", key="btn_logout", use_container_width=True):
            sign_out_farmer()
            st.rerun()
            
    # 2. LOGGED OUT STATE
    else:
        status_text = "🟢 Supabase Active" if is_supabase_connected() else "🟡 Local / Demo Mode"
        st.sidebar.markdown(f"**Farmer Portal** <small style='color: #6b7280;'>({status_text})</small>", unsafe_allow_html=True)
        
        # 1-Click Demo Login for Quick Testing / Hackathon
        if st.sidebar.button("⚡ 1-Click Demo Login", key="btn_quick_demo", use_container_width=True):
            quick_demo_login()
            st.sidebar.success("Logged in as Murugan (Erode)!")
            st.rerun()
            
        with st.sidebar.expander("🔑 Sign In / Register", expanded=False):
            auth_tab1, auth_tab2 = st.tabs(["Sign In", "Sign Up"])
            
            with auth_tab1:
                with st.form("sidebar_signin_form"):
                    in_email = st.text_input("Email", key="in_email")
                    in_pass = st.text_input("Password", type="password", key="in_pass")
                    btn_signin = st.form_submit_button("Sign In")
                    if btn_signin:
                        if in_email and in_pass:
                            success, msg = sign_in_farmer(in_email, in_pass)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("Please enter email & password.")
                            
            with auth_tab2:
                with st.form("sidebar_signup_form"):
                    up_name = st.text_input("Farmer Name", key="up_name")
                    up_village = st.text_input("Village / District", key="up_village")
                    up_email = st.text_input("Email", key="up_email")
                    up_pass = st.text_input("Password", type="password", key="up_pass")
                    btn_signup = st.form_submit_button("Register Account")
                    if btn_signup:
                        if up_name and up_village and up_email and up_pass:
                            success, msg = sign_up_farmer(up_email, up_pass, up_name, up_village)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("Please fill in all registration fields.")
