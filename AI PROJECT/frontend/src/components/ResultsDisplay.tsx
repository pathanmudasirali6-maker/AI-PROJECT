import { DecisionOutcome } from "@/types";
import ComparisonTable from "./ComparisonTable";
import ConfidenceScore from "./ConfidenceScore";

export default function ResultsDisplay({ data }: { data: DecisionOutcome }) {
  return (
    <div className="flex flex-col gap-8 mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6 rounded-xl shadow-sm">
        <h2 className="text-xl font-bold text-zinc-900 dark:text-white mb-2">Executive Summary</h2>
        <p className="text-zinc-600 dark:text-zinc-300">{data.summary}</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          <ComparisonTable features={data.comparison_table} />
        </div>
        <div className="md:col-span-1">
          <ConfidenceScore score={data.confidence_score} />
          
          <div className="mt-6 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6 rounded-xl shadow-sm">
            <h3 className="text-sm font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-4">Final Recommendation</h3>
            <p className="text-zinc-800 dark:text-zinc-200 font-medium">{data.recommendation}</p>
          </div>
        </div>
      </div>

      <div className="bg-zinc-50 dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 p-4 rounded-xl shadow-sm text-sm text-zinc-500 dark:text-zinc-400">
        <span className="font-semibold text-zinc-700 dark:text-zinc-300">Sources: </span>
        {data.sources_cited.join(", ")}
      </div>
    </div>
  );
}
