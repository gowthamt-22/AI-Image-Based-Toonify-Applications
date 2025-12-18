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

# Premium Modern Design - Matching Landing Page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Vibrant Animated Gradient Background - Same as Landing */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe, #00f2fe);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #ffd700, #ffed4e, #fff44f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 2rem;
        letter-spacing: -1px;
        filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8));
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 3rem;
        justify-content: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1rem 2.5rem;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.25);
        color: #ffd700;
        border-bottom: none;
    }
    
    /* Input Fields */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 1rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.3) !important;
        background: rgba(255, 255, 255, 0.3) !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stTextInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        width: 100% !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5) !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #ff5252, #ff7043) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.7) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Hide Streamlit branding and sidebar */
    #MainMenu, footer, header {visibility: hidden !important;}
    [data-testid="stSidebar"], section[data-testid="stSidebar"], .css-1d391kg {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header with premium styling
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <h1>🎨 TOONIFY</h1>
    <p style='color: #94a3b8; font-size: 1.3rem; margin-top: -1rem;'>Join thousands of creators transforming their images</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("⬅ Back to Home", use_container_width=True, key="back_home"):
        st.switch_page("landing.py")

st.markdown("<br>", unsafe_allow_html=True)

# Tabs for Login/Register
tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])

# LOGIN TAB
with tab1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        login_email = st.text_input("📧 Email", key="login_email", placeholder="your.email@example.com")
        login_password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 LOGIN", key="login_btn"):
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        reg_username = st.text_input("👤 Username", key="reg_username", placeholder="Choose a username")
        reg_email = st.text_input("📧 Email", key="reg_email", placeholder="your.email@example.com")
        reg_password = st.text_input("🔒 Password", type="password", key="reg_password", placeholder="Create a strong password")
        reg_confirm = st.text_input("🔐 Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ CREATE ACCOUNT", key="register_btn"):
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

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Enhanced showcase section
st.markdown("""
<div style='text-align: center; margin: 3rem 0 2rem 0;'>
    <h3 style='color: #cbd5e1; font-size: 1.5rem; font-weight: 700;'>✨ Transform Any Photo into Art</h3>
    <p style='color: #64748b; font-size: 1.05rem; margin-top: 0.5rem;'>Join thousands creating stunning cartoons</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")
images = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=250&h=250&fit=crop",
    "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=250&h=250&fit=crop",
    "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=250&h=250&fit=crop",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=250&h=250&fit=crop"
]

for col, img in zip([col1, col2, col3, col4], images):
    with col:
        st.markdown(f"""
        <div style='border-radius: 16px; overflow: hidden; border: 2px solid rgba(99, 102, 241, 0.3); transition: all 0.3s ease;'>
            <img src='{img}' style='width: 100%; display: block;'>
        </div>
        """, unsafe_allow_html=True)

# If authenticated, redirect to toonify studio
if st.session_state.authenticated:
    st.switch_page("pages/toonify_studio.py")
