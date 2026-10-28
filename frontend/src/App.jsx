
import { useEffect, useState } from "react";
import {
  ShieldCheck,
  ShieldAlert,
  Search,
  LockKeyhole,
  Activity,
  Clock3,
  ExternalLink,
  CircleCheck,
  CircleAlert,
  LoaderCircle,
  Code2,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [url, setUrl] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
useEffect(() => {
  let isMounted = true;

  async function checkApiStatus() {
    try {
      const response = await fetch(`${API_URL}/health`);

      if (!response.ok) {
        throw new Error("API unavailable");
      }

      if (isMounted) {
        setApiStatus("online");
      }
    } catch {
      if (isMounted) {
        setApiStatus("offline");
      }
    }
  }

  checkApiStatus();

  const intervalId = setInterval(checkApiStatus, 15000);

  return () => {
    isMounted = false;
    clearInterval(intervalId);
  };
}, []);

async function analyzeUrl(event) {
  event.preventDefault();

  const submittedUrl = url.trim();

  if (!submittedUrl) {
    setError("Please enter a URL to analyze.");
    setResult(null);
    return;
  }

  let parsedUrl;

  try {
    parsedUrl = new URL(
      /^[a-zA-Z][a-zA-Z\d+.-]*:\/\//.test(submittedUrl)
        ? submittedUrl
        : `https://${submittedUrl}`
    );
  } catch {
    setError("Please enter a valid URL, such as example.com.");
    setResult(null);
    return;
  }

  if (!["http:", "https:"].includes(parsedUrl.protocol)) {
    setError("Only HTTP and HTTPS URLs are supported.");
    setResult(null);
    return;
  }

  if (!parsedUrl.hostname.includes(".")) {
    setError("Please enter a complete domain, such as example.com.");
    setResult(null);
    return;
  }

  const normalizedUrl = parsedUrl.href;

  setLoading(true);
  setError("");
  setResult(null);

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: normalizedUrl }),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(
        data.detail || "The URL could not be analyzed. Please try again."
      );
    }

    setResult(data);

    setHistory((previousHistory) => [
      {
        id: `${Date.now()}-${Math.random()}`,
        url: normalizedUrl,
        result: data,
        time: new Date().toLocaleTimeString(),
      },
      ...previousHistory,
    ].slice(0, 8));
  } catch (error) {
    setError(
      error.message === "Failed to fetch"
        ? "Cannot connect to the detection API. Check that your backend is running."
        : error.message || "Something went wrong. Please try again."
    );
  } finally {
    setLoading(false);
  }
}

  const isPhishing =
    result && Number(result.predicted_class) === 1;

  const confidence = result
    ? Math.max(
        0,
        Math.min(100, Number(result.confidence) * 100)
      )
    : 0;

  const phishingCount = history.filter(
    (item) => item.prediction === 1
  ).length;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a href="#" className="brand">
          <span className="brand-icon">
            <ShieldCheck size={25} />
          </span>
          <span>
            <strong>PhishGuard</strong>
            <small>AI SECURITY</small>
          </span>
        </a>

        <div className="sidebar-label">WORKSPACE</div>

        <a href="#scanner" className="nav-item active">
          <Search size={18} />
          URL Scanner
        </a>

        <a href="#history" className="nav-item">
          <Clock3 size={18} />
          Scan History
        </a>

        <div className="sidebar-bottom">
          <div className="status-card">
  <span className={`status-dot ${apiStatus}`} />
  <div>
    <strong>Detection API</strong>
    <small>
      {apiStatus === "online"
        ? "Connected and responding"
        : apiStatus === "offline"
          ? "Backend unavailable"
          : "Checking connection..."}
    </small>
  </div>
