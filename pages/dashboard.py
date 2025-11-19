import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page config
st.set_page_config(
    page_title="Dashboard - Toonify",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access the dashboard")
    if st.button("Go to Login"):
        st.switch_page("pages/login.py")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main .block-container {
        padding: 3rem 4rem !important;
    }
    
    .navbar {
        background: white;
        padding: 1.5rem 3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: -3rem -4rem 2rem -4rem;
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
    }
    
    .navbar-user {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .user-name {
        font-weight: 600;
        color: #374151;
    }
    
    .logout-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        cursor: pointer;
    }
    
    .dashboard-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subheader {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .welcome-text {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    .info-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .info-card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .info-item {
        margin: 0.8rem 0;
        font-size: 1rem;
        color: #333;
    }
    
    .info-label {
        font-weight: 600;
        color: #555;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Smooth animations and transitions */
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
    
    .welcome-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .info-card {
        animation: fadeInUp 0.7s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15) !important;
    }
    
    .feature-box {
        animation: fadeInUp 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-10px) scale(1.02);
    }
    
    .navbar {
        animation: slideIn 0.5s ease-out;
    }
    
    .stAlert {
        animation: fadeIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access the dashboard")
    if st.button("Go to Login"):
        st.switch_page("pages/login.py")
    st.stop()

# Top Navigation Bar
st.markdown(f"""
<div class="navbar">
    <div class="navbar-brand">🎨 Toonify</div>
    <div class="navbar-user">
        <span class="user-name">👤 {st.session_state.user_data['username']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🎨 Toonify Studio", use_container_width=True, key="studio_btn"):
        st.switch_page("pages/toonify_studio.py")
with col2:
    if st.button("👤 View Profile", use_container_width=True, key="profile_btn"):
        st.switch_page("pages/profile.py")
with col3:
    if st.button("🏠 Dashboard", use_container_width=True, key="dashboard_btn"):
        st.rerun()
with col4:
    if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.success("Logged out successfully!")
        st.switch_page("landing.py")

st.markdown("<br>", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="dashboard-header">🎨 Toonify Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subheader">Your Creative Workspace</div>', unsafe_allow_html=True)

# User Welcome Card
st.markdown(f"""
<div class="welcome-card">
    <div class="welcome-title">Hello, {st.session_state.user_data['username']}! 👋</div>
    <div class="welcome-text">Welcome to Toonify! Click 'Toonify Studio' above to start transforming your images!</div>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Launch Toonify Studio", use_container_width=False, key="launch_studio"):
    st.switch_page("pages/toonify_studio.py")

# Feature Placeholder
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🖼️</div>
        <div class="feature-title">Cartoon Effect</div>
        <p style="font-size: 0.95rem; opacity: 0.9;">Edge Detection<br>Bilateral Filtering<br>Color Quantization</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="feature-icon">✏️</div>
        <div class="feature-title">Sketch Effect</div>
        <p style="font-size: 0.95rem; opacity: 0.9;">Grayscale Conversion<br>Edge Enhancement<br>Pencil Drawing Style</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Custom Filters</div>
        <p style="font-size: 0.95rem; opacity: 0.9;">Stylization<br>Color Adjustments<br>Custom Effects</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Account Information
st.markdown('<div class="dashboard-subheader" style="margin-top: 2rem;">📊 Your Profile</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">📧 Contact Details</div>
        <div class="info-item"><span class="info-label">Username:</span> {}</div>
        <div class="info-item"><span class="info-label">Email:</span> {}</div>
        {}
    </div>
    """.format(
        st.session_state.user_data['username'],
        st.session_state.user_data['email'],
        f'<div class="info-item"><span class="info-label">Mobile:</span> {st.session_state.user_data["mobile_no"]}</div>' if st.session_state.user_data.get('mobile_no') else ''
    ), unsafe_allow_html=True)

with col2:
    personal_info = []
    if st.session_state.user_data.get('full_name'):
        personal_info.append(f'<div class="info-item"><span class="info-label">Full Name:</span> {st.session_state.user_data["full_name"]}</div>')
    if st.session_state.user_data.get('age'):
        personal_info.append(f'<div class="info-item"><span class="info-label">Age:</span> {st.session_state.user_data["age"]}</div>')
    if st.session_state.user_data.get('gender'):
        personal_info.append(f'<div class="info-item"><span class="info-label">Gender:</span> {st.session_state.user_data["gender"]}</div>')
    
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">👤 Personal Info</div>
        {}
    </div>
    """.format(''.join(personal_info) if personal_info else '<div class="info-item">No personal information provided</div>'), unsafe_allow_html=True)

with col3:
    location_info = []
    if st.session_state.user_data.get('city'):
        location_info.append(f'<div class="info-item"><span class="info-label">City:</span> {st.session_state.user_data["city"]}</div>')
    if st.session_state.user_data.get('location'):
        location_info.append(f'<div class="info-item"><span class="info-label">State:</span> {st.session_state.user_data["location"]}</div>')
    location_info.append(f'<div class="info-item"><span class="info-label">Account Type:</span> {st.session_state.user_data.get("account_type", "user").title()}</div>')
    
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">📍 Location</div>
        {}
    </div>
    """.format(''.join(location_info)), unsafe_allow_html=True)
