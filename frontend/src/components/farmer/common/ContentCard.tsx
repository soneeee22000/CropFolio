/** Content feed item card with Burmese text and optional audio. */

interface ContentCardProps {
  title: string;
  titleMm: string | null;
  body: string;
  bodyMm: string | null;
  contentType: string;
  audioUrl: string | null;
  publishedAt: string | null;
  onView?: () => void;
  onHelpful?: (helpful: boolean) => void;
}

const TYPE_ICONS: Record<string, string> = {
  weather_alert:
    "M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z",
  pest_alert:
    "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z",
  fertilizer_reminder:
    "M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z",
  tip: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
  market_update: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
};

const TYPE_COLORS: Record<string, string> = {
  weather_alert: "text-blue-400",
  pest_alert: "text-danger",
  fertilizer_reminder: "text-primary",
  tip: "text-accent",
  market_update: "text-primary",
};

const TYPE_LABELS: Record<string, string> = {
  weather_alert: "ရာသီဥတု",
  pest_alert: "ပိုးမွှား",
  fertilizer_reminder: "ဓာတ်မြေသြဇာ",
  tip: "အကြံပြု",
  market_update: "ဈေးကွက်",
};

/** Single content card in the farmer feed. */
export function ContentCard({
  title,
  titleMm,
  body,
  bodyMm,
  contentType,
  audioUrl,
  onHelpful,
}: ContentCardProps) {
  const icon = TYPE_ICONS[contentType] ?? TYPE_ICONS.tip;
  const color = TYPE_COLORS[contentType] ?? "text-text-secondary";
  const label = TYPE_LABELS[contentType] ?? contentType;

  return (
    <div className="rounded-xl bg-surface-elevated border border-border p-4">
      {/* Type badge */}
      <div className="flex items-center gap-2 mb-2">
        <svg
          className={`w-5 h-5 ${color}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d={icon} />
        </svg>
        <span className={`text-xs font-semibold ${color} font-myanmar`}>
          {label}
        </span>
      </div>

      {/* Title */}
      <h3 className="font-semibold text-text-primary text-base">
        {titleMm ?? title}
      </h3>

      {/* Body */}
      <p className="text-sm text-text-secondary mt-2 line-clamp-3 font-myanmar">
        {bodyMm ?? body}
      </p>

      {/* Audio player */}
      {audioUrl && (
        <div className="mt-3">
          <audio controls className="w-full h-10" preload="none">
            <source src={audioUrl} />
          </audio>
        </div>
      )}

      {/* Helpful buttons */}
      {onHelpful && (
        <div className="flex gap-2 mt-3">
          <button
            onClick={() => onHelpful(true)}
            className="flex-1 py-2 rounded-lg border border-border text-text-secondary text-sm hover:border-primary hover:text-primary transition-colors min-h-[44px]"
          >
            အသုံးဝင်ပါတယ်
          </button>
          <button
            onClick={() => onHelpful(false)}
            className="flex-1 py-2 rounded-lg border border-border text-text-secondary text-sm hover:border-danger hover:text-danger transition-colors min-h-[44px]"
          >
            မဟုတ်ပါ
          </button>
        </div>
      )}
    </div>
  );
}
