from __future__ import annotations
from typing import Dict, List
import pandas as pd
from src.config import FEATURE_COLUMNS
from src.ml.model_loader import load_deployed_model, load_metadata

# Broad physical/system limits. These protect impossible values such as negative rainfall
# or pH above 14. Dataset-range validation below protects misleading ML extrapolation.
HARD_LIMITS = {
    "N": (0, 200, "Nitrogen should be non-negative and normally below 200 for this dataset style."),
    "P": (0, 200, "Phosphorus should be non-negative and normally below 200 for this dataset style."),
    "K": (0, 250, "Potassium should be non-negative and normally below 250 for this dataset style."),
    "temperature": (0, 60, "Temperature looks outside a practical agricultural range."),
    "humidity": (0, 100, "Humidity must be between 0% and 100%."),
    "ph": (0, 14, "pH must be between 0 and 14."),
    "rainfall": (0, 500, "Rainfall should be non-negative and normally below 500 mm for this dataset style."),
}

FEATURE_DISPLAY_NAMES = {
    "N": "Nitrogen / N",
    "P": "Phosphorus / P",
    "K": "Potassium / K",
    "temperature": "Temperature (°C)",
    "humidity": "Humidity (%)",
    "ph": "pH",
    "rainfall": "Rainfall (mm)",
}


def build_basic_input(temperature: float, humidity: float, rainfall: float) -> Dict[str, float]:
    metadata = load_metadata()
    med = metadata.get("feature_medians", {})
    return {
        "N": float(med.get("N", 37)),
        "P": float(med.get("P", 51)),
        "K": float(med.get("K", 32)),
        "temperature": float(temperature),
        "humidity": float(humidity),
        "ph": float(med.get("ph", 6.43)),
        "rainfall": float(rainfall),
    }


def build_advanced_input(N, P, K, temperature, humidity, ph, rainfall) -> Dict[str, float]:
    return {
        "N": float(N),
        "P": float(P),
        "K": float(K),
        "temperature": float(temperature),
        "humidity": float(humidity),
        "ph": float(ph),
        "rainfall": float(rainfall),
    }


def get_feature_ranges() -> Dict[str, Dict[str, float]]:
    """Return min/max/mean/median ranges learned from the training dataset metadata."""
    metadata = load_metadata()
    return metadata.get("feature_ranges", {})


def validate_inputs(values: Dict[str, float]) -> List[str]:
    """Soft warnings used for display after a valid prediction.

    This function remains for informative warnings. The actual blocking check is
    handled by get_blocking_input_errors() before prediction.
    """
    warnings: List[str] = []
    for feature, value in values.items():
        low, high, msg = HARD_LIMITS.get(feature, (None, None, None))
        if low is not None and (value < low or value > high):
            warnings.append(f"{feature}: {msg}")
    return warnings


def get_blocking_input_errors(values: Dict[str, float]) -> List[str]:
    """Block predictions outside the dataset's learned range.

    A scikit-learn classifier can technically output a crop for any numeric row,
    even unrealistic inputs such as all zeros. For an FYP/agriculture system, that
    is misleading, so the app blocks out-of-dataset predictions and asks the user
    to enter values within the training range.
    """
    ranges = get_feature_ranges()
    errors: List[str] = []

    for feature in FEATURE_COLUMNS:
        value = float(values.get(feature, 0.0))
        display_name = FEATURE_DISPLAY_NAMES.get(feature, feature)

        hard_low, hard_high, hard_msg = HARD_LIMITS.get(feature, (None, None, None))
        if hard_low is not None and (value < hard_low or value > hard_high):
            errors.append(f"{display_name}: {hard_msg} Entered value: {value:.2f}.")
            continue

        if feature in ranges:
            mn = float(ranges[feature]["min"])
            mx = float(ranges[feature]["max"])
            if value < mn or value > mx:
                errors.append(
                    f"{display_name}: entered {value:.2f}, but the accepted dataset range is {mn:.2f} to {mx:.2f}."
                )

    return errors


def confidence_level(confidence: float) -> str:
    if confidence >= 0.80:
        return "High"
    if confidence >= 0.55:
        return "Moderate"
    return "Low"


def confidence_explanation(level: str) -> str:
    return {
        "High": "The Random Forest model strongly prefers this crop based on the dataset patterns.",
        "Moderate": "The model has a reasonable preference, but similar crops may also be possible.",
        "Low": "The model is uncertain. Advanced Mode inputs and real soil testing are recommended.",
    }[level]


def predict_crop(values: Dict[str, float]) -> Dict:
    blocking_errors = get_blocking_input_errors(values)
    if blocking_errors:
        raise ValueError("Prediction blocked because one or more inputs are outside the trained dataset range.")

    model = load_deployed_model()
    df = pd.DataFrame([[values[c] for c in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    prediction = str(model.predict(df)[0])
    probabilities = model.predict_proba(df)[0]
    classes = list(model.classes_)
    ranked = sorted(zip(classes, probabilities), key=lambda item: item[1], reverse=True)
    top = [{"crop": str(c), "probability": float(p)} for c, p in ranked[:5]]
    conf = float(top[0]["probability"])
    level = confidence_level(conf)
    return {
        "recommended_crop": prediction,
        "confidence": conf,
        "confidence_level": level,
        "confidence_explanation": confidence_explanation(level),
        "top_candidates": top,
        "warnings": validate_inputs(values),
    }
