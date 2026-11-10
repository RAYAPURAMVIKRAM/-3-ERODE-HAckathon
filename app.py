import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path
_ROOT_DIR = str(Path(__file__).resolve().parent)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

import streamlit as st
from locales import t
from auth_ui import render_auth_sidebar, render_top_navbar, inject_high_contrast_css
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

st.markdown(t("select_tool_msg", lang))

st.page_link("pages/1_💬_Agri_Chat.py", label=f"**{t('chat_page', lang)}:** {t('chat_page_desc', lang)}", icon="💬")
st.page_link("pages/2_📸_Crop_Vision.py", label=f"**{t('vision_page', lang)}:** {t('vision_page_desc', lang)}", icon="📸")
st.page_link("pages/3_🌾_Optimizer.py", label=f"**{t('opt_page', lang)}:** {t('opt_page_desc', lang)}", icon="🌾")
st.page_link("pages/4_📈_Market_SOS.py", label=f"**{t('market_sos_page', lang)}:** {t('market_sos_desc', lang)}", icon="📈")
st.page_link("pages/5_🛒_Agri_Market.py", label=f"**{t('market_page', lang)}:** {t('market_page_desc', lang)}", icon="🛒")
