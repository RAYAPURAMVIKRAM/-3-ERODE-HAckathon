import os
import streamlit as st
import google.generativeai as genai
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from auth_ui import render_auth_sidebar

# 1. LOAD ENVIRONMENT VARIABLES WITH CACHE OVERRIDE
load_dotenv(override=True)
raw_key = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEY = raw_key.strip(' "\'')

# 2. STREAMLIT PAGE CONFIGURATION
st.set_page_config(page_title="Agri Chat | STARK-X", page_icon="💬", layout="centered")

# RENDER SIDEBAR AUTH
with st.sidebar:
    render_auth_sidebar()

# 3. WHATSAPP THEME CUSTOM CSS
st.markdown("""
<style>
    .stApp { background-color: #efeae2; background-image: radial-gradient(#d4cdb4 1px, transparent 1px); background-size: 20px 20px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .wa-header { background: linear-gradient(135deg, #075e54, #128c7e); color: white; padding: 14px 18px; border-radius: 12px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15); }
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

# 4. MULTILINGUAL TOGGLE
st.markdown("""
<div class="wa-header">
    <div class="wa-header-left">
        <div class="wa-avatar">🌱</div>
        <div>
            <h3 class="wa-title">STARK-X Agri Advisor</h3>
            <p class="wa-status">🟢 Online | Multi-Language Desk</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

lang_option = st.radio("Select Language / மொழியைத் தேர்ந்தெடுக்கவும்", ["English", "Tamil (தமிழ்)", "Telugu (తెలుగు)"], horizontal=True)
lang_map = {"English": "en", "Tamil (தமிழ்)": "ta", "Telugu (తెలుగు)": "te"}
target_lang = lang_map[lang_option]

# 5. MASTER AGRONOMY PROMPT
MASTER_AGRONOMY_PROMPT = """
You are STARK-X, an empathetic, simple, and highly knowledgeable agricultural advisor for Indian farmers (Tamil Nadu focus).
Rules:
1. Always evaluate Soil Type, Temperature, and Water Availability.
2. Provide a Percentage Suitability score (e.g., '🌱 Suitability: 85%').
3. Format with clear bullet points.
4. Keep it concise, practical, and highly accurate.
Knowledge Base:
- Rice/Paddy: Clay/Alluvial, pH 5.5-7.0, high water. Do not recommend if water is low.
- Millets/Ragi: Red/Sandy-loam, highly drought-tolerant.
- Turmeric: Well-drained loamy, Erode region, high value.
- Cotton: Black soil, medium water, hot climate.
"""

# 6. INITIALIZE CHAT HISTORY
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Vanakkam! I am your STARK-X farming advisor. Tell me your village, soil type, and water availability, or ask me any crop question!"}]

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"], avatar="user" if msg["role"] == "user" else "assistant").markdown(msg["content"])

# 7. SAFE TRANSLATION & LLM HANDLER (No Streaming)
def get_starkx_response(user_prompt):
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API Key is missing. Check your .env file."
    
    try:
        genai.configure(api_key=GEMINI_API_KEY, transport="rest")
        
        # Translate to English for AI processing if needed
        proc_prompt = user_prompt
        if target_lang != "en":
            try:
                proc_prompt = GoogleTranslator(source=target_lang, target='en').translate(user_prompt)
            except Exception:
                proc_prompt = user_prompt
            
        recent_context = ""
        for item in st.session_state.chat_history[-4:]:
            role_label = "Farmer" if item["role"] == "user" else "Advisor"
            recent_context += f"{role_label}: {item['content']}\n"
            
        full_input = f"{recent_context}\nFarmer asks: {proc_prompt}"
        
        # Fetch the FULL text at once to prevent translation crashes
        try:
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=MASTER_AGRONOMY_PROMPT)
            response = model.generate_content(full_input, stream=False)
        except Exception:
            model = genai.GenerativeModel('gemini-flash-latest', system_instruction=MASTER_AGRONOMY_PROMPT)
            response = model.generate_content(full_input, stream=False)
            
        final_text = response.text
        
        # Translate back to the user's language
        if target_lang != "en":
            try:
                final_text = GoogleTranslator(source='en', target=target_lang).translate(final_text)
            except Exception:
                pass
            
        return final_text
    except Exception as e:
        return f"⚠️ Error generating response. Please try again. ({str(e)})"

# 8. CHAT INPUT
user_input = st.chat_input("Ask about your crops, soil, water, or district...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("STARK-X is thinking & translating..."):
            reply = get_starkx_response(user_input)
            st.markdown(reply)
            
    st.session_state.chat_history.append({"role": "assistant", "content": reply})