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
from auth_ui import render_auth_sidebar
from locales import t

# 1. LOAD ENVIRONMENT VARIABLES WITH CACHE OVERRIDE
load_dotenv(override=True)
raw_key = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEY = raw_key.strip(' "\'')

# 2. STREAMLIT PAGE CONFIGURATION
st.set_page_config(page_title="Agri Chat | STARK-X", page_icon="💬", layout="centered")

# RENDER SIDEBAR AUTH & PERSISTENT LANGUAGE SELECTOR
with st.sidebar:
    render_auth_sidebar()

# 3. HIGH-CONTRAST MODERN FARM FRESH UI WITH BOLD TYPOGRAPHY
st.markdown("""
<style>
    /* Force Light Color Scheme across all browsers & OS dark-mode overrides */
    :root {
        color-scheme: light !important;
        --text-color: #0f172a !important;
        --background-color: #f8fafc !important;
        --secondary-background-color: #ffffff !important;
    }

    /* Base Page Styling: Professional, clean, light-slate agricultural canvas */
    .stApp {
        background-color: #f8fafc !important;
        background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px) !important;
        background-size: 24px 24px !important;
        color: #0f172a !important;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
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
        box-shadow: 0 4px 16px rgba(6, 78, 59, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
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
        background: #ffffff !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 26px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important;
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
        background: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05) !important;
    }
    .lang-showcase-title {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #1e293b !important;
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
        background: #eff6ff !important;
        border: 2px solid #3b82f6 !important;
    }
    .lang-pill-ta {
        background: #f0fdf4 !important;
        border: 2px solid #22c55e !important;
    }
    .lang-pill-te {
        background: #fff7ed !important;
        border: 2px solid #f97316 !important;
    }
    .lang-txt-en {
        font-size: 16px !important;
        font-weight: 900 !important;
        color: #1d4ed8 !important;
        display: block !important;
    }
    .lang-txt-ta {
        font-size: 18px !important;
        font-weight: 900 !important;
        color: #15803d !important;
        display: block !important;
    }
    .lang-txt-te {
        font-size: 18px !important;
        font-weight: 900 !important;
        color: #c2410c !important;
        display: block !important;
    }

    /* Streamlit Radio Buttons: BOLD, CRISP, HIGH-CONTRAST LABELS */
    div[data-testid="stRadio"] {
        margin-top: -4px !important;
        margin-bottom: 14px !important;
    }
    div[data-testid="stRadio"] > div {
        gap: 12px !important;
        justify-content: flex-start !important;
        flex-wrap: wrap !important;
    }
    div[data-testid="stRadio"] label {
        background: #ffffff !important;
        border: 2.5px solid #94a3b8 !important;
        border-radius: 12px !important;
        padding: 8px 18px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: #059669 !important;
        background: #f0fdf4 !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked) {
        background: #dcfce7 !important;
        border-color: #059669 !important;
        box-shadow: 0 0 0 2px #059669 !important;
    }
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label div {
        font-size: 1.15rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        letter-spacing: 0.3px !important;
    }

    /* ==========================================================
       ULTRA HIGH-CONTRAST CHAT MESSAGE BUBBLES (ASSISTANT & USER)
       ========================================================== */
    
    /* Default Chat Container: 100% Solid Opaque Pure White Card */
    div[data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #059669 !important; /* Prominent Advisor Accent */
        border-radius: 16px !important;
        padding: 18px 22px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.09) !important;
        max-width: 95% !important;
        opacity: 1 !important;
    }

    /* Universal Text Color Lock: Prevents dark-mode washed-out/transparent text */
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"],
    div[data-testid="stChatMessage"] .stMarkdown,
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] div {
        color: #0f172a !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        line-height: 1.75 !important;
    }

    /* Bold and Emphasis Words in Assistant Reply */
    div[data-testid="stChatMessage"] strong,
    div[data-testid="stChatMessage"] b {
        color: #047857 !important;
        font-weight: 800 !important;
    }

    /* Headings inside AI Response */
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] h4,
    div[data-testid="stChatMessage"] h5,
    div[data-testid="stChatMessage"] h6 {
        color: #064e3b !important;
        font-weight: 800 !important;
        margin-top: 14px !important;
        margin-bottom: 8px !important;
    }

    /* Lists inside AI Response */
    div[data-testid="stChatMessage"] ul,
    div[data-testid="stChatMessage"] ol {
        color: #0f172a !important;
        padding-left: 24px !important;
        margin: 8px 0 12px 0 !important;
    }
    div[data-testid="stChatMessage"] li {
        margin-bottom: 6px !important;
        color: #0f172a !important;
    }

    /* Code & Quotes inside AI Response */
    div[data-testid="stChatMessage"] code {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        border: 1px solid #cbd5e1 !important;
        font-size: 0.95em !important;
    }
    div[data-testid="stChatMessage"] blockquote {
        border-left: 4px solid #10b981 !important;
        background-color: #f0fdf4 !important;
        color: #064e3b !important;
        padding: 10px 16px !important;
        border-radius: 0 10px 10px 0 !important;
        margin: 10px 0 !important;
        font-weight: 600 !important;
    }

    /* User Message Bubble Overrides */
    div[data-testid="stChatMessage"]:has([data-testid*="User"]),
    div[data-testid="stChatMessage"]:has([data-testid*="user"]),
    div[data-testid="stChatMessage"]:has([aria-label*="user" i]) {
        background-color: #dcfce7 !important;
        border: 2px solid #86efac !important;
        border-right: 6px solid #16a34a !important;
        border-left: 2px solid #86efac !important;
        margin-left: auto !important;
        margin-right: 4px !important;
        border-top-right-radius: 4px !important;
        box-shadow: 0 3px 12px rgba(22, 163, 74, 0.12) !important;
    }

    div[data-testid="stChatMessage"]:has([data-testid*="User"]) [data-testid="stChatMessageContent"],
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) .stMarkdown,
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) p,
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) span,
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) li,
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) [data-testid="stChatMessageContent"],
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) .stMarkdown,
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) p,
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) span,
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) li {
        color: #064e3b !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }

    div[data-testid="stChatMessage"]:has([data-testid*="User"]) strong,
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) strong {
        color: #022c22 !important;
        font-weight: 900 !important;
    }

    /* Avatars */
    div[data-testid*="ChatMessageAvatar"],
    div[data-testid*="chatAvatarIcon"] {
        background-color: #f1f5f9 !important;
        border-radius: 50% !important;
        border: 2px solid #94a3b8 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12) !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) div[data-testid*="ChatMessageAvatar"],
    div[data-testid="stChatMessage"]:has([data-testid*="user"]) div[data-testid*="ChatMessageAvatar"] {
        background-color: #bbf7d0 !important;
        border-color: #22c55e !important;
    }

    /* Chat Spinner (Thinking state) */
    div[data-testid="stSpinner"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #f59e0b !important;
        border-radius: 14px !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stSpinner"] * {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
    }

    /* Chat Input Bar */
    div[data-testid="stChatInput"] {
        border-radius: 16px !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border: 2px solid #64748b !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.25) !important;
        color: #0f172a !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: #059669 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #ffffff !important;
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

# 7. ZERO-LAG NATIVE LLM HANDLER (Multi-Model Cascade)
def get_starkx_response(user_prompt, active_lang):
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API Key is missing. Check your .env file."
    
    try:
        genai.configure(api_key=GEMINI_API_KEY, transport="rest")
        
        # Build conversation context
        recent_context = ""
        for item in st.session_state.chat_history[-4:]:
            role_label = "Farmer" if item["role"] == "user" else "Advisor"
            recent_context += f"{role_label}: {item['content']}\n"
            
        full_input = f"{recent_context}\nFarmer asks: {user_prompt}"
        
        # Generate complete response natively in farmer's selected language
        sys_inst = build_native_system_instruction(active_lang)
        gen_config = genai.types.GenerationConfig(
            max_output_tokens=600,
            temperature=0.3
        )
        
        candidate_models = ['gemini-flash-lite-latest', 'gemini-3.5-flash', 'gemini-3.1-flash-lite', 'gemini-1.5-flash']
        response_text = ""
        for m_name in candidate_models:
            try:
                model = genai.GenerativeModel(
                    m_name,
                    system_instruction=sys_inst,
                    generation_config=gen_config
                )
                res = model.generate_content(full_input, stream=False)
                if res and res.text:
                    response_text = res.text
                    break
            except Exception:
                continue
            
        if not response_text:
            return "⚠️ Currently unable to reach AI agronomy service. Please retry in a few seconds."
            
        return response_text
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"

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