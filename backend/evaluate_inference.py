
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from backend.app.dataset_features import extract_dataset_features


# Load and prepare the original dataset
df = pd.read_csv("data/raw_urls.csv")
df = df.dropna(subset=["url", "label"])
df = df.drop_duplicates(subset=["url"], keep="first")

df["label"] = df["label"].astype(int)

excluded = {"label", "url", "dom", "tld"}
feature_columns = [
    col
    for col in df.select_dtypes(include="number").columns
    if col not in excluded
]

# Reproduce the original train/test split
X = df[feature_columns].replace(
    [float("inf"), -float("inf")], float("nan")
)
y = df["label"]

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Load the trained model
saved = joblib.load("models/phishing_model.joblib")
model = saved["model"]

print(f"Evaluating {len(X_test)} held-out URLs...")
print("Extracting URL features. This may take a few minutes.")

# Extract features directly from each URL
rows = []

for url in df.loc[X_test.index, "url"]:
    features = extract_dataset_features(url)
    rows.append([features[col] for col in feature_columns])

X_inference = pd.DataFrame(
    rows,
    columns=feature_columns,
    index=X_test.index,
)

# Predict using the extracted features
predictions = model.predict(X_inference)

print("\n=== Full Held-Out Inference Evaluation ===")
print(f"Test URLs: {len(y_test)}")
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Benign", "Phishing"],
        zero_division=0,
    )
)

print("Confusion matrix:")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))
print("\nRows = actual class; columns = predicted class.")
print("Class 0 = benign; class 1 = phishing.")
