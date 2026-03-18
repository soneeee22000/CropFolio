interface ConfidenceGaugeProps {
  value: number;
  label?: string;
  size?: number;
}

/** SVG radial gauge showing confidence/success probability. */
export function ConfidenceGauge({
  value,
  label = "Success",
  size = 100,
}: ConfidenceGaugeProps) {
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const filled = circumference * value;
  const center = size / 2;
  const pct = Math.round(value * 100);

  const color = value >= 0.7 ? "#1B7A4A" : value >= 0.4 ? "#D4940A" : "#C43B3B";

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="-rotate-90">
        {/* Background track */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke="currentColor"
          className="text-border"
          strokeWidth={6}
        />
        {/* Filled arc */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={6}
          strokeDasharray={`${filled} ${circumference - filled}`}
          strokeLinecap="round"
          className="transition-all duration-700"
        />
      </svg>
      <div
        className="absolute flex flex-col items-center justify-center"
        style={{ width: size, height: size }}
      >
        <span className="font-data text-xl font-medium text-text-primary">
          {pct}%
        </span>
      </div>
      <span className="text-[10px] uppercase tracking-wide text-text-tertiary">
        {label}
      </span>
    </div>
  );
}
