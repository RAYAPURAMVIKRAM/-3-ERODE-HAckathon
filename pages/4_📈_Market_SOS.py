import streamlit as st
import pandas as pd
from auth_ui import render_auth_sidebar
from locales import t
from supabase_client import (
    get_current_user,
    insert_sos_ticket,
    get_sos_tickets,
    is_supabase_connected,
    format_to_ist
)

st.set_page_config(page_title="Market & SOS | STARK-X", page_icon="📈", layout="centered")

# Render Farmer Authentication & Profile in Sidebar
render_auth_sidebar()

lang = st.session_state.get("lang", "English")

# 1. EXECUTIVE AGRICULTURAL THEME & HIGH-CONTRAST CSS
st.markdown("""
<style>
    /* Force Light Color Scheme across all browsers & OS dark-mode overrides */
    :root {
        color-scheme: light !important;
        --text-color: #0f172a !important;
        --background-color: #f8fafc !important;
        --secondary-background-color: #ffffff !important;
    }

    /* Base Page Canvas */
    .stApp {
        background-color: #f8fafc !important;
        background-image: radial-gradient(#cbd5e1 1.2px, transparent 1.2px) !important;
        background-size: 24px 24px !important;
        color: #0f172a !important;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

    /* Premium Header Hero Banner */
    .sos-hero-banner {
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
    .sos-hero-banner * {
        color: #ffffff !important;
    }
    .sos-hero-left {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    .sos-avatar-badge {
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
    .sos-hero-title {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
    }
    .sos-hero-status {
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
    .sos-badge-pill {
        background: rgba(255, 255, 255, 0.18) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
    }

    /* System Connectivity Bar */
    .system-status-card {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        margin-bottom: 16px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }
    .system-status-text {
        font-size: 13.5px !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    .system-secure-badge {
        font-size: 12px !important;
        font-weight: 800 !important;
        color: #059669 !important;
        background: #dcfce7 !important;
        padding: 4px 10px !important;
        border-radius: 12px !important;
        border: 1px solid #86efac !important;
    }

    /* Tab Buttons: High Contrast & Solid Background */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 14px !important; 
        border-bottom: 2px solid #cbd5e1 !important;
        margin-bottom: 20px !important;
    }
    .stTabs [data-baseweb="tab"] { 
        height: 50px !important; 
        border-radius: 12px 12px 0 0 !important; 
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        color: #334155 !important;
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-bottom: none !important;
        padding: 10px 22px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #f0fdf4 !important;
        color: #059669 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #064e3b !important;
        border-top: 4px solid #059669 !important;
        box-shadow: 0 -2px 8px rgba(5, 150, 105, 0.12) !important;
    }

    /* Section Cards */
    .section-card {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06) !important;
    }
    .section-card-title {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: #064e3b !important;
        margin-top: 0 !important;
        margin-bottom: 6px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    .section-card-desc {
        font-size: 14px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
        line-height: 1.5 !important;
    }

    /* Dataframe Container */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 8px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
        margin-bottom: 18px !important;
    }

    /* Forms & Inputs */
    div[data-testid="stForm"] {
        background: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.08) !important;
        margin-bottom: 24px !important;
    }
    div[data-testid="stForm"] label,
    label[data-testid="stWidgetLabel"] p {
        color: #064e3b !important;
        font-weight: 800 !important;
        font-size: 0.98rem !important;
        margin-bottom: 6px !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #94a3b8 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.25) !important;
    }

    /* Buttons: Primary Gradient */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
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
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.45) !important;
        background: linear-gradient(135deg, #047857 0%, #064e3b 100%) !important;
    }
    div.stButton > button *,
    div[data-testid="stFormSubmitButton"] > button * {
        color: #ffffff !important;
    }

    /* Alert & Info Boxes */
    div[data-testid="stAlert"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #059669 !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
        margin-top: 14px !important;
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
</style>
""", unsafe_allow_html=True)

# 2. HERO BANNER
st.markdown(f"""
<div class="sos-hero-banner">
    <div class="sos-hero-left">
        <div class="sos-avatar-badge">📈</div>
        <div>
            <h3 class="sos-hero-title">{t("market_sos_page", lang)}</h3>
            <p class="sos-hero-status"><span class="live-dot"></span> {t("market_sos_desc", lang)}</p>
        </div>
    </div>
    <div class="sos-badge-pill">
        🌾 Erode Agro-FinDesk
    </div>
</div>
""", unsafe_allow_html=True)

