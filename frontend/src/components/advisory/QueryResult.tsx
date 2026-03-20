import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import type { QueryHistoryEntry } from "@/types/advisory";

interface QueryResultProps {
  entry: QueryHistoryEntry;
}

const CONFIDENCE_COLORS: Record<string, string> = {
  high: "bg-emerald-500/10 text-emerald-600",
  medium: "bg-amber-500/10 text-amber-600",
  low: "bg-red-500/10 text-red-600",
};

/** Renders a Q&A pair with confidence badge and data sources. */
export function QueryResult({ entry }: QueryResultProps) {
  const [showMM, setShowMM] = useState(false);
  const { result } = entry;

  const level =
    result.confidence >= 0.7
      ? "high"
      : result.confidence >= 0.4
        ? "medium"
        : "low";

  const answer = showMM ? result.answer_mm : result.answer;

  return (
    <div className="border border-border rounded-xl overflow-hidden">
      {/* Question */}
      <div className="px-5 py-3 bg-surface-subtle border-b border-border">
        <p className="text-sm text-text-primary font-medium">
          {entry.question}
        </p>
      </div>

      {/* Answer */}
      <div className="p-5 space-y-3">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span
              className={`text-xs px-2 py-0.5 rounded-full font-medium ${CONFIDENCE_COLORS[level]}`}
            >
              {Math.round(result.confidence * 100)}% confidence
            </span>
            {!result.has_ai && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-600 font-medium">
                No AI
              </span>
            )}
          </div>
          <button
            onClick={() => setShowMM(!showMM)}
            className="text-xs px-2 py-1 rounded border border-border text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors"
          >
            {showMM ? "EN" : "MM"}
          </button>
        </div>

        <div className="prose prose-sm max-w-none text-text-secondary leading-relaxed">
          <ReactMarkdown rehypePlugins={[rehypeSanitize]}>
            {answer}
          </ReactMarkdown>
        </div>

        {result.data_sources.length > 0 && (
          <div className="flex items-center gap-2 pt-2">
            <span className="text-xs text-text-tertiary">Sources:</span>
            {result.data_sources.map((src) => (
              <span
                key={src}
                className="text-xs px-1.5 py-0.5 rounded bg-surface-subtle text-text-tertiary"
              >
                {src.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
