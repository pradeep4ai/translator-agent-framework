type Props = {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
  disabled?: boolean;
};

export function TranslatorCard({ value, onChange, placeholder, disabled }: Props) {
  return (
    <div className="rounded-2xl border-2 border-gray-200 bg-white p-4 shadow-sm">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        rows={6}
        maxLength={4000}
        className="w-full resize-none outline-none text-lg font-medium placeholder:text-gray-400 bg-transparent"
      />
      <div className="text-right text-xs text-gray-400">{value.length} / 4000</div>
    </div>
  );
}
