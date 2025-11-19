import streamlit as st

# Page config
st.set_page_config(
    page_title="Toonify - Image Cartoonizer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    [data-testid="stHeader"] {
        display: none;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
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
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 200% 200%;
        animation: gradient 15s ease infinite;
        padding: 4rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1%, transparent 1%);
        background-size: 50px 50px;
        animation: float 20s linear infinite;
    }
    
    .main-header {
        font-size: 5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
        animation: fadeInUp 1s ease-out;
    }
    
    .sub-header {
        font-size: 1.8rem;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 2px solid transparent;
    }
    
    .feature-box:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border: 2px solid #667eea;
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        padding: 1.2rem 4rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.7);
        animation: pulse 1s infinite;
    }
    
    .stats-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stats-number {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 3rem 0 2rem 0;
    }
    
    .testimonial-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .footer-section {
        background: linear-gradient(135deg, #434343 0%, #000000 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-top: 4rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="main-header">🎨 Toonify</div>
    <div class="sub-header">Transform Your Images into Stunning Cartoons</div>
</div>
""", unsafe_allow_html=True)

# Call to Action Buttons - Right after hero
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    col_left, col_right = st.columns(2)
    
    with col_left:
        if st.button("🚀 Login", use_container_width=True, key="login_top"):
            st.switch_page("pages/login.py")
    
    with col_right:
        if st.button("✨ Create Account", use_container_width=True, key="register_top"):
            st.switch_page("pages/register.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Stats Section
st.markdown('<div class="section-title">🚀 Why Choose Toonify?</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-number">10K+</div>
        <div class="stats-label">Happy Users</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="stats-number">50K+</div>
        <div class="stats-label">Images Processed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <div class="stats-number">15+</div>
        <div class="stats-label">Art Styles</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stats-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <div class="stats-number">99%</div>
        <div class="stats-label">Satisfaction</div>
    </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown('<div class="section-title">✨ Amazing Features</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🖼️</div>
        <div class="feature-title">Cartoon Effects</div>
        <div class="feature-text">Convert your photos into beautiful cartoon-style images instantly with advanced AI algorithms</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">✏️</div>
        <div class="feature-title">Sketch Mode</div>
        <div class="feature-text">Create stunning pencil sketch effects from any image with realistic artistic touch</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🎭</div>
        <div class="feature-title">Multiple Styles</div>
        <div class="feature-text">Choose from various artistic styles and filters to match your creative vision</div>
    </div>
    """, unsafe_allow_html=True)

# Second row of features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Lightning Fast</div>
        <div class="feature-text">Process images in seconds with our optimized algorithms and powerful backend</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Custom Filters</div>
        <div class="feature-text">Fine-tune effects with customizable parameters to get exactly the look you want</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">💾</div>
        <div class="feature-title">Easy Export</div>
        <div class="feature-text">Download your creations in high quality, ready to share on social media</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Testimonials Section
st.markdown('<div class="section-title">💬 What Our Users Say</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="testimonial-box">
        <p style="font-size: 1.1rem; font-style: italic; color: #333;">"Absolutely amazing! Transformed my photos into stunning cartoons in seconds."</p>
        <p style="font-weight: 600; color: #555; margin-top: 1rem;">- Sarah M.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial-box" style="background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);">
        <p style="font-size: 1.1rem; font-style: italic; color: #333;">"The best image editing tool I've ever used. So easy and fun!"</p>
        <p style="font-weight: 600; color: #555; margin-top: 1rem;">- John D.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="testimonial-box" style="background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);">
        <p style="font-size: 1.1rem; font-style: italic; color: #333;">"Perfect for creating unique content for my social media!"</p>
        <p style="font-weight: 600; color: #555; margin-top: 1rem;">- Emily R.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("## 🎨 Toonify")
st.markdown("### The Art of Cartooning Images")
st.markdown("")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 📍 Contact Us")
    st.markdown("""
    **Address:**  
    Toonify Studios  
    123 Creative Avenue, Tech Park  
    Innovation District  
    City, State - 560001  
    India
    
    **📧 Email:** gowtham@gmail.com  
    **📞 Phone:** +91 7010149674
    """)

st.markdown("")
st.markdown("---")
st.caption("© 2025 Toonify. All rights reserved.")
st.caption("Powered by OpenCV & Streamlit")
