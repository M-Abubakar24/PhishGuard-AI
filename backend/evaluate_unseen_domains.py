
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline

df = pd.read_csv("data/raw_urls.csv")
df = df.dropna(subset=["url", "label"])
df = df.drop_duplicates(subset=["url"], keep="first").reset_index(drop=True)
df["label"] = df["label"].astype(int)

excluded = {"label", "url", "dom", "tld"}
feature_columns = [
    col
    for col in df.select_dtypes(include="number").columns
    if col not in excluded
]

X = df[feature_columns].replace(
    [float("inf"), -float("inf")], float("nan")
)
y = df["label"]

# Use the dataset's domain column to keep domains separate.
groups = df["dom"].fillna("").astype(str).str.lower().str.strip()

# If a domain is missing, keep that URL in its own group.
missing = groups.eq("")
groups.loc[missing] = (
    "__missing_domain__" + df.index[missing].astype(str)
)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42,
)

train_idx, test_idx = next(splitter.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

train_domains = set(groups.iloc[train_idx])
test_domains = set(groups.iloc[test_idx])
overlap = train_domains.intersection(test_domains)

print(f"Training URLs: {len(train_idx)}")
print(f"Test URLs: {len(test_idx)}")
print(f"Training domains: {len(train_domains)}")
print(f"Test domains: {len(test_domains)}")
print(f"Overlapping domains: {len(overlap)}")
print(f"Training label counts:\n{y_train.value_counts().sort_index()}")
print(f"Test label counts:\n{y_test.value_counts().sort_index()}")

if overlap:
    raise RuntimeError("Domain overlap detected; evaluation stopped.")

if y_train.nunique() < 2 or y_test.nunique() < 2:
    raise RuntimeError(
        "One split contains only one class. Try another random_state."
    )

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )),
])

print("\nTraining evaluation model on training domains...")
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\n=== Unseen-Domain Evaluation ===")
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Benign", "Phishing"],
    zero_division=0,
))

print("Confusion matrix:")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))
print("\nRows = actual class; columns = predicted class.")
