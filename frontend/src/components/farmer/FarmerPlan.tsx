/** Crop plan listing and detail view for farmers. */

import { useState, useEffect } from "react";
import { listPlans, acceptPlan, rejectPlan } from "@/api/farmer";
import type { CropPlan } from "@/types/farmer";

const STATUS_STYLES: Record<string, string> = {
  draft: "bg-warning/10 text-warning",
  active: "bg-primary/10 text-primary",
  completed: "bg-primary/20 text-primary",
  abandoned: "bg-danger/10 text-danger",
};

const STATUS_LABELS: Record<string, string> = {
  draft: "မူကြမ်း",
  active: "လက်ခံပြီး",
  completed: "ပြီးစီးပြီ",
  abandoned: "ပယ်ဖျက်ပြီ",
};

/** Crop plan management for farmers. */
export function FarmerPlan() {
  const [plans, setPlans] = useState<CropPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  const loadPlans = () => {
    setLoading(true);
    listPlans()
      .then(setPlans)
      .catch(() => setPlans([]))
      .finally(() => setLoading(false));
  };

  useEffect(loadPlans, []);

  const handleAccept = async (planId: string) => {
    await acceptPlan(planId);
    loadPlans();
  };

  const handleReject = async (planId: string) => {
    await rejectPlan(planId);
    loadPlans();
  };

  return (
    <div className="space-y-6 max-w-lg mx-auto">
      <h1 className="text-xl font-display text-text-primary font-myanmar">
        သီးနှံ အစီအစဉ်များ
      </h1>

      {loading ? (
        <p className="text-text-tertiary text-center py-8">Loading...</p>
      ) : plans.length === 0 ? (
        <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
          <p className="text-text-secondary font-myanmar">အစီအစဉ် မရှိသေးပါ</p>
          <p className="text-text-tertiary text-sm mt-1">
            Register a farm and generate a plan to get started
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className="rounded-xl bg-surface-elevated border border-border overflow-hidden"
            >
              {/* Plan header */}
              <button
                onClick={() =>
                  setExpanded(expanded === plan.id ? null : plan.id)
                }
                className="w-full p-4 text-left min-h-[44px]"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-text-primary">
                      {plan.crop_ids.join(", ")}
                    </p>
                    <p className="text-sm text-text-secondary mt-0.5">
                      {plan.season} {plan.year}
                    </p>
                  </div>
                  <span
                    className={`shrink-0 px-2 py-1 rounded-md text-xs font-semibold ${
                      STATUS_STYLES[plan.status] ?? ""
                    }`}
                  >
                    {STATUS_LABELS[plan.status] ?? plan.status}
                  </span>
                </div>
                {plan.portfolio_weights && (
                  <div className="flex gap-2 mt-2 flex-wrap">
                    {Object.entries(plan.portfolio_weights).map(
                      ([crop, weight]) => (
                        <span
                          key={crop}
                          className="text-xs px-2 py-0.5 rounded bg-surface border border-border-subtle text-text-secondary"
                        >
                          {crop}: {Math.round(weight * 100)}%
                        </span>
                      ),
                    )}
                  </div>
                )}
              </button>

              {/* Expanded detail */}
              {expanded === plan.id && (
                <div className="border-t border-border px-4 pb-4">
                  {/* Confidence metrics */}
                  {plan.confidence_metrics && (
                    <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
                      <div className="text-text-tertiary">
                        Success probability
                      </div>
                      <div className="text-text-primary font-semibold">
                        {Math.round(
                          (plan.confidence_metrics.success_probability ?? 0) *
                            100,
                        )}
                        %
                      </div>
                    </div>
                  )}

                  {/* Applications schedule */}
                  {plan.applications.length > 0 && (
                    <div className="mt-4">
                      <p className="text-sm font-semibold text-text-secondary mb-2 font-myanmar">
                        ဓာတ်မြေသြဇာ အစီအစဉ်
                      </p>
                      <div className="space-y-2">
                        {plan.applications.map((app) => (
                          <div
                            key={app.id}
                            className={`rounded-lg px-3 py-2 text-sm border ${
                              app.applied
                                ? "border-primary/30 bg-primary/5"
                                : "border-border bg-surface"
                            }`}
                          >
                            <div className="flex justify-between">
                              <span className="text-text-primary">
                                {app.fertilizer_name}
                              </span>
                              <span className="text-text-tertiary">
                                Day {app.planned_day}
                              </span>
                            </div>
                            <p className="text-text-secondary text-xs mt-0.5">
                              {app.crop_id} · {app.stage} ·{" "}
                              {app.planned_rate_kg_per_ha} kg/ha
                              {app.applied && " ✓"}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions for draft plans */}
                  {plan.status === "draft" && (
                    <div className="flex gap-3 mt-4">
                      <button
                        onClick={() => handleAccept(plan.id)}
                        className="flex-1 py-2.5 rounded-lg bg-primary text-white font-semibold text-sm min-h-[44px]"
                      >
                        လက်ခံပါ
                      </button>
                      <button
                        onClick={() => handleReject(plan.id)}
                        className="flex-1 py-2.5 rounded-lg border border-danger text-danger font-semibold text-sm min-h-[44px]"
                      >
                        ပယ်ဖျက်ပါ
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
