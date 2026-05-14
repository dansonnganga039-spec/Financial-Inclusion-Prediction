import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import TARGET_COL
from src.explainability.local import fallback_contributions, shap_contributions
from src.modeling.prediction import (
    contributing_factors,
    default_value,
    editable_feature_columns,
    field_label,
    model_feature_columns,
    probability_band,
    recommendations,
)
from src.utils import inclusion_label
from src.visualization.plotting import DIVERGING_SCALE, apply_chart_style, confidence_gauge


def render_prediction_lab(df: pd.DataFrame, model, metrics: dict) -> None:
    st.subheader("Prediction Lab")
    st.caption("Estimate financial inclusion likelihood and translate the score into action.")

    feature_columns = model_feature_columns(df, metrics)
    editable_fields = editable_feature_columns(df, feature_columns)

    sample = df[feature_columns].iloc[0].copy()
    for field in editable_fields:
        sample[field] = default_value(df[field])

    with st.form("prediction_form"):
        profile_tab, access_tab, trust_tab = st.tabs(["Profile", "Access", "Trust"])
        tab_lookup = {
            "County": profile_tab,
            "respondent_sex": profile_tab,
            "respondent_age": profile_tab,
            "education": profile_tab,
            "monthly_income_ksh": profile_tab,
            "incomegp": profile_tab,
            "mobile_money_access": access_tab,
            "mobile_money_active": access_tab,
            "cost_to_nearest_bank": access_tab,
            "walk_time_to_nearest_bank": access_tab,
            "cost_to_nearest_mobile_money_agent": access_tab,
            "walk_time_to_nearest_mobile_money_agent": access_tab,
            "trusted_financial_provider": trust_tab,
        }

        for field in editable_fields:
            with tab_lookup.get(field, profile_tab):
                if pd.api.types.is_numeric_dtype(df[field]):
                    field_values = pd.to_numeric(df[field], errors="coerce")
                    sample[field] = st.number_input(
                        field_label(field),
                        value=float(field_values.median()),
                        min_value=float(field_values.min()),
                        max_value=float(field_values.max()),
                    )
                else:
                    options = sorted(df[field].dropna().astype(str).unique())
                    current = str(sample[field]) if pd.notna(sample[field]) else options[0]
                    default_index = options.index(current) if current in options else 0
                    sample[field] = st.selectbox(field_label(field), options, index=default_index)

        submitted = st.form_submit_button("Predict inclusion probability", type="primary")

    if not submitted:
        return

    row = pd.DataFrame([sample])[feature_columns]
    probability = float(model.predict_proba(row)[0, 1])
    prediction = int(probability >= 0.5)
    _render_prediction_result(sample, row, model, probability, prediction, metrics)


def _render_prediction_result(
    sample: pd.Series,
    row: pd.DataFrame,
    model,
    probability: float,
    prediction: int,
    metrics: dict,
) -> None:
    baseline = float(metrics.get("target_rate", 0.0))
    band, band_note = probability_band(probability)
    delta = probability - baseline

    result_col, baseline_col, band_col = st.columns(3)
    result_col.metric("Prediction", inclusion_label(prediction), f"{probability:.1%} probability")
    baseline_col.metric(
        "Dataset average",
        f"{baseline:.1%}" if baseline else "N/A",
        f"{delta:+.1%} vs average" if baseline else None,
    )
    band_col.metric("Confidence band", band)

    left, right = st.columns([1, 2])
    with left:
        st.plotly_chart(confidence_gauge(probability), use_container_width=True)
    with right:
        if probability >= 0.80:
            st.success(band_note)
        elif probability >= 0.50:
            st.warning(band_note)
        else:
            st.error(band_note)

        reasons = contributing_factors(sample)
        if reasons:
            st.info("Key contributing factors: " + ", ".join(reasons))

        st.markdown("**Recommended decision-support actions**")
        for recommendation in recommendations(sample, probability):
            st.write(f"- {recommendation}")

    _render_contribution_panel(sample, row, model)


def _render_contribution_panel(sample: pd.Series, row: pd.DataFrame, model) -> None:
    contributions = shap_contributions(model, row)
    source = "SHAP contribution"
    if contributions.empty:
        contributions = fallback_contributions(model, sample)
        source = "Feature-importance driver"

    if contributions.empty:
        return

    st.subheader("Feature Contribution Panel")
    fig = px.bar(
        contributions.sort_values("absolute_contribution"),
        x="contribution",
        y="feature",
        orientation="h",
        color="contribution",
        color_continuous_scale=DIVERGING_SCALE,
        labels={"feature": "Feature", "contribution": source},
    )
    max_abs = contributions["contribution"].abs().max()
    if max_abs:
        fig.update_coloraxes(cmin=-max_abs, cmax=max_abs, colorbar_tickfont_color="#111827")
    fig.update_layout(height=max(520, len(contributions) * 34 + 150))
    st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    display = contributions[["feature", "contribution"]].copy()
    display["selected_value"] = display["feature"].map(lambda feature: sample.get(feature, ""))
    st.dataframe(display, width="stretch", hide_index=True)
