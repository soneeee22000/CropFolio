interface FertilizerBadgeProps {
  formulation: string;
  name?: string;
  score?: number;
  size?: "sm" | "md";
}

/** NPK formulation badge with color-coded segments. */
export function FertilizerBadge({
  formulation,
  name,
  score,
  size = "md",
}: FertilizerBadgeProps) {
  const parts = formulation.split("-");
  const hasNPK = parts.length >= 3;

  const sizeClasses =
    size === "sm" ? "text-[10px] px-2 py-0.5" : "text-xs px-2.5 py-1";

  return (
    <div className="inline-flex items-center gap-2">
      <span
        className={`inline-flex items-center gap-1 rounded-md border border-border font-mono font-medium ${sizeClasses}`}
      >
        {hasNPK ? (
          <>
            <span className="text-blue-500">{parts[0]}</span>
            <span className="text-text-tertiary">-</span>
            <span className="text-amber-500">{parts[1]}</span>
            <span className="text-text-tertiary">-</span>
            <span className="text-red-400">{parts[2]}</span>
            {parts[3] && (
              <>
                <span className="text-text-tertiary">-</span>
                <span className="text-green-500">{parts[3]}</span>
              </>
            )}
          </>
        ) : (
          <span className="text-text-secondary">{formulation}</span>
        )}
      </span>
      {name && <span className="text-xs text-text-secondary">{name}</span>}
      {score !== undefined && (
        <span className="text-[10px] text-text-tertiary">
          ({(score * 100).toFixed(0)}%)
        </span>
      )}
    </div>
  );
}
