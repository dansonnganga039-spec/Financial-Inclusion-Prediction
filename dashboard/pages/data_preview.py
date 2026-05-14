import streamlit as st


def render_data_preview(filtered_df) -> None:
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df.head(100), width="stretch", hide_index=True)
