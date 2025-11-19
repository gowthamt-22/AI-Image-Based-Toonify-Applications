import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend

# Page config
st.set_page_config(
    page_title="Login - Toonify",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize backend
backend = Backend()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    [data-testid="column"] {
        padding: 0 !important;
    }
    
    .main .block-container {
        max-width: 100%;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .login-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        min-height: 100vh;
        gap: 0;
    }
    
    .left-section {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 4rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .left-section::before {
        content: '';
        position: absolute;
        width: 500px;
        height: 500px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        top: -200px;
        right: -200px;
    }
    
    .left-section::after {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        bottom: -100px;
        left: -100px;
    }
    
    .content-wrapper {
        position: relative;
        z-index: 1;
    }
    
    .brand-logo {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .brand-tagline {
        font-size: 1.5rem;
        font-weight: 300;
        opacity: 0.95;
        text-align: center;
        max-width: 500px;
        line-height: 1.6;
        margin-bottom: 3rem;
    }
    
    .feature-list {
        text-align: left;
        max-width: 400px;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        font-size: 1.1rem;
    }
    
    .feature-icon {
        width: 50px;
        height: 50px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1.5rem;
        font-size: 1.5rem;
    }
    
    .right-section {
        background: #ffffff;
        padding: 4rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .form-container {
        max-width: 450px;
        margin: 0 auto;
        width: 100%;
    }
    
    .login-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .login-subheader {
        color: #6b7280;
        font-size: 1.05rem;
        margin-bottom: 2.5rem;
    }
    
    .stTextInput label {
        font-weight: 600;
        color: #374151;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1.5px solid #e5e7eb;
        padding: 0.85rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
        background: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 0.9rem;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        margin-top: 1.5rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }
    
    .divider-text {
        text-align: center;
        color: #9ca3af;
        font-size: 0.9rem;
        margin: 2rem 0;
        position: relative;
    }
    
    .divider-text::before,
    .divider-text::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 42%;
        height: 1px;
        background: #e5e7eb;
    }
    
    .divider-text::before { left: 0; }
    .divider-text::after { right: 0; }
    
    .secondary-btn {
        background: #f9fafb !important;
        color: #374151 !important;
        border: 1.5px solid #e5e7eb !important;
        font-weight: 500 !important;
    }
    
    .secondary-btn:hover {
        background: #f3f4f6 !important;
        border-color: #d1d5db !important;
    }
    
    /* Error and success message animations */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stAlert {
        animation: shake 0.5s ease-in-out, fadeIn 0.3s ease-out !important;
        border-radius: 8px !important;
    }
    
    .element-container {
        animation: slideIn 0.4s ease-out;
    }
    
    /* Loading spinner */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #6366f1;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
</style>
""", unsafe_allow_html=True)

# Check if already logged in
if st.session_state.authenticated:
    st.success(f"Welcome back, {st.session_state.user_data['username']}!")
    st.info("You are already logged in.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Dashboard"):
            st.switch_page("pages/dashboard.py")
    with col2:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()
    st.stop()

# Login Page Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="left-section">
        <div class="content-wrapper">
            <div class="brand-logo">🎨 Toonify</div>
            <div class="brand-tagline">Transform your images into stunning cartoons with AI-powered effects</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="right-section">', unsafe_allow_html=True)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="login-header">Welcome back</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subheader">Enter your credentials to access your account</div>', unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="name@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        remember_me = st.checkbox("Remember me for 30 days")
        
        submit = st.form_submit_button("Sign in")
        
        if submit:
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                # Show loading spinner
                with st.spinner("🔐 Authenticating..."):
                    success, message, user_data = backend.login_user(email, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.remember_me = remember_me
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.switch_page("pages/toonify_studio.py")
                else:
                    st.error(f"❌ {message}")
    
    # Forgot password link
    col_left, col_right = st.columns([1, 1])
    with col_right:
        if st.button("Forgot password?", use_container_width=True, key="forgot_pass"):
            st.switch_page("pages/forgot_password.py")
    
    st.markdown('<div class="divider-text">OR</div>', unsafe_allow_html=True)
    
    if st.button("Create new account", use_container_width=True, key="register"):
        st.switch_page("pages/register.py")
    
    if st.button("← Back to home", use_container_width=True, key="home"):
        st.switch_page("landing.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
