import pandas as pd
import plotly.express as px
import streamlit as st

from src.visualization.plotting import SEQUENTIAL_SCALE, apply_chart_style


def get_feature_importance(model) -> pd.DataFrame:
    preprocessor = model.named_steps.get("preprocessing")
    estimator = model.named_steps.get("model")
    if preprocessor is None or estimator is None:
        return pd.DataFrame()

    feature_names = preprocessor.get_feature_names_out()
    source_columns = []
    for _, _, columns in preprocessor.transformers_:
        if isinstance(columns, list):
            source_columns.extend(columns)
    source_columns = sorted(set(source_columns), key=len, reverse=True)

    if hasattr(estimator, "get_feature_importance"):
        importances = estimator.get_feature_importance()
    elif hasattr(estimator, "feature_importances_"):
        importances = estimator.feature_importances_
    else:
        return pd.DataFrame()

    importance_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    importance_df["source_column"] = importance_df["feature"].apply(
        lambda feature: next(
            (
                column
                for column in source_columns
                if feature.replace("num__", "").replace("cat__", "") == column
                or feature.replace("num__", "").replace("cat__", "").startswith(f"{column}_")
            ),
            feature.replace("num__", "").replace("cat__", ""),
        )
    )
    return importance_df.sort_values("importance", ascending=False)


def show_feature_importance(model) -> None:
    st.subheader("Key Drivers of Financial Inclusion")
    with st.expander("How to interpret this section"):
        st.write(
            "Higher values show which variables the model uses most when separating "
            "financially included and excluded respondents. These are model signals, "
            "not proof that one factor directly causes inclusion."
        )
    importance_df = get_feature_importance(model)

    if importance_df.empty:
        st.info("Feature importance is unavailable for the current saved model.")
        return

    top_n = st.slider("Number of features to show", 5, 30, 15)
    top_features = importance_df.head(top_n).sort_values("importance")

    fig = px.bar(
        top_features,
        x="importance",
        y="feature",
        orientation="h",
        color="importance",
        color_continuous_scale=SEQUENTIAL_SCALE,
        hover_data={"feature": True, "source_column": True, "importance": ":.3f"},
        labels={
            "feature": "Feature",
            "source_column": "Original Column",
            "importance": "Importance",
        },
    )
    fig.update_layout(coloraxis_colorbar_title="Importance")
    fig.update_layout(height=max(560, top_n * 34 + 160))
    fig.update_coloraxes(cmin=0, colorbar_tickfont_color="#111827")
    st.plotly_chart(apply_chart_style(fig), width="stretch")

    grouped = (
        importance_df.groupby("source_column", as_index=False)["importance"]
        .sum()
        .sort_values("importance", ascending=False)
        .head(10)
    )
    fig_grouped = px.bar(
        grouped.sort_values("importance"),
        x="importance",
        y="source_column",
        orientation="h",
        color="importance",
        color_continuous_scale=SEQUENTIAL_SCALE,
        hover_data={"source_column": True, "importance": ":.3f"},
        labels={"source_column": "Original Column", "importance": "Total Importance"},
    )
    fig_grouped.update_layout(coloraxis_colorbar_title="Importance")
    fig_grouped.update_layout(height=560)
    fig_grouped.update_coloraxes(cmin=0, colorbar_tickfont_color="#111827")
    st.plotly_chart(apply_chart_style(fig_grouped), width="stretch")
