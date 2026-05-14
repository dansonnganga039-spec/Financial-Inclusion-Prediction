import streamlit as st

from src.visualization.charts import show_charts


def render_visuals(filtered_df) -> None:
    st.subheader("Who Is Affected and Where?")
    with st.expander("How to read these charts"):
        st.write(
            "Use the demographic charts to understand who is affected, then use the "
            "county map to see where financial inclusion is stronger or weaker across Kenya."
        )
    show_charts(filtered_df)
