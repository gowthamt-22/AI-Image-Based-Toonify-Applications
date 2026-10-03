import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
import time
import random
import string

from filters.cartoon_filter import apply_cartoon_filter
from filters.sketch_filter import apply_sketch_filter

try:
    from filters.pencil_filter import apply_pencil_color_filter
except ImportError:
    pass

def load_css():
    css = """
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

    /* Hide standard Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Global Background and Typography */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #6B46C1 0%, #38BDF8 100%);
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif !important;
        color: white !important;
    }

    /* Ensure text is white where necessary */
    p, h1, h2, h3, h4, h5, h6, span, label, .stMarkdown, li {
        color: white !important;
    }

    /* Primary Action Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #FF6B00, #FACC15) !important;
        color: #111 !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        box-shadow: 0 4px 15px rgba(250, 204, 21, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(250, 204, 21, 0.6) !important;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 15px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .glass-card-dark {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin: 15px 0;
    }

    /* Inputs & Selectors */
    div.stTextInput > div > div > input, div.stPasswordInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px !important;
        color: #111 !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* File Uploader styling */
    [data-testid="stFileUploader"] > section, [data-testid="stFileUploaderDropzone"], [data-testid="stFileUploadDropzone"] {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px !important;
        border: 2px dashed #FACC15 !important;
        padding: 20px !important;
    }
    [data-testid="stFileUploader"] div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {
        color: white !important;
    }
    [data-testid="stFileUploader"] button {
        background: linear-gradient(45deg, #FF6B00, #FACC15) !important;
        color: #111 !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        padding: 5px 20px !important;
        box-shadow: 0 4px 15px rgba(250, 204, 21, 0.3) !important;
    }

    /* Custom Badges */
    .badge-price {
        background: #FACC15;
        color: #111 !important;
        border-radius: 20px;
        padding: 5px 15px;
        font-weight: 800;
        font-size: 14px;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 0 10px rgba(250, 204, 21, 0.5);
    }
    
    .selected-card {
        border: 3px solid #FACC15 !important;
        transform: scale(1.02);
    }
    
    .stats-banner {
        background: rgba(0,0,0,0.5);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 40px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background-color: #FACC15 !important;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'preview_image' not in st.session_state:
        st.session_state.preview_image = None
    if 'filter_name' not in st.session_state:
        st.session_state.filter_name = None
    if 'tx_id' not in st.session_state:
        st.session_state.tx_id = None
        
    # Adjustment sliders state
    if 'brightness' not in st.session_state: st.session_state.brightness = 1.0
    if 'contrast' not in st.session_state: st.session_state.contrast = 1.0
    if 'saturation' not in st.session_state: st.session_state.saturation = 1.0
    if 'sharpness' not in st.session_state: st.session_state.sharpness = 1.0

def navigate_to(page):
    st.session_state.page = page

def apply_adjustments_and_filter(img_bytes, filter_name):
    # Load Image
    pil_image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    
    # 1. Apply PIL Enhancements (Brightness, Contrast, Saturation, Sharpness)
    enhancer = ImageEnhance.Brightness(pil_image)
    pil_image = enhancer.enhance(st.session_state.brightness)
    
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(st.session_state.contrast)
    
    enhancer = ImageEnhance.Color(pil_image)
    pil_image = enhancer.enhance(st.session_state.saturation)
    
    enhancer = ImageEnhance.Sharpness(pil_image)
    pil_image = enhancer.enhance(st.session_state.sharpness)
    
    # Convert to CV2
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    # 2. Apply AI Filter
    processed = cv_image
    if filter_name == "Cartoon":
        processed = apply_cartoon_filter(cv_image)
    elif filter_name == "Pencil Sketch":
        processed = apply_sketch_filter(cv_image, sketch_type="Gray")
    elif filter_name == "Watercolor":
        processed = cv2.bilateralFilter(cv_image, 15, 150, 150)
    elif filter_name == "Comic":
        processed = apply_sketch_filter(cv_image, sketch_type="Color")
    elif filter_name == "Oil Paint":
        processed = cv2.xphoto.oilPainting(cv_image, 7, 1) if hasattr(cv2, 'xphoto') else apply_cartoon_filter(cv_image, 50, 5, 12)
    elif filter_name == "Pop Art":
        processed = cv2.applyColorMap(cv_image, cv2.COLORMAP_AUTUMN)
    elif filter_name == "Anime":
        processed = apply_cartoon_filter(cv_image, 80, 12, 6)
    else: # Classic
        processed = apply_cartoon_filter(cv_image)

    return cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

def page_home():
    st.markdown("""
        <style>
        .block-container { padding-top: 2rem !important; }
        .hero-title { text-align: center; color: #FACC15 !important; font-size: 5rem; font-weight: 800; text-shadow: 0 0 25px rgba(250, 204, 21, 0.6); letter-spacing: 3px; margin-bottom: 0; }
        .hero-subtitle { text-align: center; color: #111 !important; font-size: 2.5rem; font-weight: 800; margin-top: 10px; margin-bottom: 15px; }
        .hero-desc { text-align: center; font-size: 1.2rem; max-width: 800px; margin: 0 auto 40px auto; line-height: 1.6; }
        </style>
        <div style="margin-top: 5vh;">
            <div class="hero-title">🎨 TOONIFY</div>
            <div class="hero-subtitle">Transform Your Images into Stunning Cartoons</div>
            <div class="hero-desc">Experience the power of AI-driven image transformation. Convert any photo into beautiful cartoon artwork in seconds with our advanced CartoonGAN technology.</div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col1, col2, col3, _ = st.columns([2, 1.2, 1.2, 1.2, 2])
    with col1:
        if st.button("🚀 Get Started Free"): navigate_to("register"); st.rerun()
    with col2:
        if st.button("🔒 Login"): navigate_to("login"); st.rerun()
    with col3:
        if st.button("✨ Register"): navigate_to("register"); st.rerun()

    st.markdown("<br><h2 style='text-align:center;'>✨ Powerful Features</h2>", unsafe_allow_html=True)
    fcol1, fcol2, fcol3 = st.columns(3)
    features = [
        ("⚡ Lightning Fast", "Under 2s processing time"),
        ("🎨 8 Unique Styles", "Classic, Pencil, Watercolor, Comic, Oil, Pop Art, Anime"),
        ("🤖 AI Precision", "Advanced CartoonGAN technology"),
        ("🎛️ Full Control", "Adjust brightness, contrast, and sharpness"),
        ("👍 Easy to Use", "Upload, Select, Download workflow"),
        ("🔒 100% Secure", "No images stored on our servers")
    ]
    for i, (title, desc) in enumerate(features):
        with [fcol1, fcol2, fcol3][i % 3]:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; min-height:180px;">
                <h3 style="color:#FACC15 !important;">{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
        <div class="stats-banner">
            <h2 style="margin:0; color:#FACC15 !important;">🏆 100K+ Images Transformed &nbsp;|&nbsp; 8 AI Styles &nbsp;|&nbsp; <2s Processing Time &nbsp;|&nbsp; 99% Satisfaction</h2>
        </div>
    """, unsafe_allow_html=True)

def page_auth():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔒 LOGIN", "✨ REGISTER"])
        
        with tab1:
            st.text_input("📧 Email", placeholder="your.email@example.com", key="l_email")
            st.text_input("🔑 Password", placeholder="Enter your password", type="password", key="l_pwd")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 LOGIN", use_container_width=True, key="btn_login"):
                st.session_state.logged_in = True
                navigate_to("dashboard")
                st.rerun()
                
        with tab2:
            st.text_input("👤 Username", placeholder="Choose a username")
            st.text_input("📧 Email", placeholder="your.email@example.com")
            st.text_input("🔑 Password", placeholder="Create a strong password", type="password")
            st.text_input("🔑 Confirm Password", placeholder="Confirm your password", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ REGISTER", use_container_width=True, key="btn_register"):
                st.session_state.logged_in = True
                navigate_to("dashboard")
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Back to Home", use_container_width=True):
            navigate_to("home")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def page_dashboard():
    # Top Navigation Bar
    col1, col2, col3, col4, col5 = st.columns([2, 0.5, 1, 1, 1])
    with col1:
        st.markdown("<h2 style='color: #FACC15 !important; margin: 0;'>🎨 TOONIFY STUDIO</h2>", unsafe_allow_html=True)
    with col3:
        st.button("📋 History", use_container_width=True)
    with col4:
        st.button("👤 Dashboard", use_container_width=True)
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    # Flow Control
    if st.session_state.page == "checkout":
        page_checkout()
        return
    elif st.session_state.page == "success":
        page_success()
        return

    # Upload Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Drag and drop file here</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "bmp", "webp"], label_visibility="collapsed")
    st.markdown("<p style='text-align:center; color:#ccc !important;'>Limit 200MB per file · JPG, JPEG, PNG, BMP, WEBP</p>", unsafe_allow_html=True)
    
    if uploaded_file:
        if st.session_state.uploaded_image != uploaded_file.getvalue():
            st.session_state.uploaded_image = uploaded_file.getvalue()
            st.session_state.preview_image = None
        st.success("✅ Image loaded successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.uploaded_image:
        return

    st.markdown("---")
    st.markdown("<h3>🎨 Style Selection</h3>", unsafe_allow_html=True)
    
    filters = [
        {"name": "Classic", "icon": "🎭"}, {"name": "Pencil Sketch", "icon": "✏️"},
        {"name": "Watercolor", "icon": "🎨"}, {"name": "Comic", "icon": "📚"},
        {"name": "Oil Paint", "icon": "🖼️"}, {"name": "Pop Art", "icon": "🌟"},
        {"name": "Anime", "icon": "🎬"}, {"name": "Cartoon", "icon": "🎯"}
    ]
    
    f_cols = st.columns(4)
    for i, f in enumerate(filters):
        with f_cols[i % 4]:
            is_sel = st.session_state.filter_name == f['name']
            css_class = "glass-card selected-card" if is_sel else "glass-card"
            
            st.markdown(f"""
            <div class="{css_class}" style="text-align: center; padding: 20px 10px; margin: 10px 0;">
                <h1 style="margin:0;">{f['icon']}</h1>
                <h4 style="margin: 10px 0;">{f['name']}</h4>
                <div class="badge-price">₹99.00</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {f['name']}", key=f"sel_{f['name']}", use_container_width=True):
                st.session_state.filter_name = f['name']
                st.rerun()

    if st.session_state.filter_name:
        st.markdown("---")
        st.markdown("<h3>🎛️ Fine-Tune Parameters</h3>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.session_state.brightness = st.slider("Brightness", 0.5, 2.0, st.session_state.brightness, 0.1)
        with c2: st.session_state.contrast = st.slider("Contrast", 0.5, 2.0, st.session_state.contrast, 0.1)
        with c3: st.session_state.saturation = st.slider("Saturation", 0.0, 3.0, st.session_state.saturation, 0.1)
        with c4: st.session_state.sharpness = st.slider("Sharpness", 0.0, 3.0, st.session_state.sharpness, 0.1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚙️ Apply Adjustments & Preview", use_container_width=True):
            with st.spinner("Processing Preview..."):
                try:
                    st.session_state.preview_image = apply_adjustments_and_filter(st.session_state.uploaded_image, st.session_state.filter_name)
                except Exception as e:
                    st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.preview_image is not None:
        st.markdown("---")
        st.markdown("<h3>🖼️ Transformation Result</h3>", unsafe_allow_html=True)
        
        r1, r2 = st.columns(2)
        with r1:
            st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown("<h4>Original Image</h4>", unsafe_allow_html=True)
            orig_pil = Image.open(io.BytesIO(st.session_state.uploaded_image))
            st.image(orig_pil, use_container_width=True)
            st.markdown(f"<p>Dimensions: {orig_pil.width} x {orig_pil.height} pixels</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with r2:
            st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown(f"<h4>Style Applied: {st.session_state.filter_name}</h4>", unsafe_allow_html=True)
            st.image(st.session_state.preview_image, use_container_width=True)
            st.markdown("<p>Preview generated successfully.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🛒 Pay ₹99.00 & Download High-Res", use_container_width=True):
            st.session_state.page = "checkout"
            st.rerun()

def page_checkout():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>🔒 Secure Payment</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <h3>🛒 {st.session_state.filter_name} Download</h3>
            <h2 style="color:#FACC15 !important; margin:0;">₹99.00</h2>
            <ul style="list-style-type: none; padding-left: 0; margin-top: 15px;">
                <li>✅ High-res transformed image</li>
                <li>✅ PNG format without compression</li>
                <li>✅ Immediate download</li>
                <li>✅ No watermarks</li>
                <li>✅ Commercial use allowed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Payment Method**")
        st.radio("", ["💳 Credit/Debit Card", "🔵 PayPal", "🇬 Google Pay", "🍏 Apple Pay"], horizontal=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.text_input("Cardholder Name", placeholder="John Doe")
        st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
        
        c1, c2 = st.columns(2)
        with c1: st.selectbox("Exp Month", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        with c2: st.selectbox("Exp Year", ["2026", "2027", "2028", "2029", "2030"])
        st.text_input("CVV", placeholder="XXX", type="password")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔒 Pay ₹99.00", use_container_width=True):
            with st.spinner("Processing secure payment..."):
                time.sleep(2)
            st.session_state.tx_id = "TXN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            st.session_state.page = "success"
            st.rerun()
            
        st.markdown("<p style='text-align:center; font-size: 12px; margin-top: 10px;'>🔒 256-bit SSL Secure Encryption</p>", unsafe_allow_html=True)
        
        if st.button("❌ Cancel & Return", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def page_success():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown('<div class="glass-card-dark" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 4rem; margin:0;'>✅</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#4ade80 !important;'>Payment Successful!</h2>", unsafe_allow_html=True)
        st.markdown("<p>Your transaction has been completed successfully.</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <table style="width:100%; text-align:left; background:rgba(255,255,255,0.1); border-radius:10px; padding:20px; margin:20px 0;">
            <tr><td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);"><b>Transaction ID:</b></td> <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">{st.session_state.tx_id}</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);"><b>Payment Method:</b></td> <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Credit Card</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);"><b>Amount:</b></td> <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.1);">₹99.00</td></tr>
            <tr><td style="padding:10px;"><b>Status:</b></td> <td style="padding:10px; color:#4ade80;">Completed</td></tr>
        </table>
        """, unsafe_allow_html=True)
        
        st.image(st.session_state.preview_image, use_container_width=True)
        
        buf = io.BytesIO()
        Image.fromarray(st.session_state.preview_image).save(buf, format="PNG")
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="👇👇 DOWNLOAD YOUR IMAGE NOW 👇👇",
            data=buf.getvalue(),
            file_name=f"toonify_{st.session_state.filter_name}_{st.session_state.tx_id}.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎨 Create Another"):
                st.session_state.preview_image = None
                st.session_state.uploaded_image = None
                st.session_state.page = "dashboard"
                st.rerun()
        with c2:
            if st.button("🏠 Back to Home"):
                st.session_state.preview_image = None
                st.session_state.uploaded_image = None
                st.session_state.page = "home"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Toonify Studio", page_icon="🎨", layout="wide")
    load_css()
    init_session_state()
    
    if st.session_state.page == "home": page_home()
    elif st.session_state.page in ["login", "register"]: page_auth()
    elif st.session_state.page in ["dashboard", "checkout", "success"]: page_dashboard()
    else: page_home()

if __name__ == "__main__":
    main()
