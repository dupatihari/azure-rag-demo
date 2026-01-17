import { useState } from "react";
import "./App.css";

const API_URL =
  "https://func-campaign-insights-uks01.azurewebsites.net/api/getcampaigninsights";

export default function App() {
  const [question, setQuestion] = useState(
    "What is the budget allocation for the Q3 Summer campaign?"
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const ask = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(
        `${API_URL}?q=${encodeURIComponent(question)}`
      );

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Campaign Insights (RAG Demo)</h2><h4> - By Hari dupati</h4>

      <textarea
        rows={3}
        style={{ width: "100%" }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <br />
      <button onClick={ask} disabled={loading} style={{ marginTop: 12 }}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: 12 }}>
          Error: {error}
        </p>
      )}

      {result && (
        <div style={{ marginTop: 24 }}>
          <h3>Summary</h3>
          <p>{result.rag?.summary}</p>

          <h3>Key Points</h3>
          <ul>
            {result.rag?.keyPoints?.map((k, i) => (
              <li key={i}>{k}</li>
            ))}
          </ul>

          <h3>Recommendations</h3>
          <ul>
            {result.rag?.recommendations?.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>

          <h3>Citations</h3>
          <ul>
            {result.citations?.map((c) => (
              <li key={c.id}>{c.source}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
