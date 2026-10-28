# PhishGuard AI 🛡️

**AI-powered phishing URL detection using machine learning and explainable URL risk indicators.**

PhishGuard AI is a machine-learning-based web application that classifies URLs as potentially benign or phishing. It combines URL feature extraction, a trained Random Forest classifier, a FastAPI REST API, and a React dashboard to provide accessible URL analysis.

> **Disclaimer:** PhishGuard AI is an educational cybersecurity project. Its predictions are not a guarantee that a URL is safe or malicious. Do not rely on this tool as your sole security measure.

## ✨ Features

- **URL feature extraction:** Extracts 22 numerical features from URLs, including URL length, subdomain count, character ratios, HTTPS usage, path length, and entropy.
- **Machine-learning classification:** Uses a Random Forest classifier trained on a labeled URL dataset.
- **REST API:** Provides URL predictions through FastAPI.
- **Interactive dashboard:** React-based interface for submitting URLs and viewing classifications.
- **Confidence scores:** Displays the model's reported prediction confidence.
- **Session scan history:** Shows recent URL analyses in the current browser session.
- **Input validation:** Validates submitted URLs before processing.
- **Model evaluation:** Includes scripts for evaluating held-out test data and unseen-domain performance.
- **CORS configuration:** Allows the configured frontend development origin to communicate with the API.

## 🧰 Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Machine learning | Scikit-learn, Random Forest |
| Data processing | Pandas, NumPy |
| Model persistence | Joblib |
| URL processing | `tldextract` |
| Frontend | React, Vite, JavaScript, CSS |
| API testing | Pytest, HTTPX |
| Version control | Git, GitHub |

## 🏗️ Architecture

```text
User
  |
  v
React Dashboard
  |
  | HTTP POST /predict
  v
FastAPI Backend
  |
  v
URL Validation
  |
  v
URL Feature Extraction
  |
  v
Trained Random Forest Model
  |
  v
Prediction + Confidence
  |
  v
React Results Dashboard
```

The application analyzes URL characteristics without visiting the submitted website.

## 📊 Model Evaluation

The project was evaluated using two different data-splitting strategies.

| Evaluation | Accuracy | Phishing Precision | Phishing Recall | Phishing F1-score |
|---|---:|---:|---:|---:|
| Random held-out test set | 97.60% | 90% | 93% | 92% |
| Unseen-domain split | 96.39% | 92% | 89% | 91% |

**Random held-out test set**
- Test URLs: 23,047
- Confusion matrix: 19,394 true negatives, 335 false positives, 217 false negatives, and 3,101 true positives.

**Unseen-domain evaluation**
- Test URLs: 24,215
- Domains were separated between training and test sets using the dataset's domain field.
- Confusion matrix: 19,113 true negatives, 372 false positives, 502 false negatives, and 4,228 true positives.

The unseen-domain evaluation is a useful additional check of generalization beyond a random URL split. Its reliability depends on the quality of the dataset's domain field and the evaluation methodology.

These results describe performance on the evaluated dataset; they do not establish real-world detection performance on every URL or current phishing campaign.

## 📁 Project Structure

```text
PhishGuard-AI/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── dataset_features.py
│   ├── train.py
│   ├── verify_feature_parity.py
│   ├── evaluate_inference.py
│   ├── evaluate_unseen_domains.py
│   └── check_test_predictions.py
├── data/
│   └── raw_urls.csv
├── models/
│   └── phishing_model.joblib
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
├── .gitignore
└── README.md
```

*Note: The dataset and trained model may be excluded from Git through `.gitignore`. The structure above illustrates the local development layout; filenames may vary if the project has evolved.*

## ⚙️ Getting Started

### Prerequisites

Install the following:

- Python 3.11 or another Python version supported by your dependencies
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/M-Abubakar24/PhishGuard-AI.git
cd PhishGuard-AI
```

### 2. Set up the Python environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, you can use the environment's Python executable directly.

Install the backend dependencies:

```powershell
python -m pip install fastapi "uvicorn[standard]" scikit-learn pandas numpy joblib tldextract pytest httpx
```

### 3. Prepare the model

The API requires the trained model at:

```text
models/phishing_model.joblib
```

If the model is not included in the repository, obtain the dataset from its original source and place it at `data/raw_urls.csv`. Then run:

```powershell
python backend/train.py
```

Training may take several minutes, depending on your system.

### 4. Start the backend

Run this command from the repository root:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

### 5. Start the React frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, normally:

```text
http://localhost:5173
```

Ensure that the backend is running and that the API's CORS configuration permits the frontend origin.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API root or service information |
| GET | `/health` | Health check |
| POST | `/predict` | Classify a submitted URL |

### Example request

`POST /predict`

```json
{
  "url": "https://example.com"
}
```

The API returns a JSON response containing the submitted URL, predicted class, confidence, and an explanatory note.

The exact response fields and class-label mapping should be verified against the current backend implementation.

## 🧪 Evaluation and Testing

The repository includes scripts for model evaluation and feature consistency checks.

From the project root, run the scripts available in your checkout, for example:

```powershell
python backend/verify_feature_parity.py
python backend/evaluate_inference.py
python backend/evaluate_unseen_domains.py
```

To run automated tests, use:

```powershell
python -m pytest
```

The available test files and coverage depend on the current repository version.

## 🔐 Security and Limitations

- Predictions are based on URL characteristics learned from the training dataset.
- Legitimate URLs may be incorrectly classified as phishing, and phishing URLs may be classified as benign.
- A valid HTTPS connection does not guarantee that a website is trustworthy.
- The confidence score is a model output, not a guarantee of correctness.
- The current application does not visit or crawl submitted websites.
- The model should be evaluated against newer, independent datasets before being used for real-world security decisions.
- Before public deployment, review API rate limits, logging, error handling, dependency security, and production CORS settings.

## 🚀 Future Improvements

- Add richer, evidence-based explanations for individual predictions.
- Improve evaluation using newer and independent phishing datasets.
- Add automated API and input-validation tests.
- Introduce production deployment and environment-based configuration.
- Add monitoring and safe model-version management.
- Improve accessibility and mobile responsiveness.

## 👨‍💻 Author

**Muhammad Abubakar**

Software Engineering graduate interested in machine learning, cybersecurity, and full-stack application development.

- GitHub: [M-Abubakar24](https://github.com/M-Abubakar24)

## 📄 License

Add a license file if you intend to publish this project for reuse. Until then, no open-source license should be assumed.
