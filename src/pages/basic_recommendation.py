from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.ml.predict_service import build_basic_input, predict_crop, get_blocking_input_errors, get_feature_ranges
from src.ml.model_loader import load_metadata
from src.database.predictions_repo import add_prediction
from src.database.notifications_repo import add_notification
from src.ui.components import show_result, show_input_errors
from src.ui.layout import page_header, section_title, card


def render(user: dict, language: str) -> None:
    page_header(t(language, "basic_title"), t(language, "basic_subtitle"), "basic", t(language, "quick_prediction_mode"))

    metadata = load_metadata()
    med = metadata.get("feature_medians", {})
    st.markdown(
        f"""
        <div class='info-box'>
            <b>{t(language, 'default_values_used')}</b><br>
            N={med.get('N', 37):.2f}, P={med.get('P', 51):.2f}, K={med.get('K', 32):.2f}, pH={med.get('ph', 6.43):.2f}
        </div>
        """,
        unsafe_allow_html=True,
    )

    ranges = get_feature_ranges()
    range_note = (
        "Only weather values within the training dataset range are accepted. N, P, K, and pH still use dataset medians in Basic Mode."
        if language == "English"
        else "Hanya nilai cuaca dalam julat dataset latihan diterima. N, P, K dan pH masih menggunakan median dataset dalam Mod Asas."
    )
    st.markdown(f"<div class='info-box'><b>Input validation:</b> {range_note}</div>", unsafe_allow_html=True)

    section_title(t(language, "enter_weather_values"), t(language, "enter_weather_values_subtitle"))
    with st.form("basic_form"):
        c1, c2, c3 = st.columns(3)
        temperature = c1.number_input(t(language, "temperature"), min_value=float(ranges["temperature"]["min"]), max_value=float(ranges["temperature"]["max"]), value=float(ranges["temperature"]["median"]), step=0.1)
        humidity = c2.number_input(t(language, "humidity"), min_value=float(ranges["humidity"]["min"]), max_value=float(ranges["humidity"]["max"]), value=float(ranges["humidity"]["median"]), step=0.1)
        rainfall = c3.number_input(t(language, "rainfall"), min_value=float(ranges["rainfall"]["min"]), max_value=float(ranges["rainfall"]["max"]), value=float(ranges["rainfall"]["median"]), step=0.1)
        submitted = st.form_submit_button(t(language, "predict_crop"), type="primary", use_container_width=True)

    if submitted:
        values = build_basic_input(temperature, humidity, rainfall)
        errors = get_blocking_input_errors(values)
        if errors:
            st.session_state.pop("last_basic_result", None)
            show_input_errors(errors, language)
        else:
            try:
                result = predict_crop(values)
                st.session_state.last_basic_result = {"values": values, "result": result}
            except Exception as exc:
                st.session_state.pop("last_basic_result", None)
                st.error(f"Prediction failed: {exc}")

    data = st.session_state.get("last_basic_result")
    if data:
        show_result(data["result"], language)
        if st.button(t(language, "save_to_history"), use_container_width=True):
            add_prediction(user["id"], "Basic", data["values"], data["result"])
            add_notification(user["id"], "Prediction saved", "Your Basic Mode prediction was saved to your private history.", "success")
            st.success(t(language, "prediction_saved_private"))
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            card(t(language, "when_to_use"), t(language, "when_to_use_body"), "🌤️")
        with c2:
            card(t(language, "limitation"), t(language, "limitation_body"), "⚠️")
        with c3:
            card(t(language, "best_demo_use"), t(language, "best_demo_use_body"), "🎓")
