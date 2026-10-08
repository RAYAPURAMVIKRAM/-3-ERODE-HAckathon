import os
import streamlit as st
from dotenv import load_dotenv
from auth_ui import render_auth_sidebar

# Force reload the environment variables
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
        margin-bottom: 16px;
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

    /* Modern Bottom Input Field */
    div[data-testid="stChatInput"] {
        border-radius: 24px;
    }
    div[data-testid="stChatInput"] > div {
        border-radius: 24px !important;
        border: 1px solid #128c7e !important;
    }

    /* Quick Action / Suggestion Chips */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }
    .chip-btn {
        background-color: #ffffff;
        border: 1px solid #128c7e;
        color: #075e54;
        padding: 5px 12px;
        border-radius: 16px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
    }
</style>
""", unsafe_allow_html=True)

# 4. MASTER AGRONOMY PROMPT (SYSTEM INSTRUCTION)
MASTER_AGRONOMY_PROMPT = """
You are STARK-X, an empathetic, simple, accessible, and highly knowledgeable agricultural advisor and agronomist dedicated to Indian farmers, with specialized expertise in Tamil Nadu (especially Erode, Salem, Coimbatore, Tiruppur, and nearby Cauvery/Bhavani basin areas).

Your Core Persona:
- Empathetic, warm, encouraging, and respectful.
- Use simple, direct, non-academic language that any farmer can understand immediately.
- Never make the farmer feel bad or blamed for previous crop choices.

Multi-Lingual Language Rule:
- Automatically detect and reply in the EXACT language/style used by the farmer:
  * English: Simple, clear Indian English.
  * Tamil (தமிழ்): Natural, courteous Tamil (வணக்கம், வாழ்த்துக்கள், எளிய நடை).
  * Tanglish: Tamil written in English letters (e.g. "Vanakkam! Unga mannu red soil ah iruntha Ragi nallave varum.").

Core Master Rules:
Rule 1: 'Can I grow [Crop]?'
- Evaluate 3 core pillars: Soil Type, Temperature/Climate, and Water Availability.
- Always provide an explicit Percentage Suitability score (e.g., '🌱 Suitability: 85%').
- Format evaluation with clear bullet points:
  * 🪨 Soil: [Good / Moderate / Bad] - Explain soil compatibility (texture, pH, drainage).
  * 💧 Water: [Good / Moderate / Bad] - Water requirement vs farmer's availability.
  * ☀️ Climate/Temperature: [Good / Moderate / Bad] - Season and weather fit.
  * 💡 Practical Farmer Tip: A practical step or soil preparation advice.

Rule 2: 'What should I grow?'
- Recommend the Top 3 crops ranked by percentage suitability.
- Account for water scarcity, soil condition, and seasonal market potential.
- Format with clear numbered list:
  1. [Crop 1] - [XX]% Suitability (Reason: drought tolerance, quick harvest, good returns)
  2. [Crop 2] - [XX]% Suitability (Reason...)
  3. [Crop 3] - [XX]% Suitability (Reason...)

Rule 3: 'I am growing [Crop]'
- Check for crop-soil or water mismatch.
- If another crop yields better economic return or fits their water constraints, suggest it politely and constructively without criticizing the farmer.

Agronomic Knowledge Base:
- Rice (Paddy / நெல்): Requires heavy clay or alluvial soil with water holding capacity, pH 5.5-7.0, very high continuous water demand. Suffers severe drought stress during shortages.
- Millets / Ragi (கேழ்வரகு / தினை / கம்பு): Best in Red soil / Sandy-loam. Highly drought-tolerant with low water demand. Top recommendation during water-stressed spells or dry seasons.
- Turmeric (மஞ்சள்): High-value commercial crop, iconic in Erode. Needs well-drained loamy or alluvial soil, moderate water, strictly avoid waterlogging.
- Cotton (பருத்தி): Thrives in Black soil (Regur), medium water demand, hot climate.
- Sugarcane (கரும்பு): Extremely high water demand; strongly advise caution if groundwater/borewell is depleting.
- Groundnut (வேர்க்கடலை): Red/sandy loam, medium water requirement, excellent soil-enriching diversification crop.

Keep responses structured, concise, and easy to read on mobile screens.
"""

# 5. WHATSAPP HEADER UI
st.markdown("""
<div class="wa-header">
    <div class="wa-header-left">
        <div class="wa-avatar">🌱</div>
        <div>
            <h3 class="wa-title">STARK-X Agri Advisor</h3>
            <p class="wa-status">🟢 Online | Tamil Nadu Agronomy Desk</p>
        </div>
    </div>
    <div class="wa-badge">WhatsApp View</div>
</div>
""", unsafe_allow_html=True)

# 6. SIDEBAR CONTROLS & API KEY CHECK
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
                "content": "Vanakkam! I am your STARK-X farming advisor. Tell me your village/district, what soil you have, and your water availability, or ask me about any crop!"
            }
        ]
        if "interaction_id" in st.session_state:
            del st.session_state["interaction_id"]
        st.rerun()

# 7. INITIALIZE PERSISTENT CONVERSATION HISTORY
GREETING_MESSAGE = "Vanakkam! I am your STARK-X farming advisor. Tell me your village/district, what soil you have, and your water availability, or ask me about any crop!"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": GREETING_MESSAGE
        }
    ]

# 8. DISPLAY EXISTING CHAT MESSAGES
for msg in st.session_state.chat_history:
    avatar_icon = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# 9. GEMINI LLM INTERACTION HANDLER (BULLETPROOF FALLBACK)
import google.generativeai as genai

def generate_gemini_stream(prompt: str):
    if not GEMINI_API_KEY:
        yield "⚠️ Gemini API Key is missing."
        return

    try:
        genai.configure(api_key=GEMINI_API_KEY, transport="rest")
        
        recent_history_context = ""
        if len(st.session_state.chat_history) > 1:
            recent_history_context = "Previous Conversation:\n"
            for item in st.session_state.chat_history[-6:]:
                role_label = "Farmer" if item["role"] == "user" else "Advisor"
                recent_history_context += f"{role_label}: {item['content']}\n"

        # Injecting the Master Prompt directly to bypass parameter restrictions
        full_input = f"{MASTER_AGRONOMY_PROMPT}\n\n{recent_history_context}\nFarmer: {prompt}\n\nSTARK-X:"

        # Try gemini-pro, with automatic fallback to gemini-flash-latest if deprecated on endpoint
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(full_input, stream=False)
        except Exception:
            model = genai.GenerativeModel("gemini-flash-latest")
            response = model.generate_content(full_input, stream=False)

        yield response.text

    except Exception as e:
        yield f"⚠️ API Error: {str(e)}"

# 10. CHAT INPUT & EXECUTION
user_input = st.chat_input("Ask about your crops, soil, water, or district...")

if "queued_query" in st.session_state:
    user_input = st.session_state.pop("queued_query")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant", avatar="assistant"):
        # Windows Defender Bypass: Manually render text instead of using st.write_stream
        message_placeholder = st.empty()
        response_text = ""
        with st.spinner("STARK-X is thinking..."):
            for chunk in generate_gemini_stream(user_input):
                response_text += chunk
                message_placeholder.markdown(response_text)
            
    if response_text:
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})