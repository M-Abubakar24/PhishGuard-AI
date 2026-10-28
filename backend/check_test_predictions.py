
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from backend.app.dataset_features import extract_dataset_features

df = pd.read_csv("data/raw_urls.csv")
df = df.dropna(subset=["url", "label"]).drop_duplicates(
    subset=["url"], keep="first"
)

excluded = {"label", "url", "dom", "tld"}
feature_columns = [
    col for col in df.select_dtypes(include="number").columns
    if col not in excluded
]

# Recreate the same held-out split used during training.
X_train, X_test, y_train, y_test = train_test_split(
    df[feature_columns].replace([float("inf"), -float("inf")], float("nan")),
    df["label"].astype(int),
    test_size=0.20,
    random_state=42,
    stratify=df["label"].astype(int),
)

saved = joblib.load("models/phishing_model.joblib")
model = saved["model"]

# Select benign URLs from the held-out test set.
phishing = df.loc[X_test.index].loc[y_test == 1].head(20)

print("Testing 20 held-out benign URLs:\n")

for _, row in phishing.iterrows():
    features = extract_dataset_features(row["url"])
    sample = pd.DataFrame(
        [[features[c] for c in feature_columns]],
        columns=feature_columns,
    )
    prediction = int(model.predict(sample)[0])
    probabilities = model.predict_proba(sample)[0]
    classes = list(model.classes_)
    phishing_probability = float(probabilities[classes.index(1)])

    print(
        f"Actual={int(row['label'])} | Predicted={prediction} | "
        f"Phishing probability={phishing_probability:.3f} | {row['url']}"
    )
