import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { COMPLIANCE_COLORS } from "@/constants/map";
import { useLanguage } from "@/i18n/LanguageContext";

interface CompliancePieChartProps {
  compliant: number;
  warning: number;
  deviation: number;
}

/** Recharts donut showing compliant/warning/deviation distribution. */
export function CompliancePieChart({
  compliant,
  warning,
  deviation,
}: CompliancePieChartProps) {
  const { t } = useLanguage();

  const data = [
    {
      name: t("fieldMonitor.compliant"),
      value: compliant,
      color: COMPLIANCE_COLORS.compliant,
    },
    {
      name: t("fieldMonitor.warning"),
      value: warning,
      color: COMPLIANCE_COLORS.warning,
    },
    {
      name: t("fieldMonitor.deviation"),
      value: deviation,
      color: COMPLIANCE_COLORS.deviation,
    },
  ].filter((d) => d.value > 0);

  return (
    <div className="h-48 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={40}
            outerRadius={70}
            dataKey="value"
            paddingAngle={2}
            stroke="none"
          >
            {data.map((entry) => (
              <Cell key={entry.name} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name) => [String(value), String(name)]}
            contentStyle={{
              background: "var(--color-surface-elevated)",
              border: "1px solid var(--color-border)",
              borderRadius: "8px",
              fontSize: "12px",
            }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex justify-center gap-4 -mt-2">
        {data.map((entry) => (
          <div
            key={entry.name}
            className="flex items-center gap-1.5 text-xs text-text-secondary"
          >
            <span
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: entry.color }}
            />
            {entry.name} ({entry.value})
          </div>
        ))}
      </div>
    </div>
  );
}
