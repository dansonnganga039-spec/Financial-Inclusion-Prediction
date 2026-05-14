import streamlit as st

from src.explainability.importance import show_feature_importance


def render_explainability(model) -> None:
    show_feature_importance(model)

    st.subheader("Local Explanation Readiness")
    st.write(
        "Prediction-level explanations are available in the Prediction Lab after a profile "
        "is scored. The app will use SHAP contributions when the deployment environment "
        "has `shap` installed, then fall back to model feature-importance drivers."
    )
