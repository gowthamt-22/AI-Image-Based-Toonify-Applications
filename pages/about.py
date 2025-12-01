import streamlit as st

st.set_page_config(
    page_title="About Toonify",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .about-hero {
        padding: 6rem 4rem;
        background: #000;
        text-align: center;
    }
    
    .about-title {
        font-size: 6rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #00fff0 0%, #a855f7 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -3px;
    }
    
    .about-subtitle {
        font-size: 1.5rem;
        color: #888;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        line-height: 1.8;
    }
    
    .section {
        padding: 5rem 4rem;
        background: #0a0a0a;
    }
    
    .section:nth-child(even) {
        background: #000;
    }
    
    .section-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #fff;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #00fff0, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .content-box {
        background: #141414;
        border: 2px solid #222;
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
    }
    
    .content-text {
        color: #aaa;
        font-size: 1.2rem;
        line-height: 1.9;
        margin-bottom: 1.5rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-item {
        background: #141414;
        border: 2px solid #222;
        border-radius: 20px;
        padding: 2.5rem;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        border-color: #00fff0;
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0, 255, 240, 0.3);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
    }
    
    .feature-title {
        font-size: 1.8rem;
        font-weight: 900;
        color: #fff;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #888;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        justify-content: center;
        margin-top: 3rem;
    }
    
    .tech-badge {
        background: linear-gradient(135deg, #00fff0, #a855f7);
        color: #000;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 900;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00fff0, #a855f7, #ff006e) !important;
        color: #000 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        padding: 1rem 3rem !important;
        border-radius: 50px !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 10px 40px rgba(0, 255, 240, 0.4) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 15px 50px rgba(0, 255, 240, 0.6) !important;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 3rem;
        max-width: 1200px;
        margin: 4rem auto;
    }
    
    .stat-box {
        text-align: center;
    }
    
    .stat-number {
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00fff0, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin-bottom: 1rem;
    }
    
    .stat-label {
        color: #888;
        font-size: 1.3rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="about-hero">
    <h1 class="about-title">ABOUT TOONIFY</h1>
    <p class="about-subtitle">
        The world's most advanced AI-powered image cartoonization platform, transforming ordinary photos into extraordinary cartoon artwork with cutting-edge neural network technology.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏠 Back to Home"):
        st.switch_page("landing.py")

# What is Toonify
st.markdown("""
<div class="section">
    <h2 class="section-title">What is <span class="gradient-text">TOONIFY</span>?</h2>
    <div class="content-box">
        <p class="content-text">
            Toonify is a revolutionary AI-based image transformation tool that leverages state-of-the-art deep learning models to convert regular photographs into stunning cartoon-style artwork. Built on the powerful CartoonGAN architecture, Toonify represents the pinnacle of computer vision and neural style transfer technology.
        </p>
        <p class="content-text">
            Our platform makes professional-grade image transformation accessible to everyone - from casual users creating fun social media content to professional artists seeking creative inspiration. With just a few clicks, you can transform any photo into a work of art.
        </p>
    </div>
    
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-number">100K+</div>
            <div class="stat-label">TRANSFORMATIONS</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">5</div>
            <div class="stat-label">UNIQUE STYLES</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">&lt;2s</div>
            <div class="stat-label">PROCESSING TIME</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">99%</div>
            <div class="stat-label">SATISFACTION</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Key Features
st.markdown("""
<div class="section">
    <h2 class="section-title"><span class="gradient-text">Key</span> Features</h2>
    
    <div class="feature-grid">
        <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI-Powered</div>
            <div class="feature-desc">Advanced CartoonGAN transformer neural network for exceptional quality and accuracy</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-desc">Process images in under 2 seconds with our highly optimized pipeline</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">5 Unique Styles</div>
            <div class="feature-desc">Classic, Smooth, Pencil Sketch, Watercolor, and Comic Book effects</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">🔧</div>
            <div class="feature-title">Full Control</div>
            <div class="feature-desc">Fine-tune brightness, contrast, saturation, and sharpness parameters</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">📱</div>
            <div class="feature-title">User-Friendly</div>
            <div class="feature-desc">Intuitive interface - upload, transform, and download in seconds</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">100% Secure</div>
            <div class="feature-desc">Your images are processed securely and never stored on our servers</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Technology Stack
st.markdown("""
<div class="section">
    <h2 class="section-title"><span class="gradient-text">Technology</span> Stack</h2>
    <div class="content-box">
        <p class="content-text">
            Toonify is built using cutting-edge technologies and frameworks to deliver the best possible performance and user experience:
        </p>
    </div>
    
    <div class="tech-stack">
        <div class="tech-badge">PYTHON 3.11</div>
        <div class="tech-badge">PYTORCH</div>
        <div class="tech-badge">OPENCV</div>
        <div class="tech-badge">STREAMLIT</div>
        <div class="tech-badge">CARTOONGAN</div>
        <div class="tech-badge">PIL/PILLOW</div>
        <div class="tech-badge">NUMPY</div>
        <div class="tech-badge">TORCHVISION</div>
    </div>
</div>
""", unsafe_allow_html=True)

# How It Works
st.markdown("""
<div class="section">
    <h2 class="section-title">How It <span class="gradient-text">Works</span></h2>
    
    <div class="feature-grid">
        <div class="feature-item">
            <div class="feature-icon">1️⃣</div>
            <div class="feature-title">Upload Image</div>
            <div class="feature-desc">Select any photo from your device - portraits, landscapes, or any image you want to transform</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">2️⃣</div>
            <div class="feature-title">Choose Style</div>
            <div class="feature-desc">Pick from 5 unique cartoon styles based on your creative vision and preferences</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">3️⃣</div>
            <div class="feature-title">AI Processing</div>
            <div class="feature-desc">Our CartoonGAN neural network transforms your image with professional quality</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">4️⃣</div>
            <div class="feature-title">Fine-Tune</div>
            <div class="feature-desc">Adjust brightness, contrast, saturation, and sharpness to perfect your artwork</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">5️⃣</div>
            <div class="feature-title">Download</div>
            <div class="feature-desc">Save your transformed image in high quality and share it with the world</div>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon">✨</div>
            <div class="feature-title">Enjoy</div>
            <div class="feature-desc">Use your cartoon artwork for social media, profiles, or creative projects</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Mission & Vision
st.markdown("""
<div class="section">
    <h2 class="section-title">Our <span class="gradient-text">Mission</span></h2>
    <div class="content-box">
        <p class="content-text">
            <strong style="color: #00fff0;">Mission:</strong> To democratize advanced AI technology and make professional-grade image transformation accessible to everyone, regardless of technical expertise or artistic background.
        </p>
        <p class="content-text">
            <strong style="color: #a855f7;">Vision:</strong> To become the world's leading platform for AI-powered creative tools, empowering millions of users to express their creativity and transform their visual content in innovative ways.
        </p>
        <p class="content-text">
            <strong style="color: #ff006e;">Values:</strong> Innovation, Accessibility, Quality, Security, and User-Centric Design drive everything we do at Toonify.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("""
<div class="section" style="text-align: center; padding: 6rem 4rem;">
    <h2 class="section-title">Ready to <span class="gradient-text">Transform</span>?</h2>
    <p class="about-subtitle">
        Join thousands of users creating stunning cartoon artwork with Toonify
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Creating Now"):
        st.switch_page("pages/login.py")

# Footer
st.markdown("""
<div class="section" style="padding: 3rem 4rem; text-align: center; background: #000; border-top: 2px solid #141414;">
    <p style="color: #888; font-size: 1rem;">
        Crafted with ❤️ by <span style="background: linear-gradient(135deg, #00fff0, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">TOONIFY TEAM</span>
    </p>
    <p style="color: #666; font-size: 0.9rem; margin-top: 1rem;">
        © 2025 Toonify • All Rights Reserved • AI-Powered Image Transformation
    </p>
</div>
""", unsafe_allow_html=True)
