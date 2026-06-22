import pandas as pd

from dashboard.filters import apply_filters


def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "County": ["Nairobi", "Nakuru", "Nairobi"],
            "respondent_sex": ["Female", "Male", "Male"],
            "respondent_age": [24, 40, 61],
        }
    )


def test_empty_county_selection_returns_no_records() -> None:
    assert apply_filters(sample_data(), selected_counties=[]).empty


def test_empty_sex_selection_returns_no_records() -> None:
    assert apply_filters(sample_data(), selected_sex=[]).empty


def test_filters_combine() -> None:
    result = apply_filters(
        sample_data(),
        selected_counties=["Nairobi"],
        selected_sex=["Male"],
        age_range=(50, 70),
    )
    assert result.index.tolist() == [2]
