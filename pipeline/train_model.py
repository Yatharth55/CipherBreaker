import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np
from joblib import dump
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# ---------------- GPU DETECTION ---------------- #

USE_CUML = False
USE_XGB_GPU = False

try:
    from cuml.ensemble import RandomForestClassifier as cuRF
    from cuml.preprocessing import LabelEncoder as cuLabelEncoder
    import cupy as cp

    USE_CUML = True
    print("🚀 Using GPU via cuML")

except Exception:
    try:
        import xgboost as xgb
        from xgboost import XGBClassifier

        # Check GPU support
        try:
            _ = xgb.DeviceQuantileDMatrix
            USE_XGB_GPU = True
            print("🚀 Using GPU via XGBoost")
        except Exception:
            print("⚠️ XGBoost GPU not available")

    except ImportError:
        print("⚠️ No GPU libraries found, using CPU")

if not USE_CUML and not USE_XGB_GPU:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    print("⚠️ Using CPU (sklearn)")

# ---------------- PATHS ---------------- #

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "Data" / "dataset.csv"
MODELS_DIR = BASE_DIR / "Models"
MODEL_PATH = MODELS_DIR / "cipher_classifier.joblib"
METRICS_PATH = MODELS_DIR / "training_metrics.json"
LABEL_COLUMN = "cipher_type"


# ---------------- DATA LOADING ---------------- #

def load_dataset(dataset_path):
    dataset_path = Path(dataset_path)

    with dataset_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []

        if LABEL_COLUMN not in fieldnames:
            raise ValueError(f"Missing '{LABEL_COLUMN}' column")

        feature_names = [name for name in fieldnames if name.startswith("f")]

        features, labels = [], []

        for row in reader:
            features.append([float(row[name]) for name in feature_names])
            labels.append(row[LABEL_COLUMN].strip())

    return np.array(features, dtype=np.float32), np.array(labels), feature_names


def can_stratify(labels, test_size):
    counts = Counter(labels)
    if len(counts) < 2 or min(counts.values()) < 2:
        return False

    total = len(labels)
    test_n = int(total * test_size)
    train_n = total - test_n

    return test_n >= len(counts) and train_n >= len(counts)


# ---------------- TRAINING ---------------- #

def train_model(
    dataset_path=DATASET_PATH,
    model_path=MODEL_PATH,
    metrics_path=METRICS_PATH,
    test_size=0.2,
    random_state=42,
    n_estimators=300,
):
    features, labels, feature_names = load_dataset(dataset_path)

    # -------- cuML (BEST) -------- #
    if USE_CUML:
        label_encoder = cuLabelEncoder()
        encoded_labels = label_encoder.fit_transform(labels)

        stratify = encoded_labels if can_stratify(labels, test_size) else None

        X_train, X_test, y_train, y_test = train_test_split(
            features, encoded_labels, test_size=test_size,
            random_state=random_state, stratify=stratify
        )

        # Move to GPU
        X_train = cp.asarray(X_train)
        X_test = cp.asarray(X_test)
        y_train = cp.asarray(y_train)
        y_test = cp.asarray(y_test)

        model = cuRF(
            n_estimators=n_estimators,
            max_depth=16,
            n_streams=4,
            random_state=random_state,
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test).get()
        y_test_cpu = y_test.get()

    # -------- XGBOOST GPU -------- #
    elif USE_XGB_GPU:
        from sklearn.preprocessing import LabelEncoder

        label_encoder = LabelEncoder()
        encoded_labels = label_encoder.fit_transform(labels)

        stratify = encoded_labels if can_stratify(labels, test_size) else None

        X_train, X_test, y_train, y_test = train_test_split(
            features, encoded_labels, test_size=test_size,
            random_state=random_state, stratify=stratify
        )

        model = XGBClassifier(
            tree_method="gpu_hist",
            predictor="gpu_predictor",
            n_estimators=n_estimators,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=random_state,
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        y_test_cpu = y_test

    # -------- CPU FALLBACK -------- #
    else:
        from sklearn.preprocessing import LabelEncoder

        label_encoder = LabelEncoder()
        encoded_labels = label_encoder.fit_transform(labels)

        stratify = encoded_labels if can_stratify(labels, test_size) else None

        X_train, X_test, y_train, y_test = train_test_split(
            features, encoded_labels, test_size=test_size,
            random_state=random_state, stratify=stratify
        )

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            n_jobs=-1,
            random_state=random_state,
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        y_test_cpu = y_test

    # -------- METRICS -------- #

    decoded_truth = label_encoder.inverse_transform(y_test_cpu)
    decoded_predictions = label_encoder.inverse_transform(predictions)

    metrics = {
        "samples": len(features),
        "feature_count": len(feature_names),
        "accuracy": accuracy_score(y_test_cpu, predictions),
        "classification_report": classification_report(
            decoded_truth, decoded_predictions,
            output_dict=True, zero_division=0
        ),
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    dump({
        "model": model,
        "label_encoder": label_encoder,
        "feature_names": feature_names,
        "metrics": metrics,
    }, model_path)

    Path(metrics_path).write_text(json.dumps(metrics, indent=2))

    return metrics


# ---------------- CLI ---------------- #

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=str(DATASET_PATH))
    parser.add_argument("--model-out", default=str(MODEL_PATH))
    parser.add_argument("--metrics-out", default=str(METRICS_PATH))
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--n-estimators", type=int, default=300)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()

    metrics = train_model(
        dataset_path=args.dataset,
        model_path=args.model_out,
        metrics_path=args.metrics_out,
        test_size=args.test_size,
        random_state=args.random_state,
        n_estimators=args.n_estimators,
    )

    print(f"✅ Accuracy: {metrics['accuracy']:.4f}")