</div>
          <div className="sidebar-note">
            <LockKeyhole size={17} />
            <p>Analyze suspicious links without opening them.</p>
          </div>

          <a
            className="github-link"
            href="https://github.com/M-Abubakar24"
            target="_blank"
            rel="noreferrer"
          >
           <Code2 size={17} />
            GitHub profile
            <ExternalLink size={13} />
          </a>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace /</span>{" "}
            <strong>URL Scanner</strong>
          </div>
          <div className="topbar-status">
            <span className="status-dot" />
            Local development
          </div>
        </header>

        <section className="page-heading">
          <div className="eyebrow">
            <Activity size={15} />
            MACHINE LEARNING THREAT ANALYSIS
          </div>

          <h1>Stay one step ahead of <span>phishing.</span></h1>

          <p>
            Analyze a URL with our machine learning model to identify
            potentially suspicious links before you visit them.
          </p>
        </section>

        <section className="scanner-card" id="scanner">
          <div className="card-heading">
            <div className="card-icon">
              <Search size={20} />
            </div>
            <div>
              <h2>URL Security Scanner</h2>
              <p>Enter a complete URL for analysis.</p>
            </div>
          </div>

          <form onSubmit={analyzeUrl}>
            <label htmlFor="url-input">Website URL</label>

            <div className="input-wrap">
              <Search size={19} />
              <input
                id="url-input"
                type="text"
                value={url}
                onChange={(event) => setUrl(event.target.value)}
                placeholder="https://example.com/login"
                maxLength={2048}
                autoComplete="url"
                spellCheck="false"
              />
              {url && (
                <button
                  className="clear-button"
                  type="button"
                  onClick={() => {
                    setUrl("");
                    setError("");
                    setResult(null);
                  }}
                >
                  Clear
                </button>
              )}
            </div>

            <button
              className="analyze-button"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <LoaderCircle className="spin" size={18} />
                  Analyzing URL...
                </>
              ) : (
                <>
                  <ShieldCheck size={19} />
                  Analyze URL
                </>
              )}
            </button>
          </form>

          <div className="privacy-note">
            <LockKeyhole size={15} />
            This scanner does not intentionally visit the submitted URL.
          </div>

          {error && (
            <div className="error-message" role="alert">
              <CircleAlert size={19} />
              <span>{error}</span>
            </div>
          )}
        </section>

        {result && (
          <section
            className={`result-card ${isPhishing ? "danger" : "safe"}`}
            aria-live="polite"
          >
            <div className="result-top">
              <div className="result-symbol">
                {isPhishing ? (
                  <ShieldAlert size={28} />
                ) : (
                  <ShieldCheck size={28} />
                )}
              </div>
              <div className="result-title">
                <span className="result-kicker">ANALYSIS COMPLETE</span>
                <h2>
                  {isPhishing
                    ? "Potential phishing detected"
                    : "Classified as benign"}
                </h2>
                <p>
                  {isPhishing
                    ? "Avoid interacting with this URL unless you can independently verify it."
                    : "The model classified this URL as benign. This does not guarantee that it is safe."}
                </p>
              </div>
              <span className="result-badge">
                {isPhishing ? "SUSPICIOUS" : "BENIGN"}
              </span>
            </div>

            <div className="result-url">
              <span>Analyzed URL</span>
              <p>{result.url || url}</p>
            </div>

            <div className="confidence-section">
              <div className="confidence-label">
                <span>Model-reported confidence</span>
                <strong>{confidence.toFixed(1)}%</strong>
              </div>
              <div className="confidence-track">
                <div
                  className="confidence-fill"
                  style={{ width: `${confidence}%` }}
                />
              </div>
              <p>
                This score reflects the model's reported confidence, not a
                guarantee of safety or a calibrated real-world risk estimate.
              </p>
            </div>

            <div className="result-disclaimer">
              <CircleAlert size={17} />
              <span>
                Automated classification can produce false positives and
                false negatives. Verify important links through trusted
                channels.
              </span>
            </div>
          </section>
        )}

        <section className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon blue">
              <Activity size={20} />
            </div>
            <span>URLs analyzed this session</span>
            <strong>{history.length}</strong>
            <small>Recent scans in this browser session</small>
          </div>

          <div className="metric-card">
            <div className="metric-icon red">
              <ShieldAlert size={20} />
            </div>
            <span>Potential phishing results</span>
            <strong>{phishingCount}</strong>
            <small>Classified as phishing by the model</small>
          </div>

          <div className="metric-card">
            <div className="metric-icon green">
              <CircleCheck size={20} />
            </div>
            <span>Benign classifications</span>
            <strong>{history.length - phishingCount}</strong>
            <small>Not a guarantee that URLs are safe</small>
          </div>
        </section>

        <section className="history-card" id="history">
<div className="history-heading">
  <div>
    <h2>Recent scan history</h2>
    <p>Your latest URL analyses in this session.</p>
  </div>

<section className="security-info">
  <div className="security-info-header">
    <h2>About PhishGuard AI</h2>
    <p>
      Understand how the detection system helps identify potentially
      suspicious URLs.
    </p>
  </div>

  <div className="security-info-grid">
    <article className="security-info-card">
      <h3>URL Feature Analysis</h3>
      <p>
        Examines URL characteristics and extracted features to estimate
        whether a link may be associated with phishing.
      </p>
    </article>

    <article className="security-info-card">
      <h3>Machine Learning</h3>
      <p>
        Uses a trained classification model to generate a prediction
        and confidence score for submitted URLs.
      </p>
    </article>

    <article className="security-info-card">
      <h3>Security Disclaimer</h3>
      <p>
        Predictions are estimates, not guarantees. Avoid entering
        passwords or sensitive information on untrusted websites.
      </p>
    </article>
  </div>
</section>

  <div className="history-actions">
    <span className="history-count">{history.length} scans</span>

    {history.length > 0 && (
      <button
        type="button"
        className="history-action-button"
        onClick={() => setHistory([])}
      >
        Clear history
      </button>
    )}
  </div>
</div>

          {history.length === 0 ? (
            <div className="empty-history">
              <div className="empty-icon">
                <Clock3 size={24} />
              </div>
              <strong>No scans yet</strong>
              <p>Your analysis results will appear here.</p>
            </div>
          ) : (
            <div className="history-table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>URL</th>
                    <th>Classification</th>
                    <th>Confidence</th>
                    <th>Time</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((item) => (
                    <tr key={item.id}>
                      <td className="history-url">{item.url}</td>
                      <td>
                        <span
                          className={`table-badge ${
                            item.prediction === 1 ? "danger" : "safe"
                          }`}
                        >
                          {item.prediction === 1
                            ? "Potential phishing"
                            : "Benign"}
                        </span>
                      </td>
                      <td>{(item.confidence * 100).toFixed(1)}%</td>
                      <td>{item.time}</td>
<td>
  <button
    type="button"
    className="history-action-button"
    onClick={() => {
      setUrl(item.url);
      setError("");
      setResult(null);
      document.getElementById("scanner")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
      document.getElementById("url-input")?.focus();
    }}
  >
    Rescan
  </button>
</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer className="footer">
          <span>PhishGuard AI · Educational cybersecurity project</span>
          <span>ML-powered URL classification</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
