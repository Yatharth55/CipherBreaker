import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "Data" / "dataset.csv"
MODELS_DIR = BASE_DIR / "Models"
MODEL_PATH = MODELS_DIR / "cipher_classifier.joblib"
METRICS_PATH = MODELS_DIR / "training_metrics.json"
LABEL_COLUMN = "cipher_type"


def load_dataset(dataset_path):
    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    with dataset_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []

        if not fieldnames:
            raise ValueError(f"Dataset file is empty: {dataset_path}")

        if LABEL_COLUMN not in fieldnames:
            raise ValueError(f"Dataset must contain a '{LABEL_COLUMN}' column.")

        feature_names = [name for name in fieldnames if name.startswith("f")]
        if not feature_names:
            raise ValueError("Dataset must contain at least one feature column.")

        features = []
        labels = []

        for row_number, row in enumerate(reader, start=2):
            label = (row.get(LABEL_COLUMN) or "").strip()
            if not label:
                raise ValueError(f"Missing label value on row {row_number}.")

            try:
                feature_row = [float(row[name]) for name in feature_names]
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid numeric feature value on row {row_number}."
                ) from exc

            features.append(feature_row)
            labels.append(label)

    if not features:
        raise ValueError(f"Dataset contains no samples: {dataset_path}")

    return features, labels, feature_names


def can_stratify(labels, test_size):
    label_counts = Counter(labels)

    if len(label_counts) < 2:
        return False

    if min(label_counts.values()) < 2:
        return False

    total_samples = len(labels)
    test_samples = max(1, int(round(total_samples * test_size)))
    train_samples = total_samples - test_samples

    return test_samples >= len(label_counts) and train_samples >= len(label_counts)


def train_model(
    dataset_path=DATASET_PATH,
    model_path=MODEL_PATH,
    metrics_path=METRICS_PATH,
    test_size=0.2,
    random_state=42,
    n_estimators=300,
):
    features, labels, feature_names = load_dataset(dataset_path)

    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)

    stratify_labels = encoded_labels if can_stratify(labels, test_size) else None

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        encoded_labels,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_labels,
    )

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    decoded_truth = label_encoder.inverse_transform(y_test)
    decoded_predictions = label_encoder.inverse_transform(predictions)

    metrics = {
        "dataset_path": str(Path(dataset_path).resolve()),
        "samples": len(features),
        "feature_count": len(feature_names),
        "labels": list(label_encoder.classes_),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": accuracy_score(y_test, predictions),
        "classification_report": classification_report(
            decoded_truth,
            decoded_predictions,
            output_dict=True,
            zero_division=0,
        ),
    }

    model_path = Path(model_path)
    metrics_path = Path(metrics_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "label_encoder": label_encoder,
        "feature_names": feature_names,
        "metrics": metrics,
    }

    dump(artifact, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    return metrics


def build_parser():
    parser = argparse.ArgumentParser(
        description="Train a cipher classifier from Data/dataset.csv."
    )
    parser.add_argument(
        "--dataset",
        default=str(DATASET_PATH),
        help="Path to the dataset CSV file.",
    )
    parser.add_argument(
        "--model-out",
        default=str(MODEL_PATH),
        help="Where to save the trained model artifact.",
    )
    parser.add_argument(
        "--metrics-out",
        default=str(METRICS_PATH),
        help="Where to save the training metrics JSON.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of samples reserved for evaluation.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed used for the train/test split and model.",
    )
    parser.add_argument(
        "--n-estimators",
        type=int,
        default=300,
        help="Number of trees used by the random forest classifier.",
    )
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    metrics = train_model(
        dataset_path=args.dataset,
        model_path=args.model_out,
        metrics_path=args.metrics_out,
        test_size=args.test_size,
        random_state=args.random_state,
        n_estimators=args.n_estimators,
    )

    print(
        f"Training complete. Accuracy: {metrics['accuracy']:.4f}. "
        f"Model saved to {args.model_out}"
    )
