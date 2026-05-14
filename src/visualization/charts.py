import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import CHART_COLORS, TARGET_COL
from src.data import load_county_geojson
from src.utils import county_key, inclusion_label
from src.visualization.plotting import SEQUENTIAL_SCALE, apply_chart_style


def show_overview(df: pd.DataFrame, metrics: dict) -> None:
    if df.empty:
        included_rate = 0
        excluded_count = 0
        included_count = 0
    else:
        included_rate = df[TARGET_COL].mean()
        excluded_count = int((df[TARGET_COL] == 0).sum())
        included_count = int((df[TARGET_COL] == 1).sum())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Records", f"{len(df):,}")
    col2.metric("Included", f"{included_count:,}", f"{included_rate:.1%}")
    col3.metric("Excluded", f"{excluded_count:,}", f"{1 - included_rate:.1%}")
    col4.metric("Model ROC-AUC", f"{metrics.get('roc_auc', 0):.3f}" if metrics else "N/A")


def show_charts(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No records match the selected filters.")
        return

    chart_df = df.copy()
    chart_df["inclusion_status"] = chart_df[TARGET_COL].map(inclusion_label)

    left, right = st.columns(2)

    with left:
        st.subheader("Financial Inclusion Split")
        split = (
            chart_df["inclusion_status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="count")
        )
        split["share"] = split["count"] / split["count"].sum()
        fig = px.bar(
            split,
            x="status",
            y="count",
            color="status",
            color_discrete_map=CHART_COLORS,
            text="count",
            hover_data={"status": True, "count": ":,", "share": ":.1%"},
            labels={"status": "Status", "count": "Respondents", "share": "Share"},
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_yaxes(range=[0, split["count"].max() * 1.16])
        st.plotly_chart(apply_chart_style(fig), use_container_width=True)

    with right:
        st.subheader("Inclusion by Sex")
        if "respondent_sex" in df:
            by_sex = (
                df.groupby("respondent_sex", dropna=False)[TARGET_COL]
                .agg(records="size", inclusion_rate="mean")
                .reset_index()
            )
            by_sex["inclusion_rate_pct"] = by_sex["inclusion_rate"] * 100
            by_sex = by_sex.sort_values("inclusion_rate_pct", ascending=False)
            fig = px.bar(
                by_sex,
                x="respondent_sex",
                y="inclusion_rate_pct",
                color="respondent_sex",
                color_discrete_sequence=["#2563eb", "#d97706", "#0f766e", "#7c3aed"],
                text="inclusion_rate_pct",
                hover_data={
                    "respondent_sex": True,
                    "records": ":,",
                    "inclusion_rate_pct": ":.1f",
                    "inclusion_rate": False,
                },
                labels={
                    "respondent_sex": "Respondent Sex",
                    "inclusion_rate_pct": "Inclusion Rate (%)",
                    "records": "Respondents",
                },
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_yaxes(range=[0, max(100, by_sex["inclusion_rate_pct"].max() * 1.16)])
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("Respondent sex column is unavailable.")

    show_county_charts(df)
    show_age_distribution(chart_df)


def show_county_charts(df: pd.DataFrame) -> None:
    if "County" not in df:
        st.info("County column is unavailable.")
        return

    county_summary = (
        df.groupby("County", dropna=False)
        .agg(records=(TARGET_COL, "size"), inclusion_rate=(TARGET_COL, "mean"))
        .query("records >= 20")
        .sort_values("inclusion_rate", ascending=False)
        .reset_index()
    )
    county_summary["county_key"] = county_summary["County"].map(county_key)
    county_summary["inclusion_rate_pct"] = county_summary["inclusion_rate"] * 100

    st.subheader("County Inclusion Heatmap")
    geojson = load_county_geojson()
    fig = px.choropleth_map(
        county_summary,
        geojson=geojson,
        locations="county_key",
        featureidkey="properties.county_key",
        color="inclusion_rate_pct",
        color_continuous_scale=SEQUENTIAL_SCALE,
        opacity=0.9,
        center={"lat": 0.15, "lon": 37.9},
        zoom=5.5,
        map_style="carto-positron",
        range_color=(
            county_summary["inclusion_rate_pct"].min(),
            county_summary["inclusion_rate_pct"].max(),
        ),
        hover_name="County",
        hover_data={"county_key": False, "records": ":,", "inclusion_rate_pct": ":.1f"},
        labels={"records": "Respondents", "inclusion_rate_pct": "Inclusion Rate (%)"},
    )
    fig.update_traces(marker_line_color="#ffffff", marker_line_width=1.0)
    fig.update_layout(
        height=760,
        coloraxis_colorbar_title="Inclusion %",
        map=dict(bearing=0, pitch=0),
    )
    fig.update_coloraxes(colorbar_tickfont_color="#111827", colorbar_title_font_color="#111827")
    st.plotly_chart(apply_chart_style(fig), use_container_width=True, config={"scrollZoom": True})

    unmatched_counties = sorted(
        set(county_summary["county_key"])
        - {feature["properties"]["county_key"] for feature in geojson["features"]}
    )
    if unmatched_counties:
        st.warning(
            "Some counties could not be matched to the map boundaries: "
            + ", ".join(unmatched_counties)
        )

    st.subheader("Top Counties by Inclusion Rate")
    top_counties = county_summary.sort_values("inclusion_rate_pct", ascending=False).head(15).copy()
    fig = px.bar(
        top_counties.sort_values("inclusion_rate_pct"),
        x="inclusion_rate_pct",
        y="County",
        orientation="h",
        color="inclusion_rate_pct",
        color_continuous_scale=SEQUENTIAL_SCALE,
        hover_data={"County": True, "records": ":,", "inclusion_rate_pct": ":.1f"},
        labels={
            "County": "County",
            "records": "Respondents",
            "inclusion_rate_pct": "Inclusion Rate (%)",
        },
    )
    fig.update_layout(coloraxis_colorbar_title="Rate")
    fig.update_coloraxes(cmin=0, colorbar_tickfont_color="#111827")
    fig.update_xaxes(range=[0, max(100, top_counties["inclusion_rate_pct"].max() * 1.08)])
    st.plotly_chart(apply_chart_style(fig), use_container_width=True)
    st.dataframe(
        top_counties[["County", "records", "inclusion_rate_pct"]].rename(
            columns={"inclusion_rate_pct": "inclusion_rate"}
        ),
        use_container_width=True,
        hide_index=True,
    )


def show_age_distribution(chart_df: pd.DataFrame) -> None:
    if "respondent_age" not in chart_df:
        return

    st.subheader("Age Distribution by Inclusion Status")
    age_df = chart_df.copy()
    age_df["respondent_age"] = pd.to_numeric(age_df["respondent_age"], errors="coerce")
    age_df = age_df.dropna(subset=["respondent_age"])
    fig = px.histogram(
        age_df,
        x="respondent_age",
        color="inclusion_status",
        barmode="overlay",
        nbins=30,
        color_discrete_map=CHART_COLORS,
        hover_data={"inclusion_status": True, "respondent_age": ":.0f"},
        labels={
            "respondent_age": "Respondent Age",
            "inclusion_status": "Status",
            "count": "Respondents",
        },
    )
    fig.update_traces(opacity=0.82)
    st.plotly_chart(apply_chart_style(fig), use_container_width=True)
