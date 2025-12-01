import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import Backend

st.set_page_config(
    page_title="Login - Toonify",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

backend = Backend()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

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
    
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
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
    
    .login-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #00fff0 0%, #a855f7 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .login-subtitle {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="login-title">LOGIN</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">Welcome back to Toonify!</p>', unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.switch_page("landing.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("LOGIN NOW"):
        if email and password:
            success, message, user_data = backend.login_user(email, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_data = user_data
                st.success("✅ " + message)
                st.switch_page("pages/dashboard.py")
            else:
                st.error("❌ " + message)
        else:
            st.warning("⚠️ Please fill in all fields")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Don't have an account? Register"):
        st.switch_page("pages/register.py")
