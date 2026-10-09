import os
import re
import urllib.parse
import streamlit as st
from dotenv import load_dotenv
from auth_ui import render_auth_sidebar
from supabase_client import (
    get_current_user,
    fetch_marketplace_crops,
    add_marketplace_crop
)

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

# 4. CUSTOM CSS FOR MOBILE-FIRST CARDS & REELS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Marketplace Card Styling */
    .market-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .market-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(46, 123, 50, 0.15);
        border-color: #2e7b32;
    }
    .crop-title {
        font-size: 20px;
        font-weight: 800;
        color: #1b4332;
        margin-bottom: 6px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 8px;
    }
    .badge-qty {
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
    }
    .badge-price {
        background: #fff8e1;
        color: #f57f17;
        border: 1px solid #ffe082;
    }
    .badge-loc {
        background: #e0f2fe;
        color: #0369a1;
        border: 1px solid #bae6fd;
    }
    .farmer-info {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 14px;
    }
    .wa-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        background-color: #25D366;
        color: #ffffff !important;
        font-size: 15px;
        font-weight: 700;
        padding: 12px 18px;
        border-radius: 10px;
        text-decoration: none;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.35);
        transition: background-color 0.2s, transform 0.1s;
    }
    .wa-button:hover {
        background-color: #1ebe5d;
        transform: scale(1.01);
    }

    /* Reels Mobile Vertical Video Frame */
    .reel-container {
        max-width: 420px;
        margin: 0 auto 32px auto;
        background: #0f172a;
        border: 2px solid #334155;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        position: relative;
    }
    .reel-video {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 22px;
    }
    .reel-meta {
        padding: 16px 20px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.8) 0%, #0f172a 100%);
        color: #f8fafc;
    }
    .reel-creator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 700;
        color: #4ade80;
        margin-bottom: 6px;
    }
    .reel-caption {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    .reel-actions {
        display: flex;
        gap: 16px;
        font-size: 13px;
        font-weight: 600;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

from locales import t

lang = st.session_state.get("lang", "English")

# 5. PAGE HEADER
st.title(t("market_title", lang))
st.markdown(t("market_sub", lang))

# 6. TWO TABS
tab_market, tab_reels = st.tabs([t("market_tab1", lang), t("market_tab2", lang)])

# ================= TAB 1: DIRECT MARKETPLACE =================
with tab_market:
    st.subheader(t("post_harvest_title", lang))
    st.caption("Wholesale buyers, food processing units, and exporters across Erode will contact you directly on WhatsApp.")

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
        st.markdown(f"**Estimated Total Lot Value:** `₹{total_lot_val:,.2f}`")

        submitted = st.form_submit_button(t("post_btn", lang), use_container_width=True)
        if submitted:
            if not farmer_name.strip():
                st.error("Please enter the farmer name.")
            elif not phone_wa.strip() or len(re.sub(r'[^0-9]', '', phone_wa)) < 10:
                st.error("Please enter a valid 10-digit WhatsApp phone number.")
            elif not location.strip():
                st.error("Please specify your location or village.")
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

    st.markdown("---")
    st.subheader(t("active_listings_title", lang))

    # Fetch active crop listings
    crops = fetch_marketplace_crops()

    if not crops:
        st.info("No crop listings yet. Be the first farmer to list your harvest above!")
    else:
        st.markdown(f"Showing **{len(crops)}** verified lots in Kongu Nadu / Erode agricultural belt:")

        for item in crops:
            c_name = item.get("crop_name", "Agricultural Produce")
            f_name = item.get("farmer_name", "Farmer")
            raw_phone = item.get("phone_whatsapp", "")
            qty = float(item.get("quantity_kg", 0.0))
            price = float(item.get("price_per_kg", 0.0))
            loc = item.get("location", "Erode")
            date_str = item.get("created_at", "")
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
    st.subheader("📱 Agri Reels • Fast Mobile Agronomy Tips")
    st.caption("Scroll through high-impact agronomy techniques, TNAU research hacks, and organic methods.")

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
                    <span style="background: rgba(74, 222, 128, 0.2); padding: 2px 8px; border-radius: 12px; font-size: 11px;">Verified Expert</span>
                </div>
                <div style="font-weight: 700; font-size: 15px; margin-bottom: 4px; color: #ffffff;">
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
