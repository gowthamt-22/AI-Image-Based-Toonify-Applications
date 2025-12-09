import streamlit as st
from PIL import Image
import base64

st.set_page_config(
    page_title="Toonify - AI Cartoonizer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject minimal CSS for dark background
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    .main .block-container {
        padding-top: 1rem;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    p {
        color: #cccccc !important;
        font-size: 1.1rem;
    }
    .glowing-title {
        text-align: center;
        font-size: 4.5rem;
        background: linear-gradient(135deg, #00fff0, #a855f7, #ff006e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(0,255,240,0.5), 0 0 40px rgba(168,85,247,0.5), 0 0 60px rgba(255,0,110,0.5);
    }
    @keyframes glow {
        from {
            filter: drop-shadow(0 0 10px rgba(0,255,240,0.8)) drop-shadow(0 0 20px rgba(168,85,247,0.8));
        }
        to {
            filter: drop-shadow(0 0 20px rgba(168,85,247,0.8)) drop-shadow(0 0 40px rgba(255,0,110,0.8));
        }
    }
</style>
""", unsafe_allow_html=True)

# Top Navigation with Login
col_logo, col_space, col_login = st.columns([2, 2, 1])
with col_logo:
    st.markdown("<h2 style='color: #00fff0; margin: 0;'>🎨 TOONIFY</h2>", unsafe_allow_html=True)
with col_login:
    if st.button("🔐 LOGIN / REGISTER", use_container_width=True, type="primary"):
        st.switch_page("pages/auth.py")

st.markdown("<hr style='border: 1px solid #333; margin: 1rem 0;'>", unsafe_allow_html=True)

# Hero Section
st.markdown("<h1 class='glowing-title'>🎨 TOONIFY</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-size: 2.5rem; margin-top: -1rem;'>Transform Your Images into Stunning Cartoons</h2>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #888; margin-bottom: 2rem;'>Powered by cutting-edge AI technology. Toonify converts your photos into beautiful cartoon-style artwork in seconds.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Example transformations
st.markdown("<h3 style='text-align: center; color: #00fff0; font-size: 2rem; margin: 2rem 0 1.5rem 0;'>✨ See The Magic</h3>", unsafe_allow_html=True)

# Create a more attractive before/after layout
examples = [
    {
        "title": "🏔️ Landscape",
        "before": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop",
        "after": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop&sat=180&con=130"
    },
    {
        "title": "👤 Portrait", 
        "before": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop",
        "after": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop&sat=160"
    },
    {
        "title": "🐾 Animals",
        "before": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=300&h=200&fit=crop",
        "after": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=300&h=200&fit=crop&sat=160"
    }
]

for example in examples:
    st.markdown(f"<h4 style='text-align: center; color: #a855f7; margin: 2rem 0 1rem 0;'>{example['title']}</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.markdown("<p style='text-align: center; color: #00fff0; font-weight: 600; margin-bottom: 0.5rem;'>BEFORE</p>", unsafe_allow_html=True)
            st.image(example["before"], use_container_width=True)
        with subcol2:
            st.markdown("<p style='text-align: center; color: #ff006e; font-weight: 600; margin-bottom: 0.5rem;'>AFTER</p>", unsafe_allow_html=True)
            st.image(example["after"], use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Features Section
st.markdown("<h2 style='text-align: center; font-size: 3rem; margin: 4rem 0 2rem 0;'>✨ Key Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #333; text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>⚡</div>
        <h3 style='color: #00fff0; margin-bottom: 1rem;'>Lightning Fast</h3>
        <p style='color: #aaa;'>Process images in under 2 seconds with optimized AI</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #333; text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🎨</div>
        <h3 style='color: #a855f7; margin-bottom: 1rem;'>5 Unique Styles</h3>
        <p style='color: #aaa;'>Classic, Smooth, Pencil, Watercolor, Comic</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #333; text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🎯</div>
        <h3 style='color: #ff006e; margin-bottom: 1rem;'>AI Precision</h3>
        <p style='color: #aaa;'>CartoonGAN transformer technology</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #333; text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🔧</div>
        <h3 style='color: #00fff0; margin-bottom: 1rem;'>Full Control</h3>
        <p style='color: #aaa;'>Adjust brightness, contrast, saturation, sharpness</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #333; text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>📱</div>
        <h3 style='color: #a855f7; margin-bottom: 1rem;'>Easy to Use</h3>
        <p style='color: #aaa;'>Upload, transform, download - that simple!</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #333; text-align: center;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🔒</div>
        <h3 style='color: #ff006e; margin-bottom: 1rem;'>100% Secure</h3>
        <p style='color: #aaa;'>Images processed securely, never stored</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Stats Section
st.markdown("<h2 style='text-align: center; font-size: 3rem; margin: 4rem 0 3rem 0;'>📊 By The Numbers</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>100K+</div>
        <p style='font-size: 1.3rem; color: #888; font-weight: 700;'>TRANSFORMATIONS</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>5</div>
        <p style='font-size: 1.3rem; color: #888; font-weight: 700;'>STYLES</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>&lt;2s</div>
        <p style='font-size: 1.3rem; color: #888; font-weight: 700;'>PROCESSING</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center;'>
        <div style='font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>99%</div>
        <p style='font-size: 1.3rem; color: #888; font-weight: 700;'>SATISFACTION</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# How It Works
st.markdown("<h2 style='text-align: center; font-size: 3rem; margin: 4rem 0 3rem 0;'>🔄 How It Works</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #00fff0; text-align: center; height: 100%;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>1️⃣</div>
        <h3 style='color: #00fff0; margin-bottom: 1rem;'>Upload Image</h3>
        <p style='color: #aaa;'>Select any photo from your device</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #a855f7; text-align: center; height: 100%;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>2️⃣</div>
        <h3 style='color: #a855f7; margin-bottom: 1rem;'>Choose Style</h3>
        <p style='color: #aaa;'>Pick from 5 unique cartoon effects</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #1a1a1a; padding: 2rem; border-radius: 16px; border: 2px solid #ff006e; text-align: center; height: 100%;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>3️⃣</div>
        <h3 style='color: #ff006e; margin-bottom: 1rem;'>Download</h3>
        <p style='color: #aaa;'>Save & share your cartoon artwork</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# CTA Section
st.markdown("<h2 style='text-align: center; font-size: 3.5rem; margin: 4rem 0 2rem 0;'>Ready to Create Magic? ✨</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.4rem; color: #888; margin-bottom: 3rem;'>Join thousands of users transforming their photos today</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎨 Get Started Free", use_container_width=True, type="primary"):
        st.switch_page("pages/auth.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem 1rem; border-top: 1px solid #333; margin-top: 3rem;'>
    <p style='color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;'>
        📧 support@toonify.com • 📱 +91 80 1234 5678 • 📍 Bangalore, India
    </p>
    <p style='color: #888; font-size: 1rem; margin: 0.5rem 0;'>
        Crafted with ❤️ by <span style='background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>TOONIFY TEAM</span>
    </p>
    <p style='color: #666; font-size: 0.85rem; margin-top: 0.5rem;'>
        © 2025 Toonify • All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
