import pandas as pd
import streamlit as st


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
            selected_sex = []

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

    filtered = df.copy()
    if counties:
        filtered = filtered[filtered["County"].astype(str).isin(selected_counties)]
    if selected_sex:
        filtered = filtered[filtered["respondent_sex"].astype(str).isin(selected_sex)]
    if age_range and "respondent_age" in filtered:
        age = pd.to_numeric(filtered["respondent_age"], errors="coerce")
        filtered = filtered[age.between(age_range[0], age_range[1])]
    return filtered
