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
        padding-top: 3rem;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    p {
        color: #cccccc !important;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("<h1 style='text-align: center; font-size: 4.5rem; background: linear-gradient(135deg, #00fff0, #a855f7, #ff006e); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🎨 TOONIFY</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-size: 2.5rem; margin-top: -1rem;'>Transform Your Images into Stunning Cartoons</h2>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #888; margin-bottom: 2rem;'>Powered by cutting-edge AI technology. Toonify converts your photos into beautiful cartoon-style artwork in seconds.</p>", unsafe_allow_html=True)

# Buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔐 LOGIN", use_container_width=True, type="primary"):
            st.switch_page("pages/auth.py")
    with col_b:
        if st.button("📝 REGISTER", use_container_width=True):
            st.switch_page("pages/auth.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Example transformations
st.markdown("<h3 style='text-align: center; color: #00fff0; font-size: 2rem; margin: 2rem 0 1.5rem 0;'>✨ Example Transformations</h3>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 3, 1])
with col_center:
    # Landscape
    st.markdown("<p style='text-align: center; color: #a855f7; font-weight: 700; font-size: 1.1rem;'>Landscape</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop", width=300, caption="Original")
    with col2:
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=250&fit=crop&sat=150&con=120", width=300, caption="Cartoon")

    st.markdown("<br>", unsafe_allow_html=True)

    # Animals
    st.markdown("<p style='text-align: center; color: #a855f7; font-weight: 700; font-size: 1.1rem;'>Animals</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=250&fit=crop", width=300, caption="Original")
    with col2:
        st.image("https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=250&fit=crop&sat=140&con=110", width=300, caption="Cartoon")

    st.markdown("<br>", unsafe_allow_html=True)

    # Architecture
    st.markdown("<p style='text-align: center; color: #a855f7; font-weight: 700; font-size: 1.1rem;'>Architecture</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400&h=250&fit=crop", width=300, caption="Original")
    with col2:
        st.image("https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400&h=250&fit=crop&sat=130", width=300, caption="Cartoon")

    st.markdown("<br>", unsafe_allow_html=True)

    # Objects
    st.markdown("<p style='text-align: center; color: #a855f7; font-weight: 700; font-size: 1.1rem;'>Objects</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=250&fit=crop", width=300, caption="Original")
    with col2:
        st.image("https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=250&fit=crop&sat=140&con=120", width=300, caption="Cartoon")

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
<div style='text-align: center; padding: 3rem; border-top: 2px solid #333; margin-top: 4rem;'>
    <p style='color: #888; font-size: 1rem;'>
        Crafted with ❤️ by <span style='background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>TOONIFY TEAM</span>
    </p>
    <p style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
        © 2025 Toonify • All Rights Reserved • AI-Powered Image Transformation
    </p>
</div>
""", unsafe_allow_html=True)
