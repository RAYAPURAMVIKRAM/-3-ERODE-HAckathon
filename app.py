import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path
_ROOT_DIR = str(Path(__file__).resolve().parent)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

import streamlit as st
from locales import t
from auth_ui import render_auth_sidebar, render_top_navbar, inject_high_contrast_css, find_page
from supabase_client import get_current_user

st.set_page_config(page_title="STARK-X | AgriPirate", page_icon="🌱", layout="centered", initial_sidebar_state="expanded")

# 1. INJECT GLOBAL HIGH-CONTRAST DARK GLASSMORPHIC THEME
inject_high_contrast_css()

# 2. RENDER TOP NAVIGATION BAR
render_top_navbar("home")

# 3. RENDER AUTH SIDEBAR & PERSISTENT LANGUAGE SELECTOR
render_auth_sidebar()

lang = st.session_state.get("lang", "English")

st.image("https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
st.title(t("app_title", lang))
st.subheader(t("app_subtitle", lang))

# Display personalized welcome banner if logged in
user = get_current_user()
if user:
    welcome_text = t("welcome_farmer", lang).format(name=user.get('name', 'Farmer'), village=user.get('village', 'Tamil Nadu'))
    st.success(f"🌾 {welcome_text}")

st.markdown(f"#### 🚀 {t('select_tool_msg', lang)}")

modules = [
    ("1_", "💬 " + t('chat_page', lang), t('chat_page_desc', lang), "btn_home_chat"),
    ("2_", "📸 " + t('vision_page', lang), t('vision_page_desc', lang), "btn_home_vision"),
    ("3_", "🌾 " + t('opt_page', lang), t('opt_page_desc', lang), "btn_home_opt"),
    ("4_", "📈 " + t('market_sos_page', lang), t('market_sos_desc', lang), "btn_home_sos"),
    ("5_", "🛒 " + t('market_page', lang), t('market_page_desc', lang), "btn_home_market"),
]

for prefix, title, desc, btn_key in modules:
    col_info, col_btn = st.columns([4, 1])
    with col_info:
        st.markdown(f"**{title}**  \n<span style='color:#94a3b8; font-size:13px;'>{desc}</span>", unsafe_allow_html=True)
    with col_btn:
        page_path = find_page(prefix)
        if st.button("Launch ➔", key=btn_key, use_container_width=True):
            if page_path:
                st.switch_page(page_path)
    st.markdown("<hr style='margin: 8px 0; border: none; border-bottom: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
