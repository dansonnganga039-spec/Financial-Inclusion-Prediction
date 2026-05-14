from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
GEO_DATA_DIR = DATA_DIR / "geo"
MODELS_DIR = PROJECT_DIR / "models"

DATA_PATH = PROCESSED_DATA_DIR / "clean_data.csv"
COUNTY_GEOJSON_PATH = GEO_DATA_DIR / "kenya_counties.geojson"
MODEL_PATH = MODELS_DIR / "model.pkl"
METRICS_PATH = MODELS_DIR / "model_metrics.json"

TARGET_COL = "financially_included"
CHART_COLORS = {"Included": "#2563eb", "Excluded": "#d97706"}

APP_TITLE = "Financial Inclusion Predictor"
APP_SUBTITLE = "FinAccess 2021 dashboard and prediction model"
