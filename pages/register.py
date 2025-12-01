import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import Backend

st.set_page_config(
    page_title="Register - Toonify",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

backend = Backend()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    [data-testid="stSidebar"], [data-testid="stHeader"] {
        display: none;
    }
    
    .main {
        background: #000;
    }
    
    .block-container {
        padding: 3rem !important;
    }
    
    .stTextInput>div>div>input {
        background: #1a1a1a !important;
        border: 2px solid #333 !important;
        border-radius: 16px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        color: #fff !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00fff0 !important;
        box-shadow: 0 0 30px rgba(0, 255, 240, 0.3) !important;
    }
    
    .stTextInput label {
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00fff0, #a855f7, #ff006e) !important;
        color: #000 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        padding: 1rem 2rem !important;
        border-radius: 16px !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 10px 40px rgba(0, 255, 240, 0.4) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 50px rgba(0, 255, 240, 0.6) !important;
    }
    
    .register-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #00fff0 0%, #a855f7 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .register-subtitle {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="register-title">REGISTER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="register-subtitle">Create your Toonify account</p>', unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.switch_page("landing.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="Choose a username")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    if st.button("CREATE ACCOUNT"):
        if username and email and password and confirm_password:
            if password == confirm_password:
                success, message, user_id = backend.register_user(username, email, password)
                if success:
                    st.success("✅ " + message + " Please login.")
                    st.balloons()
                    if st.button("Go to Login"):
                        st.switch_page("pages/login.py")
                else:
                    st.error("❌ " + message)
            else:
                st.error("❌ Passwords don't match")
        else:
            st.warning("⚠️ Please fill in all fields")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Already have an account? Login"):
        st.switch_page("pages/login.py")
