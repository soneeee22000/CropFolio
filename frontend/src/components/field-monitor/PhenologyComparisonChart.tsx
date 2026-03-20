import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { useLanguage } from "@/i18n/LanguageContext";
import type { PlotObservation } from "@/types/field-monitor";

interface PhenologyComparisonChartProps {
  observations: PlotObservation[];
}

/** Recharts line chart: expected vs observed VH dB over time. */
export function PhenologyComparisonChart({
  observations,
}: PhenologyComparisonChartProps) {
  const { t } = useLanguage();

  const data = observations.map((obs) => ({
    date: obs.date.slice(5),
    observed: obs.observed_vh_db,
    expected: obs.expected_vh_db,
  }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 8, right: 16, bottom: 8, left: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10, fill: "var(--color-text-tertiary)" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 10, fill: "var(--color-text-tertiary)" }}
            tickLine={false}
            label={{
              value: "VH (dB)",
              angle: -90,
              position: "insideLeft",
              style: { fontSize: 10, fill: "var(--color-text-tertiary)" },
            }}
          />
          <Tooltip
            contentStyle={{
              background: "var(--color-surface-elevated)",
              border: "1px solid var(--color-border)",
              borderRadius: "8px",
              fontSize: "12px",
            }}
          />
          <Legend wrapperStyle={{ fontSize: "11px" }} />
          <Line
            type="monotone"
            dataKey="expected"
            name={t("fieldMonitor.expectedVH")}
            stroke="#1B7A4A"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="observed"
            name={t("fieldMonitor.observedVH")}
            stroke="#D4940A"
            strokeWidth={2}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
