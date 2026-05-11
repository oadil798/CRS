from __future__ import annotations
import sqlite3
import streamlit as st
from src.content.translations import t
from src.database import users_repo
from src.auth.auth_service import change_password
from src.database.notifications_repo import add_notification
from src.ui.layout import page_header, section_title, card


def render(user: dict, language: str) -> None:
    page_header(t(language, "profile_title"), t(language, "profile_subtitle"), "profile", t(language, "account_settings"))

    section_title(t(language, "account_information"), t(language, "account_information_subtitle"))
    with st.form("profile_form"):
        full_name = st.text_input(t(language, "full_name"), value=user["full_name"])
        username = st.text_input(t(language, "username"), value=user["username"])
        email = st.text_input(t(language, "email"), value=user["email"])
        preferred_language = st.selectbox(t(language, "preferred_language"), ["English", "Bahasa Melayu"], index=0 if user.get("preferred_language") == "English" else 1)
        submitted = st.form_submit_button(t(language, "update_profile"), type="primary", use_container_width=True)

    if submitted:
        try:
            users_repo.update_profile(user["id"], full_name, username, email, preferred_language)
            st.session_state.language = preferred_language
            add_notification(user["id"], "Profile updated", "Your profile/account information was updated.", "success")
            st.success(t(language, "profile_updated"))
            st.rerun()
        except sqlite3.IntegrityError:
            st.error(t(language, "username_email_exists"))

    section_title(t(language, "change_password"), t(language, "change_password_subtitle"))
    with st.form("password_form"):
        current = st.text_input(t(language, "current_password"), type="password")
        new = st.text_input(t(language, "new_password"), type="password")
        confirm = st.text_input(t(language, "confirm_new_password"), type="password")
        change = st.form_submit_button(t(language, "change_password"), use_container_width=True)
    if change:
        if new != confirm:
            st.error(t(language, "passwords_no_match"))
        else:
            ok, msg = change_password(user["id"], current, new)
            st.success(msg) if ok else st.error(msg)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        card(t(language, "privacy"), t(language, "privacy_body"), "🔐")
    with c2:
        card(t(language, "role"), f"{t(language, 'role_body')} {user['role'].title()}.", "👤")
