import streamlit as st
import pandas as pd
from auth_ui import render_auth_sidebar
from supabase_client import (
    get_current_user,
    insert_sos_ticket,
    get_sos_tickets,
    is_supabase_connected
)

st.set_page_config(page_title="Market & SOS | STARK-X", page_icon="📈", layout="centered")

# Render Farmer Authentication & Profile in Sidebar
render_auth_sidebar()

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .sos-header { text-align: center; color: #d32f2f; font-family: sans-serif; }
    .fin-header { text-align: center; color: #1976d2; font-family: sans-serif; }
    .db-badge { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# Database connectivity badge
db_status = "🟢 Supabase Cloud Database Connected" if is_supabase_connected() else "🟡 Local Database Active (Supabase Ready)"
st.caption(f"Backend Status: {db_status}")

# --- UI TABS ---
tab1, tab2 = st.tabs(["📈 Live Market (FinTech)", "🚨 SOS Helpdesk"])

# --- TAB 1: MARKET PRICES & FINTECH ---
with tab1:
    st.markdown("<h3 class='fin-header'>Live Mandi Prices (Erode/TN Region)</h3>", unsafe_allow_html=True)
    
    # Simulated Live Data
    market_data = {
        "Crop": ["Turmeric (Bulb)", "Rice (Paddy - Grade A)", "Cotton (Long Staple)", "Millets (Ragi)", "Groundnut"],
        "Current Price (₹/Quintal)": ["₹12,450", "₹2,203", "₹7,100", "₹3,500", "₹6,400"],
        "Trend": ["⬆️ High Demand", "➡️ Stable", "⬇️ Dropping", "⬆️ Rising", "➡️ Stable"]
    }
    df = pd.DataFrame(market_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### 💰 STARK-X Financial Advisor")
    st.write("Get AI-driven strategies on when to hold or sell your harvest based on predictive market trends.")
    
    if st.button("Generate Financial Strategy", use_container_width=True):
        with st.spinner("Analyzing market trends..."):
            st.success("Strategy Generated!")
            st.info(
                "**Turmeric Outlook:** Erode markets are showing a 12% week-over-week price surge due to export demands. "
                "**Recommendation:** Hold current stock for another 14 days for peak pricing. \n\n"
                "**Millets / Ragi:** Subsidies for drought-resistant crops are driving up local MSP (Minimum Support Price). "
                "**Recommendation:** Sell 50% now to cover operational costs, hold 50% for direct-to-consumer premium sales."
            )

# --- TAB 2: SOS HELPDESK ---
with tab2:
    st.markdown("<h3 class='sos-header'>🚨 Community SOS Helpdesk</h3>", unsafe_allow_html=True)
    st.write("Report critical farm failures, severe water shortages, or market fraud. STARK-X automatically alerts the Student Agricultural Union for physical intervention.")
    
    # Pre-fill name and village if logged in
    user = get_current_user() or {}
    default_name = user.get("name", "")
    default_village = user.get("village", "")
    
    with st.form("sos_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            farmer_name = st.text_input("Farmer Name", value=default_name)
        with col2:
            village = st.text_input("Village / District", value=default_village)
            
        category = st.selectbox("Issue Category", ["Severe Water Scarcity", "Unknown Crop Disease Outbreak", "Market/Middleman Fraud", "Equipment Failure"])
        description = st.text_area("Describe the emergency...")
        
        submitted = st.form_submit_button("🚨 Submit SOS Ticket")
        
        if submitted:
            if farmer_name and village and description:
                insert_sos_ticket(farmer_name, village, category, description)
                st.success("Ticket logged successfully! The Student Union has been alerted.")
            else:
                st.error("Please fill in all fields.")
                
    st.markdown("---")
    st.subheader("📋 Active Union Interventions (Live Database)")
    if st.button("🔄 Refresh Database"):
        st.rerun()
        
    tickets_df = get_sos_tickets()
    
    if tickets_df is None or tickets_df.empty:
        st.write("No active SOS tickets.")
    else:
        st.dataframe(tickets_df, use_container_width=True, hide_index=True)
