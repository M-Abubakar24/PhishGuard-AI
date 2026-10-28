
import pandas as pd

from backend.app.dataset_features import extract_dataset_features

df = pd.read_csv("data/raw_urls.csv")
df = df.dropna(subset=["url", "label"])
df = df.drop_duplicates(subset=["url"], keep="first")

excluded = {"label", "url", "dom", "tld"}
feature_columns = [
    col
    for col in df.select_dtypes(include="number").columns
    if col not in excluded
]

# Check 1,000 URLs sampled from the dataset, reproducibly.
sample = df.sample(
    n=min(1000, len(df)),
    random_state=42,
)

mismatch_count = 0
total_values = 0
examples = []

for _, row in sample.iterrows():
    extracted = extract_dataset_features(row["url"])

    for column in feature_columns:
        expected = row[column]
        actual = extracted[column]
        total_values += 1

        if pd.isna(expected):
            continue

        if pd.isna(actual) or abs(float(expected) - float(actual)) > 1e-6:
            mismatch_count += 1

            if len(examples) < 10:
                examples.append(
                    {
                        "url": row["url"],
                        "feature": column,
                        "dataset_value": expected,
                        "extracted_value": actual,
                    }
                )

print(f"URLs checked: {len(sample)}")
print(f"Feature values compared: {total_values}")
print(f"Mismatches: {mismatch_count}")

if examples:
    print("\nFirst mismatches:")
    for item in examples:
        print(item)
else:
    print("\nNo mismatches found in the sampled URLs.")