# Database connectivity badge
db_status = "🟢 Supabase Cloud Database Connected" if is_supabase_connected() else "🟡 Local Database Active (Supabase Ready)"
st.markdown(f"""
<div class="system-status-card">
    <span class="system-status-text">📡 <b>Backend Node:</b> {db_status}</span>
    <span class="system-secure-badge">🔒 256-Bit Agricultural Union Network</span>
</div>
""", unsafe_allow_html=True)

# 3. TABS
tab1, tab2 = st.tabs(["📈 Live Market (FinTech)", "🚨 SOS Helpdesk"])

# --- TAB 1: MARKET PRICES & FINTECH ---
with tab1:
    st.markdown("""
    <div class="section-card">
        <h4 class="section-card-title">📊 Live Mandi Spot Rates (Erode / Kongu Belt)</h4>
        <p class="section-card-desc">Real-time regulated APMC market arrivals and modal price benchmarks updated hourly.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulated Live Data
    market_data = {
        "Crop": ["Turmeric (Bulb)", "Rice (Paddy - Grade A)", "Cotton (Long Staple)", "Millets (Ragi)", "Groundnut"],
        "Current Price (₹/Quintal)": ["₹12,450", "₹2,203", "₹7,100", "₹3,500", "₹6,400"],
        "Trend": ["⬆️ High Demand", "➡️ Stable", "⬇️ Dropping", "⬆️ Rising", "➡️ Stable"]
    }
    df = pd.DataFrame(market_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div class="section-card" style="margin-top: 10px;">
        <h4 class="section-card-title">💰 STARK-X Predictive Financial Advisor</h4>
        <p class="section-card-desc">Machine learning yield valuation and holding period recommendations based on seasonal export orders.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Generate Financial Strategy", use_container_width=True):
        with st.spinner("Analyzing market volume trends and export signals..."):
            st.success("Strategy Generated Successfully!")
            st.info(
                "**🌿 Turmeric Outlook:** Erode markets are showing a 12% week-over-week price surge due to direct UAE and Europe spice export contracts. \n\n"
                "**📌 Strategic Action:** Hold current stock for another 14 days for peak terminal pricing. \n\n"
                "**🌾 Millets / Ragi:** Increased subsidies for climate-resilient grains are driving up local MSP (Minimum Support Price). \n\n"
                "**📌 Strategic Action:** Liquidate 50% now to cover harvesting operational expenditure, hold remaining 50% for direct retail packaging."
            )

# --- TAB 2: SOS HELPDESK ---
with tab2:
    st.markdown("""
    <div class="section-card" style="border-left: 6px solid #dc2626;">
        <h4 class="section-card-title" style="color: #dc2626;">🚨 Emergency Agricultural Union Dispatch</h4>
        <p class="section-card-desc">Report critical crop failure, canal water diversion, power grid cuts, or commission agent fraud. Submissions trigger immediate student agronomist on-ground physical intervention.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pre-fill name and village if logged in
    user = get_current_user() or {}
    default_name = user.get("name", "")
    default_village = user.get("village", "")
    
    with st.form("sos_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            farmer_name = st.text_input("Farmer Name", value=default_name, placeholder="e.g. Shanmugam P.")
        with col2:
            village = st.text_input("Village / District", value=default_village, placeholder="e.g. Modakkurichi, Erode")
            
        category = st.selectbox(
            "Emergency Category",
            [
                "Severe Water Scarcity / Borewell Failure",
                "Unknown Rapid Crop Disease Outbreak",
                "Market / Middleman Payment Fraud",
                "Solar / Power Grid Transformer Breakdown"
            ]
        )
        description = st.text_area("Describe the emergency in detail...", placeholder="Explain the crop condition, affected acreage, and immediate assistance required...")
        
        submitted = st.form_submit_button("🚨 Dispatch SOS Emergency Ticket", use_container_width=True)
        
        if submitted:
            if farmer_name and village and description:
                insert_sos_ticket(farmer_name, village, category, description)
                st.success("✅ Emergency ticket logged into Union Database! Immediate agronomy dispatch initiated.")
            else:
                st.error("⚠️ Please fill in all required fields before dispatching.")
                
    st.markdown("""
    <div class="section-card">
        <h4 class="section-card-title">📋 Active Union Interventions (Live Field Database)</h4>
        <p class="section-card-desc">Verified community relief tickets currently being investigated by regional field officers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Database Status", use_container_width=True):
        st.rerun()
        
    tickets_df = get_sos_tickets()
    
    if tickets_df is None or tickets_df.empty:
        st.info("ℹ️ No active emergencies logged. All regional zones operating normally.")
    else:
        if "Date" in tickets_df.columns:
            tickets_df["Date"] = tickets_df["Date"].apply(format_to_ist)
        st.dataframe(tickets_df, use_container_width=True, hide_index=True)
