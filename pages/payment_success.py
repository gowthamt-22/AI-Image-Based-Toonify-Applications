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
    page_title="Payment Success - Toonify",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize
backend = Backend()
processor = ImageProcessor()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access this page")
    if st.button("Go to Login"):
        st.switch_page("pages/auth.py")
    st.stop()

# Check if payment was completed
if 'payment_completed' not in st.session_state or not st.session_state.payment_completed:
    st.warning("⚠️ No payment found")
    if st.button("Go to Studio"):
        st.switch_page("pages/toonify_studio.py")
    st.stop()

# Theme CSS
theme_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    .success-container {
        background: rgba(74, 222, 128, 0.1);
        border-radius: 20px;
        padding: 3rem;
        border: 2px solid #4ade80;
        text-align: center;
        margin: 2rem 0;
    }
    .success-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    .transaction-details {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# Main content
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Success message
    st.markdown("""
    <div class='success-container'>
        <div class='success-icon'>✅</div>
        <h1 style='color: #4ade80; margin-bottom: 1rem;'>Payment Successful!</h1>
        <p style='color: #fff; font-size: 1.2rem;'>Your transaction has been completed successfully</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Transaction details
    st.markdown("<div class='transaction-details'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #fff; text-align: center; margin-bottom: 1.5rem;'>📋 Transaction Details</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='color: #999;'>Transaction ID:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #999;'>Payment Method:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #999;'>Amount:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #999;'>Status:</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='color: #00fff0;'><strong>{st.session_state.transaction_id}</strong></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #fff;'>Credit/Debit Card</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #fff;'><strong>$2.99 USD</strong></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #4ade80;'><strong>✓ Completed</strong></p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Download section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #fff; text-align: center;'>📥 Download Your Image</h3>", unsafe_allow_html=True)
    
    if 'processed_image' in st.session_state and st.session_state.processed_image:
        # Show the processed image
        st.image(st.session_state.processed_image, caption="Your Cartoonized Image (No Watermark)", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Download button
        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            # Convert image to bytes for download
            image_bytes = processor.image_to_bytes(st.session_state.processed_image)
            
            if st.download_button(
                label="⬇️ Download High-Quality Image",
                data=image_bytes,
                file_name=f"toonify_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png",
                type="primary",
                use_container_width=True
            ):
                # Record download
                user_id = st.session_state.user_data['user_id']
                image_id = st.session_state.pending_payment_image_id
                payment_id = st.session_state.payment_id
                
                backend.record_download(user_id, image_id, payment_id)
                st.success("✅ Download started!")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎨 Create Another", use_container_width=True):
            # Clear payment session
            if 'payment_completed' in st.session_state:
                del st.session_state.payment_completed
            if 'payment_id' in st.session_state:
                del st.session_state.payment_id
            if 'transaction_id' in st.session_state:
                del st.session_state.transaction_id
            if 'pending_payment_image_id' in st.session_state:
                del st.session_state.pending_payment_image_id
            
            st.switch_page("pages/toonify_studio.py")
    
    with col_btn2:
        if st.button("🏠 Back to Home", use_container_width=True):
            # Clear payment session
            if 'payment_completed' in st.session_state:
                del st.session_state.payment_completed
            if 'payment_id' in st.session_state:
                del st.session_state.payment_id
            if 'transaction_id' in st.session_state:
                del st.session_state.transaction_id
            if 'pending_payment_image_id' in st.session_state:
                del st.session_state.pending_payment_image_id
            
            st.switch_page("landing.py")
    
    # Additional info
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
        <p>💾 Your download link will remain active indefinitely</p>
        <p>📧 A receipt has been sent to your registered email</p>
        <p>❓ Need help? Contact support@toonify.com</p>
    </div>
    """, unsafe_allow_html=True)
