"""
Login and Authentication UI Components
"""
import streamlit as st
import time
from auth.database import verify_user, create_user
from auth.sessions import create_session
from auth.data_logging import save_access_log
from auth.validation import validate_password

def show_login_page():
    """Display the login and signup page"""
    # Enhanced login page with better styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   background-clip: text; font-size: 3rem; margin-bottom: 1rem;">
            PII De-Identification Tool
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            Secure • Fast • Reliable PII Detection & Anonymization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for Login and Sign Up with better styling
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        with st.form("login_form"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                username = st.text_input("Username", key="login_username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
                remember_me = st.checkbox("Remember me", help="Keep me logged in across browser sessions")
                login_submitted = st.form_submit_button("Login", use_container_width=True)
            
            if login_submitted:
                if verify_user(username, password):
                    save_access_log(username, "Login")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    
                    # Create session token for persistent login
                    session_token = create_session(username)
                    st.session_state.session_token = session_token
                    
                    # If remember me is checked, redirect with session token
                    if remember_me:
                        # Redirect with session token in URL
                        st.markdown(f"""
                        <script>
                        // Redirect with session token
                        const currentUrl = window.location.href.split('?')[0];
                        const newUrl = currentUrl + '?session_token={session_token}&username={username}';
                        window.location.href = newUrl;
                        </script>
                        """, unsafe_allow_html=True)
                        st.stop()
                    
                    st.success("Login successful! Welcome back!")
                    time.sleep(1)  # Short delay for better UX
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
    
    with tab2:
        st.markdown("### Create New Account")
        
        # Add password requirements info
        st.markdown("""
        <div style=" padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="margin-bottom: 0.5rem; font-weight: bold;">Password Requirements:</p>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>Minimum 8 characters</li>
                <li>At least one uppercase letter</li>
                <li>At least one lowercase letter</li>
                <li>At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        with st.form("signup_form"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                new_username = st.text_input("Choose a username", key="signup_username", placeholder="Enter a unique username")
                new_password = st.text_input("Choose a password", type="password", key="signup_password", placeholder="Create a strong password")
                confirm_password = st.text_input("Confirm password", type="password", key="confirm_password", placeholder="Re-enter your password")
                signup_submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if signup_submitted:
                if not new_username or not new_password:
                    st.error("Please fill in all fields")
                else:
                    # Validate password strength
                    is_valid, message = validate_password(new_password)
                    if not is_valid:
                        st.error(message)
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        if create_user(new_username, new_password):
                            save_access_log(new_username, "Signup")
                            st.success("Account created successfully! Please log in.")
                        else:
                            st.error("Username already exists. Please choose a different username.")
