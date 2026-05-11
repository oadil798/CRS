from __future__ import annotations
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
APP_NAME = "Crop Recommendation System"
APP_ICON = "🌾"
APP_VERSION = "Professional FYP Build"

DATASET_PATH = BASE_DIR / "data" / "raw" / "Crop_recommendation.csv"
DATABASE_PATH = BASE_DIR / "data" / "app_data.db"
MODELS_DIR = BASE_DIR / "models"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
CROP_IMAGES_DIR = BASE_DIR / "assets" / "crops"
BACKGROUNDS_DIR = BASE_DIR / "assets" / "backgrounds"
STYLE_PATH = BASE_DIR / "assets" / "styles" / "main.css"

FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET_COLUMN = "label"

RF_MODEL_PATH = MODELS_DIR / "random_forest_pipeline.joblib"
SVM_MODEL_PATH = MODELS_DIR / "svm_pipeline.joblib"
GNB_MODEL_PATH = MODELS_DIR / "gaussiannb_pipeline.joblib"
METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"
METRICS_PATH = ARTIFACTS_DIR / "metrics_summary.csv"
FEATURE_IMPORTANCE_PATH = ARTIFACTS_DIR / "rf_feature_importance.csv"

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "Admin@123"
DEFAULT_USER_USERNAME = "demo"
DEFAULT_USER_PASSWORD = "Demo@123"
