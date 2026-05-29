export type Language = {
  code: string;
  name: string;
  script: string;
  group: "indian" | "western";
};

export type TranslateResponse = {
  translation: string | null;
  source_lang: string;
  target_lang: string;
  detected_lang: string | null;
  detection_confidence: number | null;
  lang_mismatch_warning: string | null;
  provider_used: string | null;
  model_used: string | null;
  quality_score: number | null;
  quality_notes: string | null;
  attempts: number;
  latency_ms: Record<string, number>;
  errors: string[];
};

export async function fetchLanguages(): Promise<Language[]> {
  const res = await fetch("/api/languages");
  if (!res.ok) throw new Error(`languages: ${res.status}`);
  const data = await res.json();
  return data.languages as Language[];
}

export async function translate(
  source_lang: string,
  target_lang: string,
  text: string
): Promise<TranslateResponse> {
  const res = await fetch("/api/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_lang, target_lang, text }),
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail?.detail?.errors?.join("; ") || `translate: ${res.status}`);
  }
  return res.json();
}
