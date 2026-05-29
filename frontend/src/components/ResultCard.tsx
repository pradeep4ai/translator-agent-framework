import { TranslateResponse } from "../api";

type Props = {
  result: TranslateResponse | null;
  loading: boolean;
  error: string | null;
};

function QualityBadge({ score }: { score: number | null }) {
  if (score == null) return null;
  const color =
    score >= 4 ? "bg-duo-green text-white" : score === 3 ? "bg-duo-gold text-duo-slate" : "bg-red-500 text-white";
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${color}`}>
      quality {score}/5
    </span>
  );
}

export function ResultCard({ result, loading, error }: Props) {
  return (
    <div className="rounded-2xl border-2 border-duo-green bg-white p-4 shadow-sm min-h-[180px] flex flex-col">
      {loading && <div className="text-gray-400 italic">Translating...</div>}
      {error && <div className="text-red-600 font-bold">{error}</div>}
      {!loading && !error && result && (
        <>
          <div className="text-lg font-medium whitespace-pre-wrap flex-1">{result.translation}</div>
          <div className="mt-3 flex flex-wrap gap-2 items-center text-xs">
            {result.provider_used && (
              <span className="px-2 py-0.5 rounded-full bg-duo-blue text-white font-bold">
                {result.provider_used}
              </span>
            )}
            {result.model_used && (
              <span className="px-2 py-0.5 rounded-full bg-gray-200 text-duo-slate font-mono">
                {result.model_used}
              </span>
            )}
            <QualityBadge score={result.quality_score} />
            {result.attempts > 1 && (
              <span className="px-2 py-0.5 rounded-full bg-duo-gold text-duo-slate font-bold">
                retried ({result.attempts}x)
              </span>
            )}
            {result.translation && (
              <button
                onClick={() => navigator.clipboard.writeText(result.translation!)}
                className="ml-auto text-duo-blue hover:underline font-bold"
              >
                Copy
              </button>
            )}
          </div>
          {result.lang_mismatch_warning && (
            <div className="mt-2 text-xs text-orange-600 font-bold">
              ! {result.lang_mismatch_warning}
            </div>
          )}
        </>
      )}
      {!loading && !error && !result && (
        <div className="text-gray-400 italic">Translation will appear here.</div>
      )}
    </div>
  );
}
