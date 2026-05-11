from __future__ import annotations
from typing import Dict
import pandas as pd
from src.config import DATASET_PATH, FEATURE_COLUMNS, TARGET_COLUMN

def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    required = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")
    return df[required].copy()

def build_metadata(df: pd.DataFrame) -> Dict:
    return {
        "dataset_rows": int(len(df)),
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "crop_labels": sorted(df[TARGET_COLUMN].unique().tolist()),
        "number_of_crops": int(df[TARGET_COLUMN].nunique()),
        "feature_medians": {c: float(df[c].median()) for c in FEATURE_COLUMNS},
        "feature_ranges": {
            c: {
                "min": float(df[c].min()),
                "max": float(df[c].max()),
                "mean": float(df[c].mean()),
                "median": float(df[c].median()),
            }
            for c in FEATURE_COLUMNS
        },
        "deployed_model": "Random Forest",
        "basic_mode_note": "Basic Mode uses dataset median/default values for N, P, K, and pH.",
    }
