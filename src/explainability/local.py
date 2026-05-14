import numpy as np
import pandas as pd

from src.explainability.importance import get_feature_importance


def _feature_names(model) -> list[str]:
    preprocessor = model.named_steps.get("preprocessing")
    if preprocessor is None:
        return []
    return list(preprocessor.get_feature_names_out())


def shap_contributions(model, row: pd.DataFrame, max_features: int = 12) -> pd.DataFrame:
    try:
        import shap
    except ImportError:
        return pd.DataFrame()

    preprocessor = model.named_steps.get("preprocessing")
    estimator = model.named_steps.get("model")
    if preprocessor is None or estimator is None:
        return pd.DataFrame()

    try:
        transformed = preprocessor.transform(row)
        if hasattr(transformed, "toarray"):
            transformed = transformed.toarray()
        explainer = shap.TreeExplainer(estimator)
        shap_values = explainer.shap_values(transformed)
    except Exception:
        return pd.DataFrame()

    if isinstance(shap_values, list):
        values = shap_values[-1][0]
    else:
        values = np.asarray(shap_values)[0]

    contributions = pd.DataFrame(
        {
            "feature": _feature_names(model),
            "contribution": values,
            "absolute_contribution": np.abs(values),
        }
    )
    return contributions.sort_values("absolute_contribution", ascending=False).head(max_features)


def fallback_contributions(model, sample: pd.Series, max_features: int = 8) -> pd.DataFrame:
    importance_df = get_feature_importance(model)
    if importance_df.empty:
        return pd.DataFrame()

    drivers = (
        importance_df.groupby("source_column", as_index=False)["importance"]
        .sum()
        .sort_values("importance", ascending=False)
    )
    drivers = drivers[drivers["source_column"].isin(sample.index)].head(max_features)
    if drivers.empty:
        return pd.DataFrame()

    return pd.DataFrame(
        {
            "feature": drivers["source_column"],
            "contribution": drivers["importance"],
            "absolute_contribution": drivers["importance"].abs(),
        }
    )
