import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend

# Page config
st.set_page_config(
    page_title="Register - Toonify",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize backend
backend = Backend()

# Custom CSS
st.markdown("""
<style>
    .register-header {
        text-align: center;
        color: #4CAF50;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .register-subheader {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
    }
    .password-requirements {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf0 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 0.9rem;
        border-left: 4px solid #4CAF50;
    }
    .section-divider {
        background-color: #4CAF50;
        height: 2px;
        margin: 1.5rem 0;
        border-radius: 2px;
    }
    .form-section {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .section-title {
        color: #4CAF50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
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
        border-top: 3px solid #4CAF50;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
</style>
""", unsafe_allow_html=True)

# Registration Form
st.markdown('<div class="register-header">🎨 Create Account</div>', unsafe_allow_html=True)
st.markdown('<div class="register-subheader">Join Toonify and start transforming your images!</div>', unsafe_allow_html=True)

with st.form("register_form", clear_on_submit=False):
    # Account Information Section
    st.markdown('<div class="section-title">📝 Account Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username*", placeholder="Choose a username", help="3-20 characters, letters, numbers, and underscores")
    with col2:
        email = st.text_input("Email*", placeholder="Enter your email", help="Valid email address required")
    
    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input("Password*", type="password", placeholder="Create a password", help="Follow requirements below")
    with col2:
        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Re-enter your password")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Personal Information Section
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
    with col2:
        age = st.number_input("Age", min_value=13, max_value=120, value=None, placeholder="Enter your age")
    
    col1, col2 = st.columns(2)
    with col1:
        mobile_no = st.text_input("Mobile Number", placeholder="10-digit mobile number", max_chars=10)
    with col2:
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other", "Prefer not to say"])
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", placeholder="Enter your city")
    with col2:
        location = st.text_input("Location/State", placeholder="Enter your state/location")
    
    # Password Requirements
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="password-requirements">
        <strong>🔒 Password Requirements:</strong><br>
        ✓ At least 8 characters long<br>
        ✓ One uppercase letter (A-Z)<br>
        ✓ One lowercase letter (a-z)<br>
        ✓ One digit (0-9)<br>
        ✓ One special character (!@#$%^&*)
    </div>
    """, unsafe_allow_html=True)
    
    submit = st.form_submit_button("✨ Create Account", use_container_width=True)
    
    if submit:
        if not username or not email or not password or not confirm_password:
            st.error("❌ Please fill in all required fields (marked with *)")
        elif password != confirm_password:
            st.error("❌ Passwords do not match")
        else:
            # Show loading spinner
            with st.spinner("🔄 Creating your account..."):
                # Prepare optional fields
                gender_val = None if gender == "Select" else gender
                age_val = None if age == 0 else age
                
                success, message, user_id = backend.register_user(
                    username, email, password, full_name, 
                    age_val, mobile_no, gender_val, location, city
                )
            
            if success:
                st.success(f"✅ {message}")
                st.info("🎉 Please login with your credentials")
                st.balloons()
            else:
                st.error(f"❌ {message}")

st.markdown("---")

# Login Link
col1, col2 = st.columns(2)
with col1:
    if st.button("Already have an account? Login", use_container_width=True):
        st.switch_page("pages/login.py")
with col2:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("landing.py")
