from __future__ import annotations
import base64
from pathlib import Path
import streamlit as st
from src.config import STYLE_PATH, APP_NAME, BACKGROUNDS_DIR

BACKGROUND_MAP = {
    "login": "login.jpg",
    "home": "home.jpg",
    "basic": "basic.jpg",
    "advanced": "advanced.jpg",
    "history": "history.jpg",
    "model": "model.jpg",
    "profile": "profile.jpg",
    "notifications": "notifications.jpg",
    "chat": "chat.jpg",
    "help": "help.jpg",
    "admin": "admin.jpg",
    "users": "users.jpg",
    "logs": "logs.jpg",
}

@st.cache_data(show_spinner=False)
def _image_as_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("utf-8")

def apply_global_styles() -> None:
    """Load the external CSS file into Streamlit.

    The CSS file itself is kept as pure CSS so VS Code does not show
    false CSS syntax errors from <style> tags inside a .css file.
    """
    if STYLE_PATH.exists():
        css = STYLE_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def set_page_background(page_key: str = "home") -> None:
    filename = BACKGROUND_MAP.get(page_key, "home.jpg")
    path = BACKGROUNDS_DIR / filename
    if not path.exists():
        return
    encoded = _image_as_base64(str(path))
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(90deg, rgba(4, 19, 10, 0.48) 0%, rgba(10, 40, 18, 0.20) 48%, rgba(4, 17, 9, 0.36) 100%),
                linear-gradient(180deg, rgba(8, 31, 14, 0.10), rgba(5, 19, 10, 0.18)),
                url("data:image/jpeg;base64,{encoded}") center center / cover fixed no-repeat !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_header(user: dict) -> None:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="sidebar-logo">🌾</div>
            <div>
                <div class="sidebar-title">{APP_NAME}</div>
                <div class="sidebar-subtitle">{user['role'].title()} Workspace</div>
            </div>
        </div>
        <div class="sidebar-user-card">
            <div class="sidebar-user-name">{user['full_name']}</div>
            <div class="sidebar-user-email">{user['email']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def page_header(title: str, subtitle: str, page_key: str = "home", eyebrow: str | None = None) -> None:
    set_page_background(page_key)
    eyebrow_html = f"<div class='page-eyebrow'>{eyebrow}</div>" if eyebrow else ""
    st.markdown(
        f"""
        <section class='page-hero'>
            {eyebrow_html}
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

def hero(title: str, subtitle: str) -> None:
    page_header(title, subtitle, "home")

def metric_card(label: str, value: str, icon: str = "🌱") -> None:
    st.markdown(
        f"""
        <div class='metric-card'>
          <div class='metric-icon'>{icon}</div>
          <div>
            <div class='label'>{label}</div>
            <div class='value'>{value}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def card(title: str, body: str, icon: str = "🌿") -> None:
    st.markdown(
        f"""
        <div class='glass-card hover-lift'>
          <div class='card-icon'>{icon}</div>
          <h3>{title}</h3>
          <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def section_title(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-title'><h2>{title}</h2><p>{subtitle}</p></div>", unsafe_allow_html=True)
