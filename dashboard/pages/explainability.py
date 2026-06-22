import streamlit as st

from src.explainability.importance import show_feature_importance


def render_explainability(model) -> None:
    show_feature_importance(model)

    st.subheader("Prediction Explanation Readiness")
    st.write(
        "Prediction-level explanations are available in the Prediction Lab after a profile is scored. "
        "The app uses detailed contribution values when the deployment environment supports them, "
        "then falls back to the strongest saved model drivers."
    )
