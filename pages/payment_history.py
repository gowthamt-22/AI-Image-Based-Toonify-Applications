import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import Backend

# Page config
st.set_page_config(
    page_title="Payment History - Toonify",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize
backend = Backend()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Please login to access payment history")
    if st.button("Go to Login"):
        st.switch_page("pages/auth.py")
    st.stop()

# Theme CSS
theme_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    .payment-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s;
    }
    .payment-card:hover {
        transform: translateY(-5px);
        border-color: #00fff0;
    }
    .status-completed {
        color: #4ade80;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
    .status-failed {
        color: #ef4444;
        font-weight: bold;
    }
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# Header
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.markdown("<h1 style='text-align: center; color: #fff; font-size: 2.5rem; margin-bottom: 2rem;'>📜 Payment History</h1>", unsafe_allow_html=True)

# Navigation buttons
col_nav1, col_nav2, col_nav3 = st.columns(3)
with col_nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("landing.py")
with col_nav2:
    if st.button("🎨 Studio", use_container_width=True):
        st.switch_page("pages/toonify_studio.py")
with col_nav3:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.switch_page("landing.py")

st.markdown("---")

# Get payment history
user_id = st.session_state.user_data['user_id']
payments = backend.get_user_payment_history(user_id)

if payments:
    # Summary statistics
    total_spent = sum(p['amount'] for p in payments if p['payment_status'] == 'completed')
    completed_count = sum(1 for p in payments if p['payment_status'] == 'completed')
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: rgba(0, 255, 240, 0.1); border-radius: 15px;'>
            <h3 style='color: #00fff0; margin: 0;'>${total_spent:.2f}</h3>
            <p style='color: #999; margin: 0.5rem 0 0 0;'>Total Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: rgba(168, 85, 247, 0.1); border-radius: 15px;'>
            <h3 style='color: #a855f7; margin: 0;'>{completed_count}</h3>
            <p style='color: #999; margin: 0.5rem 0 0 0;'>Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: rgba(255, 0, 110, 0.1); border-radius: 15px;'>
            <h3 style='color: #ff006e; margin: 0;'>{len(payments)}</h3>
            <p style='color: #999; margin: 0.5rem 0 0 0;'>Total Transactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #fff;'>🧾 Transaction History</h2>", unsafe_allow_html=True)
    
    # Display each payment
    for payment in payments:
        status_class = "status-completed" if payment['payment_status'] == 'completed' else "status-pending" if payment['payment_status'] == 'pending' else "status-failed"
        status_icon = "✅" if payment['payment_status'] == 'completed' else "⏳" if payment['payment_status'] == 'pending' else "❌"
        
        payment_date = datetime.fromisoformat(payment['payment_date']).strftime("%B %d, %Y at %I:%M %p")
        
        st.markdown(f"""
        <div class='payment-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h3 style='color: #fff; margin: 0;'>{status_icon} Cartoon Image Download</h3>
                    <p style='color: #999; margin: 0.5rem 0;'>📅 {payment_date}</p>
                    <p style='color: #00fff0; margin: 0;'>🔖 Transaction ID: {payment['transaction_id']}</p>
                </div>
                <div style='text-align: right;'>
                    <h2 style='color: #fff; margin: 0;'>${payment['amount']:.2f}</h2>
                    <p class='{status_class}' style='margin: 0.5rem 0;'>{payment['payment_status'].upper()}</p>
                    <p style='color: #999; margin: 0;'>💳 {payment['payment_method']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
else:
    # No payments yet
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.05); border-radius: 20px; margin: 2rem 0;'>
        <h2 style='color: #999; margin-bottom: 1rem;'>📭 No Payments Yet</h2>
        <p style='color: #666;'>You haven't made any purchases yet.</p>
        <p style='color: #666;'>Start creating amazing cartoon images in the studio!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("🎨 Go to Studio", type="primary", use_container_width=True):
            st.switch_page("pages/toonify_studio.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0;'>
    <p>Need help with a transaction? Contact support@toonify.com</p>
    <p>All payments are processed securely with industry-standard encryption</p>
</div>
""", unsafe_allow_html=True)
