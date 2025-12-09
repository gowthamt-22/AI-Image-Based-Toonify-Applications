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

# Initialize session state
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'current_style' not in st.session_state:
    st.session_state.current_style = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Theme CSS
if st.session_state.theme == 'dark':
    theme_css = """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        }
        .main-title {
            color: #fff;
            text-align: center;
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00fff0, #a855f7, #ff006e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            color: #888;
            text-align: center;
            font-size: 1.2rem;
        }
        .style-card {
            background: #1a1a1a;
            padding: 1.5rem;
            border-radius: 16px;
            border: 2px solid #333;
            text-align: center;
            transition: all 0.3s;
        }
        .style-card:hover {
            border-color: #00fff0;
            box-shadow: 0 0 30px rgba(0, 255, 240, 0.3);
        }
        .section-title {
            color: #00fff0;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 2rem 0 1rem 0;
        }
        .stButton button {
            border-radius: 12px !important;
            font-weight: 700 !important;
        }
    </style>
    """
else:
    theme_css = """
    <style>
        .stApp {
            background: linear-gradient(135deg, #f0f0f0 0%, #ffffff 100%);
        }
        .main-title {
            color: #000;
            text-align: center;
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00d4ff, #7b2ff7, #ff006e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            color: #555;
            text-align: center;
            font-size: 1.2rem;
        }
        .style-card {
            background: #fff;
            padding: 1.5rem;
            border-radius: 16px;
            border: 2px solid #ddd;
            text-align: center;
            transition: all 0.3s;
        }
        .style-card:hover {
            border-color: #00d4ff;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        }
        .section-title {
            color: #00d4ff;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 2rem 0 1rem 0;
        }
        .stButton button {
            border-radius: 12px !important;
            font-weight: 700 !important;
        }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

# Header with theme toggle
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown('<h1 class="main-title">🎨 TOONIFY STUDIO</h1>', unsafe_allow_html=True)
with col2:
    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/payment_history.py")
with col3:
    if st.button("🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
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
        st.markdown('<h2 class="section-title">🎨 Choose Your Style (8 Options)</h2>', unsafe_allow_html=True)
        
        # First Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">🎭</div><p style="font-weight: 700; margin-top: 0.5rem;">Classic</p></div>', unsafe_allow_html=True)
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
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">🌊</div><p style="font-weight: 700; margin-top: 0.5rem;">Smooth</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="smooth", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🎨 Initializing...")
                progress_bar.progress(20)
                
                status_text.text("🎨 Creating smooth effect...")
                progress_bar.progress(50)
                
                st.session_state.processed_image = processor.convert_to_cartoon(
                    st.session_state.original_image, style='smooth'
                )
                st.session_state.current_style = "Smooth"
                
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                st.balloons()
                st.rerun()
        
        with col3:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">✏️</div><p style="font-weight: 700; margin-top: 0.5rem;">Pencil</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="pencil", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='pencil'
                    )
                    st.session_state.current_style = "Pencil"
                st.success("✅ Applied!")
                st.rerun()
        
        with col4:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">🎨</div><p style="font-weight: 700; margin-top: 0.5rem;">Watercolor</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="watercolor", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='watercolor'
                    )
                    st.session_state.current_style = "Watercolor"
                st.success("✅ Applied!")
                st.rerun()
        
        # Second Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">📚</div><p style="font-weight: 700; margin-top: 0.5rem;">Comic</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="comic", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='comic'
                    )
                    st.session_state.current_style = "Comic"
                st.success("✅ Applied!")
                st.rerun()
        
        with col2:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">🖼️</div><p style="font-weight: 700; margin-top: 0.5rem;">Oil Paint</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="oil", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='classic'
                    )
                    st.session_state.current_style = "Oil Paint"
                st.success("✅ Applied!")
                st.rerun()
        
        with col3:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">🌟</div><p style="font-weight: 700; margin-top: 0.5rem;">Pop Art</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="pop", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='smooth'
                    )
                    st.session_state.current_style = "Pop Art"
                st.success("✅ Applied!")
                st.rerun()
        
        with col4:
            st.markdown('<div class="style-card"><div style="font-size: 3rem;">🎬</div><p style="font-weight: 700; margin-top: 0.5rem;">Anime</p></div>', unsafe_allow_html=True)
            if st.button("Apply", key="anime", use_container_width=True, type="primary"):
                with st.spinner("🎨 Processing..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, style='watercolor'
                    )
                    st.session_state.current_style = "Anime"
                st.success("✅ Applied!")
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
            
            # Download/Payment button below images
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                # Generate unique image ID for payment tracking
                import hashlib
                image_id = hashlib.md5(f"{st.session_state.user_data['user_id']}_{datetime.now().isoformat()}_{st.session_state.current_style}".encode()).hexdigest()
                
                # Check if user has already paid for this image
                user_id = st.session_state.user_data['user_id']
                has_paid, payment_info = backend.verify_payment(user_id, image_id)
                
                if has_paid:
                    # User has paid - allow download
                    img_bytes = processor.image_to_bytes(st.session_state.processed_image, format='PNG')
                    st.download_button(
                        label="⬇️ Download High-Quality Image",
                        data=img_bytes,
                        file_name=f"toonify_{st.session_state.current_style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png",
                        use_container_width=True,
                        type="primary"
                    )
                    st.success("✅ Payment verified - Download available")
                else:
                    # User needs to pay first
                    st.markdown("""
                    <div style='text-align: center; padding: 1rem; background: rgba(255, 193, 7, 0.1); border-radius: 10px; margin-bottom: 1rem;'>
                        <p style='color: #ffc107; font-size: 1.1rem; margin: 0;'>
                            💎 Premium Download - $2.99
                        </p>
                        <p style='color: #999; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
                            High-resolution, no watermark, commercial license
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("💳 Pay & Download ($2.99)", use_container_width=True, type="primary"):
                        # Store image ID for payment processing
                        st.session_state.pending_payment_image_id = image_id
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
