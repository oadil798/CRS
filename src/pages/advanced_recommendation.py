from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.ml.predict_service import build_advanced_input, predict_crop, get_blocking_input_errors, get_feature_ranges
from src.database.predictions_repo import add_prediction
from src.database.notifications_repo import add_notification
from src.ui.components import show_result, show_input_errors
from src.ui.layout import page_header, section_title, card


def render(user: dict, language: str) -> None:
    page_header(t(language, "advanced_title"), t(language, "advanced_subtitle"), "advanced", t(language, "recommended_mode"))

    ranges = get_feature_ranges()
    range_note = (
        "Only values within the training dataset range are accepted. This prevents misleading predictions such as all-zero inputs."
        if language == "English"
        else "Hanya nilai dalam julat dataset latihan diterima. Ini mengelakkan ramalan yang mengelirukan seperti input semua sifar."
    )
    st.markdown(f"<div class='info-box'><b>Input validation:</b> {range_note}</div>", unsafe_allow_html=True)

    section_title(t(language, "enter_soil_weather"), t(language, "enter_soil_weather_subtitle"))
    with st.form("advanced_form"):
        c1, c2, c3 = st.columns(3)
        N = c1.number_input(t(language, "nitrogen"), min_value=float(ranges["N"]["min"]), max_value=float(ranges["N"]["max"]), value=float(ranges["N"]["median"]), step=1.0)
        P = c2.number_input(t(language, "phosphorus"), min_value=float(ranges["P"]["min"]), max_value=float(ranges["P"]["max"]), value=float(ranges["P"]["median"]), step=1.0)
        K = c3.number_input(t(language, "potassium"), min_value=float(ranges["K"]["min"]), max_value=float(ranges["K"]["max"]), value=float(ranges["K"]["median"]), step=1.0)

        c4, c5, c6, c7 = st.columns(4)
        temperature = c4.number_input(t(language, "temperature"), min_value=float(ranges["temperature"]["min"]), max_value=float(ranges["temperature"]["max"]), value=float(ranges["temperature"]["median"]), step=0.1)
        humidity = c5.number_input(t(language, "humidity"), min_value=float(ranges["humidity"]["min"]), max_value=float(ranges["humidity"]["max"]), value=float(ranges["humidity"]["median"]), step=0.1)
        ph = c6.number_input(t(language, "ph"), min_value=float(ranges["ph"]["min"]), max_value=float(ranges["ph"]["max"]), value=float(ranges["ph"]["median"]), step=0.1)
        rainfall = c7.number_input(t(language, "rainfall"), min_value=float(ranges["rainfall"]["min"]), max_value=float(ranges["rainfall"]["max"]), value=float(ranges["rainfall"]["median"]), step=0.1)
        submitted = st.form_submit_button(t(language, "predict_crop"), type="primary", use_container_width=True)

    if submitted:
        values = build_advanced_input(N, P, K, temperature, humidity, ph, rainfall)
        errors = get_blocking_input_errors(values)
        if errors:
            st.session_state.pop("last_advanced_result", None)
            show_input_errors(errors, language)
        else:
            try:
                result = predict_crop(values)
                st.session_state.last_advanced_result = {"values": values, "result": result}
            except Exception as exc:
                st.session_state.pop("last_advanced_result", None)
                st.error(f"Prediction failed: {exc}")

    data = st.session_state.get("last_advanced_result")
    if data:
        show_result(data["result"], language)
        if st.button(t(language, "save_to_history"), use_container_width=True):
            add_prediction(user["id"], "Advanced", data["values"], data["result"])
            add_notification(user["id"], "Prediction saved", "Your Advanced Mode prediction was saved to your private history.", "success")
            st.success(t(language, "prediction_saved_private"))
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            card(t(language, "full_feature_input"), t(language, "full_feature_input_body"), "🧪")
        with c2:
            card(t(language, "more_reliable"), t(language, "more_reliable_body"), "✅")
        with c3:
            card(t(language, "best_for_report"), t(language, "best_for_report_body"), "📘")
