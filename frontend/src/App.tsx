import { useEffect, useState } from "react";
import { fetchLanguages, translate, Language, TranslateResponse } from "./api";
import { LanguagePicker } from "./components/LanguagePicker";
import { TranslatorCard } from "./components/TranslatorCard";
import { ResultCard } from "./components/ResultCard";

export default function App() {
  const [languages, setLanguages] = useState<Language[]>([]);
  const [source, setSource] = useState("hi");
  const [target, setTarget] = useState("en");
  const [text, setText] = useState("");
  const [result, setResult] = useState<TranslateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLanguages()
      .then(setLanguages)
      .catch((e) => setError(String(e)));
  }, []);

  async function onTranslate() {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await translate(source, target, text);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  function swap() {
    setSource(target);
    setTarget(source);
    if (result?.translation) {
      setText(result.translation);
      setResult(null);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-8">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-extrabold text-duo-green">Polyglot</h1>
        <p className="text-gray-500 font-bold">
          Indian languages &lt;&gt; English / German / French, powered by a custom agent framework
        </p>
      </header>

      <main className="w-full max-w-4xl space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] gap-3 items-end">
          <LanguagePicker languages={languages} value={source} onChange={setSource} label="From" />
          <button
            onClick={swap}
            className="rounded-xl border-2 border-gray-200 px-3 py-2 font-bold hover:bg-gray-100 hidden md:block"
            title="Swap"
          >
            &lt;&gt;
          </button>
          <LanguagePicker languages={languages} value={target} onChange={setTarget} label="To" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <TranslatorCard
            value={text}
            onChange={setText}
            placeholder="Type or paste text..."
            disabled={loading}
          />
          <ResultCard result={result} loading={loading} error={error} />
        </div>

        <div className="flex justify-center">
          <button
            onClick={onTranslate}
            disabled={loading || !text.trim() || source === target}
            className="bg-duo-green hover:bg-duo-greenDark disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-extrabold uppercase tracking-wider px-8 py-3 rounded-2xl shadow-[0_4px_0_#46A302] active:translate-y-[2px] active:shadow-[0_2px_0_#46A302]"
          >
            {loading ? "Translating..." : "Translate"}
          </button>
        </div>
      </main>

      <footer className="mt-12 text-xs text-gray-400">
        Custom agent framework - {languages.length} languages loaded
      </footer>
    </div>
  );
}
