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
        st.switch_page("pages/login.py")
    st.stop()

# Initialize session state for images
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'processing_history' not in st.session_state:
    st.session_state.processing_history = []

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .navbar {
        background: white;
        padding: 1rem 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: -3rem -4rem 2rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .navbar-brand {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .studio-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .studio-subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .upload-box {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        border: 3px dashed #667eea;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-box:hover {
        border-color: #764ba2;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    .image-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .style-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .style-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    .style-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .style-name {
        font-weight: 600;
        color: #333;
        font-size: 1rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .image-container {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown('<div class="navbar-brand">🎨 Toonify Studio</div>', unsafe_allow_html=True)
with col2:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")
with col3:
    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/profile.py")
with col4:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.switch_page("landing.py")

st.markdown("<br>", unsafe_allow_html=True)

# Header
st.markdown('<div class="studio-header">🎨 Transform Your Images</div>', unsafe_allow_html=True)
st.markdown('<div class="studio-subtitle">Upload an image and apply stunning cartoon effects</div>', unsafe_allow_html=True)

# File Upload Section
st.markdown("### 📤 Upload Image")
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
    help="Supported formats: JPG, PNG, BMP, WEBP"
)

if uploaded_file is not None:
    # Validate and store image
    with st.spinner("🔄 Loading image..."):
        valid, result = processor.validate_image(uploaded_file)
    
    if valid:
        # Resize if needed
        original_img = processor.resize_image(result, max_size=1024)
        st.session_state.original_image = original_img
        st.success("✅ Image loaded successfully!")
        
        # Display original and processed images side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🖼️ Original Image")
            st.image(st.session_state.original_image, use_container_width=True)
            st.caption(f"Size: {st.session_state.original_image.size[0]} x {st.session_state.original_image.size[1]} px")
        
        with col2:
            st.markdown("#### ✨ Processed Image")
            if st.session_state.processed_image:
                st.image(st.session_state.processed_image, use_container_width=True)
                
                # Download button
                img_bytes = processor.image_to_bytes(st.session_state.processed_image, format='PNG')
                st.download_button(
                    label="⬇️ Download Processed Image",
                    data=img_bytes,
                    file_name=f"toonify_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.info("👈 Select a style to process your image")
        
        st.markdown("---")
        
        # Style Selection
        st.markdown("### 🎨 Choose a Style")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🎭", key="classic", use_container_width=True, help="Classic Cartoon"):
                with st.spinner("🎨 Applying Classic Cartoon effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image, 
                        style='classic'
                    )
                st.success("✅ Classic Cartoon applied!")
                st.rerun()
            st.caption("**Classic**")
        
        with col2:
            if st.button("🌊", key="smooth", use_container_width=True, help="Smooth Cartoon"):
                with st.spinner("🎨 Applying Smooth Cartoon effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image,
                        style='smooth'
                    )
                st.success("✅ Smooth Cartoon applied!")
                st.rerun()
            st.caption("**Smooth**")
        
        with col3:
            if st.button("✏️", key="pencil", use_container_width=True, help="Pencil Sketch"):
                with st.spinner("🎨 Applying Pencil Sketch effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image,
                        style='pencil'
                    )
                st.success("✅ Pencil Sketch applied!")
                st.rerun()
            st.caption("**Pencil**")
        
        with col4:
            if st.button("🎨", key="watercolor", use_container_width=True, help="Watercolor"):
                with st.spinner("🎨 Applying Watercolor effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image,
                        style='watercolor'
                    )
                st.success("✅ Watercolor applied!")
                st.rerun()
            st.caption("**Watercolor**")
        
        with col5:
            if st.button("📚", key="comic", use_container_width=True, help="Comic Book"):
                with st.spinner("🎨 Applying Comic Book effect..."):
                    st.session_state.processed_image = processor.convert_to_cartoon(
                        st.session_state.original_image,
                        style='comic'
                    )
                st.success("✅ Comic Book applied!")
                st.rerun()
            st.caption("**Comic**")
        
        # Advanced Controls (if image is processed)
        if st.session_state.processed_image:
            st.markdown("---")
            st.markdown("### 🎛️ Adjustments")
            
            col1, col2 = st.columns(2)
            
            with col1:
                brightness = st.slider("💡 Brightness", 0.5, 2.0, 1.0, 0.1)
                if brightness != 1.0:
                    temp_img = processor.adjust_brightness(st.session_state.processed_image, brightness)
                    st.image(temp_img, caption="Preview", use_container_width=True)
                    if st.button("Apply Brightness", use_container_width=True):
                        st.session_state.processed_image = temp_img
                        st.success("✅ Brightness applied!")
                        st.rerun()
            
            with col2:
                contrast = st.slider("🌓 Contrast", 0.5, 2.0, 1.0, 0.1)
                if contrast != 1.0:
                    temp_img = processor.adjust_contrast(st.session_state.processed_image, contrast)
                    st.image(temp_img, caption="Preview", use_container_width=True)
                    if st.button("Apply Contrast", use_container_width=True):
                        st.session_state.processed_image = temp_img
                        st.success("✅ Contrast applied!")
                        st.rerun()
        
        # Reset button
        st.markdown("---")
        if st.button("🔄 Start New Image", use_container_width=False):
            st.session_state.original_image = None
            st.session_state.processed_image = None
            st.rerun()
    
    else:
        st.error(f"❌ {result}")

else:
    # Upload prompt
    st.markdown("""
    <div class="upload-box">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📸</div>
        <h3>Upload Your Image</h3>
        <p style="color: #666; margin-top: 1rem;">
            Drag and drop or click to browse<br>
            Supports: JPG, PNG, BMP, WEBP
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Style Preview Cards
    st.markdown("### 🎨 Available Styles")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="style-card">
            <div class="style-icon">🎭</div>
            <div class="style-name">Classic</div>
            <p style="font-size: 0.8rem; color: #666;">Traditional cartoon with edge detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="style-card">
            <div class="style-icon">🌊</div>
            <div class="style-name">Smooth</div>
            <p style="font-size: 0.8rem; color: #666;">Smooth cartoon with soft edges</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="style-card">
            <div class="style-icon">✏️</div>
            <div class="style-name">Pencil</div>
            <p style="font-size: 0.8rem; color: #666;">Hand-drawn pencil sketch</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="style-card">
            <div class="style-icon">🎨</div>
            <div class="style-name">Watercolor</div>
            <p style="font-size: 0.8rem; color: #666;">Artistic watercolor painting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="style-card">
            <div class="style-icon">📚</div>
            <div class="style-name">Comic</div>
            <p style="font-size: 0.8rem; color: #666;">Comic book style with strong edges</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>🎨 Toonify Studio</strong> - Transform your images with AI-powered cartoon effects</p>
    <p style="font-size: 0.9rem;">Logged in as: <strong>{}</strong></p>
</div>
""".format(st.session_state.user_data['username']), unsafe_allow_html=True)
