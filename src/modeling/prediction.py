import pandas as pd

from src.config import TARGET_COL


EXCLUDED_FEATURES = {
    TARGET_COL,
    "bank_usage",
    "mobile_money_usage",
    "insurance_usage",
}

EDITABLE_FIELDS = [
    "County",
    "respondent_sex",
    "respondent_age",
    "education",
    "monthly_income_ksh",
    "incomegp",
    "trusted_financial_provider",
    "mobile_money_access",
    "mobile_money_active",
    "cost_to_nearest_bank",
    "walk_time_to_nearest_bank",
    "cost_to_nearest_mobile_money_agent",
    "walk_time_to_nearest_mobile_money_agent",
]


def field_label(field: str) -> str:
    return field.replace("_", " ").title()


def model_feature_columns(df: pd.DataFrame, metrics: dict) -> list[str]:
    return metrics.get("features") or [col for col in df.columns if col not in EXCLUDED_FEATURES]


def editable_feature_columns(df: pd.DataFrame, feature_columns: list[str]) -> list[str]:
    return [field for field in EDITABLE_FIELDS if field in feature_columns and field in df]


def default_value(series: pd.Series):
    if pd.api.types.is_numeric_dtype(series):
        return float(pd.to_numeric(series, errors="coerce").median())
    values = series.dropna()
    if values.empty:
        return ""
    return str(values.mode().iloc[0])


def probability_band(probability: float) -> tuple[str, str]:
    if probability >= 0.80:
        return "High likelihood", "This respondent shows a high likelihood of financial inclusion."
    if probability >= 0.50:
        return "Moderate likelihood", "This respondent shows a moderate likelihood of financial inclusion."
    return "High exclusion risk", "This respondent is at high risk of financial exclusion."


def as_yes(value: object) -> bool:
    return str(value).strip().lower() in {"yes", "y", "1", "true"}


def contributing_factors(sample: pd.Series) -> list[str]:
    reasons = []
    if as_yes(sample.get("mobile_money_access")):
        reasons.append("Mobile money access")
    if as_yes(sample.get("mobile_money_active")):
        reasons.append("Active mobile money use")
    if as_yes(sample.get("trusted_financial_provider")):
        reasons.append("Trust in financial providers")
    if pd.to_numeric(sample.get("respondent_age"), errors="coerce") > 30:
        reasons.append("Higher age demographic")
    if pd.to_numeric(sample.get("monthly_income_ksh"), errors="coerce") > 0:
        reasons.append("Reported monthly income")
    return reasons


def recommendations(sample: pd.Series, probability: float) -> list[str]:
    output = []
    if probability < 0.50:
        output.append("Prioritize outreach for formal account access and digital finance onboarding.")
    elif probability < 0.80:
        output.append("Strengthen the respondent's path from access to active formal financial use.")
    else:
        output.append("Maintain access quality and identify which services are sustaining inclusion.")

    if not as_yes(sample.get("mobile_money_access")):
        output.append("Improve mobile money access or proximity to agents.")
    if not as_yes(sample.get("trusted_financial_provider")):
        output.append("Address trust barriers through transparent product information and community channels.")
    return output
