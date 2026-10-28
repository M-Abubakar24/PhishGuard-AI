# PhishGuard AI — Machine Learning Phishing URL Detector

PhishGuard AI is a machine-learning cybersecurity project that analyzes URL characteristics to predict whether a URL may be associated with phishing.

The project combines a Python/FastAPI backend with a React frontend to provide an interactive URL scanning dashboard.

## Features

- Machine-learning-based phishing URL classification
- URL feature extraction
- FastAPI prediction endpoint
- Interactive React dashboard
- URL input validation for HTTP and HTTPS
- API connection status indicator
- Confidence score and scan results
- Recent scan history, rescanning, and clearing history
- Error handling for invalid inputs and unavailable backend services

## Technology Stack

- **Frontend:** React, Vite, JavaScript, CSS
- **Backend:** Python, FastAPI
- **Machine Learning:** scikit-learn-compatible model workflow
- **Data Processing:** pandas and NumPy, where used by the project

## Model Evaluation

The model was evaluated using two data-splitting approaches.

| Evaluation | Accuracy | Phishing Precision | Phishing Recall | Phishing F1-score |
|---|---:|---:|---:|---:|
| Random train/test split | 97.60% | 90% | 93% | 0.92 |
| Unseen-domain split | 96.39% | 92% | 89% | 0.91 |

The unseen-domain evaluation provides an additional test of generalization to domains not represented in the training split. Results depend on the dataset and evaluation method.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/M-Abubakar24/PhishGuard-AI.git
cd PhishGuard-AI
```

### 2. Activate the Python environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Start the backend

From the project root, run:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The API should be available at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 4. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local address shown by Vite, usually `http://localhost:5173`.

## Security Disclaimer

PhishGuard AI is an educational cybersecurity project. Its predictions are estimates and may produce false positives or false negatives. A benign prediction does not guarantee that a URL is safe. Do not use this tool as the sole basis for security decisions.

## Author

**Muhammad Abubakar**

GitHub: [M-Abubakar24](https://github.com/M-Abubakar24)
