from __future__ import annotations
import json
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from src.config import (
    FEATURE_COLUMNS, TARGET_COLUMN, MODELS_DIR, ARTIFACTS_DIR, RF_MODEL_PATH, SVM_MODEL_PATH,
    GNB_MODEL_PATH, METADATA_PATH, METRICS_PATH, FEATURE_IMPORTANCE_PATH
)
from src.ml.data_utils import load_dataset, build_metadata

def _save_report(y_true, y_pred, path):
    pd.DataFrame(classification_report(y_true, y_pred, output_dict=True, zero_division=0)).transpose().to_csv(path)

def _save_confusion(y_true, y_pred, labels, path, title):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(cm)
    ax.set_title(title)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=7)
    ax.set_yticklabels(labels, fontsize=7)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=6)
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)

def train_all_models():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "confusion_matrices").mkdir(parents=True, exist_ok=True)

    df = load_dataset()
    X, y = df[FEATURE_COLUMNS], df[TARGET_COLUMN]
    labels = sorted(y.unique().tolist())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

    models = {
        "Random Forest": Pipeline([("model", RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced"))]),
        "SVM": Pipeline([("scaler", StandardScaler()), ("model", SVC(kernel="rbf", C=10, gamma="scale", probability=True, random_state=42))]),
        "GaussianNB": Pipeline([("scaler", StandardScaler()), ("model", GaussianNB())]),
    }
    paths = {"Random Forest": RF_MODEL_PATH, "SVM": SVM_MODEL_PATH, "GaussianNB": GNB_MODEL_PATH}

    metric_rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metric_rows.append({
            "model": name,
            "accuracy": accuracy_score(y_test, pred),
            "precision_macro": precision_score(y_test, pred, average="macro", zero_division=0),
            "recall_macro": recall_score(y_test, pred, average="macro", zero_division=0),
            "f1_macro": f1_score(y_test, pred, average="macro", zero_division=0),
            "deployed": name == "Random Forest",
        })
        joblib.dump(model, paths[name])
        file_name = name.lower().replace(" ", "_")
        _save_report(y_test, pred, ARTIFACTS_DIR / f"{file_name}_classification_report.csv")
        _save_confusion(y_test, pred, labels, ARTIFACTS_DIR / "confusion_matrices" / f"{file_name}_confusion_matrix.png", f"{name} Confusion Matrix")

    pd.DataFrame(metric_rows).to_csv(METRICS_PATH, index=False)

    rf = models["Random Forest"].named_steps["model"]
    pd.DataFrame({"feature": FEATURE_COLUMNS, "importance": rf.feature_importances_}).sort_values("importance", ascending=False).to_csv(FEATURE_IMPORTANCE_PATH, index=False)

    metadata = build_metadata(df)
    metadata.update({
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "random_state": 42,
        "test_size": 0.2,
        "model_comparison": metric_rows,
    })
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (ARTIFACTS_DIR / "training_summary.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata

if __name__ == "__main__":
    train_all_models()
    print("Training completed. Random Forest remains the deployed model.")
