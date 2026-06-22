import pandas as pd
import streamlit as st


def apply_filters(
    df: pd.DataFrame,
    selected_counties: list[str] | None = None,
    selected_sex: list[str] | None = None,
    age_range: tuple[int, int] | None = None,
) -> pd.DataFrame:
    filtered = df.copy()
    if selected_counties is not None and "County" in filtered:
        filtered = filtered[filtered["County"].astype(str).isin(selected_counties)]
    if selected_sex is not None and "respondent_sex" in filtered:
        filtered = filtered[filtered["respondent_sex"].astype(str).isin(selected_sex)]
    if age_range is not None and "respondent_age" in filtered:
        age = pd.to_numeric(filtered["respondent_age"], errors="coerce")
        filtered = filtered[age.between(age_range[0], age_range[1])]
    return filtered


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.divider()
        st.header("Filters")
        counties = sorted(df["County"].dropna().astype(str).unique()) if "County" in df else []
        selected_counties = st.multiselect("County", counties, default=counties)

        if "respondent_sex" in df:
            sex_options = sorted(df["respondent_sex"].dropna().astype(str).unique())
            selected_sex = st.multiselect("Respondent sex", sex_options, default=sex_options)
        else:
            selected_sex = None

        if "respondent_age" in df:
            age_values = pd.to_numeric(df["respondent_age"], errors="coerce").dropna()
            if age_values.empty:
                age_range = None
            else:
                min_age = int(age_values.min())
                max_age = int(age_values.max())
                age_range = st.slider("Age range", min_age, max_age, (min_age, max_age))
        else:
            age_range = None

    return apply_filters(
        df,
        selected_counties=selected_counties if counties else None,
        selected_sex=selected_sex,
        age_range=age_range,
    )
