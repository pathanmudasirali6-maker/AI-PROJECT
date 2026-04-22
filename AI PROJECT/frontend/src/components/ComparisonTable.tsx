import { ComparisonFeature } from "@/types";

export default function ComparisonTable({ features }: { features: ComparisonFeature[] }) {
  return (
    <div className="overflow-hidden bg-white dark:bg-zinc-900 shadow-sm sm:rounded-lg border border-zinc-200 dark:border-zinc-800">
      <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-800">
        <thead className="bg-zinc-50 dark:bg-zinc-950">
          <tr>
            <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-zinc-900 dark:text-zinc-100 sm:pl-6">Feature</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-zinc-900 dark:text-zinc-100">Option A</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-zinc-900 dark:text-zinc-100">Option B</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-zinc-900 dark:text-zinc-100">Winner</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800 bg-white dark:bg-zinc-900">
          {features.map((feature, idx) => (
            <tr key={idx}>
              <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-zinc-900 dark:text-zinc-100 sm:pl-6">{feature.feature_name}</td>
              <td className="px-3 py-4 text-sm text-zinc-500 dark:text-zinc-400">{feature.option_a_detail}</td>
              <td className="px-3 py-4 text-sm text-zinc-500 dark:text-zinc-400">{feature.option_b_detail}</td>
              <td className="whitespace-nowrap px-3 py-4 text-sm font-bold text-indigo-600 dark:text-indigo-400">{feature.winner || "Tie"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
