import streamlit as st
import sys
import os
from datetime import datetime
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend

# Page config
st.set_page_config(
    page_title="Payment Gateway - Toonify",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize
backend = Backend()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access payment")
    if st.button("Go to Login"):
        st.switch_page("pages/auth.py")
    st.stop()

# Check if there's an image OR premium style to pay for
if 'pending_payment_image_id' not in st.session_state and 'pending_style' not in st.session_state:
    st.warning("⚠️ No payment required")
    if st.button("Back to Studio"):
        st.switch_page("pages/toonify_studio.py")
    st.stop()

# Determine payment type and amount
payment_type = "premium_style" if 'pending_style' in st.session_state else "image_download"
style_name = "Premium Style"  # Default

if payment_type == "premium_style":
    amount = 99.00
    style_name = st.session_state.get('pending_style_name', 'Premium Style')
    payment_title = f"🎨 {style_name} Premium Style"
    payment_description = f"Unlock the {style_name} effect forever"
else:
    amount = 2.99
    payment_title = "🎨 Premium Cartoon Download"
    payment_description = "Download your cartoonized image"

# Theme CSS - Matching Landing Page
theme_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Vibrant Animated Gradient Background - Same as Landing */
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
    
    .payment-container {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
    }
    .price-tag {
        font-size: 3rem;
        font-weight: bold;
        color: #00fff0;
        text-align: center;
        margin: 1rem 0;
    }
    .feature-list {
        color: #fff;
        font-size: 1.1rem;
        line-height: 2rem;
    }
    .secure-badge {
        text-align: center;
        color: #4ade80;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: #fff; font-size: 2.5rem; margin-bottom: 2rem;'>💳 Secure Payment</h1>", unsafe_allow_html=True)

# Create columns for layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Payment details
    st.markdown("<div class='payment-container'>", unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='color: #fff; text-align: center;'>{payment_title}</h2>", unsafe_allow_html=True)
    
    # Price
    st.markdown(f"<div class='price-tag'>₹{amount:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #999;'>{payment_description}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # What's included
    st.markdown("<h3 style='color: #fff;'>✨ What's Included:</h3>", unsafe_allow_html=True)
    
    if payment_type == "premium_style":
        st.markdown(f"""
        <div class='feature-list'>
            ✅ Unlock {style_name} effect forever<br>
            ✅ Unlimited use of this style<br>
            ✅ High-quality transformations<br>
            ✅ All future updates included<br>
            ✅ Commercial use allowed
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='feature-list'>
            ✅ High-resolution cartoonized image<br>
            ✅ PNG format with transparency support<br>
            ✅ Lifetime download access<br>
            ✅ No watermarks<br>
            ✅ Commercial use license
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Payment method selection
    st.markdown("<h3 style='color: #fff;'>💳 Select Payment Method:</h3>", unsafe_allow_html=True)
    
    payment_method = st.radio(
        "Choose payment method",
        ["Credit/Debit Card", "PayPal", "Google Pay", "Apple Pay"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Payment form
    if payment_method == "Credit/Debit Card":
        col1, col2 = st.columns(2)
        with col1:
            card_name = st.text_input("Cardholder Name", placeholder="John Doe")
        with col2:
            card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=19)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            expiry_month = st.selectbox("Month", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        with col4:
            expiry_year = st.selectbox("Year", ["2025", "2026", "2027", "2028", "2029", "2030"])
        with col5:
            cvv = st.text_input("CVV", placeholder="123", max_chars=3, type="password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Process payment button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button(f"🔒 Pay ₹{amount:.2f}", type="primary", use_container_width=True):
            # Validate inputs for card payment
            if payment_method == "Credit/Debit Card":
                if not card_name or not card_number or not cvv:
                    st.error("❌ Please fill in all payment details")
                elif len(card_number.replace(" ", "")) < 15:
                    st.error("❌ Invalid card number")
                elif len(cvv) != 3:
                    st.error("❌ Invalid CVV")
                else:
                    # Process payment
                    with st.spinner("🔄 Processing payment..."):
                        time.sleep(2)  # Simulate payment processing
                        
                        if payment_type == "premium_style":
                            # Unlock premium style
                            style_key = st.session_state.pending_style
                            if 'purchased_styles' not in st.session_state:
                                st.session_state.purchased_styles = []
                            st.session_state.purchased_styles.append(style_key)
                            
                            # Clear pending style
                            del st.session_state.pending_style
                            del st.session_state.pending_style_name
                            
                            st.success(f"✅ {style_name} unlocked successfully!")
                            time.sleep(1)
                            st.switch_page("pages/toonify_studio.py")
                        else:
                            # Process image download payment
                            user_id = st.session_state.user_data['user_id']
                            image_id = st.session_state.pending_payment_image_id
                            
                            success, message, payment_data = backend.create_payment(
                                user_id=user_id,
                                image_id=image_id,
                                amount=amount,
                                payment_method=payment_method
                            )
                            
                            if success:
                                # Process the payment
                                payment_id = payment_data['payment_id']
                                transaction_id = payment_data['transaction_id']
                                
                                success, msg = backend.process_payment(payment_id, transaction_id)
                                
                                if success:
                                    st.session_state.payment_completed = True
                                    st.session_state.payment_id = payment_id
                                    st.session_state.transaction_id = transaction_id
                                    st.success("✅ Payment successful!")
                                    time.sleep(1)
                                    st.switch_page("pages/payment_success.py")
                                else:
                                    st.error(f"❌ {msg}")
                            else:
                                st.error(f"❌ {message}")
            else:
                # For other payment methods, simulate quick processing
                with st.spinner(f"🔄 Redirecting to {payment_method}..."):
                    time.sleep(2)
                    
                    if payment_type == "premium_style":
                        # Unlock premium style
                        style_key = st.session_state.pending_style
                        if 'purchased_styles' not in st.session_state:
                            st.session_state.purchased_styles = []
                        st.session_state.purchased_styles.append(style_key)
                        
                        # Clear pending style
                        del st.session_state.pending_style
                        del st.session_state.pending_style_name
                        
                        st.success(f"✅ {style_name} unlocked successfully!")
                        time.sleep(1)
                        st.switch_page("pages/toonify_studio.py")
                    else:
                        # Process image download payment
                        user_id = st.session_state.user_data['user_id']
                        image_id = st.session_state.pending_payment_image_id
                        
                        success, message, payment_data = backend.create_payment(
                            user_id=user_id,
                            image_id=image_id,
                            amount=amount,
                            payment_method=payment_method
                        )
                        
                        if success:
                            payment_id = payment_data['payment_id']
                            transaction_id = payment_data['transaction_id']
                            
                            success, msg = backend.process_payment(payment_id, transaction_id)
                            
                            if success:
                                st.session_state.payment_completed = True
                                st.session_state.payment_id = payment_id
                                st.session_state.transaction_id = transaction_id
                                st.success("✅ Payment successful!")
                                time.sleep(1)
                                st.switch_page("pages/payment_success.py")
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error(f"❌ {message}")
    
    # Cancel button
    st.markdown("<br>", unsafe_allow_html=True)
    col_cancel1, col_cancel2, col_cancel3 = st.columns([1, 2, 1])
    with col_cancel2:
        if st.button("Cancel Payment", use_container_width=True):
            # Clear payment state
            if 'pending_payment_image_id' in st.session_state:
                del st.session_state.pending_payment_image_id
            if 'pending_style' in st.session_state:
                del st.session_state.pending_style
            if 'pending_style_name' in st.session_state:
                del st.session_state.pending_style_name
            st.switch_page("pages/toonify_studio.py")
    
    # Security badges
    st.markdown("""
    <div class='secure-badge'>
        🔒 Secure Payment | 256-bit SSL Encryption<br>
        Your payment information is safe and encrypted
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Preview image if available
if 'processed_image' in st.session_state and st.session_state.processed_image:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #fff;'>📸 Your Cartoonized Image Preview</h3>", unsafe_allow_html=True)
    
    col_prev1, col_prev2, col_prev3 = st.columns([1, 1, 1])
    with col_prev2:
        st.image(st.session_state.processed_image, caption="Preview (Watermark will be removed after payment)", use_container_width=True)
