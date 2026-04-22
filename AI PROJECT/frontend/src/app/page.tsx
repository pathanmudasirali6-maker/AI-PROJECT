"use client";

import { useState } from "react";
import QueryForm from "@/components/QueryForm";
import ResultsDisplay from "@/components/ResultsDisplay";
import { DecisionOutcome } from "@/types";

export default function Home() {
  const [result, setResult] = useState<DecisionOutcome | null>(null);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 font-[family-name:var(--font-geist-sans)]">
      <header className="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-xl">
              I
            </div>
            <h1 className="text-xl font-bold tracking-tight">InsightForge</h1>
          </div>
          <div className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
            Decision Intelligence Platform
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-zinc-900 to-zinc-500 dark:from-white dark:to-zinc-400">
            Compute Your Decisions
          </h2>
          <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
            Stop guessing. Input your strategic question below, and InsightForge will retrieve factual context, structurally compare your options, and generate a validated confidence score.
          </p>
        </div>

        <QueryForm onResult={setResult} />

        {result && (
          <div className="mt-8 border-t border-zinc-200 dark:border-zinc-800 pt-8">
            <ResultsDisplay data={result} />
          </div>
        )}
      </main>
    </div>
  );
}
