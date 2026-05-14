import streamlit as st

from dashboard.filters import filter_data
from dashboard.navigation import sidebar_navigation
from dashboard.pages.data_preview import render_data_preview
from dashboard.pages.explainability import render_explainability
from dashboard.pages.overview import render_overview
from dashboard.pages.prediction_lab import render_prediction_lab
from dashboard.pages.visuals import render_visuals
from dashboard.style import apply_dashboard_style
from src.config import APP_SUBTITLE, APP_TITLE
from src.data import load_data, load_metrics, load_model


st.set_page_config(page_title=APP_TITLE, page_icon=":bar_chart:", layout="wide")


def main() -> None:
    apply_dashboard_style()
    page = sidebar_navigation()

    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    df = load_data()
    model = load_model()
    metrics = load_metrics()
    filtered = filter_data(df)

    if filtered.empty:
        render_overview(filtered, metrics)
        st.info("Adjust the sidebar filters to bring records back into the dashboard.")
        return

    if page == "Overview":
        render_overview(filtered, metrics)
    elif page == "Who and Where":
        render_visuals(filtered)
    elif page == "Explainability":
        render_explainability(model)
    elif page == "Prediction Lab":
        render_prediction_lab(df, model, metrics)
    elif page == "Data Preview":
        render_data_preview(filtered)

    st.caption("Built using FinAccess 2021 data, Streamlit, Plotly, CatBoost, and SHAP-ready explanations.")


if __name__ == "__main__":
    main()
