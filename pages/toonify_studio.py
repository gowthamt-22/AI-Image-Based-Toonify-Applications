import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend
from image_processor import ImageProcessor

# Page config
st.set_page_config(
    page_title="Toonify Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize
backend = Backend()
processor = ImageProcessor()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access Toonify Studio")
    if st.button("Go to Login"):
        st.switch_page("pages/auth.py")
    st.stop()

# Define premium and free styles
FREE_STYLES = []  # No free styles - all require payment
PREMIUM_STYLES = ['classic', 'pencil', 'watercolor', 'comic', 'oil', 'pop', 'anime']  # All styles require payment
PREMIUM_PRICE = 99.00  # Price for all styles

# Initialize session state - ALWAYS ensure these exist
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'current_style' not in st.session_state:
    st.session_state.current_style = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'premium_access' not in st.session_state:
    st.session_state.premium_access = False
if 'purchased_styles' not in st.session_state:
    st.session_state.purchased_styles = []

# Theme CSS - Dark Mode Only
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
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
    
    /* Hide Sidebar completely */
    [data-testid="stSidebar"], section[data-testid="stSidebar"], .css-1d391kg {
        display: none !important;
    }
    #MainMenu, footer, header {
        visibility: hidden !important;
    }
        
    .main-title {
        color: #fff;
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffd700, #ffed4e, #fff44f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8));
    }
    .subtitle {
        color: #ffffff;
        text-align: center;
        font-size: 1.2rem;
    }
    .style-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        text-align: center;
        transition: all 0.3s;
    }
    .style-card:hover {
        border-color: #ffd700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        background: rgba(255, 255, 255, 0.25);
    }
    .section-title {
        color: #ffd700;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 2px 10px rgba(255, 215, 0, 0.5);
    }
        
.stButton button {
        border-radius: 50px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.7) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown('<h1 class="main-title">🎨 TOONIFY STUDIO</h1>', unsafe_allow_html=True)
with col2:
    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/payment_history.py")
with col3:
    if st.button("👤 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")
with col4:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.switch_page("landing.py")

