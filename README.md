# Financial Inclusion Predictor

A Streamlit analytical dashboard for exploring financial inclusion patterns in Kenya using FinAccess 2021 data. The app combines reusable preprocessing artifacts, a saved CatBoost model, visual analytics, global explainability, and respondent-level prediction support.

## What The System Does

- Presents high-level financial inclusion metrics for filtered records.
- Explores demographic and county-level inclusion patterns.
- Scores a respondent profile with the saved model.
- Shows model confidence, confidence level, key drivers, and action-oriented recommendations.
- Provides global feature-importance views and prediction-level explanation fallbacks.

## System Workflow

```text
FinAccess raw dataset
  -> preprocessing pipeline
  -> target engineering
  -> feature preparation
  -> model training
  -> evaluation
  -> saved artifacts
  -> dashboard inference
  -> explainability system
  -> visual analytics
  -> user interaction
```

## Project Structure

```text
Financial_Inclusion_Proje/
  app.py                         Streamlit entry point and page router
  requirements.txt               Python dependencies
  requirements-dev.txt           Test/development dependencies
  runtime.txt                    Python runtime hint for deployment
  MODEL_CARD.md                  Intended use, limitations, and safeguards
  PROJECT_SUMMARY.md             Project and dashboard change summary
  run_dashboard.bat              Windows helper for local launch
  .gitignore                     Git exclusions
  .streamlit/
    config.toml                  Streamlit server and theme config
  dashboard/
    filters.py                   Sidebar filters
    navigation.py                Sidebar page selection
    style.py                     Dashboard CSS and readability overrides
    pages/
      overview.py                Overview page
      visuals.py                 Who and Where page
      explainability.py          Explainability page
      prediction_lab.py          Prediction Lab page
      data_preview.py            Filtered data preview page
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
    model.sha256                 Model integrity checksum
    model_metrics.json           Saved model metrics and feature list
    model_provenance.json        Data/model hashes and environment metadata
  notebooks/
    Financial Inclusion Predictor.ipynb
  src/
    config.py                    Shared paths, constants, and chart colors
    data.py                      Cached data/model/metrics loaders
    utils.py                     Shared helper functions
    preprocessing/
      build_artifacts.py         Data/model artifact rebuild workflow
    modeling/
      prediction.py              Prediction Lab helper logic
    explainability/
      importance.py              Global feature-importance charts
      local.py                   SHAP/fallback contribution helpers
    visualization/
      charts.py                  Dashboard charts and county map
      plotting.py                Shared Plotly styling and gauge
  tests/                         Unit and repository artifact smoke tests
  .github/workflows/ci.yml       GitHub Actions compile/test workflow
```

## Architecture Notes

`app.py` is intentionally thin. It configures Streamlit, loads shared artifacts, applies filters, and routes to page renderers. Heavy analytical work lives under `src/`, while dashboard-specific layout lives under `dashboard/`.

Reusable layers:

- `src.data`: cached artifact loading.
- `src.preprocessing`: artifact rebuild workflow.
- `src.modeling`: prediction helper logic.
- `src.explainability`: global and local explanation logic.
- `src.visualization`: reusable chart and gauge builders.

Tightly coupled layers:

- `dashboard/pages/*`: Streamlit presentation and page layout.
- `src.visualization.charts`: chart assumptions tied to the processed dataset columns.
- `src.preprocessing.build_artifacts`: depends on local raw data and metadata files.

Operationally fragile layers:

- Model artifact loading from `models/model.pkl`.
- SHAP availability in the deployment environment.
- County name matching between processed data and `data/geo/kenya_counties.geojson`.

## Requirements

- Python 3.14
- Streamlit
- Pandas
- Plotly
- CatBoost
- Scikit-learn
- SHAP
- OpenPyXL, used only when rebuilding artifacts from the Excel source data

Install the exact runtime dependency set from `requirements.txt`. Contributors can install
`requirements-dev.txt` to include the test tooling.

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
python -m src.preprocessing.build_artifacts --source-data "C:\path\to\FinAccess.xlsx"
```

Alternatively, set `FINACCESS_SOURCE_DATA` before running the module:

```powershell
$env:FINACCESS_SOURCE_DATA="C:\path\to\FinAccess.xlsx"
python -m src.preprocessing.build_artifacts
```

If neither option is supplied, the builder checks the historical parent-workspace location. A successful rebuild regenerates the model, metrics, checksum, and provenance files.

Canonical artifacts live here:

- `data/processed/clean_data.csv`
- `data/geo/kenya_counties.geojson`
- `models/model.pkl`
- `models/model.sha256`
- `models/model_metrics.json`
- `models/model_provenance.json`

## Tests

```powershell
pip install -r requirements-dev.txt
pytest
```

The test suite covers target creation, filter semantics, data/metrics validation, model integrity verification, and loading the repository artifacts. GitHub Actions runs compilation and tests on pushes to `main` and on pull requests.

## Model Snapshot

The saved champion model is a `CatBoostClassifier`.

Current saved metrics:

- Rows: `22,024`
- Columns: `48`
- Target rate: `79.0%`
- Accuracy: `92.6%`
- ROC-AUC: `0.983`
- Recall for financially excluded respondents: `97.5%`
- Recall for financially included respondents: `91.3%`

These values are stored in `models/model_metrics.json`.

## Deployment Notes

For Streamlit Community Cloud or similar hosting:

- Main file: `app.py`
- Python runtime hint: `runtime.txt`
- Dependencies: `requirements.txt`
- Required data/model artifacts are included under `data/` and `models/`.
- Streamlit server and theme settings are in `.streamlit/config.toml`.
- Do not deploy duplicate root-level `clean_data.csv` or `model.pkl`; canonical copies live under `data/` and `models/`.

The saved `models/model.pkl` file is included because the dashboard needs it at runtime. If future deployment policy moves model artifacts to external storage, add `models/*.pkl` to `.gitignore` and document the retrieval step.

## Artifact Integrity And Security

Before unpickling the saved model, the application verifies it against `models/model.sha256`. Rebuilds also record model/data hashes and environment versions in `models/model_provenance.json`.

Checksum verification detects corruption and mismatched artifacts, but it does not make pickle safe when a model and checksum both come from an untrusted source. Only run artifacts from a trusted, reviewed commit. See `MODEL_CARD.md` for intended use, limitations, and evaluation gaps.

## GitHub Setup

Important: initialize Git inside this folder only. The current machine has a parent Git context above this project, so running Git commands from `C:\Users\ADMIN` may accidentally include unrelated user files.

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

## Explainability Guidance

The explainability views are designed for decision support, not causal claims. Feature importance and contribution panels show the strongest model signals behind a prediction. They should be read as directional model evidence, not as proof that a factor caused inclusion or exclusion.

For non-technical users, prefer these terms:

- "Model confidence" instead of "probability threshold".
- "Confidence level" instead of "band".
- "Key drivers" instead of "raw feature importance".
- "Selected profile value" instead of "input feature value".

## Notes

- `__pycache__/`, virtual environments, logs, Streamlit secrets, and duplicate root artifacts are ignored by `.gitignore`.
- The dashboard uses a light, high-contrast theme for readability.
- The county map depends on matching county names in the processed data to keys in the GeoJSON file.
- Missing, malformed, or checksum-mismatched artifacts are reported with user-facing dashboard errors.
