# Project Summary

## Project Overview

The Financial Inclusion Predictor is a Streamlit dashboard and machine-learning application built around FinAccess 2021 data for Kenya. It helps users explore financial inclusion patterns, identify demographic and geographic differences, understand model drivers, and estimate whether a respondent is likely to be financially included.

The project includes:

- A cleaned dataset with 22,024 records.
- A Kenya county GeoJSON file for geographic visualization.
- A saved CatBoost model pipeline.
- Saved model metrics and model feature metadata.
- A multi-page Streamlit dashboard.
- Prediction and explainability utilities.

## Dashboard Overview

The dashboard has five pages:

- Overview: headline dataset and model metrics.
- Who and Where: demographic charts, county map, county ranking, and age distribution.
- Explainability: global feature-importance visualizations and explanation-readiness notes.
- Prediction Lab: editable respondent profile, prediction probability, confidence gauge, recommendations, and feature contributions.
- Data Preview: filtered data sample for inspection.

## Model Information

The saved champion model is `CatBoostClassifier`.

Current saved performance:

- Accuracy: 92.6%
- ROC-AUC: 0.983
- Target rate: 79.0%
- Recall for excluded class: 97.5%
- Recall for included class: 91.3%

The app uses the saved model and metrics from:

- `models/model.pkl`
- `models/model_metrics.json`

## Key Dashboard Work Completed

### Geographic Map

Confirmed that the dashboard still includes the geographic map visualization. The map appears on the Who and Where page as `County Inclusion Heatmap` and uses:

- `data/geo/kenya_counties.geojson`
- county-level inclusion rates
- Plotly `choropleth_map`

### Dashboard Readability Improvements

Improved dashboard-wide readability and clarity:

- Changed the dashboard background and surfaces to a clean light theme.
- Strengthened text contrast across headings, captions, labels, cards, and widgets.
- Fixed metric-card labels that were previously almost white on white.
- Improved metric-card wrapping so long values do not disappear.
- Reformatted `CatBoostClassifier` as `CatBoost Classifier` in the model snapshot.

### Chart Readability Improvements

Standardized chart readability across all dashboard charts:

- Darkened axis titles and tick labels.
- Added stronger grid and axis contrast.
- Added outlines to bars and histogram columns.
- Replaced low-contrast color scales with readable blue and blue/orange scales.
- Improved chart margins and auto-margins.
- Improved legends and colorbar text.
- Added dynamic chart heights for long feature-importance and contribution charts.

Affected chart areas:

- Financial inclusion split.
- Inclusion by sex.
- County inclusion heatmap.
- Top counties by inclusion rate.
- Age distribution by inclusion status.
- Global feature importance.
- Grouped source-column importance.
- Prediction Lab feature contribution panel.
- Prediction Lab confidence gauge.

### Dropdown and Form Readability

Fixed unclear dropdown/select options:

- Single-select dropdowns now use light popovers with dark option text.
- Multiselect menus inherit the same readable styling.
- Hovered and selected options have clear background contrast.
- Nested BaseWeb/Streamlit option text is forced to full opacity.

### Prediction Lab Improvements

The Prediction Lab now has clearer:

- Profile form fields.
- Select dropdown options.
- Prediction metric cards.
- Confidence gauge.
- Recommendation panels.
- Feature contribution chart.

## Files Changed During Dashboard Polish

- `dashboard/style.py`
- `dashboard/pages/overview.py`
- `dashboard/pages/prediction_lab.py`
- `src/config.py`
- `src/visualization/plotting.py`
- `src/visualization/charts.py`
- `src/explainability/importance.py`

Documentation added or updated:

- `README.md`
- `PROJECT_SUMMARY.md`
- `MODEL_CARD.md`

## Repository Hardening

The repository now includes:

- SHA-256 verification before loading the pickle model.
- Model/data provenance with package and Python versions.
- Dataset, metrics, model, and GeoJSON validation.
- User-facing errors for missing or malformed artifacts.
- A configurable artifact rebuild command using `--source-data` or `FINACCESS_SOURCE_DATA`.
- Consistent empty-selection behavior for County and Respondent Sex filters.
- Unit tests and a full repository artifact smoke test.
- GitHub Actions compilation and test checks.
- A model card describing intended use, limitations, privacy, and security considerations.

## GitHub Readiness

The project is ready to publish to GitHub as a standalone repository from the `Financial_Inclusion_Proje/` directory.

Recommended before pushing:

- Initialize Git inside `Financial_Inclusion_Proje/`, not from the parent user folder.
- Confirm `git status --short` only lists project files.
- Keep `__pycache__/`, virtual environments, logs, and secrets out of Git.
- Confirm that the included data/model artifacts are acceptable to publish.

Largest included files are below GitHub's normal 100 MB file limit:

- `data/processed/clean_data.csv`: about 7.9 MB
- notebook: about 3.4 MB
- county GeoJSON: about 1.2 MB
- saved model: about 0.25 MB

## Current Local Verification

The app has been checked locally at:

```text
http://localhost:8501
```

Verification performed:

- Python compile checks on edited modules.
- Browser checks on Overview.
- Browser checks on Who and Where.
- Browser checks on Explainability.
- Browser checks on Prediction Lab.
- Visual checks for labels, charts, map, gauge, dropdowns, and option menus.
