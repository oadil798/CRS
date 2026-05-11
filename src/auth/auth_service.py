from __future__ import annotations
import sqlite3
from typing import Optional, Dict
import streamlit as st
from src.auth.password_utils import create_password_hash, verify_password
from src.database import users_repo
from src.database.notifications_repo import add_notification

def signup_user(full_name: str, username: str, email: str, password: str, preferred_language: str = "English") -> tuple[bool, str]:
    if not full_name.strip() or not username.strip() or not email.strip():
        return False, "Please complete all required fields."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    pw_hash, salt = create_password_hash(password)
    try:
        user_id = users_repo.create_user(full_name, username, email, pw_hash, salt, "user", preferred_language)
        add_notification(user_id, "Welcome", "Your account was created successfully. Advanced Mode is recommended for reliable results.", "success")
        return True, "Account created successfully. You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

def login_user(identifier: str, password: str) -> tuple[bool, str]:
    user = users_repo.get_user_by_identifier(identifier)
    if not user or not verify_password(password, user["password_hash"], user["password_salt"]):
        return False, "Invalid username/email or password."
    st.session_state.user_id = user["id"]
    st.session_state.language = user.get("preferred_language", "English")
    return True, "Login successful."

def logout_user() -> None:
    for key in ["user_id", "page"]:
        st.session_state.pop(key, None)

def get_session_user() -> Optional[Dict]:
    user_id = st.session_state.get("user_id")
    return users_repo.get_user_by_id(int(user_id)) if user_id else None

def change_password(user_id: int, current_password: str, new_password: str) -> tuple[bool, str]:
    user = users_repo.get_user_by_id(user_id)
    if not user:
        return False, "User not found."
    if not verify_password(current_password, user["password_hash"], user["password_salt"]):
        return False, "Current password is incorrect."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."
    pw_hash, salt = create_password_hash(new_password)
    users_repo.update_password(user_id, pw_hash, salt)
    add_notification(user_id, "Password updated", "Your password was updated successfully.", "success")
    return True, "Password updated successfully."
