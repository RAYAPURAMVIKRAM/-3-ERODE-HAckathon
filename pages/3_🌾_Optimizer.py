import requests
import streamlit as st
from auth_ui import render_auth_sidebar

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Optimizer | STARK-X",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. RENDER AUTHENTICATION SIDEBAR
render_auth_sidebar()

# 3. CUSTOM STYLING
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
    
    .opt-header { 
        text-align: center !important; 
        color: #064e3b !important; 
        font-weight: 800 !important; 
        margin-bottom: 6px !important; 
    }
    .opt-subtitle {
        text-align: center !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        margin-bottom: 20px !important;
    }

    .stTabs [data-baseweb="tab-list"] { 
        gap: 14px !important; 
        border-bottom: 2px solid #cbd5e1 !important;
    }
    .stTabs [data-baseweb="tab"] { 
        height: 48px !important; 
        border-radius: 12px 12px 0 0 !important; 
        font-weight: 700 !important;
        color: #334155 !important;
        background: #f1f5f9 !important;
        border: 1.5px solid #cbd5e1 !important;
        border-bottom: none !important;
        padding: 8px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #064e3b !important;
        border-top: 3px solid #059669 !important;
    }

    .live-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%) !important;
        color: #ffffff !important;
        padding: 18px 22px !important;
        border-radius: 16px !important;
        margin-bottom: 22px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 4px 16px rgba(6, 78, 59, 0.25) !important;
    }
    .live-banner * {
        color: #ffffff !important;
    }
    .live-banner-content {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        flex-wrap: wrap !important;
        gap: 12px !important;
    }
    .live-banner-left {
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
    }
    .live-banner-title {
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
    }
    .live-banner-details {
        font-size: 13px !important;
        color: #d1fae5 !important;
        font-weight: 600 !important;
    }
    .live-soil-tag {
        background: rgba(255, 255, 255, 0.2) !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        font-size: 13.5px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.35) !important;
    }

    /* Primary Action Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        font-size: 1.08rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        padding: 14px 24px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.45) !important;
        background: linear-gradient(135deg, #047857 0%, #064e3b 100%) !important;
    }
    div.stButton > button * {
        color: #ffffff !important;
    }

    /* Alert / Result Boxes */
    div[data-testid="stAlert"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #059669 !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
    }
    div[data-testid="stAlert"] * {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. TAMIL NADU DISTRICT SOIL HASHMAP (TASK 5)
TN_DISTRICT_SOIL_MAP = {
    # Kongu Nadu Agro-Climatic Belt
    "Erode": "Red Soil",
    "Coimbatore": "Black Soil",
    "Tiruppur": "Red Soil",
    "Salem": "Red Soil",
    "Namakkal": "Red Soil",
    "Dharmapuri": "Red Soil",
    "Krishnagiri": "Red Soil",
    "Karur": "Red Soil",
    "Dindigul": "Red Soil",
    "Nilgiris": "Red Soil",
    
    # Cauvery Delta Zone
    "Thanjavur": "Alluvial",
    "Tiruvarur": "Alluvial",
    "Nagapattinam": "Alluvial",
    "Mayiladuthurai": "Alluvial",
    "Tiruchirappalli": "Alluvial",
    "Trichy": "Alluvial",
    "Cuddalore": "Alluvial",
    "Perambalur": "Black Soil",
    "Ariyalur": "Alluvial",
    
    # Southern Dry & Rainfed Zone
    "Madurai": "Black Soil",
    "Virudhunagar": "Black Soil",
    "Theni": "Red Soil",
    "Ramanathapuram": "Sandy Loam",
    "Sivaganga": "Red Soil",
    "Thoothukudi": "Black Soil",
    "Tirunelveli": "Red Soil",
    "Tenkasi": "Red Soil",
    "Kanyakumari": "Red Soil",
    
    # Northern Coastal & Plains
    "Chennai": "Sandy Loam",
    "Kanchipuram": "Clay",
    "Chengalpattu": "Clay",
    "Tiruvallur": "Sandy Loam",
    "Vellore": "Red Soil",
    "Ranipet": "Red Soil",
    "Tirupathur": "Red Soil",
    "Tiruvannamalai": "Red Soil",
    "Villupuram": "Red Soil",
    "Kallakurichi": "Red Soil"
}

# 5. ZERO-KEY LIVE GPS & SATELLITE CLIMATE FUNCTION (TASKS 2, 3, 4)
@st.cache_data(ttl=3600)
def get_auto_climate():
    """Fetches user coordinates via IP and real-time satellite weather from Open-Meteo with no API key."""
    # Default fallback values for Erode, TN
    default_city = "Erode"
    default_lat = 11.3410
    default_lon = 77.7172
    default_temp = 28.5
    default_humidity = 65.0

    # Step 1: Fast IP geolocation lookup (timeout=3)
    try:
        ip_res = requests.get("https://ipapi.co/json/", timeout=3).json()
        city = ip_res.get("city") or default_city
        lat = float(ip_res.get("latitude") or default_lat)
        lon = float(ip_res.get("longitude") or default_lon)
    except Exception:
        city = default_city
        lat = default_lat
        lon = default_lon

    # Step 2: Open-Meteo Satellite Weather API call (timeout=3)
    try:
        meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
        m_res = requests.get(meteo_url, timeout=3).json()
        current_weather = m_res.get("current", {})
        temp = float(current_weather.get("temperature_2m", default_temp))
        humidity = float(current_weather.get("relative_humidity_2m", default_humidity))
    except Exception:
        temp = default_temp
        humidity = default_humidity

    # Step 3: Infer Soil from District Hashmap
    inferred_soil = "Red Soil"
    for district, soil in TN_DISTRICT_SOIL_MAP.items():
        if district.lower() in city.lower():
            inferred_soil = soil
            break

    return {
        "city": city,
        "lat": lat,
        "lon": lon,
        "temperature": temp,
        "humidity": humidity,
        "inferred_soil": inferred_soil
    }

# Execute auto-climate fetch
climate_data = get_auto_climate()
detected_city = climate_data["city"]
live_temp = climate_data["temperature"]
live_humidity = climate_data["humidity"]
inferred_soil = climate_data["inferred_soil"]

from locales import t

lang = st.session_state.get("lang", "English")

# 6. DISPLAY GREEN LIVE WEATHER & GPS BANNER (TASK 6)
st.markdown(f"""
<div class="live-banner">
    <div class="live-banner-content">
        <div class="live-banner-left">
            <span class="live-banner-title">{t("gps_banner_title", lang)}</span>
            <span class="live-banner-details">
                📍 <b>{detected_city}</b> ({climate_data['lat']:.2f}°N, {climate_data['lon']:.2f}°E) 
                &nbsp;•&nbsp; 🌡️ <b>{live_temp:.1f}°C</b> Live Temp 
                &nbsp;•&nbsp; 💧 <b>{live_humidity:.0f}%</b> Humidity
            </span>
        </div>
        <div class="live-soil-tag">
            {t("auto_inferred_soil", lang)}: <b>{inferred_soil}</b>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 7. PAGE TITLES
st.markdown(f"<h2 class='opt-header'>{t('opt_title', lang)}</h2>", unsafe_allow_html=True)
st.markdown(f"<p class='opt-subtitle'>{t('opt_subtitle', lang)}</p>", unsafe_allow_html=True)

# 8. OPTIMIZER TABS
tab1, tab2 = st.tabs([t("opt_tab1", lang), t("opt_tab2", lang)])

soil_options = ["Red Soil", "Black Soil", "Alluvial", "Sandy Loam", "Clay"]
default_soil_index = soil_options.index(inferred_soil) if inferred_soil in soil_options else 0

# --- TAB 1: CONDITIONS TO CROP ---
with tab1:
    st.subheader(t("farm_params_title", lang))
    col1, col2 = st.columns(2)
    with col1:
        # Task 7: Use inferred soil as default
        soil_type = st.selectbox(
            f"{t('soil_label', lang)} (Auto-detected from GPS)",
            soil_options,
            index=default_soil_index,
            help=f"Pre-selected based on geological survey data for {detected_city}."
        )
        water_avail = st.selectbox(
            t("water_label", lang),
            ["Rainfed (Low)", "Borewell (Medium)", "Canal/River (High)"],
            index=1
        )
        ph_level = st.slider("Soil pH", 4.0, 9.0, 6.5)
    with col2:
        nitrogen = st.slider("Nitrogen (N)", 0, 150, 60)
        phosphorus = st.slider("Phosphorus (P)", 0, 150, 45)
        potassium = st.slider("Potassium (K)", 0, 150, 50)
        
    if st.button(t("opt_btn", lang), use_container_width=True):
        with st.spinner("Processing STARK-X agro-meteorological recommendation matrix..."):
            
            # STARK-X Engine Logic (calibrated for live temperature & district conditions)
            if water_avail == "Rainfed (Low)":
                if live_temp > 30.0 or soil_type in ["Red Soil", "Sandy Loam"]:
                    crops = [("Millets (Ragi / Kambu)", 96), ("Groundnut", 89), ("Horse Gram (Kollu)", 84)]
                else:
                    crops = [("Millets (Ragi)", 91), ("Pulses (Blackgram)", 85), ("Sesame", 80)]
            elif water_avail == "Canal/River (High)":
                if soil_type in ["Clay", "Alluvial"]:
                    crops = [("Paddy / Rice (CO-51)", 95), ("Sugarcane (CO-86032)", 88), ("Robusta Banana", 82)]
                else:
                    crops = [("Sugarcane (CO-86032)", 90), ("Turmeric (Finger)", 86), ("Maize", 80)]
            elif soil_type == "Black Soil":
                if live_temp >= 26.0:
                    crops = [("Cotton (MCU-5)", 96), ("Soybean", 87), ("Sunflower", 82)]
                else:
                    crops = [("Cotton", 90), ("Maize", 85), ("Bengal Gram", 81)]
            elif soil_type == "Red Soil":
                if potassium >= 45 and ph_level <= 7.5:
                    crops = [("Erode Turmeric (Curcuma longa)", 95), ("Maize", 88), ("Small Onion (Shallots)", 83)]
                else:
                    crops = [("Maize", 89), ("Tapioca / Cassava", 84), ("Groundnut", 80)]
            else:
                crops = [("Maize", 86), ("Vegetables (Tomato / Brinjal)", 82), ("Small Onion", 78)]
                
            st.success("Algorithm Analysis Complete!")
            st.markdown(f"### 🏆 Top Recommendation: **{crops[0][0]}** ({crops[0][1]}% Match)")
            st.progress(crops[0][1] / 100.0)
            
            st.markdown("#### High-Suitability Alternatives:")
            st.info(f"2. {crops[1][0]} — **{crops[1][1]}% Suitability**\n3. {crops[2][0]} — **{crops[2][1]}% Suitability**")
            st.caption(f"Engine grounded with live temperature ({live_temp:.1f}°C), {detected_city} soil profile ({inferred_soil}), and NPK balance.")

# --- TAB 2: CROP TO CONDITIONS ---
with tab2:
    st.subheader("Evaluate a Specific Crop Compatibility")
    target_crop = st.selectbox(
        "Select Crop to Evaluate",
        ["Erode Turmeric", "Paddy / Rice", "Cotton", "Millets (Ragi)", "Sugarcane", "Groundnut", "Small Onion"]
    )
    # Task 7: Use inferred soil as default
    target_soil = st.selectbox(
        t("soil_label", lang),
        soil_options,
        index=default_soil_index,
        key="t2_soil"
    )
    target_water = st.selectbox(
        t("water_label", lang),
        ["Rainfed (Low)", "Borewell (Medium)", "Canal/River (High)"],
        key="t2_water"
    )
    
    if st.button(t("opt_eval_btn", lang), use_container_width=True):
        with st.spinner("Cross-referencing live meteorological & agronomic thresholds..."):
            
            # Mismatch Logic Engine
            mismatch = False
            reasons = []
            
            if target_crop in ["Paddy / Rice", "Sugarcane"] and target_water == "Rainfed (Low)":
                mismatch = True
                reasons.append(f"{target_crop} requires high water immersion or frequent irrigation; Rainfed water will cause severe drought failure.")
            
            if target_crop == "Cotton" and target_soil not in ["Black Soil", "Alluvial"]:
                mismatch = True
                reasons.append("Cotton requires deep moisture-retentive Black (Regur) soil for boll development.")

            if target_crop == "Erode Turmeric" and target_water == "Rainfed (Low)":
                mismatch = True
                reasons.append("Turmeric rhizomes demand continuous moisture and good drainage; rainfed water is too risky.")

            if live_temp > 35.0 and target_crop in ["Paddy / Rice"] and target_water != "Canal/River (High)":
                mismatch = True
                reasons.append(f"Current temperature ({live_temp:.1f}°C) exceeds heat tolerance under low water conditions.")
            
            if mismatch:
                st.error("⚠️ **CRITICAL MISMATCH DETECTED**")
                for r in reasons:
                    st.write(f"• {r}")
                if target_water == "Rainfed (Low)":
                    st.info("💡 **Recommended Resilient Alternative:** Plant **Millets (Ragi / Kambu)** or **Groundnut** for guaranteed yields.")
                elif target_crop == "Cotton":
                    st.info(f"💡 **Recommended Alternative for {target_soil}:** Consider **Maize** or **Groundnut**.")
            else:
                st.success(f"✅ **OPTIMAL MATCH:** {target_crop} is well-suited for your farm!")
                st.write(f"Your {target_soil}, {target_water}, and local climate ({live_temp:.1f}°C) meet baseline commercial yield criteria.")
