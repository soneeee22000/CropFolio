/** Simple weather display placeholder — will wrap existing climate service. */

/** Weather overview for farmer's township. */
export function FarmerWeather() {
  return (
    <div className="space-y-6 max-w-lg mx-auto">
      <h1 className="text-xl font-display text-text-primary font-myanmar">
        ရာသီဥတု
      </h1>

      <div className="rounded-xl bg-surface-elevated border border-border p-6 text-center">
        <svg
          className="w-16 h-16 mx-auto text-primary/30 mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          strokeWidth={1}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"
          />
        </svg>
        <p className="text-text-secondary font-myanmar text-lg">
          ရာသီဥတု အချက်အလက်များ မကြာမီ ရရှိပါမည်
        </p>
        <p className="text-text-tertiary text-sm mt-2">
          Weather data coming soon — will integrate with NASA POWER and
          Open-Meteo
        </p>
      </div>
    </div>
  );
}
