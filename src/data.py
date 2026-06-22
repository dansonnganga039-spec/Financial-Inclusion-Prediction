import json
import pickle

import pandas as pd
import streamlit as st

from src.artifacts import ArtifactError, verify_checksum
from src.config import (
    COUNTY_GEOJSON_PATH,
    DATA_PATH,
    METRICS_PATH,
    MODEL_CHECKSUM_PATH,
    MODEL_PATH,
    PROVENANCE_PATH,
)
from src.validation import (
    validate_county_geojson,
    validate_dashboard_data,
    validate_metrics,
    validate_model,
)


@st.cache_data(show_spinner="Loading dashboard data...")
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise ArtifactError(f"Processed dashboard data is missing: {DATA_PATH}")
    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as exc:
        raise ArtifactError(f"Could not read processed dashboard data: {exc}") from exc
    validate_dashboard_data(df)
    return df


@st.cache_data(show_spinner=False)
def load_county_geojson() -> dict:
    if not COUNTY_GEOJSON_PATH.exists():
        raise ArtifactError(f"County boundary data is missing: {COUNTY_GEOJSON_PATH}")
    try:
        with COUNTY_GEOJSON_PATH.open("r", encoding="utf-8-sig") as f:
            geojson = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"Could not read county boundary data: {exc}") from exc
    validate_county_geojson(geojson)
    return geojson


@st.cache_resource(show_spinner="Loading prediction model...")
def load_model():
    verify_checksum(MODEL_PATH, MODEL_CHECKSUM_PATH)
    try:
        with MODEL_PATH.open("rb") as f:
            model = pickle.load(f)
    except Exception as exc:
        raise ArtifactError(f"Could not load the verified model artifact: {exc}") from exc
    validate_model(model)
    return model


@st.cache_data(show_spinner=False)
def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        raise ArtifactError(f"Model metrics are missing: {METRICS_PATH}")
    try:
        with METRICS_PATH.open("r", encoding="utf-8") as f:
            metrics = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"Could not read model metrics: {exc}") from exc
    validate_metrics(metrics)
    return metrics


@st.cache_data(show_spinner=False)
def load_provenance() -> dict:
    if not PROVENANCE_PATH.exists():
        return {}
    try:
        with PROVENANCE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"Could not read model provenance: {exc}") from exc
