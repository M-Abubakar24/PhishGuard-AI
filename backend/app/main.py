
from pathlib import Path
from urllib.parse import urlparse

import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.app.dataset_features import extract_dataset_features


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "phishing_model.joblib"

if not MODEL_PATH.exists():
    raise RuntimeError(
        f"Model file not found: {MODEL_PATH}. Run python backend/train.py first."
    )

saved = joblib.load(MODEL_PATH)
model = saved["model"]
feature_columns = saved["feature_columns"]

app = FastAPI(
    title="PhishGuard AI",
    description="Machine-learning API for URL classification.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class URLRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="The URL to analyze. The API does not visit the URL.",
    )


def validate_url(value: str) -> str:
    value = value.strip()

    if not value:
        raise HTTPException(status_code=422, detail="URL cannot be empty.")

    candidate = value if "://" in value else f"http://{value}"
    parsed = urlparse(candidate)

    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.hostname
        or any(char.isspace() for char in value)
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise HTTPException(
            status_code=422,
            detail="Provide a valid HTTP or HTTPS URL without embedded credentials.",
        )

    try:
        parsed.port
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid URL port.")

    return candidate


@app.get("/")
def root():
    return {
        "name": "PhishGuard AI",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "feature_count": len(feature_columns),
    }


@app.post("/predict")
def predict(request: URLRequest):
    url = validate_url(request.url)

    try:
        features = extract_dataset_features(url)

        # Preserve the exact feature order used during training.
        row = pd.DataFrame(
            [[features[name] for name in feature_columns]],
            columns=feature_columns,
        )

        prediction = int(model.predict(row)[0])
        probabilities = model.predict_proba(row)[0]
        classes = list(model.classes_)
        confidence = float(probabilities[classes.index(prediction)])

        return {
            "url": url,
            "predicted_class": prediction,
            "confidence": round(confidence, 4),
            "note": (
                "Confidence is a model estimate, not a guarantee of safety. "
                "Confirm the dataset's label mapping before interpreting classes."
            ),
        }

    except HTTPException:
        raise
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Could not analyze this URL: {exc}",
        ) from exc
