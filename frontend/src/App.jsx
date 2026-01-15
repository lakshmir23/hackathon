import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadReceipt = async () => {
    if (!file) return alert("Please upload a receipt");

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/receipt/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="page">
      <div className="card">

        {/* HOME */}
        {!result && !loading && (
          <>
            <h1>🌱 Carbon Receipt Tracker</h1>
            <p className="subtitle">
              Track the environmental impact of your purchases
            </p>

            <input
              type="file"
              accept=".jpg,.png"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <button className="primary" onClick={uploadReceipt}>
              Calculate Carbon Impact
            </button>
          </>
        )}

        {/* LOADING */}
        {loading && (
          <div className="loading">
            <p>🔍 Scanning receipt...</p>
            <p>🌍 Calculating carbon footprint...</p>
          </div>
        )}

        {/* RESULTS */}
        {result && (
          <div className="result">
            <h2>🔥 Total CO₂ Emission</h2>
            <h1 className="co2">{result.total_co2} kg</h1>

            <ul>
              {result.items.map((item, i) => (
                <li key={i} className={item.co2 > 2 ? "high" : ""}>
                  {item.item} • {item.category} • {item.co2} kg
                </li>
              ))}
            </ul>

            <div className="actions">
              <button onClick={() => setResult(null)}>
                Upload Another Receipt
              </button>

              <button className="secondary">
                Download Report (PDF)
              </button>

              <button className="disabled">
                View History
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;