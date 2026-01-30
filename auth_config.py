# Firebase/Google Auth Configuration
# This module handles Firebase Authentication for AI Idea Lab

import streamlit as st
import requests
import json
import base64
from pathlib import Path
import os

# ============================================
# FIREBASE CONFIGURATION
# ============================================

# Firebase Web API Key (from Firebase Console)
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyB7VkqmwM9Nl25MTHsqjG4BnMRo1kKyjR4")

# Firebase Auth REST API endpoints
FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"


def firebase_sign_in_email(email: str, password: str) -> dict:
    """Sign in with email and password using Firebase REST API"""
    url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return {
                "success": True,
                "user_id": data.get("localId"),
                "email": data.get("email"),
                "name": data.get("displayName") or data.get("email").split("@")[0],
                "id_token": data.get("idToken"),
                "refresh_token": data.get("refreshToken"),
            }
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            # Translate common errors
            if "INVALID_LOGIN_CREDENTIALS" in error_message or "EMAIL_NOT_FOUND" in error_message or "INVALID_PASSWORD" in error_message:
                error_message = "メールアドレスまたはパスワードが正しくありません"
            return {"success": False, "error": error_message}
    except Exception as e:
        return {"success": False, "error": str(e)}


def firebase_sign_up_email(email: str, password: str) -> dict:
    """Sign up with email and password using Firebase REST API"""
    url = f"{FIREBASE_AUTH_URL}:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200:
            # Send verification email after signup
            id_token = data.get("idToken")
            email_status = "未送信"
            if id_token:
                email_res = send_email_verification(id_token)
                if email_res.get("success"):
                    email_status = "送信成功"
                else:
                    email_status = f"送信失敗: {email_res.get('error')}"
            
            return {
                "success": True,
                "user_id": data.get("localId"),
                "email": data.get("email"),
                "name": data.get("email").split("@")[0],
                "id_token": id_token,
                "refresh_token": data.get("refreshToken"),
                "email_verified": False,
                "email_status": email_status
            }
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            if error_message == "EMAIL_EXISTS":
                error_message = "このメールアドレスは既に登録されています"
            elif "WEAK_PASSWORD" in error_message:
                error_message = "パスワードは6文字以上必要です"
            elif error_message == "INVALID_EMAIL":
                error_message = "無効なメールアドレスです"
            return {"success": False, "error": error_message}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_email_verification(id_token: str) -> dict:
    """Send email verification link to user"""
    url = f"{FIREBASE_AUTH_URL}:sendOobCode?key={FIREBASE_API_KEY}"
    # NOTE: continueUrl requires the domain to be whitelisted in Firebase Console -> Authentication -> Settings -> Authorized Domains
    # Removing it temporarily to ensure email delivery works first
    # continue_url = "https://ai-idea-lab-1089461983457.asia-northeast1.run.app"
    
    payload = {
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token,
        # "continueUrl": continue_url 
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return {"success": True}
        else:
            return {"success": False, "error": response.json().get("error", {}).get("message")}
    except Exception as e:
        return {"success": False, "error": str(e)}



def refresh_token(refresh_token: str) -> dict:
    """Refresh the ID token using refresh token"""
    url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return {
                "success": True,
                "id_token": data.get("id_token"),
                "refresh_token": data.get("refresh_token"),
                "user_id": data.get("user_id"),
            }
        return {"success": False}
    except:
        return {"success": False}


def get_user_info_from_token(id_token: str) -> dict:
    """Get user information from ID token"""
    url = f"{FIREBASE_AUTH_URL}:lookup?key={FIREBASE_API_KEY}"
    payload = {"idToken": id_token}
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get("users"):
            user = data["users"][0]
            return {
                "success": True,
                "user_id": user.get("localId"),
                "email": user.get("email"),
                "name": user.get("displayName") or user.get("email", "User").split("@")[0],
                "email_verified": user.get("emailVerified", False),
            }
        return {"success": False}
    except:
        return {"success": False}


def init_auth_state():
    """Initialize authentication state in session with persistence check"""
    # Check for logout action from query params
    params = st.query_params
    if params.get("logout") == "true":
        logout_user()
        st.query_params.clear()  # Clear params and stop
        st.rerun()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "auth_error" not in st.session_state:
        st.session_state.auth_error = None
    if "auth_token" not in st.session_state:
        st.session_state.auth_token = None
    if "refresh_token" not in st.session_state:
        st.session_state.refresh_token = None
    
    # Check for token in query params (for session persistence)
    if not st.session_state.authenticated and "token" in params:
        token = params.get("token")
        if token:
            user_info = get_user_info_from_token(token)
            if user_info.get("success"):
                st.session_state.authenticated = True
                st.session_state.user_info = user_info
                st.session_state.auth_token = token


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)


