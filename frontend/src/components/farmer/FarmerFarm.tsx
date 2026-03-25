/** Farm registration and management screen. */

import { useState, useEffect } from "react";
import { listFarms, createFarm, createPlot } from "@/api/farmer";
import type { Farm } from "@/types/farmer";

/** Farm and plot management for farmers. */
export function FarmerFarm() {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [name, setName] = useState("");
  const [township, setTownship] = useState("");
  const [area, setArea] = useState("");
  const [saving, setSaving] = useState(false);

  const loadFarms = () => {
    setLoading(true);
    listFarms()
      .then(setFarms)
      .catch(() => setFarms([]))
      .finally(() => setLoading(false));
  };

  useEffect(loadFarms, []);

  const handleCreate = async () => {
    if (!name.trim() || !township.trim() || !area) return;
    setSaving(true);
    try {
      await createFarm({
        name: name.trim(),
        township_id: township.trim(),
        total_area_hectares: parseFloat(area),
      });
      setShowAdd(false);
      setName("");
      setTownship("");
      setArea("");
      loadFarms();
    } finally {
      setSaving(false);
    }
  };

  const handleAddPlot = async (farmId: string) => {
    const plotArea = prompt("Plot area in hectares:");
    if (!plotArea) return;
    await createPlot(farmId, {
      name: `Plot ${Date.now()}`,
      area_hectares: parseFloat(plotArea),
    });
    loadFarms();
  };

  return (
    <div className="space-y-6 max-w-lg mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-display text-text-primary font-myanmar">
          ကျွန်ုပ်၏ လယ်ယာ
        </h1>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="px-3 py-2 rounded-lg bg-primary text-white text-sm font-semibold min-h-[44px]"
        >
          + လယ်သစ်
        </button>
      </div>

      {/* Add farm form */}
      {showAdd && (
        <div className="rounded-xl bg-surface-elevated border border-border p-4 space-y-3">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="လယ်အမည် (e.g. North Field)"
            className="block w-full rounded-lg bg-surface border border-border px-3 py-2.5 text-text-primary focus:border-primary focus:outline-none"
            style={{ fontSize: "16px" }}
          />
          <input
            type="text"
            value={township}
            onChange={(e) => setTownship(e.target.value)}
            placeholder="Township ID (e.g. mdy_meiktila)"
            className="block w-full rounded-lg bg-surface border border-border px-3 py-2.5 text-text-primary focus:border-primary focus:outline-none"
            style={{ fontSize: "16px" }}
          />
          <input
            type="number"
            value={area}
            onChange={(e) => setArea(e.target.value)}
            placeholder="Area (hectares)"
            step="0.1"
            className="block w-full rounded-lg bg-surface border border-border px-3 py-2.5 text-text-primary focus:border-primary focus:outline-none"
            style={{ fontSize: "16px" }}
          />
          <button
            onClick={handleCreate}
            disabled={saving}
            className="w-full py-2.5 rounded-lg bg-primary text-white font-semibold disabled:opacity-50 min-h-[44px]"
          >
            {saving ? "Saving..." : "သိမ်းဆည်းပါ"}
          </button>
        </div>
      )}

      {/* Farm list */}
      {loading ? (
        <p className="text-text-tertiary text-center py-8">Loading...</p>
      ) : farms.length === 0 ? (
        <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
          <p className="text-text-secondary font-myanmar">လယ်ယာ မရှိသေးပါ</p>
          <p className="text-text-tertiary text-sm mt-1">
            Add your first farm to get started
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {farms.map((farm) => (
            <div
              key={farm.id}
              className="rounded-xl bg-surface-elevated border border-border p-4"
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-text-primary">
                    {farm.name}
                  </h3>
                  <p className="text-sm text-text-secondary">
                    {farm.township_id} · {farm.total_area_hectares} ha
                  </p>
                </div>
              </div>
              {farm.plots.length > 0 && (
                <div className="mt-3 space-y-2">
                  {farm.plots.map((plot) => (
                    <div
                      key={plot.id}
                      className="rounded-lg bg-surface border border-border-subtle px-3 py-2 text-sm"
                    >
                      <span className="text-text-primary">
                        {plot.name ?? "Plot"}
                      </span>
                      <span className="text-text-tertiary ml-2">
                        {plot.area_hectares} ha
                      </span>
                    </div>
                  ))}
                </div>
              )}
              <button
                onClick={() => handleAddPlot(farm.id)}
                className="mt-3 text-sm text-primary font-semibold min-h-[44px]"
              >
                + Plot ထပ်ထည့်ပါ
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
