from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.express as px
from src.content.translations import t
from src.ml.model_loader import load_metrics
from src.config import FEATURE_IMPORTANCE_PATH
from src.ui.layout import page_header, card, section_title


def render(user: dict, language: str) -> None:
    if user["role"] != "admin":
        page_header(t(language, "model_title"), "This academic evaluation page is available to administrators only.", "model", "Restricted page")
        st.error("Model comparison is hidden from normal users to keep the user interface focused on crop recommendation.")
        return

    page_header(t(language, "model_title"), t(language, "model_subtitle"), "model", "Academic evaluation")

    metrics = load_metrics()
    if metrics.empty:
        st.warning("Metrics not found. Run python scripts/train_models.py.")
        return

    section_title("Evaluation Metrics", "These results support the model comparison section of your report and viva explanation.")
    display = metrics.copy()
    for col in ["accuracy", "precision_macro", "recall_macro", "f1_macro"]:
        display[col] = (display[col] * 100).round(2)
    st.dataframe(display, use_container_width=True, hide_index=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        fig = px.bar(display, x="model", y="accuracy", text="accuracy", title="Model Accuracy Comparison (%)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        if FEATURE_IMPORTANCE_PATH.exists():
            fi = pd.read_csv(FEATURE_IMPORTANCE_PATH)
            fig2 = px.bar(fi, x="feature", y="importance", title="Random Forest Feature Importance")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            card("Feature importance missing", "Run the training script again to generate Random Forest feature importance.", "📊")

    st.markdown(
        """
        <div class='info-box'>
            <b>Important viva point:</b> Even if another model performs slightly better in an experiment, Random Forest remains deployed because it matches the FYP / Investigation Report scope.
        </div>
        """,
        unsafe_allow_html=True,
    )
