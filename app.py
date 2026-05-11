from __future__ import annotations
import streamlit as st

from src.config import APP_NAME, APP_ICON
from src.database.schema import initialise_database
from src.auth.auth_service import get_session_user, logout_user
from src.ui.layout import apply_global_styles, sidebar_header
from src.database.notifications_repo import count_unread
from src.database import users_repo
from src.content.translations import t
from src.pages import (
    admin_panel,
    advanced_recommendation,
    auth_pages,
    basic_recommendation,
    chat_assistant,
    help_guide,
    home,
    model_comparison,
    notifications,
    prediction_history,
    profile,
)

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

initialise_database()
apply_global_styles()

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "language" not in st.session_state:
    st.session_state.language = "English"

user = get_session_user()
if not user:
    auth_pages.render()
    st.stop()

PAGES = {
    "Home": home.render,
    "Basic Recommendation": basic_recommendation.render,
    "Advanced Recommendation": advanced_recommendation.render,
    "Prediction History": prediction_history.render,
    "Model Comparison": model_comparison.render,
    "Profile / Account": profile.render,
    "Notifications": notifications.render,
    "Chat Assistant": chat_assistant.render,
    "Help & Guide": help_guide.render,
    "Admin Dashboard": admin_panel.render_overview,
    "User Management": admin_panel.render_user_management,
    "Prediction Logs": admin_panel.render_prediction_logs,
}

unread = count_unread(user["id"])

with st.sidebar:
    sidebar_header(user)
    selected_language = st.selectbox(
        t(st.session_state.language, "nav_language"),
        ["English", "Bahasa Melayu"],
        index=0 if st.session_state.language == "English" else 1,
    )
    st.session_state.language = selected_language
    if selected_language != user.get("preferred_language"):
        users_repo.update_profile(user["id"], user["full_name"], user["username"], user["email"], selected_language)
        user["preferred_language"] = selected_language

    lang = st.session_state.language
    if user["role"] == "admin":
        NAV_ITEMS = {
            "Admin Dashboard": t(lang, "nav_admin"),
            "User Management": t(lang, "nav_users"),
            "Prediction Logs": t(lang, "nav_logs"),
            "Model Comparison": t(lang, "nav_model"),
            "Notifications": f"{t(lang, 'nav_notifications')} ({unread})" if unread else t(lang, "nav_notifications"),
            "Chat Assistant": t(lang, "nav_chat"),
            "Help & Guide": t(lang, "nav_help"),
            "Profile / Account": t(lang, "nav_profile"),
        }
    else:
        NAV_ITEMS = {
            "Home": t(lang, "nav_home"),
            "Basic Recommendation": t(lang, "nav_basic"),
            "Advanced Recommendation": t(lang, "nav_advanced"),
            "Prediction History": t(lang, "nav_history"),
            "Notifications": f"{t(lang, 'nav_notifications')} ({unread})" if unread else t(lang, "nav_notifications"),
            "Chat Assistant": t(lang, "nav_chat"),
            "Help & Guide": t(lang, "nav_help"),
            "Profile / Account": t(lang, "nav_profile"),
        }

    if st.session_state.page not in NAV_ITEMS:
        st.session_state.page = next(iter(NAV_ITEMS.keys()))

    selected = st.radio(
        "Navigation",
        list(NAV_ITEMS.keys()),
        index=list(NAV_ITEMS.keys()).index(st.session_state.page),
        format_func=lambda key: NAV_ITEMS[key],
        label_visibility="collapsed",
    )
    st.session_state.page = selected

    st.divider()
    if st.button(t(st.session_state.language, "logout"), use_container_width=True):
        logout_user()
        st.rerun()

page = PAGES.get(st.session_state.page, home.render)
page(user=user, language=st.session_state.language)
