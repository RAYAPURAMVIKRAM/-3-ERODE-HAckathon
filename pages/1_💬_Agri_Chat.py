import os
import streamlit as st
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import google.generativeai as genai
from auth_ui import render_auth_sidebar

# 1. FORCE RELOAD ENVIRONMENT VARIABLES
load_dotenv(override=True)
raw_key = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEY = raw_key.strip(' "\'')

# 2. STREAMLIT PAGE CONFIGURATION
st.set_page_config(
    page_title="Agri Chat | STARK-X",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 3. WHATSAPP THEME CUSTOM CSS
st.markdown("""
<style>
    /* WhatsApp Background & Main Container */
    .stApp {
        background-color: #efeae2;
        background-image: radial-gradient(#d4cdb4 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* WhatsApp Header Banner */
    .wa-header {
        background: linear-gradient(135deg, #075e54, #128c7e);
        color: white;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
    }
    .wa-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .wa-avatar {
        width: 44px;
        height: 44px;
        background-color: #25d366;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .wa-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        letter-spacing: 0.3px;
    }
    .wa-status {
        font-size: 0.8rem;
        color: #dcf8c6;
        margin: 2px 0 0 0;
    }
    .wa-badge {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #ffffff;
    }

    /* WhatsApp Chat Message Container Styling */
    div[data-testid="stChatMessage"] {
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
        max-width: 88%;
    }

    /* User Message Bubble: Greenish & Aligned Right */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from user"]) {
        background-color: #dcf8c6 !important;
        border: 1px solid #c7e8ab;
        margin-left: auto !important;
        margin-right: 4px !important;
        border-top-right-radius: 2px !important;
        color: #111b21 !important;
    }

    /* Assistant Message Bubble: Crisp White & Aligned Left */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]),
    div[data-testid="stChatMessage"]:has([aria-label="Chat message from assistant"]) {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0;
        margin-left: 4px !important;
        margin-right: auto !important;
        border-top-left-radius: 2px !important;
        color: #111b21 !important;
    }

    /* Ensure text in message containers stays sharp and dark */
    div[data-testid="stChatMessage"] p, 
    div[data-testid="stChatMessage"] li {
        color: #111b21 !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Language Toggle Container */
    .lang-bar {
        background: #ffffff;
        border: 1px solid #128c7e;
        border-radius: 12px;
        padding: 8px 14px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# 4. TRANSLATION HELPER (FAILSAFE)
def safe_translate(text: str, source: str, target: str) -> str:
    """Translates text using GoogleTranslator with failsafe fallback."""
    if not text or source == target:
        return text
    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"Translation notice ({source} -> {target}): {e}")
        return text

# 5. MASTER AGRONOMY PROMPT (SYSTEM INSTRUCTION)
MASTER_AGRONOMY_PROMPT = """
You are STARK-X, an empathetic, accessible, and highly knowledgeable agricultural advisor dedicated to Indian farmers, with specialized expertise in Tamil Nadu (especially Erode, Salem, Coimbatore, Tiruppur, Cauvery/Bhavani basin).

Core Rules:
1. Provide short, concise, highly practical answers (within 100-150 words).
2. For crop questions, evaluate Soil, Water, and Climate with a Percentage Suitability score.
3. Recommend specific practical remedies, fertilizer doses, and irrigation advice for local conditions.
4. Keep tone respectful, warm, and encourage the farmer.
"""

# 6. WHATSAPP HEADER UI
st.markdown("""
<div class="wa-header">
    <div class="wa-header-left">
        <div class="wa-avatar">🌱</div>
        <div>
            <h3 class="wa-title">STARK-X Agri Advisor</h3>
            <p class="wa-status">🟢 Online | Real-Time Multilingual Fast AI</p>
        </div>
    </div>
    <div class="wa-badge">Ultra-Low Latency</div>
</div>
""", unsafe_allow_html=True)

# 7. LANGUAGE SELECTION TOGGLE (TASK 2)
lang_col, _ = st.columns([3, 1])
with lang_col:
    selected_language = st.radio(
        "🌐 **Choose Language / மொழி / భాష:**",
        ["English", "Tamil (தமிழ்)", "Telugu (తెలుగు)"],
        horizontal=True,
        index=0
    )

# Language code mapping
lang_code_map = {
    "English": "en",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te"
}
target_lang_code = lang_code_map.get(selected_language, "en")

# 8. SIDEBAR CONTROLS & API KEY CHECK
with st.sidebar:
    render_auth_sidebar()
    st.image("https://images.unsplash.com/photo-1592982537447-7440770cbfc9?q=80&w=400&auto=format&fit=crop", use_container_width=True)
    st.header("⚙️ Chat Settings")
    
    if GEMINI_API_KEY:
        st.success("✅ Gemini API Key connected")
    else:
        st.error("⚠️ GEMINI_API_KEY missing in .env")
        st.caption("Please add your key to `.env`: `GEMINI_API_KEY=your_key`")
        
    st.markdown("---")
    st.markdown("**Suggested Quick Questions:**")
    quick_queries = [
        "Can I grow Turmeric in Erode red soil?",
        "What should I grow with very low borewell water?",
        "I am growing Sugarcane but water is low, what to do?",
        "வேர்க்கடலை சாகுபடிக்கு எந்த மண் ஏற்றது?"
    ]
    for q in quick_queries:
        if st.button(f"📌 {q}", key=f"quick_{q}"):
            st.session_state["queued_query"] = q
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Vanakkam! I am your STARK-X farming advisor. Tell me your village, soil type, and water availability, or ask me any crop question!"
            }
        ]
        st.rerun()

# 9. INITIALIZE PERSISTENT CONVERSATION HISTORY
GREETING_MESSAGE = "Vanakkam! I am your STARK-X farming advisor. Tell me your village, soil type, and water availability, or ask me any crop question!"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": GREETING_MESSAGE
        }
    ]

# 10. DISPLAY EXISTING CHAT MESSAGES
for msg in st.session_state.chat_history:
    avatar_icon = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# 11. GEMINI FAST GENERATION ENGINE (TASK 4)
def generate_fast_gemini(prompt_english: str) -> str:
    """Calls Gemini with gemini-1.5-flash and low-latency generation config."""
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API Key is missing. Please configure GEMINI_API_KEY in your .env file."

    try:
        genai.configure(api_key=GEMINI_API_KEY, transport="rest")
        
        # Generation configuration for ultra-low latency & concise response
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=250,
            temperature=0.3
        )

        full_input = f"{MASTER_AGRONOMY_PROMPT}\n\nFarmer Question: {prompt_english}\n\nSTARK-X Advisor:"

        # Primary: gemini-1.5-flash | Fallback: gemini-flash-latest
        try:
            model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
            response = model.generate_content(full_input, stream=False)
            return response.text
        except Exception:
            model = genai.GenerativeModel("gemini-flash-latest", generation_config=generation_config)
            response = model.generate_content(full_input, stream=False)
            return response.text

    except Exception as e:
        return f"⚠️ Advisory Error: {str(e)}"

# 12. CHAT INPUT & EXECUTION PIPELINE (TASKS 3 & 5)
user_input = st.chat_input("Ask about your crops, soil, water, or district...")

if "queued_query" in st.session_state:
    user_input = st.session_state.pop("queued_query")

if user_input:
    # Append & display original user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant", avatar="assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("⚡ STARK-X is analyzing with low latency..."):
            # Task 3: Intercept prompt -> Translate to English if selected language is not English
            if target_lang_code != "en":
                english_prompt = safe_translate(user_input, source="auto", target="en")
            else:
                english_prompt = user_input

            # Task 4: Call Gemini 1.5 Flash in English
            raw_english_response = generate_fast_gemini(english_prompt)

            # Task 5: Intercept response -> Translate back into selected regional language
            if target_lang_code != "en":
                final_response = safe_translate(raw_english_response, source="en", target=target_lang_code)
            else:
                final_response = raw_english_response

            # Display final translated response
            message_placeholder.markdown(final_response)
            
    if final_response:
        st.session_state.chat_history.append({"role": "assistant", "content": final_response})