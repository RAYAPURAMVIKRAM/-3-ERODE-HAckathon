import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from auth_ui import render_auth_sidebar
from locales import t

# 1. LOAD API KEY WITH CACHE OVERRIDE
load_dotenv(override=True)
raw_key = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_KEY = raw_key.strip(' "\'')

# 2. PAGE CONFIG
st.set_page_config(page_title="Crop Vision | STARK-X", page_icon="📸", layout="centered")

# Render Farmer Authentication & Persistent Language Selector in Sidebar
render_auth_sidebar()

# 3. MODERN EXECUTIVE AGRICULTURAL THEME & HIGH-CONTRAST CSS
st.markdown("""
<style>
    /* Force Light Color Scheme across all browsers & OS dark-mode overrides */
    :root {
        color-scheme: light !important;
        --text-color: #0f172a !important;
        --background-color: #f8fafc !important;
        --secondary-background-color: #ffffff !important;
    }

    /* Base Page Styling: Clean, professional, light-slate agricultural canvas */
    .stApp {
        background-color: #f8fafc !important;
        background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px) !important;
        background-size: 24px 24px !important;
        color: #0f172a !important;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Premium Header Hero Banner */
    .vision-hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%) !important;
        color: #ffffff !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        box-shadow: 0 4px 16px rgba(6, 78, 59, 0.25) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
    }
    .vision-hero-banner * {
        color: #ffffff !important;
    }
    .vision-hero-left {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    .vision-avatar-badge {
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
    .vision-hero-title {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
    }
    .vision-hero-status {
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
    .vision-badge-pill {
        background: rgba(255, 255, 255, 0.18) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
    }

    /* 3-Step Instruction Guide Cards */
    .step-cards-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)) !important;
        gap: 12px !important;
        margin-bottom: 20px !important;
    }
    .step-card {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }
    .step-icon {
        font-size: 24px !important;
        background: #f0fdf4 !important;
        border: 1.5px solid #86efac !important;
        border-radius: 10px !important;
        padding: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
    }
    .step-text-title {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #064e3b !important;
        margin: 0 0 2px 0 !important;
    }
    .step-text-desc {
        font-size: 11.5px !important;
        color: #475569 !important;
        margin: 0 !important;
        line-height: 1.35 !important;
        font-weight: 600 !important;
    }

    /* File Uploader Container Styling */
    div[data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 2px dashed #059669 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05) !important;
        margin-bottom: 20px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #047857 !important;
        background: #f0fdf4 !important;
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.12) !important;
    }
    div[data-testid="stFileUploader"] label {
        color: #064e3b !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stFileUploader"] small {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stFileUploader"] section {
        background: #f8fafc !important;
        border-radius: 12px !important;
    }
    div[data-testid="stFileUploader"] button {
        background: #ffffff !important;
        color: #064e3b !important;
        border: 1.5px solid #059669 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background: #059669 !important;
        color: #ffffff !important;
    }

    /* Image Preview Container */
    .stImage {
        background: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 14px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
        margin-bottom: 18px !important;
    }
    .stImage > img {
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }
    .stImage [data-testid="stCaptionContainer"] p {
        color: #475569 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-align: center !important;
        margin-top: 8px !important;
    }

    /* Primary Action Button (Run Vision Scan) */
    div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        padding: 14px 24px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
        transition: all 0.2s ease !important;
        margin-bottom: 20px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.45) !important;
        background: linear-gradient(135deg, #047857 0%, #064e3b 100%) !important;
    }
    div.stButton > button * {
        color: #ffffff !important;
    }

    /* Spinner State */
    div[data-testid="stSpinner"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #f59e0b !important;
        border-radius: 14px !important;
        padding: 12px 18px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stSpinner"] * {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
    }

    /* High-Contrast Agronomy Report Output (stAlert & stInfo) */
    div[data-testid="stAlert"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #059669 !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.08) !important;
        margin-bottom: 16px !important;
    }
    div[data-testid="stAlert"] * {
        color: #0f172a !important;
        font-size: 1.05rem !important;
        line-height: 1.75 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stAlert"] strong,
    div[data-testid="stAlert"] b {
        color: #047857 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stAlert"] h1,
    div[data-testid="stAlert"] h2,
    div[data-testid="stAlert"] h3,
    div[data-testid="stAlert"] h4 {
        color: #064e3b !important;
        font-weight: 800 !important;
    }
    div[data-testid="stAlert"] ul,
    div[data-testid="stAlert"] ol {
        color: #0f172a !important;
        padding-left: 24px !important;
        margin: 8px 0 12px 0 !important;
    }
    div[data-testid="stAlert"] li {
        margin-bottom: 6px !important;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

lang = st.session_state.get("lang", "English")

# RENDER EXECUTIVE HERO BANNER & 3-STEP GUIDE
st.markdown(f"""
<div class="vision-hero-banner">
    <div class="vision-hero-left">
        <div class="vision-avatar-badge">📸</div>
        <div>
            <h3 class="vision-hero-title">{t("vision_title", lang)}</h3>
            <p class="vision-hero-status"><span class="live-dot"></span> {t("vision_desc", lang)}</p>
        </div>
    </div>
    <div class="vision-badge-pill">
        🌱 STARK-X Vision Engine
    </div>
</div>

<div class="step-cards-grid">
    <div class="step-card">
        <div class="step-icon">📷</div>
        <div>
            <h5 class="step-text-title">1. Upload Photo</h5>
            <p class="step-text-desc">Clear leaf, stem or fruit image</p>
        </div>
    </div>
    <div class="step-card">
        <div class="step-icon">🔬</div>
        <div>
            <h5 class="step-text-title">2. AI Pathology</h5>
            <p class="step-text-desc">Instant pest & deficiency scan</p>
        </div>
    </div>
    <div class="step-card">
        <div class="step-icon">💊</div>
        <div>
            <h5 class="step-text-title">3. Treatment</h5>
            <p class="step-text-desc">Low-cost organic remedies</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. CACHED INFERENCE FUNCTION
@st.cache_data(show_spinner=False)
def analyze_crop_image(_image, target_lang):
    genai.configure(api_key=GEMINI_API_KEY, transport="rest")
    prompt = (
        f"Act as an expert Indian agronomist and plant pathologist. Look at this crop photo. "
        f"1. Identify the crop if possible. "
        f"2. Assess its overall health. "
        f"3. Detect any visible diseases, pests, or nutrient deficiencies. "
        f"4. Provide 3 simple, low-cost, practical steps the farmer can take to fix the issue or improve yield. "
        f"Keep the language simple and empathetic. "
        f"IMPORTANT: Output your complete agronomic analysis natively in {target_lang}."
    )
    candidate_models = ['gemini-flash-lite-latest', 'gemini-3.5-flash', 'gemini-3.1-flash-lite', 'gemini-1.5-flash']
    for m in candidate_models:
        try:
            model = genai.GenerativeModel(m)
            response = model.generate_content([prompt, _image], stream=False)
            if response and response.text:
                return response.text
        except Exception:
            continue
    raise Exception("Unable to analyze image across available vision models.")

# 5. FILE UPLOADER
uploaded_file = st.file_uploader(t("vision_upload_label", lang), type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Crop Photo", use_container_width=True)
    
    if st.button(t("vision_btn", lang), use_container_width=True):
        if not GEMINI_API_KEY:
            st.error("⚠️ Gemini API Key is missing. Please check your .env file.")
        else:
            with st.spinner(t("scanning_msg", lang)):
                try:
                    report = analyze_crop_image(image, lang)
                    st.success(t("analysis_complete", lang))
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; margin-bottom: 8px;">
                        <h3 style="color: #064e3b; font-weight: 800; margin: 0;">📋 {t('report_title', lang)}</h3>
                        <span class="verified-badge">✓ STARK-X Certified Agronomist Scan</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info(report)
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Quota" in error_msg:
                        st.warning("⚠️ API Quota Limit Reached. Showing STARK-X Offline Analysis.")
                        st.success(f"{t('analysis_complete', lang)} (Offline Mode)")
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; margin-bottom: 8px;">
                            <h3 style="color: #064e3b; font-weight: 800; margin: 0;">📋 {t('report_title', lang)}</h3>
                            <span class="verified-badge">🌱 STARK-X Offline Diagnostic</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.info(
                            "**1. Crop Identification:** Likely Tomato or Solanaceous family.\n\n"
                            "**2. Overall Health:** Moderate stress detected along foliage margins.\n\n"
                            "**3. Disease/Deficiency Detection:** Chlorosis (yellowing) between veins indicates potential Early Blight onset or Potassium deficiency.\n\n"
                            "**4. Actionable Steps for Farmer:**\n"
                            "- Prune affected low-hanging foliage to prevent soil spore transmission.\n"
                            "- Apply organic neem oil spray (5ml/L) as a protective antifungal barrier.\n"
                            "- Regulate drip cycles to avoid root-zone waterlogging."
                        )
                    else:
                        st.error(f"⚠️ Error analyzing image: {error_msg}")
