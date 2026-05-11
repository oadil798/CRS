from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.database.notifications_repo import get_notifications, mark_all_read
from src.ui.layout import page_header, card, section_title


def render(user: dict, language: str) -> None:
    page_header(t(language, "notifications_title"), t(language, "notifications_subtitle"), "notifications", t(language, "in_app_messages"))

    rows = get_notifications(user["id"])
    if st.button(t(language, "mark_read"), use_container_width=True):
        mark_all_read(user["id"])
        st.success(t(language, "marked_read"))
        st.rerun()

    if not rows:
        card(t(language, "no_notifications"), t(language, "no_notifications_body"), "🔔")
        return

    section_title(t(language, "recent_notifications"), t(language, "recent_notifications_subtitle"))
    for n in rows:
        status = t(language, "unread") if n["is_read"] == 0 else t(language, "read")
        icon = {"success": "✅", "warning": "⚠️", "error": "❌", "info": "ℹ️"}.get(n["notification_type"], "ℹ️")
        with st.container(border=True):
            st.markdown(f"### {icon} {n['title']}")
            st.caption(f"{n['created_at']} | {status}")
            st.write(n["message"])
