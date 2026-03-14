interface MetricCardProps {
  value: string;
  label: string;
  sublabel?: string;
  highlight?: boolean;
}

/** Large number display with label underneath. */
export function MetricCard({
  value,
  label,
  sublabel,
  highlight,
}: MetricCardProps) {
  return (
    <div
      className={`text-center p-4 rounded-lg ${highlight ? "bg-green-50 border border-green-200" : "bg-gray-50"}`}
    >
      <div
        className={`text-2xl font-bold ${highlight ? "text-green-700" : "text-gray-900"}`}
      >
        {value}
      </div>
      <div className="text-sm text-gray-600 mt-1">{label}</div>
      {sublabel && (
        <div className="text-xs text-gray-400 mt-0.5">{sublabel}</div>
      )}
    </div>
  );
}
