import argparse
import os
from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.artifacts import build_provenance, write_checksum, write_provenance


PROJECT_DIR = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = PROJECT_DIR.parent

RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
MODELS_DIR = PROJECT_DIR / "models"

DEFAULT_DATA_FILE = WORKSPACE_DIR / "Updated Anonymized Weighted FinAccess 2021_clean.xlsx"
KEEP_FILE = RAW_DIR / "FINACCESS_KEEP_COLUMNS.csv"
RENAME_FILE = RAW_DIR / "FINACCESS_RENAME_TABLE.csv"

MISSING_CODE = -999999999
TARGET_COL = "financially_included"
TARGET_SOURCE_COLS = ["bank_usage", "mobile_money_usage", "insurance_usage"]


def resolve_source_data(source_data: str | Path | None = None) -> Path:
    configured = source_data or os.environ.get("FINACCESS_SOURCE_DATA") or DEFAULT_DATA_FILE
    path = Path(configured).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"Source workbook not found: {path}. Pass --source-data or set FINACCESS_SOURCE_DATA."
        )
    return path


def load_selected_data(data_file: Path) -> pd.DataFrame:
    keep_columns = pd.read_csv(KEEP_FILE, header=None)[0].dropna().tolist()
    rename_df = pd.read_csv(RENAME_FILE)
    coded_columns = [
        "ClusterNo",
        "A9",
        "A10i",
        "A19",
        "A21",
        "A21i",
        "A23",
        "B1H_I",
        "B3A__1",
        "B3A__2",
        "B3A__3",
        "B3A__4",
        "B3A__5",
        "B3A__6",
        "B3A__7",
        "B3A__8",
        "B3A__9",
        "B3I",
        "C4",
        "D1B__14",
        "D1C__14",
        "E3__9",
        "E3__17",
        "F2__12",
        "H1B__17",
        "J1__10",
        "K2__11",
        "N2__6",
        "T4",
        "T5",
        "T6",
        "T7",
        "T8",
        "T9",
    ]
    rename_map = (
        rename_df[rename_df["original_name"].isin(coded_columns)]
        .set_index("original_name")["new_name"]
        .to_dict()
    )

    df = pd.read_excel(data_file, sheet_name="Dataset", usecols=keep_columns, engine="openpyxl")
    df = df.rename(columns=rename_map)
    df.columns = df.columns.str.strip()
    return df


def create_target(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.replace(MISSING_CODE, np.nan)
    out[TARGET_SOURCE_COLS] = out[TARGET_SOURCE_COLS].fillna("Never had")
    out[TARGET_COL] = (
        (out["bank_usage"] == "Currently have")
        | (out["mobile_money_usage"] == "Currently have")
        | (out["insurance_usage"] == "Currently have")
    ).astype(int)
    return out


def build_model(df: pd.DataFrame) -> tuple[Pipeline, dict]:
    exclude_cols = TARGET_SOURCE_COLS + [
        TARGET_COL,
        "Serial Number",
        "interview__key",
        "interview__id",
        "ClusterNo",
        "HHNo",
    ]

    X = df.drop(columns=exclude_cols, errors="ignore").replace({pd.NA: np.nan})
    y = df[TARGET_COL]

    categorical_features = X.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    numeric_features = X.select_dtypes(include=["number"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            (
                "model",
                CatBoostClassifier(
                    iterations=200,
                    depth=6,
                    learning_rate=0.1,
                    loss_function="Logloss",
                    auto_class_weights="Balanced",
                    random_state=42,
                    thread_count=1,
                    verbose=0,
                ),
            ),
        ]
    )

    stratify = y if y.nunique() == 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    metrics = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "champion_model": "CatBoostClassifier",
        "features": X.columns.tolist(),
        "target_rate": float(y.mean()),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "classification_report": classification_report(y_test, predictions, output_dict=True),
    }

    model.fit(X, y)
    return model, metrics


def main(source_data: str | Path | None = None) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    clean_data_path = PROCESSED_DIR / "clean_data.csv"
    root_clean_data_path = PROJECT_DIR / "clean_data.csv"
    configured_source = source_data or os.environ.get("FINACCESS_SOURCE_DATA")
    if configured_source:
        source_path = resolve_source_data(configured_source)
        clean_df = create_target(load_selected_data(source_path))
        clean_df.to_csv(clean_data_path, index=False)
        source_label = str(source_path)
    elif clean_data_path.exists():
        clean_df = pd.read_csv(clean_data_path)
        source_label = str(clean_data_path)
    elif root_clean_data_path.exists():
        clean_df = pd.read_csv(root_clean_data_path)
        clean_df.to_csv(clean_data_path, index=False)
        source_label = str(root_clean_data_path)
    else:
        source_path = resolve_source_data(source_data)
        clean_df = create_target(load_selected_data(source_path))
        clean_df.to_csv(clean_data_path, index=False)
        source_label = str(source_path)

    model, metrics = build_model(clean_df)
    model_path = MODELS_DIR / "model.pkl"
    with model_path.open("wb") as f:
        pickle.dump(model, f)

    checksum_path = MODELS_DIR / "model.sha256"
    model_checksum = write_checksum(model_path, checksum_path)

    provenance_path = MODELS_DIR / "model_provenance.json"
    provenance = build_provenance(
        model_path=model_path,
        data_path=clean_data_path,
        source_data=source_label,
        model_checksum=model_checksum,
    )
    write_provenance(provenance_path, provenance)

    metrics_path = MODELS_DIR / "model_metrics.json"
    metrics["artifact"] = {
        "model_sha256": model_checksum,
        "generated_at_utc": provenance["generated_at_utc"],
        "processed_data_sha256": provenance["processed_data_sha256"],
    }
    pd.Series(metrics).to_json(metrics_path, indent=2)

    print(f"Saved clean data: {clean_data_path}")
    print(f"Saved model: {model_path}")
    print(f"Saved checksum: {checksum_path}")
    print(f"Saved provenance: {provenance_path}")
    print(f"Rows: {metrics['rows']:,}")
    print(f"Target rate: {metrics['target_rate']:.3f}")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build dashboard data and model artifacts.")
    parser.add_argument(
        "--source-data",
        help="Path to the FinAccess Excel workbook. Can also use FINACCESS_SOURCE_DATA.",
    )
    args = parser.parse_args()
    main(source_data=args.source_data)
