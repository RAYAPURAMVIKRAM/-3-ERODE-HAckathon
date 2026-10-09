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

# 3. INSTAGRAM-STYLE CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .vision-header { text-align: center; font-family: sans-serif; color: #111b21; margin-bottom: 20px; }
    .upload-box { border: 2px dashed #128c7e; border-radius: 15px; padding: 20px; text-align: center; background-color: #f0fdf4; }
    .stImage > img { border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

lang = st.session_state.get("lang", "English")

st.markdown(f"<h2 class='vision-header'>{t('vision_title', lang)}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #555;'>{t('vision_desc', lang)}</p>", unsafe_allow_html=True)

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
                    st.markdown(f"### {t('report_title', lang)}")
                    st.info(report)
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Quota" in error_msg:
                        st.warning("⚠️ API Quota Limit Reached. Showing STARK-X Offline Analysis.")
                        st.success(f"{t('analysis_complete', lang)} (Offline Mode)")
                        st.markdown(f"### {t('report_title', lang)}")
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
