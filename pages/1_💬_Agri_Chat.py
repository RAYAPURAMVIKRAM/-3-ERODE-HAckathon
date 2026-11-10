import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path for Streamlit Cloud
_ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from auth_ui import render_auth_sidebar, render_top_navbar, render_bottom_back_button, inject_high_contrast_css
from locales import t

# 1. LOAD ENVIRONMENT VARIABLES WITH CACHE OVERRIDE
load_dotenv(override=True)
raw_key = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEY = raw_key.strip(' "\'')

# 2. STREAMLIT PAGE CONFIGURATION
st.set_page_config(page_title="Agri Chat | STARK-X", page_icon="💬", layout="centered")

# 3. GLOBAL HIGH-CONTRAST THEME & TOP NAVIGATOR
inject_high_contrast_css()
render_top_navbar("1_Agri_Chat")

# RENDER SIDEBAR AUTH & PERSISTENT LANGUAGE SELECTOR
with st.sidebar:
    render_auth_sidebar()

# 4. HIGH-CONTRAST CHAT STYLING
st.markdown("""
<style>
    /* Premium Header Banner */
    .chat-hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%) !important;
        color: #ffffff !important;
        padding: 16px 22px !important;
        border-radius: 16px !important;
        margin-bottom: 14px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        box-shadow: 0 4px 16px rgba(6, 78, 59, 0.4) !important;
        border: 1.5px solid #10b981 !important;
    }
    .chat-hero-banner * {
        color: #ffffff !important;
    }
    .chat-hero-left {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    .chat-avatar-badge {
        width: 48px !important;
        height: 48px !important;
        background: #0f172a !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 26px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3) !important;
        border: 2px solid #34d399 !important;
    }
    .chat-hero-title {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
    }
    .chat-hero-status {
        font-size: 0.88rem !important;
        color: #d1fae5 !important;
        font-weight: 600 !important;
        margin: 2px 0 0 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    .live-dot {
        width: 8px !important;
        height: 8px !important;
        background-color: #34d399 !important;
        border-radius: 50% !important;
        display: inline-block !important;
        box-shadow: 0 0 8px #34d399 !important;
        animation: pulse-dot 2s infinite !important;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.2); }
    }

    /* BOLD, ULTRA-VISIBLE MULTILINGUAL BAR */
    .lang-showcase-card {
        background: #0f172a !important;
        border: 2px solid #334155 !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    .lang-showcase-title {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #10b981 !important;
        margin-bottom: 8px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .lang-pills-row {
        display: flex !important;
        gap: 10px !important;
        flex-wrap: wrap !important;
    }
    .lang-pill-item {
        flex: 1 !important;
        min-width: 120px !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        text-align: center !important;
        transition: all 0.2s ease !important;
    }
    .lang-pill-en {
        background: #1e293b !important;
        border: 1.5px solid #3b82f6 !important;
    }
    .lang-pill-ta {
        background: #064e3b !important;
        border: 1.5px solid #22c55e !important;
    }
    .lang-pill-te {
        background: #78350f !important;
        border: 1.5px solid #f97316 !important;
    }
    .lang-txt-en {
        font-size: 16px !important;
        font-weight: 900 !important;
        color: #93c5fd !important;
        display: block !important;
    }
    .lang-txt-ta {
        font-size: 18px !important;
        font-weight: 900 !important;
        color: #86efac !important;
        display: block !important;
    }
    .lang-txt-te {
        font-size: 18px !important;
        font-weight: 900 !important;
        color: #fdba74 !important;
        display: block !important;
    }

    /* High-contrast Radio Buttons */
    div[data-testid="stRadio"] label {
        background: #0f172a !important;
        border: 1.5px solid #334155 !important;
        border-radius: 12px !important;
        padding: 8px 18px !important;
        color: #f8fafc !important;
    }
    div[data-testid="stRadio"] label * {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    /* HIGH-CONTRAST CHAT BUBBLES */
    div[data-testid="stChatMessage"] {
        background-color: #0f1e13 !important;
        border: 1.5px solid #1e3a24 !important;
        border-left: 6px solid #10b981 !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        color: #f8fafc !important;
    }
    div[data-testid="stChatMessage"] * {
        color: #f8fafc !important;
    }
    div[data-testid="stChatMessage"] strong, div[data-testid="stChatMessage"] b {
        color: #34d399 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stChatMessage"] h1, div[data-testid="stChatMessage"] h2, div[data-testid="stChatMessage"] h3 {
        color: #10b981 !important;
        font-weight: 800 !important;
    }

    /* User Message Bubble Overrides */
    div[data-testid="stChatMessage"]:has([data-testid*="User"]),
    div[data-testid="stChatMessage"]:has([data-testid*="user"]),
    div[data-testid="stChatMessage"]:has([aria-label*="user" i]) {
        background-color: #1e293b !important;
        border: 1.5px solid #334155 !important;
        border-right: 6px solid #38bdf8 !important;
        border-left: 1.5px solid #334155 !important;
        color: #f8fafc !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) * {
        color: #f8fafc !important;
    }

    /* Chat Input Bar */
    div[data-testid="stChatInput"] textarea {
        background-color: #0f172a !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border: 2px solid #334155 !important;
        border-radius: 14px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #10b981 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. MULTILINGUAL SYNC & TEXT COLOR DISPLAY
if "lang" not in st.session_state:
    st.session_state["lang"] = st.session_state.get("selected_lang", "English")

current_lang = st.session_state.get("lang", "English")
lang_options = ["English", "Tamil (தமிழ்)", "Telugu (తెలుగు)"]
lang_idx = lang_options.index(current_lang) if current_lang in lang_options else 0

st.markdown(f"""
<div class="chat-hero-banner">
    <div class="chat-hero-left">
        <div class="chat-avatar-badge">🌱</div>
        <div>
            <h3 class="chat-hero-title">{t("chat_title", current_lang)}</h3>
            <p class="chat-hero-status"><span class="live-dot"></span> {t("chat_status", current_lang)}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# BOLD HIGH-CONTRAST LANGUAGE CARDS DISPLAY
st.markdown("""
<div class="lang-showcase-card">
    <div class="lang-showcase-title">
        🌐 Selected Native Language / தேர்ந்தெடுக்கப்பட்ட மொழி / ఎంచుకున్న భాష
    </div>
    <div class="lang-pills-row">
        <div class="lang-pill-item lang-pill-en">
            <span class="lang-txt-en">🇬🇧 English</span>
            <small style="color: #2563eb; font-weight: 800; font-size: 11px;">Standard Global</small>
        </div>
        <div class="lang-pill-item lang-pill-ta">
            <span class="lang-txt-ta">🌾 தமிழ்</span>
            <small style="color: #16a34a; font-weight: 800; font-size: 12px;">தமிழ்நாடு வேளாண்மை</small>
        </div>
        <div class="lang-pill-item lang-pill-te">
            <span class="lang-txt-te">☀️ తెలుగు</span>
            <small style="color: #ea580c; font-weight: 800; font-size: 12px;">రైతు మిత్రుడు</small>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

lang_option = st.radio(
    t("select_language", current_lang),
    lang_options,
    index=lang_idx,
    horizontal=True,
    key="chat_lang_radio"
)
if lang_option != st.session_state.get("lang"):
    st.session_state["lang"] = lang_option
    st.session_state["selected_lang"] = lang_option
    st.rerun()

# 5. DYNAMIC NATIVE SYSTEM INSTRUCTION GENERATOR
def build_native_system_instruction(lang_name):
    base_rules = (
        "You are STARK-X, an empathetic, highly knowledgeable agronomy and precision agriculture advisor for Indian farmers, especially Tamil Nadu and South Indian regions.\n"
        "Guidelines:\n"
        "1. Always ground advice in Soil Type, Temperature, and Water Availability.\n"
        "2. Provide an estimated Percentage Suitability score when assessing crops (e.g., '🌱 Suitability: 85%').\n"
        "3. Format recommendations with clear bullet points and action-oriented steps.\n"
        "4. Keep practical advice cost-effective, organic-friendly, and actionable for smallholder farmers.\n"
        "Core Crop Knowledge:\n"
        "- Rice/Paddy: Clay/Alluvial, pH 5.5-7.0, high irrigation demand. Warn against water shortage.\n"
        "- Millets/Ragi: Red/Sandy-loam, drought-resilient, minimal water.\n"
        "- Turmeric: Loamy, well-drained, Erode belt specialty, high profit.\n"
        "- Cotton: Black soil, medium moisture, high heat tolerance.\n\n"
    )
    
    if "tamil" in lang_name.lower() or "தமிழ்" in lang_name:
        native_lang_rule = (
            "CRITICAL MANDATORY INSTRUCTION:\n"
            "You MUST generate your entire answer natively in authentic, fluent Tamil (தமிழ்). "
            "Write exclusively in Tamil script with respectful, culturally natural agricultural terms (e.g., உழவர் தோழரே, மண் வகை, பாசன வசதி, உர மேலாண்மை, பூச்சி கட்டுப்பாடு, எதிர்பார்க்கும் மகசூல்). "
            "Do NOT use transliteration. Do NOT mix English sentences. Give complete, deep agronomic advice in Tamil."
        )
    elif "telugu" in lang_name.lower() or "తెలుగు" in lang_name:
        native_lang_rule = (
            "CRITICAL MANDATORY INSTRUCTION:\n"
            "You MUST generate your entire answer natively in authentic, fluent Telugu (తెలుగు). "
            "Write exclusively in Telugu script with respectful, culturally natural agricultural terms (e.g., రైతు మిత్రమా, నేల రకం, సాగునీటి వసతి, ఎరువుల యాజమాన్యం, తెగుళ్ల నివారణ, దిగుబడి). "
            "Do NOT use transliteration. Do NOT mix English sentences. Give complete, deep agronomic advice in Telugu."
        )
    else:
        native_lang_rule = (
            "CRITICAL MANDATORY INSTRUCTION:\n"
            "You MUST generate your answer in clear, empathetic English tailored for Indian agricultural contexts."
        )
        
    return base_rules + native_lang_rule

# 6. INITIALIZE CHAT HISTORY
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": t("chat_welcome", current_lang)}]
elif len(st.session_state.chat_history) == 1 and st.session_state.chat_history[0]["role"] == "assistant":
    # Keep initial welcome greeting synced when language changes
    st.session_state.chat_history[0]["content"] = t("chat_welcome", current_lang)

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"], avatar="user" if msg["role"] == "user" else "assistant").markdown(msg["content"])

# 7. ZERO-LAG NATIVE LLM HANDLER (Gemini Cascade + Intelligent Regional Agronomy Engine)
def get_starkx_response(user_prompt, active_lang):
    try:
        from agronomy_ai import get_agronomy_chat_response
        return get_agronomy_chat_response(user_prompt, active_lang, st.session_state.get("chat_history", []))
    except Exception as e:
        return f"⚠️ Agronomy Engine Notice: {str(e)}"

# 8. CHAT INPUT
user_input = st.chat_input(t("chat_placeholder", current_lang))

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner(t("thinking_msg", current_lang)):
            reply = get_starkx_response(user_input, current_lang)
            st.markdown(reply)
            
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# 9. PROMINENT BOTTOM BACK TO HOME NAVIGATION
render_bottom_back_button()
