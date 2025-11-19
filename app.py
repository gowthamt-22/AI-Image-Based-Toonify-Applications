import streamlit as st
from auth import AuthManager
import time

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Initialize auth manager
auth_manager = AuthManager()

def show_login_page():
    """Display login page"""
    st.title("🎨 Toonify - Login")
    st.markdown("---")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Login", use_container_width=True)
        with col2:
            register_btn = st.form_submit_button("Sign Up", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                success, message, user_data = auth_manager.login_user(email, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
        
        if register_btn:
            st.session_state.page = 'register'
            st.rerun()

def show_registration_page():
    """Display registration page"""
    st.title("🎨 Toonify - Sign Up")
    st.markdown("---")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", placeholder="Choose a username")
            email = st.text_input("Email*", placeholder="Enter your email")
        
        with col2:
            full_name = st.text_input("Full Name", placeholder="Enter your full name (optional)")
            password = st.text_input("Password*", type="password", placeholder="Create a strong password")
        
        confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Re-enter your password")
        
        st.markdown("**Password Requirements:**")
        st.markdown("""
        - At least 8 characters long
        - Contains uppercase letter (A-Z)
        - Contains lowercase letter (a-z)
        - Contains digit (0-9)
        - Contains special character (!@#$%^&*)
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            back_btn = st.form_submit_button("Back to Login", use_container_width=True)
        
        if submit:
            # Validation
            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                # Attempt registration
                success, message, user_id = auth_manager.register_user(
                    username, email, password, full_name
                )
                
                if success:
                    st.success(message)
                    st.info("Please login with your credentials")
                    time.sleep(2)
                    st.session_state.page = 'login'
                    st.rerun()
                else:
                    st.error(message)
        
        if back_btn:
            st.session_state.page = 'login'
            st.rerun()

def show_main_app():
    """Display main application after login"""
    st.sidebar.title(f"Welcome, {st.session_state.user_data['username']}!")
    st.sidebar.markdown("---")
    
    # User info
    st.sidebar.info(f"**Email:** {st.session_state.user_data['email']}")
    if st.session_state.user_data['full_name']:
        st.sidebar.info(f"**Name:** {st.session_state.user_data['full_name']}")
    
    st.sidebar.markdown("---")
    
    # Account management
    if st.sidebar.button("Change Password", use_container_width=True):
        st.session_state.show_change_password = True
    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.session_state.page = 'login'
        st.success("Logged out successfully")
        time.sleep(1)
        st.rerun()
    
    # Main content
    st.title("🎨 Toonify: The Art of Cartooning Images")
    st.markdown("---")
    
    # Show change password form if requested
    if 'show_change_password' in st.session_state and st.session_state.show_change_password:
        st.subheader("Change Password")
        
        with st.form("change_password_form"):
            old_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new = st.text_input("Confirm New Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Change Password")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                if not old_password or not new_password or not confirm_new:
                    st.error("Please fill in all fields")
                elif new_password != confirm_new:
                    st.error("New passwords do not match")
                else:
                    success, message = auth_manager.change_password(
                        st.session_state.user_data['user_id'],
                        old_password,
                        new_password
                    )
                    
                    if success:
                        st.success(message)
                        st.session_state.show_change_password = False
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
            
            if cancel:
                st.session_state.show_change_password = False
                st.rerun()
    else:
        # Main application content (placeholder for image processing features)
        st.info("🎉 Authentication system is ready! Image processing features will be added in future weeks.")
        
        st.markdown("""
        ### Welcome to Toonify!
        
        This application will allow you to:
        - Upload images
        - Apply various cartoon effects
        - Use edge detection and bilateral filtering
        - Create sketch and pencil effects
        - Compare original vs cartoonized images
        
        **Coming Soon:** Image upload and processing features
        """)
        
        # Placeholder for image upload
        st.subheader("Image Processing (Coming Soon)")
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], disabled=True)
        st.info("Image processing features will be implemented in upcoming weeks")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Toonify - Image Cartoonizer",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        if st.session_state.page == 'login':
            show_login_page()
        elif st.session_state.page == 'register':
            show_registration_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
