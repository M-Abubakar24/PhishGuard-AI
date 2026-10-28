
import pandas as pd
from backend.app.dataset_features import extract_dataset_features

df = pd.read_csv("data/raw_urls.csv")

# Test a few known benign records from the training dataset.
samples = df[df["label"] == 0].head(10)

for _, row in samples.iterrows():
    calculated = extract_dataset_features(row["url"])

    expected = [
        "url_len", "dom_len", "is_ip", "tld_len", "subdom_cnt",
        "letter_cnt", "digit_cnt", "special_cnt", "eq_cnt", "qm_cnt",
        "amp_cnt", "dot_cnt", "dash_cnt", "under_cnt", "letter_ratio",
        "digit_ratio", "spec_ratio", "is_https", "slash_cnt", "entropy",
        "path_len", "query_len",
    ]

    mismatches = []
    for name in expected:
        actual = float(calculated[name])
        original = float(row[name])

        if abs(actual - original) > 1e-5:
            mismatches.append(
                f"{name}: dataset={original}, calculated={actual:.6f}"
            )

    print(f"\nURL: {row['url']}")
    print("Feature mismatches:", len(mismatches))
    for mismatch in mismatches:
        print("  -", mismatch)
