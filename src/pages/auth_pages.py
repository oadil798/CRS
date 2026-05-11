from __future__ import annotations
import streamlit as st
from src.auth.auth_service import login_user, signup_user
from src.auth.recovery_service import start_recovery, complete_recovery, inspect_token
from src.ui.layout import set_page_background


def _render_auth_marketing() -> None:
    st.markdown(
        """
        <div class="auth-marketing">
            <div>
                <div class="page-eyebrow">Machine Learning • Agriculture • FYP System</div>
                <h1>Smart Crop Recommendation Dashboard</h1>
                <p>
                    Predict the most suitable crop using soil nutrients, pH, temperature, humidity, and rainfall.
                    The deployed model remains Random Forest for academic consistency, while SVM and GaussianNB are used for comparison.
                </p>
                <div class="auth-badges">
                    <span class="auth-badge">🌾 22 Supported Crops</span>
                    <span class="auth-badge">🧪 7 Input Features</span>
                    <span class="auth-badge">🔐 Private User History</span>
                    <span class="auth-badge">📊 Admin Analytics</span>
                </div>
            </div>
            <div class="auth-stat-row">
                <div class="auth-stat"><strong>RF</strong><span>Deployed Model</span></div>
                <div class="auth-stat"><strong>3</strong><span>ML Models</span></div>
                <div class="auth-stat"><strong>SQLite</strong><span>Local Database</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    set_page_background("login")

    left, right = st.columns([1.08, 0.92], gap="large")
    with left:
        _render_auth_marketing()

    with right:
        auth_card = st.container(border=True)
        with auth_card:
            st.markdown(
                """
                <div class="auth-panel-title">Welcome Back</div>
                <div class="auth-panel-subtitle">Login, create an account, or recover your username/password.</div>
                """,
                unsafe_allow_html=True,
            )
            login_tab, signup_tab, recovery_tab = st.tabs(["Login", "Signup", "Recovery"])

            with login_tab:
                identifier = st.text_input("Username or Email", key="login_identifier", placeholder="Enter username or email")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
                if st.button("Login", type="primary", use_container_width=True):
                    ok, msg = login_user(identifier, password)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                st.caption("Use normal username/email login for this stable FYP demo build.")

            with signup_tab:
                full_name = st.text_input("Full Name", key="signup_full_name", placeholder="Example: Omer Adil")
                username = st.text_input("Username", key="signup_username", placeholder="Choose a unique username")
                email = st.text_input("Email", key="signup_email", placeholder="name@example.com")
                preferred_language = st.selectbox("Preferred Language", ["English", "Bahasa Melayu"], key="signup_language")
                password = st.text_input("Password", type="password", key="signup_password")
                confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
                if st.button("Create Account", type="primary", use_container_width=True):
                    if password != confirm:
                        st.error("Passwords do not match.")
                    else:
                        ok, msg = signup_user(full_name, username, email, password, preferred_language)
                        st.success(msg) if ok else st.error(msg)

            with recovery_tab:
                st.markdown("<div class='auth-demo-box'>Secure demo recovery uses expiring tokens stored in SQLite. In a deployed version, the same token link can be emailed through SMTP.</div>", unsafe_allow_html=True)
                mode = st.radio("Recovery Option", ["Forgot Password", "Forgot Username", "Forgot Both"], horizontal=False)
                email = st.text_input("Registered Email", key="recovery_email", placeholder="Enter the email used during signup")
                if st.button("Generate Recovery Token", use_container_width=True):
                    ok, msg, token = start_recovery(email, mode)
                    if ok:
                        st.success(msg)
                        st.code(token)
                        st.caption("Copy this token and use it below. It expires after 30 minutes and can only be used once.")
                    else:
                        st.error(msg)

                st.divider()
                token = st.text_input("Recovery Token", key="complete_token")
                token_info = inspect_token(token) if token else None
                if token_info:
                    st.info(f"Valid token for: {token_info['email']} | Recovery type: {token_info['recovery_type']}")
                new_username = st.text_input("New Username, only required for username/both recovery", key="new_recovery_username")
                new_password = st.text_input("New Password, only required for password/both recovery", type="password", key="new_recovery_password")
                if st.button("Complete Recovery", type="primary", use_container_width=True):
                    ok, msg = complete_recovery(token, new_username or None, new_password or None)
                    st.success(msg) if ok else st.error(msg)
