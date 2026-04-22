export default function ConfidenceScore({ score }: { score: number }) {
  const getColor = () => {
    if (score >= 80) return "text-green-500";
    if (score >= 50) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800">
      <h3 className="text-sm font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Confidence Score</h3>
      <div className={`text-5xl font-bold ${getColor()}`}>
        {score}%
      </div>
      <p className="text-xs text-zinc-400 mt-2 text-center">Based on factual source density & schema validation.</p>
    </div>
  );
}
