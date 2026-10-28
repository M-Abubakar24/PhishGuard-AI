
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw_urls.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "phishing_model.joblib"

RANDOM_STATE = 42


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    required_columns = {"url", "label"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain these columns: {required_columns}"
        )

    # Remove rows without a usable URL or label.
    df = df.dropna(subset=["url", "label"]).copy()

    # Keep one record per URL to reduce duplicate leakage.
    df = df.drop_duplicates(subset=["url"], keep="first")

    # Labels must be numeric and contain exactly two classes.
    df["label"] = pd.to_numeric(df["label"], errors="raise")
    if set(df["label"].unique()) != {0, 1}:
        raise ValueError("Expected binary labels 0 and 1.")

    # Use only numeric, precomputed URL features.
    excluded = {"label", "url", "dom", "tld"}
    feature_columns = [
        column
        for column in df.select_dtypes(include="number").columns
        if column not in excluded
    ]

    if not feature_columns:
        raise ValueError("No numeric feature columns were found.")

    X = df[feature_columns].replace([float("inf"), -float("inf")], float("nan"))
    y = df["label"].astype(int)

    print(f"Rows after URL deduplication: {len(df):,}")
    print(f"Features: {len(feature_columns)}")
    print("Label counts:")
    print(y.value_counts().sort_index().to_string())

    # Keep class proportions similar in both sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("\nTraining Random Forest...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\n--- Evaluation on held-out test set ---")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Class 0", "Class 1"],
            zero_division=0,
        )
    )
    print("Confusion matrix (rows=true, columns=predicted; labels 0, 1):")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "feature_columns": feature_columns,
            "labels": {
                0: "benign (verify against dataset documentation)",
                1: "phishing (verify against dataset documentation)",
            },
        },
        MODEL_PATH,
    )

    print(f"\nSaved model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
