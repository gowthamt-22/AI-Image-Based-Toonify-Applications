import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend

# Page config
st.set_page_config(
    page_title="Profile - Toonify",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize backend
backend = Backend()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access your profile")
    if st.button("Go to Login"):
        st.switch_page("pages/login.py")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .navbar {
        background: white;
        padding: 1.5rem 3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: -3rem -4rem 3rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .navbar-brand {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        cursor: pointer;
    }
    
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .profile-avatar {
        width: 120px;
        height: 120px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        margin: 0 auto 1rem auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .profile-name {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .profile-email {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .info-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .info-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    .info-row {
        display: flex;
        padding: 1rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .info-label {
        flex: 1;
        font-weight: 600;
        color: #6b7280;
    }
    
    .info-value {
        flex: 2;
        color: #111827;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
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
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .navbar {
        animation: slideIn 0.5s ease-out;
    }
    
    .profile-header {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .profile-avatar {
        animation: scaleIn 0.7s ease-out;
        transition: transform 0.3s ease;
    }
    
    .profile-avatar:hover {
        transform: scale(1.1) rotate(5deg);
    }
    
    .info-section {
        animation: fadeInUp 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .info-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stButton>button {
        animation: fadeIn 0.9s ease-out;
        transition: all 0.3s ease;
    }
    
    .stAlert {
        animation: fadeIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    if st.button("🎨 Toonify Studio", key="studio_nav"):
        st.switch_page("pages/toonify_studio.py")
with col2:
    if st.button("🏠 Dashboard", key="home_nav"):
        st.switch_page("pages/dashboard.py")
with col3:
    if st.button("👤 Profile", key="profile_nav"):
        st.rerun()
with col4:
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.switch_page("landing.py")

# Profile Header
user = st.session_state.user_data
st.markdown(f"""
<div class="profile-header">
    <div class="profile-avatar">👤</div>
    <div class="profile-name">{user['username']}</div>
    <div class="profile-email">{user['email']}</div>
</div>
""", unsafe_allow_html=True)

# Profile Information
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-section">
        <div class="info-title">📧 Contact Information</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    if user.get('mobile_no'):
        st.write(f"**Mobile:** {user['mobile_no']}")

with col2:
    st.markdown("""
    <div class="info-section">
        <div class="info-title">👤 Personal Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    if user.get('full_name'):
        st.write(f"**Full Name:** {user['full_name']}")
    if user.get('age'):
        st.write(f"**Age:** {user['age']}")
    if user.get('gender'):
        st.write(f"**Gender:** {user['gender']}")

st.markdown("<br>", unsafe_allow_html=True)

# Location Information
st.markdown("""
<div class="info-section">
    <div class="info-title">📍 Location</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if user.get('city'):
        st.write(f"**City:** {user['city']}")
with col2:
    if user.get('location'):
        st.write(f"**State/Region:** {user['location']}")
with col3:
    st.write(f"**Account Type:** {user.get('account_type', 'user').title()}")

st.markdown("<br><br>", unsafe_allow_html=True)

# Action Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✏️ Edit Profile", use_container_width=True):
        st.info("Edit profile feature coming soon!")
with col2:
    if st.button("🔒 Change Password", use_container_width=True):
        st.info("Change password feature coming soon!")
with col3:
    if st.button("🗑️ Delete Account", use_container_width=True):
        st.warning("Account deletion requires confirmation")
