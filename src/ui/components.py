from __future__ import annotations
import streamlit as st
import pandas as pd
from src.content.crop_info import get_crop_info, get_crop_image_path
from src.utils.formatting import title_crop, as_percent
from src.ui.layout import section_title
from src.content.translations import t


def show_result(result: dict, language: str = "English") -> None:
    crop = result["recommended_crop"]
    info = get_crop_info(crop)
    img = get_crop_image_path(crop)

    section_title(t(language, "recommendation_result"), t(language, "recommendation_result_subtitle"))
    col1, col2 = st.columns([1, 1.35], gap="large")
    with col1:
        if img:
            st.image(str(img), use_container_width=True)
        else:
            st.info(t(language, "crop_image_missing"))
    with col2:
        st.markdown(
            f"""
            <div class='glass-card'>
                <div class='card-icon'>🌱</div>
                <h3>{info['name']}</h3>
                <p><b>{t(language, 'model_confidence')}:</b> {as_percent(result['confidence'])}</p>
                <p><span class='pill'>{result['confidence_level']} {t(language, 'confidence')}</span></p>
                <p>{result['confidence_explanation']}</p>
                <hr style='border:none;border-top:1px solid rgba(47,125,50,0.14);margin:1rem 0;'>
                <p><b>{t(language, 'crop_information')}</b><br>{info['summary']}</p>
                <p><b>{t(language, 'care_note')}</b><br>{info['care']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_title(t(language, "top_candidates"), t(language, "top_candidates_subtitle"))
    top_df = pd.DataFrame(result["top_candidates"])
    top_df["crop"] = top_df["crop"].map(title_crop)
    top_df["probability"] = (top_df["probability"] * 100).round(2)
    st.dataframe(
        top_df.rename(columns={"crop": t(language, "crop"), "probability": t(language, "probability")}),
        use_container_width=True,
        hide_index=True,
    )

    if result.get("warnings"):
        st.markdown(
            f"<div class='warning-box'><b>{t(language, 'smart_warnings')}</b><br>" + "<br>".join(result["warnings"]) + "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='success-box'><b>{t(language, 'smart_warnings')}</b><br>{t(language, 'no_warnings')}</div>",
            unsafe_allow_html=True,
        )


def show_input_errors(errors: list[str], language: str = "English") -> None:
    if language == "Bahasa Melayu":
        title = "Ramalan disekat kerana nilai input tidak realistik"
        body = "Sistem tidak akan menghasilkan cadangan apabila nilai berada di luar julat dataset latihan, kerana keputusan tersebut boleh mengelirukan."
        fix = "Sila masukkan nilai dalam julat yang diterima sebelum membuat ramalan."
    else:
        title = "Prediction blocked because the input values are outside the trained dataset range"
        body = "The model can technically predict any numeric input, but showing a crop for unrealistic values such as all zeros would be misleading."
        fix = "Please correct the values below and run the prediction again."

    items = "".join(f"<li>{error}</li>" for error in errors)
    st.markdown(
        f"""
        <div class='invalid-input-box'>
            <h3>⚠️ {title}</h3>
            <p>{body}</p>
            <ul>{items}</ul>
            <p><b>{fix}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
