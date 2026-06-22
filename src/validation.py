import pandas as pd

from src.artifacts import ArtifactError
from src.config import TARGET_COL


REQUIRED_DATA_COLUMNS = {"County", TARGET_COL}
REQUIRED_METRIC_KEYS = {"rows", "champion_model", "features", "target_rate"}


def validate_dashboard_data(df: pd.DataFrame) -> None:
    if df.empty:
        raise ArtifactError("The processed dashboard dataset is empty.")

    missing = sorted(REQUIRED_DATA_COLUMNS - set(df.columns))
    if missing:
        raise ArtifactError(
            "The processed dataset is missing required columns: " + ", ".join(missing)
        )

    target_values = set(pd.to_numeric(df[TARGET_COL], errors="coerce").dropna().unique())
    if not target_values or not target_values.issubset({0, 1}):
        raise ArtifactError(f"{TARGET_COL} must contain only binary values 0 and 1.")


def validate_metrics(metrics: dict) -> None:
    missing = sorted(REQUIRED_METRIC_KEYS - set(metrics))
    if missing:
        raise ArtifactError("Model metrics are missing required keys: " + ", ".join(missing))
    if not isinstance(metrics["features"], list) or not metrics["features"]:
        raise ArtifactError("Model metrics must include a non-empty feature list.")


def validate_model(model) -> None:
    if not hasattr(model, "predict_proba"):
        raise ArtifactError("The saved model does not provide predict_proba().")
    if not hasattr(model, "named_steps"):
        raise ArtifactError("The saved model is not the expected fitted pipeline.")


def validate_county_geojson(geojson: dict) -> None:
    features = geojson.get("features") if isinstance(geojson, dict) else None
    if not isinstance(features, list) or not features:
        raise ArtifactError("The county GeoJSON has no features.")
    if any("county_key" not in feature.get("properties", {}) for feature in features):
        raise ArtifactError("The county GeoJSON contains features without properties.county_key.")
