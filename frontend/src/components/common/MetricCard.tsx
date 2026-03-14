interface MetricCardProps {
  value: string;
  label: string;
  sublabel?: string;
  highlight?: boolean;
}

/** Premium metric display with monospace numbers. */
export function MetricCard({
  value,
  label,
  sublabel,
  highlight,
}: MetricCardProps) {
  return (
    <div
      className={`text-center p-6 rounded-xl transition-colors ${
        highlight ? "bg-accent/5 border border-accent/20" : "bg-surface-subtle"
      }`}
    >
      <div
        className={`font-data text-3xl font-medium ${
          highlight ? "text-accent" : "text-text-primary"
        }`}
      >
        {value}
      </div>
      <div className="text-[11px] uppercase tracking-[0.1em] text-text-tertiary mt-2">
        {label}
      </div>
      {sublabel && (
        <div className="text-xs text-text-tertiary mt-2 pt-2 border-t border-border-subtle">
          {sublabel}
        </div>
      )}
    </div>
  );
}
