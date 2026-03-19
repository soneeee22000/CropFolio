import { useState } from "react";
import { formatMMK } from "@/utils/formatters";
import { useLanguage } from "@/i18n/LanguageContext";
import type { FertilizerPlan } from "@/types/fertilizer-plan";

interface FertilizerPlanCardProps {
  plan: FertilizerPlan;
}

/** LP-optimized fertilizer application plan with growth stages, NPK, ROI. */
export function FertilizerPlanCard({ plan }: FertilizerPlanCardProps) {
  const { t } = useLanguage();
  const [expanded, setExpanded] = useState(false);

  const npkTotal =
    (plan.nutrient_totals.N ?? 0) +
    (plan.nutrient_totals.P ?? 0) +
    (plan.nutrient_totals.K ?? 0);

  return (
    <div className="mt-4 border border-border rounded-lg overflow-hidden">
      {/* Header — always visible */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-4 hover:bg-surface-subtle transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <div
            className={`w-2 h-2 rounded-full ${
              plan.lp_feasible ? "bg-primary" : "bg-warning"
            }`}
          />
          <span className="text-sm font-medium text-text-primary">
            {t("fertPlan.title")}
          </span>
          <span
            className={`text-[10px] uppercase tracking-wide px-2 py-0.5 rounded ${
              plan.lp_feasible
                ? "bg-primary/10 text-primary"
                : "bg-warning/10 text-warning"
            }`}
          >
            {plan.lp_feasible
              ? t("fertPlan.optimized")
              : t("fertPlan.fallback")}
          </span>
        </div>
        <div className="flex items-center gap-4">
          <span className="font-data text-sm text-accent">
            {plan.roi_estimate.return_ratio}x ROI
          </span>
          <svg
            className={`w-4 h-4 text-text-tertiary transition-transform ${
              expanded ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            strokeWidth={2}
          >
            <path d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div className="border-t border-border p-4 space-y-5 animate-fade-in-up">
          {/* ROI callout */}
          <div className="grid grid-cols-3 gap-3">
            <div className="text-center p-3 rounded-lg bg-accent/5">
              <div className="font-data text-xl text-accent">
                {formatMMK(plan.roi_estimate.total_cost_mmk)}
              </div>
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary mt-1">
                {t("fertPlan.totalCost")}
              </div>
            </div>
            <div className="text-center p-3 rounded-lg bg-primary/5">
              <div className="font-data text-xl text-primary">
                +{plan.roi_estimate.expected_yield_increase_pct}%
              </div>
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary mt-1">
                {t("fertPlan.yieldIncrease")}
              </div>
            </div>
            <div className="text-center p-3 rounded-lg bg-accent/5">
              <div className="font-data text-xl text-accent">
                {plan.roi_estimate.return_ratio}x
              </div>
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary mt-1">
                {t("fertPlan.returnRatio")}
              </div>
            </div>
          </div>

          {/* NPK bar */}
          {npkTotal > 0 && (
            <div>
              <div className="text-xs uppercase tracking-wide text-text-tertiary mb-2">
                {t("fertPlan.nutrientDelivery")}
              </div>
              <div className="flex h-6 rounded-lg overflow-hidden">
                {plan.nutrient_totals.N > 0 && (
                  <div
                    className="bg-blue-500 flex items-center justify-center text-[10px] text-white font-medium"
                    style={{
                      width: `${(plan.nutrient_totals.N / npkTotal) * 100}%`,
                    }}
                  >
                    N: {plan.nutrient_totals.N}
                  </div>
                )}
                {plan.nutrient_totals.P > 0 && (
                  <div
                    className="bg-amber-500 flex items-center justify-center text-[10px] text-white font-medium"
                    style={{
                      width: `${(plan.nutrient_totals.P / npkTotal) * 100}%`,
                    }}
                  >
                    P: {plan.nutrient_totals.P}
                  </div>
                )}
                {plan.nutrient_totals.K > 0 && (
                  <div
                    className="bg-red-500 flex items-center justify-center text-[10px] text-white font-medium"
                    style={{
                      width: `${(plan.nutrient_totals.K / npkTotal) * 100}%`,
                    }}
                  >
                    K: {plan.nutrient_totals.K}
                  </div>
                )}
              </div>
              <div className="text-[10px] text-text-tertiary mt-1">kg/ha</div>
            </div>
          )}

          {/* Growth stage timeline */}
          {plan.applications.length > 0 && (
            <div>
              <div className="text-xs uppercase tracking-wide text-text-tertiary mb-3">
                {t("fertPlan.applicationSchedule")}
              </div>
              <div className="space-y-2">
                {plan.applications.map((app, idx) => (
                  <div
                    key={`${app.stage}-${app.fertilizer_id}-${idx}`}
                    className="flex items-center gap-3 p-3 rounded-lg border border-border"
                  >
                    <div className="flex-shrink-0 w-12 text-center">
                      <div className="font-data text-lg text-text-primary">
                        {app.day}
                      </div>
                      <div className="text-[9px] uppercase text-text-tertiary">
                        {t("fertPlan.day")}
                      </div>
                    </div>
                    <div className="w-px h-8 bg-border" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm text-text-primary font-medium truncate">
                        {app.fertilizer_name}
                      </div>
                      <div className="text-xs text-text-tertiary capitalize">
                        {app.stage.replace(/_/g, " ")} — {app.rate_kg_per_ha}{" "}
                        kg/ha
                      </div>
                    </div>
                    <div className="flex-shrink-0 font-data text-sm text-text-secondary">
                      {formatMMK(app.cost_mmk)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Flags */}
          {plan.micronutrient_flags.length > 0 && (
            <div>
              <div className="text-xs uppercase tracking-wide text-text-tertiary mb-2">
                {t("fertPlan.micronutrientAlerts")}
              </div>
              {plan.micronutrient_flags.map((flag, idx) => (
                <div
                  key={`micro-${idx}`}
                  className="flex items-start gap-2 p-2 rounded bg-warning/5 border border-warning/20 mb-1"
                >
                  <span className="text-warning text-sm mt-0.5">!</span>
                  <div>
                    <span className="text-xs font-medium text-text-primary capitalize">
                      {flag.nutrient}
                    </span>
                    <span className="text-[10px] text-text-tertiary ml-2">
                      ({flag.severity})
                    </span>
                    <div className="text-xs text-text-secondary mt-0.5">
                      {flag.recommendation}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {plan.interaction_flags.length > 0 && (
            <div>
              <div className="text-xs uppercase tracking-wide text-text-tertiary mb-2">
                {t("fertPlan.nutrientBalance")}
              </div>
              {plan.interaction_flags.map((flag, idx) => (
                <div
                  key={`interact-${idx}`}
                  className="flex items-start gap-2 p-2 rounded bg-danger/5 border border-danger/20 mb-1"
                >
                  <span className="text-danger text-sm mt-0.5">!</span>
                  <div>
                    <span className="text-xs font-medium text-text-primary">
                      {flag.ratio_name}: {flag.actual_ratio}
                    </span>
                    <span className="text-[10px] text-text-tertiary ml-2">
                      (optimal: {flag.optimal_range})
                    </span>
                    <div className="text-xs text-text-secondary mt-0.5">
                      {flag.recommendation}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
