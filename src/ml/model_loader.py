from __future__ import annotations
import json
from functools import lru_cache
import joblib
import pandas as pd
from src.config import RF_MODEL_PATH, SVM_MODEL_PATH, GNB_MODEL_PATH, METADATA_PATH, METRICS_PATH

@lru_cache(maxsize=1)
def load_deployed_model():
    if not RF_MODEL_PATH.exists():
        raise FileNotFoundError("Random Forest model not found. Run python scripts/train_models.py first.")
    return joblib.load(RF_MODEL_PATH)

@lru_cache(maxsize=3)
def load_model(name: str):
    paths = {"Random Forest": RF_MODEL_PATH, "SVM": SVM_MODEL_PATH, "GaussianNB": GNB_MODEL_PATH}
    return joblib.load(paths[name])

@lru_cache(maxsize=1)
def load_metadata():
    if not METADATA_PATH.exists():
        return {}
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))

def load_metrics() -> pd.DataFrame:
    return pd.read_csv(METRICS_PATH) if METRICS_PATH.exists() else pd.DataFrame()
