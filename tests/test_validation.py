import pandas as pd
import pytest

from src.artifacts import ArtifactError
from src.validation import validate_dashboard_data, validate_metrics


def test_valid_dashboard_data() -> None:
    validate_dashboard_data(
        pd.DataFrame({"County": ["Nairobi", "Nakuru"], "financially_included": [1, 0]})
    )


def test_dashboard_data_requires_target() -> None:
    with pytest.raises(ArtifactError, match="missing required columns"):
        validate_dashboard_data(pd.DataFrame({"County": ["Nairobi"]}))


def test_metrics_require_feature_list() -> None:
    metrics = {"rows": 1, "champion_model": "CatBoostClassifier", "features": [], "target_rate": 1.0}
    with pytest.raises(ArtifactError, match="non-empty feature list"):
        validate_metrics(metrics)
