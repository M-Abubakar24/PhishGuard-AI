
import { useState } from "react";
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
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  async function analyzeUrl(event) {
    event.preventDefault();

    const submittedUrl = url.trim();

    if (!submittedUrl) {
      setError("Please enter a URL to analyze.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: submittedUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to analyze this URL. Please try again."
        );
      }

      setResult(data);

      setHistory((previous) => [
        {
          id: `${Date.now()}-${Math.random()}`,
          url: data.url || submittedUrl,
          prediction: Number(data.predicted_class),
          confidence: Number(data.confidence),
          time: new Date().toLocaleTimeString(),
        },
        ...previous,
      ].slice(0, 8));
    } catch (err) {
      setError(
        err.message ||
          "Cannot connect to the API. Check that your FastAPI backend is running."
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
            <span className="status-dot" />
            <div>
              <strong>Detection API</strong>
              <small>Connection checked on scan</small>
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
            <span className="history-count">{history.length} scans</span>
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
