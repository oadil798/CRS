from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.content.help_content import get_help_items
from src.ui.layout import page_header, card, section_title


def render(user: dict, language: str) -> None:
    page_header(t(language, "help_title"), t(language, "help_subtitle"), "help", t(language, "user_guidance"))

    c1, c2, c3 = st.columns(3)
    with c1:
        card(t(language, "soil_values"), t(language, "soil_values_body"), "🧪")
    with c2:
        card(t(language, "weather_values"), t(language, "weather_values_body"), "🌦️")
    with c3:
        card(t(language, "real_use"), t(language, "real_use_body"), "👨‍🌾")

    section_title(t(language, "input_help"), t(language, "input_help_subtitle"))
    for title, body in get_help_items(language):
        with st.expander(title, expanded=False):
            st.write(body)

    st.markdown(
        f"""
        <div class='warning-box'>
            <b>{t(language, 'important_limitation')}</b> {t(language, 'important_limitation_body')}
        </div>
        """,
        unsafe_allow_html=True,
    )
