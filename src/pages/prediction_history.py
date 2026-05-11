from __future__ import annotations
import streamlit as st
from src.content.translations import t
from src.database.predictions_repo import get_user_predictions, to_dataframe
from src.utils.formatting import title_crop
from src.ui.layout import page_header, card, section_title


def render(user: dict, language: str) -> None:
    page_header(t(language, "history_title"), t(language, "history_subtitle"), "history", t(language, "private_user_records"))

    rows = get_user_predictions(user["id"])
    if not rows:
        c1, c2 = st.columns(2)
        with c1:
            card(t(language, "no_history_yet"), t(language, "no_history_yet_body"), "📜")
        with c2:
            card(t(language, "privacy"), t(language, "privacy_rule_body"), "🔐")
        return

    df = to_dataframe(rows)
    view = df[["created_at", "mode", "recommended_crop", "confidence_level", "confidence_percent", "N", "P", "K", "temperature", "humidity", "ph", "rainfall"]].copy()
    view["recommended_crop"] = view["recommended_crop"].map(title_crop)

    section_title(t(language, "saved_recommendations"), t(language, "saved_recommendations_subtitle"))
    st.dataframe(view.rename(columns={
        "created_at": "Date/Time", "mode": "Mode", "recommended_crop": t(language, "crop"),
        "confidence_level": "Confidence Level", "confidence_percent": t(language, "probability"),
        "temperature": t(language, "temperature"), "humidity": t(language, "humidity"), "ph": "pH", "rainfall": t(language, "rainfall")
    }), use_container_width=True, hide_index=True)

    csv = view.to_csv(index=False).encode("utf-8")
    st.download_button(t(language, "download_my_history"), csv, "my_prediction_history.csv", "text/csv", use_container_width=True)
