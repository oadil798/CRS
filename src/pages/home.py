from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.ml.model_loader import load_metadata
from src.ui.layout import page_header, metric_card, card, section_title


def render(user: dict, language: str) -> None:
    metadata = load_metadata()
    page_header(t(language, "home_title"), t(language, "home_subtitle"), "home", t(language, "user_dashboard"))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(t(language, "supported_crops"), str(metadata.get("number_of_crops", 22)), "🌾")
    with c2:
        metric_card(t(language, "input_features"), "7", "🧪")
    with c3:
        metric_card(t(language, "compared_models"), "3", "📊")
    with c4:
        metric_card(t(language, "deployed_model"), "Random Forest", "🌲")

    section_title(t(language, "choose_mode_title"), t(language, "choose_mode_subtitle"))
    a, b = st.columns(2)
    with a:
        card(t(language, "basic_card_title"), t(language, "basic_card_body"), "🌤️")
    with b:
        card(t(language, "advanced_card_title"), t(language, "advanced_card_body"), "🧪")

    section_title(t(language, "how_system_works"), t(language, "how_system_works_subtitle"))
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        card(t(language, "enter_data"), t(language, "enter_data_body"), "✍️")
    with s2:
        card(t(language, "predict"), t(language, "predict_body"), "🤖")
    with s3:
        card(t(language, "review_output"), t(language, "review_output_body"), "🔍")
    with s4:
        card(t(language, "save_history"), t(language, "save_history_body"), "🔐")

    st.markdown(
        f"""
        <div class='info-box'>
            <b>{t(language, 'academic_note')}</b> {t(language, 'academic_note_body')}
        </div>
        """,
        unsafe_allow_html=True,
    )
