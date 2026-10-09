import os
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
    /* App Background: Fresh, clean, high-contrast mint/slate palette */
    .stApp {
        background-color: #f0fdf4;
        background-image: radial-gradient(#d1fae5 1.2px, transparent 1.2px);
        background-size: 24px 24px;
        color: #0f172a;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Premium Header Banner */
    .chat-hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 14px rgba(6, 78, 59, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .chat-hero-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .chat-avatar-badge {
        width: 48px;
        height: 48px;
        background: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
        border: 2px solid #34d399;
    }
    .chat-hero-title {
        font-size: 1.28rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        letter-spacing: 0.3px;
    }
    .chat-hero-status {
        font-size: 0.85rem;
        color: #d1fae5;
        font-weight: 600;
        margin: 2px 0 0 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background-color: #34d399;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #34d399;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.2); }
    }

    /* BOLD, ULTRA-VISIBLE MULTILINGUAL BAR */
    .lang-showcase-card {
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
    }
    .lang-showcase-title {
        font-size: 13px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .lang-pills-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .lang-pill-item {
        flex: 1;
        min-width: 120px;
        padding: 8px 12px;
        border-radius: 10px;
        text-align: center;
        transition: all 0.2s ease;
    }
    .lang-pill-en {
        background: #eff6ff;
        border: 2px solid #3b82f6;
    }
    .lang-pill-ta {
        background: #f0fdf4;
        border: 2px solid #22c55e;
    }
    .lang-pill-te {
        background: #fff7ed;
        border: 2px solid #f97316;
    }
    .lang-txt-en {
        font-size: 16px;
        font-weight: 900;
        color: #1d4ed8;
        display: block;
    }
    .lang-txt-ta {
        font-size: 18px;
        font-weight: 900;
        color: #15803d;
        display: block;
    }
    .lang-txt-te {
        font-size: 18px;
        font-weight: 900;
        color: #c2410c;
        display: block;
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
    div[data-testid="stRadio"] label p {
        font-size: 1.15rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        letter-spacing: 0.3px !important;
    }

    /* High-Contrast Chat Bubbles */
    div[data-testid="stChatMessage"] {
        padding: 14px 18px !important;
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06) !important;
        max-width: 90% !important;
    }
    /* User Message Bubble */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #dcfce7 !important;
        border: 2px solid #86efac !important;
        margin-left: auto !important;
        margin-right: 4px !important;
        border-top-right-radius: 4px !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p {
        color: #064e3b !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
        line-height: 1.55 !important;
    }
    /* Assistant Message Bubble */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        margin-left: 4px !important;
        margin-right: auto !important;
        border-top-left-radius: 4px !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) li {
        color: #0f172a !important;
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        line-height: 1.65 !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) strong {
        color: #064e3b !important;
        font-weight: 800 !important;
    }

    /* Chat Input Bar */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border: 2px solid #94a3b8 !important;
        border-radius: 14px !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.2) !important;
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