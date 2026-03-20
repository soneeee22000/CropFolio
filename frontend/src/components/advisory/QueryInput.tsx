import { useState, type FormEvent } from "react";
import { useLanguage } from "@/i18n/LanguageContext";

interface QueryInputProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
  disabled: boolean;
}

/** Chat-like text input for asking questions. */
export function QueryInput({ onSubmit, isLoading, disabled }: QueryInputProps) {
  const { t } = useLanguage();
  const [question, setQuestion] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = question.trim();
    if (trimmed.length >= 3) {
      onSubmit(trimmed);
      setQuestion("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder={t("advisory.queryPlaceholder")}
        disabled={disabled || isLoading}
        minLength={3}
        maxLength={500}
        className="flex-1 p-3 rounded-lg border border-border bg-surface-elevated text-text-primary text-base placeholder:text-text-tertiary disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled || isLoading || question.trim().length < 3}
        className="px-5 py-3 rounded-lg bg-primary text-white font-medium text-sm hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
      >
        {isLoading ? (
          <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        ) : (
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        )}
        {t("advisory.ask")}
      </button>
    </form>
  );
}
