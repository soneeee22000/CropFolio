/** Farmer home screen — today's tasks, quick stats. */

import { useState, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import { getTodayTasks } from "@/api/farmer";
import type { FertilizerApplicationItem } from "@/types/farmer";

/** Home screen showing pending tasks and quick overview. */
export function FarmerHome() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<FertilizerApplicationItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTodayTasks()
      .then(setTasks)
      .catch(() => setTasks([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6 max-w-lg mx-auto">
      {/* Greeting */}
      <div>
        <h1 className="text-2xl font-display text-text-primary">
          {user?.full_name_mm ?? user?.full_name ?? "Farmer"}
        </h1>
        <p className="text-text-secondary font-myanmar mt-1">
          မင်္ဂလာပါ။ ဒီနေ့ သင့်အလုပ်တွေကို ကြည့်ပါ။
        </p>
      </div>

      {/* Pending tasks */}
      <section>
        <h2 className="text-lg font-semibold text-text-primary mb-3 font-myanmar">
          လုပ်ဆောင်ရမည့်အရာများ
        </h2>
        {loading ? (
          <div className="rounded-xl bg-surface-elevated border border-border p-6 text-center">
            <p className="text-text-tertiary">Loading...</p>
          </div>
        ) : tasks.length === 0 ? (
          <div className="rounded-xl bg-surface-elevated border border-border p-6 text-center">
            <svg
              className="w-12 h-12 mx-auto text-primary/40 mb-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p className="text-text-secondary font-myanmar">
              ယနေ့ လုပ်ဆောင်ရမည့်အရာ မရှိပါ
            </p>
            <p className="text-text-tertiary text-sm mt-1">
              No tasks for today
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="rounded-xl bg-surface-elevated border border-border p-4"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-text-primary">
                      {task.fertilizer_name}
                    </p>
                    <p className="text-sm text-text-secondary mt-0.5">
                      {task.crop_id} — {task.stage}
                    </p>
                    <p className="text-sm text-text-tertiary mt-1">
                      {task.planned_rate_kg_per_ha} kg/ha · Day{" "}
                      {task.planned_day}
                    </p>
                  </div>
                  <span className="shrink-0 px-2 py-1 rounded-md bg-warning/10 text-warning text-xs font-semibold">
                    Pending
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Quick stats placeholder */}
      <section>
        <h2 className="text-lg font-semibold text-text-primary mb-3 font-myanmar">
          အကျဉ်းချုပ်
        </h2>
        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-xl bg-surface-elevated border border-border p-4 text-center">
            <p className="text-2xl font-semibold text-primary">
              {tasks.length}
            </p>
            <p className="text-xs text-text-tertiary mt-1 font-myanmar">
              ကျန်ရှိသော လုပ်ငန်း
            </p>
          </div>
          <div className="rounded-xl bg-surface-elevated border border-border p-4 text-center">
            <p className="text-2xl font-semibold text-accent">--</p>
            <p className="text-xs text-text-tertiary mt-1 font-myanmar">
              လိုက်နာမှု ရမှတ်
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
