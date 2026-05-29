import { Language } from "../api";

type Props = {
  languages: Language[];
  value: string;
  onChange: (code: string) => void;
  label: string;
};

export function LanguagePicker({ languages, value, onChange, label }: Props) {
  const indian = languages.filter((l) => l.group === "indian");
  const western = languages.filter((l) => l.group === "western");

  return (
    <label className="flex flex-col gap-1 text-sm font-bold text-duo-slate">
      <span className="uppercase tracking-wider text-xs text-gray-500">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="border-2 border-gray-200 rounded-xl px-3 py-2 bg-white font-bold focus:outline-none focus:border-duo-blue"
      >
        <optgroup label="Indian languages">
          {indian.map((l) => (
            <option key={l.code} value={l.code}>
              {l.name}
            </option>
          ))}
        </optgroup>
        <optgroup label="Western languages">
          {western.map((l) => (
            <option key={l.code} value={l.code}>
              {l.name}
            </option>
          ))}
        </optgroup>
      </select>
    </label>
  );
}
