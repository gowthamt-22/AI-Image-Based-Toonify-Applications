import streamlit as st
from PIL import Image
import base64

st.set_page_config(
    page_title="Toonify - Transform Images to Cartoons with AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra Premium Modern CSS with Vibrant Colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* Vibrant Animated Gradient Background */
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
    
    /* Main Container */
    .main .block-container {
        padding: 3rem 2rem;
        max-width: 1400px;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 4rem 0;
        position: relative;
    }
    
    .hero-title {
        font-size: 6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffd700, #ffed4e, #fff44f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        animation: titleGlow 2s ease-in-out infinite alternate;
        filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8));
    }
    
    @keyframes titleGlow {
        from {
            filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.6));
        }
        to {
            filter: drop-shadow(0 0 40px rgba(255, 237, 78, 1));
        }
    }
    
    .hero-subtitle {
        font-size: 2rem;
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .hero-description {
        font-size: 1.25rem;
        color: #f0f9ff;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        line-height: 1.8;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    /* CTA Button */
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ff8e53);
        color: white;
        padding: 1.25rem 4rem;
        font-size: 1.5rem;
        font-weight: 700;
        border-radius: 50px;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 10px 40px rgba(255, 107, 107, 0.6);
        border: none;
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 60px rgba(255, 142, 83, 0.8);
    }
    
    /* Feature Cards with Different Colors */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s ease;
        height: 100%;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255, 255, 255, 0.6);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .feature-text {
        font-size: 1.1rem;
        color: #f0f9ff;
        line-height: 1.6;
    }
    
    /* Color variations for features */
    .color-orange { color: #ff6b6b; }
    .color-blue { color: #4facfe; }
    .color-purple { color: #c471ed; }
    .color-green { color: #11998e; }
    .color-pink { color: #f093fb; }
    .color-yellow { color: #ffd700; }
    
    /* Stats */
    .stat-number {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 1.25rem;
        color: #ffffff;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Section Titles */
    .section-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 4rem 0 3rem 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 30px rgba(255, 107, 107, 0.5) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff5252, #ff7043) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(255, 107, 107, 0.7) !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden !important;}
    [data-testid="stSidebar"], section[data-testid="stSidebar"], .css-1d391kg {
        display: none !important;
    }
    
    /* Image styling */
    img {
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class='hero-section'>
    <h1 class='hero-title'>🎨 TOONIFY</h1>
    <h2 class='hero-subtitle'>Transform Your Images into Stunning Cartoons</h2>
    <p class='hero-description'>
        Experience the power of AI-driven image transformation. Convert any photo into beautiful 
        cartoon artwork in seconds with our advanced CartoonGAN technology.
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons at the top
col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1.5])
with col2:
    if st.button("🚀 Get Started Free", key="hero_cta1", type="primary"):
        st.switch_page("pages/auth.py")
with col3:
    if st.button("🔐 Login", key="login_btn", type="secondary"):
        st.switch_page("pages/auth.py")
with col4:
    if st.button("✨ Register", key="register_btn", type="secondary"):
        st.switch_page("pages/auth.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Key Features Section
st.markdown("<h2 class='section-title'>✨ Powerful Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class='feature-card'>
        <span class='feature-icon'>⚡</span>
        <h3 class='feature-title color-orange'>Lightning Fast</h3>
        <p class='feature-text'>Transform images in under 2 seconds with optimized AI processing</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <span class='feature-icon'>🎨</span>
        <h3 class='feature-title color-blue'>8 Unique Styles</h3>
        <p class='feature-text'>Classic, Smooth, Pencil, Watercolor, Comic, Oil, Pop Art, Anime</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <span class='feature-icon'>🎯</span>
        <h3 class='feature-title color-purple'>AI Precision</h3>
        <p class='feature-text'>Advanced CartoonGAN transformer technology for perfect results</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class='feature-card'>
        <span class='feature-icon'>🔧</span>
        <h3 class='feature-title color-green'>Full Control</h3>
        <p class='feature-text'>Fine-tune brightness, contrast, saturation, and sharpness</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <span class='feature-icon'>📱</span>
        <h3 class='feature-title color-pink'>Easy to Use</h3>
        <p class='feature-text'>Upload, select style, and download - it's that simple!</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <span class='feature-icon'>🔒</span>
        <h3 class='feature-title color-yellow'>100% Secure</h3>
        <p class='feature-text'>Your images are processed securely and never stored</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Stats Section
st.markdown("<h2 class='section-title'>📊 Trusted by Thousands</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <div class='stat-number'>100K+</div>
        <div class='stat-label'>IMAGES TRANSFORMED</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <div class='stat-number'>8</div>
        <div class='stat-label'>AI STYLES</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <div class='stat-number'>&lt;2s</div>
        <div class='stat-label'>PROCESSING TIME</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <div class='stat-number'>99%</div>
        <div class='stat-label'>SATISFACTION</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# How It Works
st.markdown("<h2 class='section-title'>🔄 Simple 3-Step Process</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class='feature-card' style='text-align: center;'>
        <span class='feature-icon'>1️⃣</span>
        <h3 class='feature-title' style='color: #a78bfa;'>Upload</h3>
        <p class='feature-text'>Choose any photo from your device</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card' style='text-align: center;'>
        <span class='feature-icon'>2️⃣</span>
        <h3 class='feature-title' style='color: #c084fc;'>Transform</h3>
        <p class='feature-text'>Select from 8 stunning cartoon styles</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card' style='text-align: center;'>
        <span class='feature-icon'>3️⃣</span>
        <h3 class='feature-title' style='color: #e879f9;'>Download</h3>
        <p class='feature-text'>Save and share your masterpiece</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Final CTA
st.markdown("""
<div style='text-align: center; padding: 5rem 0 3rem 0;'>
    <h2 class='hero-subtitle' style='margin-bottom: 1.5rem;'>Ready to Transform Your Images?</h2>
    <p class='hero-description' style='margin-bottom: 3rem;'>
        Join thousands of creators making stunning cartoons with AI
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎨 Start Creating Now", key="footer_cta", type="primary"):
        st.switch_page("pages/auth.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 3rem 1rem 2rem 1rem; border-top: 1px solid rgba(139, 92, 246, 0.2); margin-top: 4rem;'>
    <h3 style='color: #a78bfa; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;'>🎨 TOONIFY</h3>
    <p style='color: #94a3b8; font-size: 1rem; margin-bottom: 1rem;'>
        Transform your photos into stunning cartoon art with AI
    </p>
    <p style='color: #64748b; font-size: 0.95rem; margin: 0.75rem 0;'>
        📧 support@toonify.com • 📱 +91 80 1234 5678
    </p>
    <p style='color: #64748b; font-size: 0.95rem; margin: 0.75rem 0;'>
        📍 Bangalore, India
    </p>
    <p style='color: #475569; font-size: 0.85rem; margin-top: 2rem;'>
        © 2025 Toonify • All Rights Reserved • Made with ❤️
    </p>
</div>
""", unsafe_allow_html=True)
