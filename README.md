# Financial Inclusion Predictor

A Streamlit dashboard and prediction tool for exploring financial inclusion patterns in Kenya using FinAccess 2021 data. The app combines summary metrics, demographic visuals, county-level geographic mapping, global model explainability, and a respondent-level prediction lab powered by a saved CatBoost model.

## Project Status

The project is ready to publish to GitHub as a standalone repository from the `Financial_Inclusion_Proje/` folder. The dataset, county GeoJSON, trained model, metrics, app code, and dependency files are all included in the project folder.

Important GitHub note: initialize Git inside this folder only. The current machine has a parent Git context above this project, so running Git commands from `C:\Users\ADMIN` may accidentally include unrelated user files.

## Features

- Interactive Streamlit dashboard with sidebar navigation and filters.
- Overview metrics for filtered records, inclusion counts, exclusion counts, ROC-AUC, target rate, and model summary.
- Demographic charts for inclusion split, sex-based inclusion rate, and age distribution.
- Kenya county choropleth map showing county-level inclusion rates.
- Top county ranking chart and supporting county summary table.
- Global model explainability through feature-importance charts.
- Prediction Lab for respondent-level inclusion probability scoring.
- Confidence gauge, probability band, contributing factors, recommendations, and feature contribution panel.
- High-contrast visual styling for metric cards, dropdowns, chart labels, chart axes, map colors, legends, and colorbars.

## Dashboard Pages

### Overview

Shows high-level metrics for the filtered dataset and saved model:

- Records
- Included respondents
- Excluded respondents
- Model ROC-AUC
- Rows in training data
- Champion model
- Target rate

### Who and Where

Explores who is affected and where inclusion differs:

- Financial inclusion split
- Inclusion by respondent sex
- County inclusion heatmap
- Top counties by inclusion rate
- Age distribution by inclusion status

### Explainability

Shows the strongest model drivers:

- Top encoded feature importances
- Grouped source-column importance
- Notes on local explanation readiness

### Prediction Lab

Lets a user edit a respondent profile and generate an inclusion probability:

- Profile, Access, and Trust tabs
- Prediction result
- Dataset-average comparison
- Confidence band
- Gauge visualization
- Recommended decision-support actions
- Feature contribution panel

### Data Preview

Shows the first 100 rows from the filtered dataset.

## Model Summary

The saved model is a `CatBoostClassifier`.

Current saved metrics:

- Rows: `22,024`
- Columns: `48`
- Target rate: `79.0%`
- Accuracy: `92.6%`
- ROC-AUC: `0.983`
- Recall for financially excluded respondents: `97.5%`
- Recall for financially included respondents: `91.3%`

These values are stored in `models/model_metrics.json`.

## Project Structure

```text
Financial_Inclusion_Proje/
  app.py                         Streamlit app entry point and page router
  requirements.txt               Python dependencies
  runtime.txt                    Python runtime hint for deployment
  run_dashboard.bat              Windows helper for local launch
  .gitignore                     Git exclusions
  .streamlit/
    config.toml                  Streamlit server/theme config
  dashboard/
    filters.py                   Sidebar filters
    navigation.py                Sidebar navigation
    style.py                     Dashboard CSS and readability overrides
    pages/
      overview.py                Overview page
      visuals.py                 Who and Where page
      explainability.py          Explainability page
      prediction_lab.py          Prediction Lab page
      data_preview.py            Data Preview page
  data/
    geo/
      kenya_counties.geojson     County boundary file for the map
    processed/
      clean_data.csv             Clean dashboard dataset
    raw/
      FINACCESS_KEEP_COLUMNS.csv Column selection metadata
      FINACCESS_RENAME_TABLE.csv Column rename metadata
  models/
    model.pkl                    Saved trained model pipeline
    model_metrics.json           Saved model metrics and feature list
  notebooks/
    Financial Inclusion Predictor.ipynb
  src/
    config.py                    Shared paths, constants, and chart colors
    data.py                      Cached data/model/metrics loaders
    utils.py                     Shared helper functions
    preprocessing/
      build_artifacts.py         Rebuild workflow for data/model artifacts
    modeling/
      prediction.py              Prediction Lab helper logic
    explainability/
      importance.py              Global feature-importance charts
      local.py                   SHAP/fallback contribution helpers
    visualization/
      charts.py                  Dashboard charts and county map
      plotting.py                Shared Plotly styling and gauge
```

## Requirements

- Python 3.12
- Streamlit
- Pandas
- Plotly
- CatBoost
- Scikit-learn
- SHAP

Install dependencies from `requirements.txt`.

## Run Locally

From inside the project folder:

```powershell
cd "C:\Users\ADMIN\Documents\New project\Financial_Inclusion_Proje"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

If you already have the existing virtual environment from the parent workspace, you can run:

```powershell
..\.venv\Scripts\streamlit.exe run app.py
```

## Rebuild Artifacts

Only rebuild artifacts if the source data, selected columns, rename mapping, or model workflow changes.

```powershell
python -m src.preprocessing.build_artifacts
```

Canonical artifacts live here:

- `data/processed/clean_data.csv`
- `data/geo/kenya_counties.geojson`
- `models/model.pkl`
- `models/model_metrics.json`

## Deployment Notes

For Streamlit Community Cloud or similar hosting:

- Main file: `app.py`
- Python runtime hint: `runtime.txt`
- Dependencies: `requirements.txt`
- Required data/model artifacts are already inside `data/` and `models/`.
- Do not deploy duplicate root-level `clean_data.csv` or `model.pkl`; canonical copies live under `data/` and `models/`.

## GitHub Setup

Run these commands from the project folder:

```powershell
cd "C:\Users\ADMIN\Documents\New project\Financial_Inclusion_Proje"
git init
git add .
git commit -m "Initial financial inclusion dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Before pushing, confirm `git status --short` only shows files inside `Financial_Inclusion_Proje/`.

## Notes

- `__pycache__/`, virtual environments, logs, Streamlit secrets, and duplicate root artifacts are ignored by `.gitignore`.
- The dashboard uses light-theme, high-contrast styling for readability.
- The county map depends on matching county names in the processed data to keys in the GeoJSON file.
