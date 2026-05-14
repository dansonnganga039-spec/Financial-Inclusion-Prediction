import json
import pickle

import pandas as pd
import streamlit as st

from src.config import COUNTY_GEOJSON_PATH, DATA_PATH, METRICS_PATH, MODEL_PATH


@st.cache_data(show_spinner="Loading dashboard data...")
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


@st.cache_data(show_spinner=False)
def load_county_geojson() -> dict:
    with COUNTY_GEOJSON_PATH.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


@st.cache_resource(show_spinner="Loading prediction model...")
def load_model():
    with MODEL_PATH.open("rb") as f:
        return pickle.load(f)


@st.cache_data(show_spinner=False)
def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return {}
    with METRICS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