def get_current_user() -> dict:
    """Get current user info"""
    if st.session_state.get("authenticated"):
        return st.session_state.get("user_info", {})
    return None


def login_user(user_info: dict):
    """Set user as logged in and persist token"""
    st.session_state.authenticated = True
    st.session_state.user_info = user_info
    st.session_state.auth_error = None
    st.session_state.auth_token = user_info.get("id_token")
    st.session_state.refresh_token = user_info.get("refresh_token")
    
    # Set token in query params for persistence
    if user_info.get("id_token"):
        st.query_params["token"] = user_info.get("id_token")


def logout_user():
    """Log out current user and clear persistence"""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.auth_error = None
    st.session_state.auth_token = None
    st.session_state.refresh_token = None
    # Clear query params
    st.query_params.clear()


# ============================================
# UI COMPONENTS
# ============================================


def render_login_page():
    """Render the login page UI - Premium Split Screen Design"""
    
    # Process pending auth actions
    if st.session_state.get("pending_action"):
        action = st.session_state.pending_action
        email = st.session_state.get("pending_email", "")
        password = st.session_state.get("pending_password", "")
        
        if action == "login":
            result = firebase_sign_in_email(email, password)
        else:  # signup
            result = firebase_sign_up_email(email, password)
        
        # Clear pending state
        st.session_state.pending_action = None
        st.session_state.pending_email = None
        st.session_state.pending_password = None
        
        if result.get("success"):
            if action == "signup":
                # Signup successful - show message and do NOT login
                st.session_state.auth_success = "アカウントを作成しました。確認メールを送信しましたので、メール内のリンクをクリックしてからログインしてください。"
                st.session_state.pending_email = None # Clear email
                st.session_state.pending_password = None # Clear password
            else:
                # Login successful
                login_user(result)
            st.rerun()
        else:
            st.session_state.auth_error = result.get("error", "認証に失敗しました")


    # Load background image
    bg_image_path = Path(__file__).parent / "assets" / "login_bg.png"
    bg_image_base64 = ""
    if bg_image_path.exists():
        with open(bg_image_path, "rb") as f:
            bg_image_base64 = base64.b64encode(f.read()).decode()

    # Load logo
    logo_path = Path(__file__).parent / "assets" / "xexon_logo.png"
    logo_base64 = ""
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()

    # Premium Split Screen CSS
    st.markdown(f"""
    <style>
    /* Global Reset & Background - FORCE DARK */
    [data-testid="stAppViewContainer"] {{
        background-color: #000000 !important;
        background-image: none !important;
    }}
    
    [data-testid="stHeader"], footer {{
        display: none !important;
    }}

    /* Remove default padding */
    .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }}

    /* --- LAYOUT FIX: Use fixed positioning for the visual side --- */
    /* This ensures it always shows up regardless of column containers */
    .visual-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 65vw; /* Match the column ratio 6.5/10 */
        height: 100vh;
        z-index: 0;
    }}
    
    .visual-bg img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .visual-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(0,0,0,0) 80%, rgba(5,5,5,1) 100%);
        pointer-events: none;
    }}

    /* --- RIGHT COLUMN (Form) --- */
    /* We target the right side column specifically */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) {{
        background-color: #050505 !important;
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 2rem !important;
        z-index: 1; /* Above bg */
        position: relative;
    }}

    /* Ensure form content is constrained */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) > div {{
        width: 100% !important;
        max-width: 440px !important;
    }}

    /* --- TYPOGRAPHY & LOGO --- */
    .logo-container-login {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .login-logo-img {{
        height: 50px;
        width: auto;
        margin-bottom: 1rem;
    }}
    
    .tagline {{
        color: #D4AF37;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.2rem;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
        text-align: center;
        opacity: 0.8;
    }}

    /* --- INPUT FIELDS (ROBUST FIX) --- */
    /* Force background transparent on ALL parts of the input */
    [data-testid="stTextInput"], 
    [data-testid="stTextInput"] > div,
    [data-testid="stTextInput"] input {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* Input Text */
    [data-testid="stTextInput"] input {{
        color: #ffffff !important;
        border-bottom: 1px solid #333 !important;
        caret-color: #D4AF37 !important;
    }}
    
    /* Chrome Autofill Fix - The "White Input" Killer */
    input:-webkit-autofill,
    input:-webkit-autofill:hover, 
    input:-webkit-autofill:focus, 
    input:-webkit-autofill:active {{
        -webkit-box-shadow: 0 0 0 30px #050505 inset !important;
        -webkit-text-fill-color: white !important;
        transition: background-color 5000s ease-in-out 0s;
    }}

    /* Focus State */
    [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {{
        border-bottom-color: #D4AF37 !important;
    }}

    /* Label Styling */
    [data-testid="stTextInput"] label {{
        color: #888888 !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }}

    /* --- BUTTONS --- */
    [data-testid="stFormSubmitButton"] button {{
        background: linear-gradient(90deg, #D4AF37 0%, #B8960F 100%) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        border-radius: 4px !important;
        padding: 0.6rem !important;
    }}
    
    [data-testid="stFormSubmitButton"] button:hover {{
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4) !important;
    }}
    
    /* Secondary (Create Account) */
    div.stButton > button {{
        background: transparent !important;
        border: 1px solid #444 !important;
        color: #888 !important;
    }}
    div.stButton > button:hover {{
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
    }}

    /* Google Placeholder */
    .google-login-box {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        padding: 10px;
        background-color: rgba(255,255,255,0.03);
        border: 1px solid #333;
        border-radius: 4px;
        margin-bottom: 2rem;
    }}
    .google-login-text {{
        color: #888;
        font-size: 0.85rem;
        margin-left: 10px;
    }}
    .divider-text {{
        text-align: center;
        color: #555;
        font-size: 0.7rem;
        margin-bottom: 1.5rem;
        letter-spacing: 0.1em;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Use a wider ratio for the visual part (6.5 : 3.5)
    col_visual, col_form = st.columns([6.5, 3.5])
    
    # --- Content ---
    with col_visual:
        # Direct HTML Injection for Background - Most Robust Method
        st.markdown(f'''
        <div class="visual-bg">
            <img src="data:image/png;base64,{bg_image_base64}">
            <div class="visual-overlay"></div>
        </div>
        ''', unsafe_allow_html=True)

    with col_form:
        # Logo Section
        if logo_base64:
            st.markdown(f'''
            <div class="logo-container-login">
                <img src="data:image/png;base64,{logo_base64}" class="login-logo-img">
                <div class="tagline">Collaborative Intelligence</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('<div class="logo-text">X-Think</div>', unsafe_allow_html=True)
        
        # Google Login
        st.markdown("""
        <div class="google-login-box">
            <span style="font-size:1.1rem;">🇬</span>
            <span class="google-login-text">Sign in with Google</span>
        </div>
        <div class="divider-text">OR LOGIN WITH EMAIL</div>
        """, unsafe_allow_html=True)
        
        # Email Form
        with st.form("login_form"):
            email = st.text_input("EMAIL ADDRESS")
            password = st.text_input("PASSWORD", type="password")
            
            # Login Button (Primary)
            login_btn = st.form_submit_button("SIGN IN")
            
            if login_btn and email and password:
                st.session_state.pending_email = email
                st.session_state.pending_password = password
                st.session_state.pending_action = "login"
                st.rerun()

        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Create Account (Secondary)
        if st.button("CREATE NEW ACCOUNT", use_container_width=True):
             if email and password:
                st.session_state.pending_email = email
                st.session_state.pending_password = password
                st.session_state.pending_action = "signup"
                st.rerun()
             else:
                 st.info("メールアドレスとパスワードを入力して「CREATE NEW ACCOUNT」を押してください")

        # Messages
        if st.session_state.get("auth_success"):
            st.success(st.session_state.auth_success)
            st.session_state.auth_success = None
        
        if st.session_state.get("auth_error"):
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None


def render_user_header():
    """Render user info with logout button in top-right corner"""
    user = get_current_user()
    if not user:
        return
    
    # Create header row with user info and logout button as HTML link
    _, col_user = st.columns([5, 1])
    with col_user:
        st.markdown(f"""
        <div style="text-align: right; margin-bottom: 4px;">
            <span style="color: #e0e0e0; font-size: 0.75rem; margin-right: 12px; font-family: sans-serif;">{user.get('email', '')}</span>
            <a href="?logout=true" target="_self" style="text-decoration: none; color: #D4AF37; font-size: 0.75rem; border: none; background: none; font-family: sans-serif;">
                🚪 Logout
            </a>
        </div>

        """, unsafe_allow_html=True)