st.markdown('<p class="subtitle">Transform your photos into stunning cartoons with AI</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# File Upload
uploaded_file = st.file_uploader(
    "📤 Upload Your Image",
    type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
    help="Supported formats: JPG, PNG, BMP, WEBP"
)

if uploaded_file is not None:
    # Load image
    with st.spinner("🔄 Loading image..."):
        valid, result = processor.validate_image(uploaded_file)
    
    if valid:
        original_img = processor.resize_image(result, max_size=1024)
        st.session_state.original_image = original_img
        st.success("✅ Image loaded successfully!")
        
        st.markdown("---")
        
        # ===== STYLES SECTION - AT THE TOP =====
        st.markdown('<h2 class="section-title">🎨 Choose Your Style - All Styles Available</h2>', unsafe_allow_html=True)
        
        st.markdown('<p style="color: #fff; text-align: center; font-size: 1.1rem; margin-bottom: 1.5rem;">🎨 <strong>Transform Your Images!</strong> See how your image looks with different effects<br/>💳 <strong>Pay to Download:</strong> ₹99 per download (high resolution, no watermark)<br/>💰 <strong>No Free Downloads:</strong> Pay each time you download</p>', unsafe_allow_html=True)
        
        # First Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">🎭</div><p style="font-weight: 700; margin-top: 0.5rem;">Classic</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="classic", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🎨 Initializing...")
                progress_bar.progress(20)
                
                status_text.text("🎨 Applying cartoon effect...")
                progress_bar.progress(50)
                
                st.session_state.processed_image = processor.convert_to_cartoon(
                    st.session_state.original_image, style='classic'
                )
                st.session_state.current_style = "Classic"
                
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                st.balloons()
                st.rerun()
        
        with col2:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">✏️</div><p style="font-weight: 700; margin-top: 0.5rem;">Pencil Sketch</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="pencil", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='pencil'
                    )
                    st.session_state.current_style = "Pencil"
                st.success("✅ Applied!")
                st.rerun()
        
        with col3:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">🎨</div><p style="font-weight: 700; margin-top: 0.5rem;">Watercolor</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="watercolor", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='watercolor'
                    )
                    st.session_state.current_style = "Watercolor"
                st.success("✅ Applied!")
                st.rerun()
        
        with col4:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">📚</div><p style="font-weight: 700; margin-top: 0.5rem;">Comic</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="comic", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='comic'
                    )
                    st.session_state.current_style = "Comic"
                st.success("✅ Applied!")
                st.rerun()

        # Second Row (Premium)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">🖼️</div><p style="font-weight: 700; margin-top: 0.5rem;">Oil Paint</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="oil", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing Oil Paint effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='oil'
                    )
                    st.session_state.current_style = "Oil Paint"
                st.success("✅ Oil Paint Applied!")
                st.rerun()
        
        with col2:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">🌟</div><p style="font-weight: 700; margin-top: 0.5rem;">Pop Art</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="pop", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing Pop Art effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='pop'
                    )
                    st.session_state.current_style = "Pop Art"
                st.success("✅ Pop Art Applied!")
                st.rerun()
        
        with col3:
            st.markdown(f'<div class="style-card"><div style="font-size: 3rem;">🎬</div><p style="font-weight: 700; margin-top: 0.5rem;">Anime</p><span style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.7rem; font-weight: 800;">₹{PREMIUM_PRICE:.2f}</span></div>', unsafe_allow_html=True)
            if st.button("Apply", key="anime", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing Anime effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='anime'
                    )
                    st.session_state.current_style = "Anime"
                st.success("✅ Anime Applied!")
                st.rerun()
        
        st.markdown("---")
        
        # ===== PARAMETERS SECTION - SEPARATE =====
        if st.session_state.processed_image:
            st.markdown('<h2 class="section-title">🎛️ Fine-Tune Parameters</h2>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                brightness = st.slider("💡 Brightness", 0.5, 2.0, 1.0, 0.1)
            with col2:
                contrast = st.slider("🔆 Contrast", 0.5, 2.0, 1.0, 0.1)
            with col3:
                saturation = st.slider("🌈 Saturation", 0.0, 2.0, 1.0, 0.1)
            with col4:
                sharpness = st.slider("🔪 Sharpness", 0.0, 2.0, 1.0, 0.1)
            
            if st.button("✨ Apply Adjustments", use_container_width=True, type="primary"):
                with st.spinner("Applying adjustments..."):
                    adjusted = processor.adjust_image(
                        st.session_state.processed_image,
                        brightness=brightness,
                        contrast=contrast,
                        saturation=saturation,
                        sharpness=sharpness
                    )
                    st.session_state.processed_image = adjusted
                st.success("✅ Adjustments applied!")
                st.rerun()
            
            st.markdown("---")
        
        # ===== IMAGE DISPLAY SECTION - SIDE BY SIDE (LEFT TO RIGHT) =====
        st.markdown('<h2 class="section-title">🖼️ Transformation Result</h2>', unsafe_allow_html=True)
        
        # Show images side by side horizontally
        if st.session_state.processed_image:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📷 Original Image")
                st.image(st.session_state.original_image, use_container_width=True)
                st.caption(f"📐 Size: {st.session_state.original_image.size[0]} x {st.session_state.original_image.size[1]} pixels")
            
            with col2:
                st.markdown(f"#### ✨ {st.session_state.current_style} Style")
                st.image(st.session_state.processed_image, use_container_width=True)
                st.caption(f"🎨 Style Applied: {st.session_state.current_style}")
            
            # Download button - ALWAYS requires payment (pay per download)
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                # Every download requires payment - no free downloads
                st.warning(f"👑 Download requires payment: ₹{PREMIUM_PRICE}")
                if st.button(f"💳 Pay ₹{PREMIUM_PRICE} & Download", use_container_width=True, type="primary"):
                    st.session_state.pending_style = st.session_state.current_style.lower().replace(' ', '_')
                    st.session_state.pending_style_name = st.session_state.current_style
                    st.switch_page("pages/payment.py")
        else:
            # Just show original image until style is selected
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📷 Original Image")
                st.image(st.session_state.original_image, use_container_width=True)
                st.caption(f"📐 Size: {st.session_state.original_image.size[0]} x {st.session_state.original_image.size[1]} pixels")
            with col2:
                st.markdown("#### ✨ Transformed Image")
                st.info("👆 Select a style above to see the transformation!")
        
        # Reset button
        st.markdown("---")
        if st.button("🔄 Upload New Image", use_container_width=False):
            st.session_state.original_image = None
            st.session_state.processed_image = None
            st.session_state.current_style = None
            st.rerun()
    
    else:
        st.error(f"❌ {result}")

else:
    st.info("👆 Upload an image to get started!")
