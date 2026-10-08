import streamlit as st
from locales import t, TRANSLATIONS
from supabase_client import (
    sign_in_farmer,
    sign_up_farmer,
    quick_demo_login,
    sign_out_farmer,
    get_current_user,
    is_supabase_connected
)

def render_auth_sidebar():
    """Renders language selector, user authentication and profile status in the sidebar."""
    # 0. SYNCHRONIZED APP LANGUAGE SELECTOR
    if "selected_lang" not in st.session_state:
        st.session_state["selected_lang"] = "English"
        
    langs = list(TRANSLATIONS.keys())
    curr_lang = st.session_state.get("selected_lang", "English")
    curr_idx = langs.index(curr_lang) if curr_lang in langs else 0
    
    st.sidebar.markdown("### 🌐 Language / மொழி / భాష")
    chosen = st.sidebar.selectbox(
        "Choose App Language",
        langs,
        index=curr_idx,
        key="app_language_selector",
        label_visibility="collapsed"
    )
    if chosen != st.session_state["selected_lang"]:
        st.session_state["selected_lang"] = chosen
        st.rerun()

    user = get_current_user()
    st.sidebar.markdown("---")
    
    # 1. LOGGED IN STATE
    if user:
        provider_badge = "🟢 Supabase Cloud" if user.get("provider") == "supabase" else "🟡 Local Session"
        st.sidebar.markdown(f"""
        <div style="background-color: #f0fdf4; border: 1px solid #86efac; padding: 12px; border-radius: 12px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🧑‍🌾</span>
                <div>
                    <strong style="color: #166534; font-size: 15px;">{user.get('name', 'Farmer')}</strong><br/>
                    <small style="color: #4b5563;">📍 {user.get('village', 'Tamil Nadu')}</small>
                </div>
            </div>
            <div style="margin-top: 8px; font-size: 11px; color: #15803d; font-weight: 600;">
                {provider_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", key="btn_logout", use_container_width=True):
            sign_out_farmer()
            st.rerun()
            
    # 2. LOGGED OUT STATE
    else:
        status_text = "🟢 Supabase Active" if is_supabase_connected() else "🟡 Local / Demo Mode"
        st.sidebar.markdown(f"**Farmer Portal** <small style='color: #6b7280;'>({status_text})</small>", unsafe_allow_html=True)
        
        # 1-Click Demo Login for Quick Testing / Hackathon
        if st.sidebar.button("⚡ 1-Click Demo Login", key="btn_quick_demo", use_container_width=True):
            quick_demo_login()
            st.sidebar.success("Logged in as Murugan (Erode)!")
            st.rerun()
            
        with st.sidebar.expander("🔑 Sign In / Register", expanded=False):
            auth_tab1, auth_tab2 = st.tabs(["Sign In", "Sign Up"])
            
            with auth_tab1:
                with st.form("sidebar_signin_form"):
                    in_email = st.text_input("Email", key="in_email")
                    in_pass = st.text_input("Password", type="password", key="in_pass")
                    btn_signin = st.form_submit_button("Sign In")
                    if btn_signin:
                        if in_email and in_pass:
                            success, msg = sign_in_farmer(in_email, in_pass)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("Please enter email & password.")
                            
            with auth_tab2:
                with st.form("sidebar_signup_form"):
                    up_name = st.text_input("Farmer Name", key="up_name")
                    up_village = st.text_input("Village / District", key="up_village")
                    up_email = st.text_input("Email", key="up_email")
                    up_pass = st.text_input("Password", type="password", key="up_pass")
                    btn_signup = st.form_submit_button("Register Account")
                    if btn_signup:
                        if up_name and up_village and up_email and up_pass:
                            success, msg = sign_up_farmer(up_email, up_pass, up_name, up_village)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("Please fill in all registration fields.")
