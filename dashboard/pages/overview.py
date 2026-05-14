import streamlit as st

from src.visualization.charts import show_overview


def render_overview(filtered_df, metrics: dict) -> None:
    st.subheader("Overview Metrics")
    show_overview(filtered_df, metrics)

    st.subheader("Model Snapshot")
    champion_model = metrics.get("champion_model", "N/A") if metrics else "N/A"
    champion_model = champion_model.replace("Classifier", " Classifier")

    left, middle, right = st.columns(3)
    left.metric("Rows in Training Data", f"{metrics.get('rows', 0):,}" if metrics else "N/A")
    middle.metric("Champion Model", champion_model)
    right.metric("Target Rate", f"{metrics.get('target_rate', 0):.1%}" if metrics else "N/A")
