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

def inject_high_contrast_css():
    """
    Injects global, high-visibility, dark glassmorphic styling across all Streamlit pages.
    Guarantees crisp, readable fonts:
    - Background: Deep Obsidian Slate (#070E18 / #0F172A)
    - Headings: Vibrant Electric Green (#10B981), Cyan (#06B6D4), Gold (#F59E0B)
    - Body text, spans, labels: Crisp bright white/silver (#FFFFFF / #F8FAFC)
    - Inputs / selects: Dark glassmorphic (#0F172A) with bright white text & #94A3B8 placeholders
    - Buttons: Vivid emerald gradient with bold white text
    - Zero unreadable or invisible text across light/dark browser modes.
    """
    st.markdown("""
    <style>
        :root {
            color-scheme: dark !important;
            --text-color: #F8FAFC !important;
            --background-color: #070E18 !important;
            --secondary-background-color: #0F172A !important;
        }

        /* 1. App Background */
        .stApp {
            background-color: #070E18 !important;
            background-image: radial-gradient(#1e293b 1px, transparent 1px) !important;
            background-size: 24px 24px !important;
            color: #F8FAFC !important;
        }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

        /* 2. Global Text & Paragraphs */
        p, span, li, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stText {
            color: #F8FAFC !important;
            font-weight: 500 !important;
        }

        /* 3. Streamlit Widget Labels */
        .stWidgetLabel, .stWidgetLabel label, .stWidgetLabel p, [data-testid="stWidgetLabel"] * {
            color: #E2E8F0 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }

        /* 4. Headings */
        h1, [data-testid="stHeadingWithActionElements"] h1 {
            color: #10B981 !important; /* Electric Green */
            font-weight: 800 !important;
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.25) !important;
        }
        h2, [data-testid="stHeadingWithActionElements"] h2 {
            color: #06B6D4 !important; /* Cyan */
            font-weight: 800 !important;
        }
        h3, [data-testid="stHeadingWithActionElements"] h3 {
            color: #F59E0B !important; /* Gold */
            font-weight: 700 !important;
        }
        h4, h5, h6 {
            color: #38BDF8 !important;
            font-weight: 700 !important;
        }

        /* 5. Inputs, Textareas, Selectboxes */
        input, textarea, [data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] {
            background-color: #0F172A !important;
            color: #FFFFFF !important;
            border: 1.5px solid #334155 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        input::placeholder, textarea::placeholder {
            color: #94A3B8 !important;
        }
        input:focus, textarea:focus, [data-baseweb="input"]:focus-within {
            border-color: #10B981 !important;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3) !important;
        }

        /* 6. Dropdown Options */
        [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
            background-color: #0F172A !important;
            border: 1.5px solid #334155 !important;
        }
        [role="option"], [data-baseweb="menu"] li {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
        }
        [role="option"]:hover, [data-baseweb="menu"] li:hover, [aria-selected="true"] {
            background-color: #1E293B !important;
            color: #10B981 !important;
        }

        /* 7. Metric Cards */
        [data-testid="stMetric"] {
            background-color: #0F172A !important;
            border: 1.5px solid #1E293B !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
        }
        [data-testid="stMetricValue"] {
            color: #10B981 !important;
            font-weight: 800 !important;
            font-size: 1.8rem !important;
        }
        [data-testid="stMetricLabel"] * {
            color: #94A3B8 !important;
            font-weight: 600 !important;
        }

        /* 8. Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            border: 1px solid #34D399 !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
        }
        .stButton > button * {
            color: #FFFFFF !important;
        }

        /* 9. Page Links (Navigation Pills) */
        div[data-testid="stPageLink-NavLink"] {
            background-color: #0F172A !important;
            border: 1.5px solid #334155 !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            margin-bottom: 6px !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stPageLink-NavLink"]:hover {
            border-color: #10B981 !important;
            background: #1E293B !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.25) !important;
        }
        div[data-testid="stPageLink-NavLink"] * {
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }

        /* 10. Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0A1120 !important;
            border-right: 1.5px solid #1E293B !important;
        }
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #0F172A !important;
            color: #FFFFFF !important;
            border: 1.5px solid #334155 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        /* 11. Alerts / Notification Cards */
        div[data-testid="stAlert"] {
            background-color: #0F172A !important;
            border: 1.5px solid #334155 !important;
            border-left: 6px solid #10B981 !important;
            border-radius: 14px !important;
            padding: 14px 18px !important;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3) !important;
        }
        div[data-testid="stAlert"] * {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }

        /* 12. Expanders */
        [data-testid="stExpander"] {
            background: #0F172A !important;
            border: 1.5px solid #1E293B !important;
            border-radius: 12px !important;
        }

        /* 13. Dataframe & Tables */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            background-color: #0F172A !important;
            border: 1.5px solid #334155 !important;
            border-radius: 10px !important;
        }

        /* 14. Chat Messages */
        [data-testid="stChatMessage"] {
            background-color: #0F172A !important;
            border: 1px solid #1E293B !important;
            border-radius: 14px !important;
            color: #F8FAFC !important;
            margin-bottom: 10px !important;
        }
        [data-testid="stChatMessage"] * {
            color: #F8FAFC !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_top_navbar(current_page="home"):
    """
    Renders a prominent, high-contrast horizontal navigation bar at the top of every page.
    Allows instantaneous navigation between Home Dashboard and all 5 core modules.
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0A1120 0%, #131F37 100%); border: 1.5px solid #334155; border-radius: 14px; padding: 10px 16px; margin-bottom: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 20px;">🌱</span>
                <span style="font-size: 14px; font-weight: 800; color: #10B981; letter-spacing: 0.5px;">STARK-X QUICK NAVIGATOR</span>
            </div>
            <div style="font-size: 11px; font-weight: 700; color: #38BDF8; background: rgba(56, 189, 248, 0.12); padding: 3px 10px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3);">
                Kongu Precision AgOS
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 High-Visibility Pill Buttons
    cols = st.columns(6)
    with cols[0]:
        st.page_link("app.py", label="🏠 Home", use_container_width=True)
    with cols[1]:
        st.page_link("pages/1_💬_Agri_Chat.py", label="💬 Agri Chat", use_container_width=True)
    with cols[2]:
        st.page_link("pages/2_📸_Crop_Vision.py", label="📸 Vision", use_container_width=True)
    with cols[3]:
        st.page_link("pages/3_🌾_Optimizer.py", label="🌾 Optimizer", use_container_width=True)
    with cols[4]:
        st.page_link("pages/4_📈_Market_SOS.py", label="📈 Market & SOS", use_container_width=True)
    with cols[5]:
        st.page_link("pages/5_🛒_Agri_Market.py", label="🛒 Market", use_container_width=True)
        
    # If on a subpage, also show prominent Back to Home banner button at top
    if current_page != "home":
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        bcol1, bcol2 = st.columns([1, 2])
        with bcol1:
            st.page_link("app.py", label="⬅️ Back to Home Dashboard", icon="🏠", use_container_width=True)

def render_bottom_back_button():
    """Renders prominent back-to-home navigation at bottom of page."""
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.page_link("app.py", label="⬅️ Back to Home Dashboard", icon="🏠", use_container_width=True)
    with col2:
        st.page_link("pages/1_💬_Agri_Chat.py", label="💬 Open Agri Chat Advisor", icon="🌱", use_container_width=True)

def render_auth_sidebar():
    """Renders persistent language selector, user authentication and profile status in the sidebar."""
    st.sidebar.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #0A1120 !important;
            border-right: 1.5px solid #1E293B !important;
        }
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #0F172A !important;
            color: #FFFFFF !important;
            border: 1.5px solid #334155 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
            border: 1px solid #34d399 !important;
            box-shadow: 0 3px 8px rgba(16, 185, 129, 0.25) !important;
        }
        section[data-testid="stSidebar"] button * {
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] [data-testid="stExpander"] {
            background: #0F172A !important;
            border: 1px solid #1E293B !important;
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
    
    # Styled Language Badges with Vivid High-Contrast Colors
    st.sidebar.markdown("""
    <div style="background: #0F172A; border: 1.5px solid #334155; border-radius: 12px; padding: 12px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
        <div style="font-size: 13px; font-weight: 800; margin-bottom: 8px; color: #10B981;">
            🌐 Regional Languages
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <span style="color: #60a5fa; font-weight: 800; font-size: 11px; background: #1e3a5f; padding: 4px 8px; border-radius: 6px; border: 1px solid #3b82f6;">
                🇬🇧 English
            </span>
            <span style="color: #4ade80; font-weight: 800; font-size: 11px; background: #064e3b; padding: 4px 8px; border-radius: 6px; border: 1px solid #10b981;">
                🌾 தமிழ்
            </span>
            <span style="color: #fbbf24; font-weight: 800; font-size: 11px; background: #78350f; padding: 4px 8px; border-radius: 6px; border: 1px solid #f59e0b;">
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
        provider_badge = "🟢 Supabase Cloud Active" if user.get("provider") == "supabase" else "🟡 Local Session Active"
        st.sidebar.markdown(f"""
        <div style="background-color: #064e3b; border: 1.5px solid #10b981; padding: 12px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 26px;">🧑‍🌾</span>
                <div>
                    <strong style="color: #ffffff; font-size: 15px; font-weight: 800;">{user.get('name', 'Farmer')}</strong><br/>
                    <small style="color: #86efac; font-weight: 600;">📍 {user.get('village', 'Tamil Nadu')}</small>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 11.5px; color: #4ade80; font-weight: 700;">
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
