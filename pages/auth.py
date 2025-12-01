import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import Backend

st.set_page_config(
    page_title="Login / Register - Toonify",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

backend = Backend()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Simple dark theme
st.markdown("""
<style>
    .stApp {
        background: #000;
    }
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #00fff0, #a855f7, #ff006e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1rem 2rem;
    }
    .stTabs [aria-selected="true"] {
        color: #00fff0;
        border-bottom: 3px solid #00fff0;
    }
    .stTextInput input {
        background: #1a1a1a !important;
        border: 2px solid #333 !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 0.8rem !important;
        font-size: 1.1rem !important;
    }
    .stTextInput input:focus {
        border-color: #00fff0 !important;
        box-shadow: 0 0 20px rgba(0, 255, 240, 0.3) !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00fff0, #a855f7) !important;
        color: #000 !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        border-radius: 12px !important;
        width: 100% !important;
        border: none !important;
    }
    .stButton button:hover {
        box-shadow: 0 10px 40px rgba(0, 255, 240, 0.5) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🎨 TOONIFY")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("landing.py")

st.markdown("<br>", unsafe_allow_html=True)

# Example images showcase
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 1rem;'>✨ Transform Any Photo into Art</p>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=200&fit=crop", use_container_width=True)
with col2:
    st.image("https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=200&h=200&fit=crop", use_container_width=True)
with col3:
    st.image("https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=200&h=200&fit=crop", use_container_width=True)
with col4:
    st.image("https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200&h=200&fit=crop", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs for Login/Register
tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])

# LOGIN TAB
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    login_email = st.text_input("Email", key="login_email", placeholder="your.email@example.com")
    login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("LOGIN", key="login_btn"):
        if login_email and login_password:
            with st.spinner("Logging in..."):
                success, message, user_data = backend.login_user(login_email, login_password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.success("✅ Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        else:
            st.warning("⚠️ Please enter email and password")

# REGISTER TAB
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    reg_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
    reg_email = st.text_input("Email", key="reg_email", placeholder="your.email@example.com")
    reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a strong password")
    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("CREATE ACCOUNT", key="register_btn"):
        if reg_username and reg_email and reg_password and reg_confirm:
            if reg_password == reg_confirm:
                with st.spinner("Creating account..."):
                    success, message, user_id = backend.register_user(reg_username, reg_email, reg_password)
                    if success:
                        st.success("✅ Registration successful! Please login.")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
            else:
                st.error("❌ Passwords don't match")
        else:
            st.warning("⚠️ Please fill in all fields")

# If authenticated, redirect to toonify studio
if st.session_state.authenticated:
    st.switch_page("pages/toonify_studio.py")
