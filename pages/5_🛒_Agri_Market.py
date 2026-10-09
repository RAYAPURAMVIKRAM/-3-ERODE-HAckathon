import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path for Streamlit Cloud
_ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

import re
import urllib.parse
import streamlit as st
from dotenv import load_dotenv
from auth_ui import render_auth_sidebar
from locales import t
from supabase_client import (
    get_current_user,
    fetch_marketplace_crops,
    add_marketplace_crop
)

def format_to_ist(ts_val):
    """Formats timestamp string to Indian Standard Time (IST)."""
    if not ts_val:
        return ""
    ts_str = str(ts_val).strip()
    try:
        if "T" in ts_str or "+" in ts_str or ts_str.endswith("Z"):
            from datetime import datetime, timezone, timedelta
            ist = timezone(timedelta(hours=5, minutes=30))
            cleaned = ts_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(cleaned)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(ist).strftime("%Y-%m-%d %H:%M")
        return ts_str
    except Exception:
        return ts_str

# 1. FORCE LOAD ENV VARIABLES
load_dotenv(override=True)

# 2. PAGE CONFIG
st.set_page_config(
    page_title="Agri Market & Reels | STARK-X",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 3. RENDER AUTHENTICATION SIDEBAR
render_auth_sidebar()

lang = st.session_state.get("lang", "English")

# 4. EXECUTIVE AGRICULTURAL THEME & HIGH-CONTRAST CSS
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
    .market-hero-banner {
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
    .market-hero-banner * {
        color: #ffffff !important;
    }
    .market-hero-left {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    .market-avatar-badge {
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
    .market-hero-title {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
    }
    .market-hero-status {
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
    .market-badge-pill {
        background: rgba(255, 255, 255, 0.18) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px !important;
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
        margin-bottom: 4px !important;
        line-height: 1.5 !important;
    }

    /* Post Harvest Form & Inputs */
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
    div[data-testid="stNumberInput"] input,
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
    div[data-testid="stNumberInput"] input:focus {
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

    /* Marketplace Crop Cards (Pure White Card with Green Left Accent) */
    .market-card {
        background: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-left: 6px solid #059669 !important;
        border-radius: 18px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    .market-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(5, 150, 105, 0.16) !important;
        border-color: #059669 !important;
    }
    .crop-title {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: #064e3b !important;
        margin-bottom: 10px !important;
    }
    .badge-pill {
        display: inline-block !important;
        padding: 6px 12px !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        margin-right: 8px !important;
        margin-bottom: 10px !important;
    }
    .badge-qty {
        background: #dcfce7 !important;
        color: #166534 !important;
        border: 1.5px solid #86efac !important;
    }
    .badge-price {
        background: #fef3c7 !important;
        color: #92400e !important;
        border: 1.5px solid #fcd34d !important;
    }
    .badge-loc {
        background: #e0f2fe !important;
        color: #075985 !important;
        border: 1.5px solid #7dd3fc !important;
    }
    .farmer-info {
        font-size: 14px !important;
        color: #334155 !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
    }
    .wa-button {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        width: 100% !important;
        background-color: #16a34a !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        padding: 13px 20px !important;
        border-radius: 12px !important;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35) !important;
        transition: background-color 0.2s, transform 0.1s !important;
    }
    .wa-button:hover {
        background-color: #15803d !important;
        transform: scale(1.01) !important;
        color: #ffffff !important;
    }

    /* Reels Mobile Vertical Frame & Explicit Contrast Lock */
    .reel-container {
        max-width: 440px !important;
        margin: 0 auto 32px auto !important;
        background: #0f172a !important;
        border: 3px solid #334155 !important;
        border-radius: 24px !important;
        overflow: hidden !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35) !important;
        position: relative !important;
    }
    .reel-video {
        width: 100% !important;
        height: auto !important;
        display: block !important;
        border-radius: 20px 20px 0 0 !important;
    }
    .reel-meta {
        padding: 18px 22px !important;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, #0f172a 100%) !important;
    }
    .reel-container,
    .reel-container *,
    .reel-meta,
    .reel-meta * {
        color: #f8fafc !important;
    }
    .reel-creator {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        font-size: 14.5px !important;
        font-weight: 800 !important;
        color: #4ade80 !important;
        margin-bottom: 8px !important;
    }
    .reel-creator * {
        color: #4ade80 !important;
    }
    .reel-title {
        font-weight: 800 !important;
        font-size: 16px !important;
        margin-bottom: 6px !important;
        color: #ffffff !important;
    }
    .reel-caption {
        font-size: 13.5px !important;
        color: #e2e8f0 !important;
        line-height: 1.5 !important;
        font-weight: 500 !important;
        margin-bottom: 12px !important;
    }
    .reel-actions {
        display: flex !important;
        gap: 16px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
    }
    .reel-actions * {
        color: #94a3b8 !important;
    }

    /* Valuation Box */
    .lot-valuation-card {
        background: #f0fdf4 !important;
        border: 1.5px solid #86efac !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 16px !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        color: #166534 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
</style>
""", unsafe_allow_html=True)

# 5. PAGE HERO BANNER
st.markdown(f"""
<div class="market-hero-banner">
    <div class="market-hero-left">
        <div class="market-avatar-badge">🛒</div>
        <div>
            <h3 class="market-hero-title">{t("market_title", lang)}</h3>
            <p class="market-hero-status"><span class="live-dot"></span> {t("market_sub", lang)}</p>
        </div>
    </div>
    <div class="market-badge-pill">
        🌾 Direct Farmer Trade
    </div>
</div>
""", unsafe_allow_html=True)

# 6. TWO TABS
tab_market, tab_reels = st.tabs([t("market_tab1", lang), t("market_tab2", lang)])

# ================= TAB 1: DIRECT MARKETPLACE =================
with tab_market:
    st.markdown(f"""
    <div class="section-card">
        <h4 class="section-card-title">📝 {t("post_harvest_title", lang)}</h4>
        <p class="section-card-desc">Wholesale buyers, food processing units, and exporters across Erode will contact you directly on WhatsApp.</p>
    </div>
    """, unsafe_allow_html=True)

    # Check for current logged in user to auto-fill
    current_user = get_current_user()
    default_name = current_user.get("name", "") if current_user else ""
    default_loc = current_user.get("village", "Perundurai, Erode") if current_user else "Perundurai, Erode"

    # Form to post new crop harvest
    with st.form("post_harvest_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            farmer_name = st.text_input(t("farmer_name_label", lang), value=default_name, placeholder="e.g. Murugan K.")
            crop_name = st.selectbox(
                t("crop_name_label", lang),
                [
                    "Erode Organic Turmeric (Finger)",
                    "Turmeric (Bulb)",
                    "Sugarcane (CO-86032)",
                    "Cotton (MCU-5)",
                    "Pearl Millet (Kambu / Bajra)",
                    "Finger Millet (Ragi)",
                    "Tapioca / Sago Tubers",
                    "Small Onion (Shallots / Chinna Vengayam)",
                    "Robusta Banana"
                ]
            )
            location = st.text_input(t("location_label", lang), value=default_loc, placeholder="e.g. Perundurai, Erode")

        with col2:
            phone_wa = st.text_input(t("phone_label", lang), placeholder="e.g. +91 98765 43210 or 9876543210")
            quantity_kg = st.number_input(t("qty_label", lang), min_value=10.0, max_value=50000.0, value=250.0, step=25.0)
            price_per_kg = st.number_input(t("price_label", lang), min_value=1.0, max_value=2000.0, value=145.0, step=5.0)

        # Expected lot valuation
        total_lot_val = quantity_kg * price_per_kg
        st.markdown(f"""
        <div class="lot-valuation-card">
            <span>📦 Estimated Total Lot Valuation</span>
            <span style="font-size: 18px; font-weight: 900;">₹{total_lot_val:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button(t("post_btn", lang), use_container_width=True)
        if submitted:
            if not farmer_name.strip():
                st.error("⚠️ Please enter the farmer name.")
            elif not phone_wa.strip() or len(re.sub(r'[^0-9]', '', phone_wa)) < 10:
                st.error("⚠️ Please enter a valid 10-digit WhatsApp phone number.")
            elif not location.strip():
                st.error("⚠️ Please specify your location or village.")
            else:
                success = add_marketplace_crop(
                    farmer=farmer_name.strip(),
                    phone=phone_wa.strip(),
                    crop=crop_name,
                    qty=float(quantity_kg),
                    price=float(price_per_kg),
                    loc=location.strip()
                )
                if success:
                    st.success(f"🎉 **{crop_name}** ({quantity_kg} kg) has been successfully listed in the Marketplace!")
                    st.rerun()
                else:
                    st.error("Could not save listing. Please try again.")

    st.markdown(f"""
    <div class="section-card" style="margin-top: 10px;">
        <h4 class="section-card-title">🌾 {t("active_listings_title", lang)}</h4>
        <p class="section-card-desc">Verified farmer lots ready for immediate procurement. Click the WhatsApp button to chat directly with the farmer.</p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch active crop listings
    crops = fetch_marketplace_crops()

    if not crops:
        st.info("ℹ️ No crop listings yet. Be the first farmer to list your harvest above!")
    else:
        st.markdown(f"Showing **{len(crops)}** verified lots in Kongu Nadu / Erode agricultural belt:")

        for item in crops:
            c_name = item.get("crop_name", "Agricultural Produce")
            f_name = item.get("farmer_name", "Farmer")
            raw_phone = item.get("phone_whatsapp", "")
            qty = float(item.get("quantity_kg", 0.0))
            price = float(item.get("price_per_kg", 0.0))
            loc = item.get("location", "Erode")
            date_str = format_to_ist(item.get("created_at", ""))
            total_price = qty * price

            # Clean phone for WhatsApp URL
            clean_digits = re.sub(r'[^0-9]', '', str(raw_phone))
            if len(clean_digits) == 10:
                clean_phone = "91" + clean_digits
            elif len(clean_digits) > 10:
                clean_phone = clean_digits
            else:
                clean_phone = "919876543210"

            # Pre-filled WhatsApp Inquiry Message
            msg_text = (
                f"Vanakkam {f_name}! I saw your listing for {c_name} ({qty:,.0f} kg @ Rs.{price:,.0f}/kg) "
                f"on STARK-X Direct Market in {loc}. Is this lot available for immediate purchase?"
            )
            encoded_msg = urllib.parse.quote(msg_text)
            wa_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"

            # Render HTML Card
            st.markdown(f"""
            <div class="market-card">
                <div class="crop-title">🌿 {c_name}</div>
                <div style="margin-bottom: 8px;">
                    <span class="badge-pill badge-qty">⚖️ {qty:,.0f} kg Available</span>
                    <span class="badge-pill badge-price">💰 ₹{price:,.2f} / kg</span>
                    <span class="badge-pill badge-loc">📍 {loc}</span>
                </div>
                <div class="farmer-info">
                    👤 <b>Farmer:</b> {f_name} &nbsp;•&nbsp; 📦 <b>Lot Total:</b> ₹{total_price:,.2f}
                    {f" &nbsp;•&nbsp; 🕒 {date_str}" if date_str else ""}
                </div>
                <a href="{wa_link}" target="_blank" class="wa-button">
                    {t("wa_btn", lang)}
                </a>
            </div>
            """, unsafe_allow_html=True)


# ================= TAB 2: AGRI REELS =================
with tab_reels:
    st.markdown("""
    <div class="section-card">
        <h4 class="section-card-title">📱 Agri Reels • Fast Mobile Agronomy Tips</h4>
        <p class="section-card-desc">Scroll through high-impact agronomy techniques, TNAU research hacks, and organic methods.</p>
    </div>
    """, unsafe_allow_html=True)

    reels_data = [
        {
            "title": "Turmeric Seed Rhizome Dip with Trichoderma",
            "creator": "@erode_krishi_vigyan",
            "caption": "Prevent Rhizome Rot (Pythium) before planting! Dip seed rhizomes in Trichoderma viride solution (4g/kg) for 30 minutes to shield root zones.",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            "likes": "14.2k",
            "comments": "384"
        },
        {
            "title": "Sugarcane Drip Fertigation & Earthing Up",
            "creator": "@bhavani_sugarcane_lab",
            "caption": "Earthing up CO-86032 cane at 90 days. Boosts tiller strength, saves 40% water, and ensures zero lodging during North-East monsoons.",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
            "likes": "9.8k",
            "comments": "216"
        },
        {
            "title": "Panchagavya + Neem Oil Foliar Spray Hacks",
            "creator": "@tamil_organic_farmer",
            "caption": "Natural immunity booster against leaf spot and whiteflies! Spray 3% Panchagavya with 5ml/L neem oil early morning for 100% organic pest repel.",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
            "likes": "22.5k",
            "comments": "649"
        }
    ]

    for reel in reels_data:
        st.markdown(f"""
        <div class="reel-container">
            <video class="reel-video" autoplay loop muted playsinline controls>
                <source src="{reel['video_url']}" type="video/mp4">
                Your browser does not support HTML5 video.
            </video>
            <div class="reel-meta">
                <div class="reel-creator">
                    🌱 <b>{reel['creator']}</b>
                    <span style="background: rgba(74, 222, 128, 0.2); padding: 3px 8px; border-radius: 12px; font-size: 11px; border: 1px solid rgba(74, 222, 128, 0.4);">✓ Verified Expert</span>
                </div>
                <div class="reel-title">
                    {reel['title']}
                </div>
                <div class="reel-caption">
                    {reel['caption']}
                </div>
                <div class="reel-actions">
                    <span>❤️ {reel['likes']}</span>
                    <span>💬 {reel['comments']}</span>
                    <span>↗️ WhatsApp Share</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
