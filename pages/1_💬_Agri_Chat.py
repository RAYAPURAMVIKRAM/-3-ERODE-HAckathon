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

# 3. WHATSAPP THEME CUSTOM CSS
st.markdown("""
<style>
    .stApp { background-color: #efeae2; background-image: radial-gradient(#d4cdb4 1px, transparent 1px); background-size: 20px 20px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .wa-header { background: linear-gradient(135deg, #075e54, #128c7e); color: white; padding: 14px 18px; border-radius: 12px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15); }
    .wa-header-left { display: flex; align-items: center; gap: 12px; }
    .wa-avatar { width: 44px; height: 44px; background-color: #25d366; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); }
    .wa-title { font-size: 1.15rem; font-weight: 700; margin: 0; color: #ffffff; }
    .wa-status { font-size: 0.8rem; color: #dcf8c6; margin: 2px 0 0 0; }
    div[data-testid="stChatMessage"] { padding: 10px 14px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12); max-width: 88%; }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background-color: #dcf8c6 !important; border: 1px solid #c7e8ab; margin-left: auto !important; margin-right: 4px !important; border-top-right-radius: 2px !important; color: #111b21 !important; }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { background-color: #ffffff !important; border: 1px solid #e2e8f0; margin-left: 4px !important; margin-right: auto !important; border-top-left-radius: 2px !important; color: #111b21 !important; }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li { color: #111b21 !important; font-size: 0.95rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# 4. MULTILINGUAL SYNC & TEXT COLOR DISPLAY
if "lang" not in st.session_state:
    st.session_state["lang"] = st.session_state.get("selected_lang", "English")

current_lang = st.session_state.get("lang", "English")
lang_options = ["English", "Tamil (தமிழ்)", "Telugu (తెలుగు)"]
lang_idx = lang_options.index(current_lang) if current_lang in lang_options else 0

st.markdown(f"""
<div class="wa-header">
    <div class="wa-header-left">
        <div class="wa-avatar">🌱</div>
        <div>
            <h3 class="wa-title">{t("chat_title", current_lang)}</h3>
            <p class="wa-status">{t("chat_status", current_lang)}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Distinct Color Badge Bar for Languages
st.markdown("""
<div style="background: #ffffff; padding: 8px 12px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
    <span style="font-size: 12px; font-weight: 700; color: #475569;">🗣️ Native LLM Output:</span>
    <div style="display: flex; gap: 8px;">
        <span style="color: #2563eb; font-weight: 800; font-size: 12px; background: #eff6ff; padding: 2px 8px; border-radius: 6px; border: 1px solid #bfdbfe;">
            🇬🇧 English
        </span>
        <span style="color: #16a34a; font-weight: 800; font-size: 12px; background: #f0fdf4; padding: 2px 8px; border-radius: 6px; border: 1px solid #bbf7d0;">
            🌾 தமிழ்
        </span>
        <span style="color: #ea580c; font-weight: 800; font-size: 12px; background: #fff7ed; padding: 2px 8px; border-radius: 6px; border: 1px solid #fed7aa;">
            ☀️ తెలుగు
        </span>
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

# 7. ZERO-LAG NATIVE LLM HANDLER (Non-Streaming, No External Translators)
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