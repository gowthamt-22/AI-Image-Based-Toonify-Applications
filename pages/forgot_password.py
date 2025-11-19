import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend

# Page config
st.set_page_config(
    page_title="Forgot Password - Toonify",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize backend
backend = Backend()

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .main .block-container {
        padding: 3rem 1rem;
    }
    
    .forgot-card {
        background: white;
        max-width: 500px;
        margin: 0 auto;
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.25);
    }
    
    .forgot-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .forgot-subheader {
        text-align: center;
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }
    
    .stTextInput label {
        font-weight: 600;
        color: #374151;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1.5px solid #e5e7eb;
        padding: 0.85rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
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
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }
    
    /* Smooth animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .forgot-card {
        animation: scaleIn 0.5s ease-out;
    }
    
    .forgot-header {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .forgot-subheader {
        animation: fadeIn 0.7s ease-out;
    }
    
    .stTextInput {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .stButton>button {
        animation: fadeIn 0.9s ease-out;
    }
    
    .stAlert {
        animation: shake 0.5s ease-in-out, fadeIn 0.3s ease-out !important;
    }
</style>
""", unsafe_allow_html=True)

# Forgot Password Form
st.markdown('<div class="forgot-card">', unsafe_allow_html=True)
st.markdown('<div class="forgot-header">🔒 Reset Password</div>', unsafe_allow_html=True)
st.markdown('<div class="forgot-subheader">Enter your email to receive password reset instructions</div>', unsafe_allow_html=True)

with st.form("forgot_password_form"):
    email = st.text_input("Email Address", placeholder="name@example.com")
    
    submit = st.form_submit_button("Send Reset Link")
    
    if submit:
        if not email:
            st.error("❌ Please enter your email address")
        else:
            # Show loading spinner
            with st.spinner("🔄 Checking email..."):
                # Check if email exists
                user = backend.db.get_user_by_email(email)
            
            if user:
                st.success(f"✅ Password reset link sent to {email}")
                st.info("📧 (Demo mode: In production, an email would be sent)")
            else:
                st.error("❌ Email address not found in our system")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("← Back to Login", use_container_width=True):
        st.switch_page("pages/login.py")
with col2:
    if st.button("Create Account", use_container_width=True):
        st.switch_page("pages/register.py")

st.markdown('</div>', unsafe_allow_html=True)
