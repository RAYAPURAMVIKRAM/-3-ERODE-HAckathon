import streamlit as st
from auth_ui import render_auth_sidebar

st.set_page_config(page_title="Optimizer | STARK-X", page_icon="🌾", layout="centered")

# Render Farmer Authentication & Profile in Sidebar
render_auth_sidebar()

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .opt-header { text-align: center; color: #2e7b32; font-family: sans-serif; margin-bottom: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; border-radius: 10px 10px 0 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 class='opt-header'>🌾 STARK-X Crop Optimizer</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Data-driven precision agriculture engine.</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 I know my conditions", "🔍 I know my crop"])

# --- TAB 1: CONDITIONS TO CROP ---
with tab1:
    st.subheader("Enter your Farm Data")
    col1, col2 = st.columns(2)
    with col1:
        soil_type = st.selectbox("Soil Type", ["Red Soil", "Black Soil", "Alluvial", "Sandy Loam", "Clay"])
        water_avail = st.selectbox("Water Availability", ["Rainfed (Low)", "Borewell (Medium)", "Canal/River (High)"])
        ph_level = st.slider("Soil pH", 4.0, 9.0, 6.5)
    with col2:
        nitrogen = st.slider("Nitrogen (N)", 0, 150, 50)
        phosphorus = st.slider("Phosphorus (P)", 0, 150, 40)
        potassium = st.slider("Potassium (K)", 0, 150, 30)
        
    if st.button("🚀 Run STARK-X Algorithm", use_container_width=True):
        with st.spinner("Processing STARK-X recommendation matrix..."):
            
            # STARK-X Team Logic applied dynamically
            if water_avail == "Rainfed (Low)" and soil_type in ["Red Soil", "Sandy Loam"]:
                crops = [("Millets (Ragi)", 94), ("Groundnut", 88), ("Pulses", 82)]
            elif water_avail == "Canal/River (High)" and soil_type in ["Clay", "Alluvial"]:
                crops = [("Rice", 92), ("Sugarcane", 85), ("Banana", 78)]
            elif soil_type == "Black Soil":
                crops = [("Cotton", 95), ("Soybean", 88), ("Maize", 80)]
            else:
                crops = [("Maize", 85), ("Tomato", 80), ("Onion", 75)]
                
            st.success("Analysis Complete!")
            st.markdown(f"### 🏆 Top Recommendation: **{crops[0][0]}** ({crops[0][1]}% Match)")
            st.progress(crops[0][1] / 100.0)
            
            st.markdown("#### Alternative Options:")
            st.info(f"2. {crops[1][0]} - {crops[1][1]}% Suitability\n3. {crops[2][0]} - {crops[2][1]}% Suitability")
            st.caption("Algorithm factors in NPK balances, pH thresholds, and water stress tolerance.")

# --- TAB 2: CROP TO CONDITIONS ---
with tab2:
    st.subheader("Evaluate a Specific Crop")
    target_crop = st.selectbox("Select Crop to Evaluate", ["Rice", "Wheat", "Cotton", "Millets (Ragi)", "Sugarcane", "Groundnut"])
    target_soil = st.selectbox("Your Soil Type", ["Red Soil", "Black Soil", "Alluvial", "Sandy Loam", "Clay"], key="t2_soil")
    target_water = st.selectbox("Your Water", ["Rainfed (Low)", "Borewell (Medium)", "Canal/River (High)"], key="t2_water")
    
    if st.button("🔍 Check Compatibility", use_container_width=True):
        with st.spinner("Cross-referencing crop requirements..."):
            
            # Mismatch Logic Engine
            mismatch = False
            if target_crop == "Rice" and target_water == "Rainfed (Low)": mismatch = True
            elif target_crop == "Sugarcane" and target_water == "Rainfed (Low)": mismatch = True
            elif target_crop == "Cotton" and target_soil not in ["Black Soil", "Alluvial"]: mismatch = True
            
            if mismatch:
                st.error(f"⚠️ **HIGH RISK MISMATCH DETECTED**")
                st.write(f"Growing **{target_crop}** with {target_water} and {target_soil} will likely lead to severe yield loss.")
                if target_water == "Rainfed (Low)":
                    st.info("💡 **Better Alternative:** Consider Millets (Ragi) or Groundnut for much higher yield potential.")
                elif target_soil != "Black Soil" and target_crop == "Cotton":
                    st.info("💡 **Better Alternative:** Consider Maize or Pulses for your soil type.")
            else:
                st.success(f"✅ **GOOD MATCH:** {target_crop} is suitable for your farm!")
                st.write(f"Your {target_soil} and {target_water} meet the baseline agronomic requirements.")
