"use client";

import { useState } from "react";
import { DecisionOutcome } from "@/types";

export default function QueryForm({ onResult }: { onResult: (data: DecisionOutcome) => void }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [statusText, setStatusText] = useState("");

  const steps = [
    "Analyzing query...",
    "Retrieving enterprise context...",
    "Evaluating comparisons...",
    "Validating schema..."
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setError("");

    // Start loading steps animation loops
    let stepIndex = 0;
    setStatusText(steps[0]);
    const stepInterval = setInterval(() => {
      stepIndex = (stepIndex + 1) % steps.length;
      setStatusText(steps[stepIndex]);
    }, 1500);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";
      const res = await fetch(`${apiUrl}/api/v1/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });
      
      if (!res.ok) {
        throw new Error(`Failed to fetch data: ${res.statusText}`);
      }
      
      const data: DecisionOutcome = await res.json();
      onResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred during evaluation.");
    } finally {
      clearInterval(stepInterval);
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto w-full">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="E.g., Compare AWS vs Google Cloud for a machine learning startup emphasizing cost and specialized compute..."
          className="w-full p-4 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none min-h-[120px] resize-y"
          disabled={loading}
        />
        <div className="flex items-center justify-between">
          <div className="text-red-500 text-sm">{error}</div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-medium rounded-lg shadow-sm transition-colors"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {statusText}
              </span>
            ) : "Analyze Decision"}
          </button>
        </div>
      </form>
    </div>
  );
}
