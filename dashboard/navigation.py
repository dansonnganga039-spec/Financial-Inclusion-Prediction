import streamlit as st


PAGES = [
    "Overview",
    "Who and Where",
    "Explainability",
    "Prediction Lab",
    "Data Preview",
]


def sidebar_navigation() -> str:
    with st.sidebar:
        st.title("Financial Inclusion")
        return st.radio("Navigation", PAGES, label_visibility="collapsed")
