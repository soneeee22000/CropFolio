import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import { Card } from "@/components/common/Card";
import type { AdvisorySectionData } from "@/types/advisory";

interface AdvisorySectionProps {
  section: AdvisorySectionData;
  icon: string;
}

/** Advisory section card with EN/MM toggle and markdown rendering. */
export function AdvisorySection({ section, icon }: AdvisorySectionProps) {
  const [showMM, setShowMM] = useState(false);
  const content = showMM ? section.content_mm : section.content;

  return (
    <Card>
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
            <svg
              className="w-5 h-5 text-primary"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d={icon} />
            </svg>
          </div>
          <h4 className="font-display text-lg text-text-primary">
            {section.title}
          </h4>
        </div>
        <button
          onClick={() => setShowMM(!showMM)}
          className="text-xs px-2 py-1 rounded border border-border text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors flex-shrink-0"
        >
          {showMM ? "EN" : "MM"}
        </button>
      </div>
      <div className="prose prose-sm max-w-none text-text-secondary leading-relaxed">
        <ReactMarkdown rehypePlugins={[rehypeSanitize]}>
          {content}
        </ReactMarkdown>
      </div>
    </Card>
  );
}
