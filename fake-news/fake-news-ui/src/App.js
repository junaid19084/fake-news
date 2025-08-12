import { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', { text });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">📰 Fake News Detector</h1>

      <textarea
        className="w-full max-w-2xl p-4 border border-gray-300 rounded-lg shadow-sm mb-4"
        rows={6}
        placeholder="Paste your news article here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={handleSubmit}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Check Authenticity"}
      </button>

      {result && (
        <div className="mt-6 p-4 rounded shadow bg-white max-w-xl w-full text-center">
          <p className="text-lg">
            Result:{" "}
            <span className={`font-bold ${result.prediction === "Real" ? "text-green-600" : "text-red-600"}`}>
              {result.prediction}
            </span>
          </p>
          <p className="text-sm text-gray-500 mt-2">Source: {result.source}</p>
        </div>
      )}
    </div>
  );
}

export default App;
