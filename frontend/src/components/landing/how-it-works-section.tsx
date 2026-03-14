import { useInView } from "./use-in-view";
import { MapPin, CloudRain, PieChart, Shuffle } from "./icons";

const steps = [
  {
    number: "01",
    title: "Select Township",
    description: "Choose from 25 Myanmar agricultural townships",
    icon: MapPin,
    mockUI: (
      <div className="bg-surface-elevated border border-border rounded-lg p-4 space-y-3">
        <div className="text-xs text-text-tertiary font-body uppercase tracking-wide">
          Township
        </div>
        <div className="flex items-center gap-2 bg-surface-subtle rounded-md p-3">
          <MapPin className="w-4 h-4 text-primary" />
          <span className="font-body text-sm">Magway</span>
          <span className="ml-auto text-xs text-text-tertiary">
            Central Myanmar
          </span>
        </div>
        <div className="grid grid-cols-3 gap-2">
          {["Mandalay", "Sagaing", "Bago"].map((t) => (
            <div
              key={t}
              className="text-xs text-text-tertiary bg-surface-subtle/50 rounded px-2 py-1 text-center font-body"
            >
              {t}
            </div>
          ))}
        </div>
      </div>
    ),
  },
  {
    number: "02",
    title: "Assess Climate Risk",
    description:
      "Real-time drought and flood probability from NASA satellite data",
    icon: CloudRain,
    mockUI: (
      <div className="bg-surface-elevated border border-border rounded-lg p-4 space-y-3">
        <div className="text-xs text-text-tertiary font-body uppercase tracking-wide">
          Climate Risk Analysis
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-body">Drought Risk</span>
            <span className="text-sm font-data text-accent">32%</span>
          </div>
          <div className="h-2 bg-surface-subtle rounded-full overflow-hidden">
            <div className="h-full bg-accent w-[32%] rounded-full" />
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-body">Flood Risk</span>
            <span className="text-sm font-data text-primary">18%</span>
          </div>
          <div className="h-2 bg-surface-subtle rounded-full overflow-hidden">
            <div className="h-full bg-primary w-[18%] rounded-full" />
          </div>
        </div>
      </div>
    ),
  },
  {
    number: "03",
    title: "Optimize Portfolio",
    description: "Markowitz optimization finds the ideal crop mix",
    icon: PieChart,
    mockUI: (
      <div className="bg-surface-elevated border border-border rounded-lg p-4 space-y-3">
        <div className="text-xs text-text-tertiary font-body uppercase tracking-wide">
          Optimal Allocation
        </div>
        <div className="flex items-center gap-4">
          <div className="relative w-20 h-20">
            <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90">
              <circle
                cx="18"
                cy="18"
                r="15"
                fill="none"
                stroke="#e5e5e3"
                strokeWidth="3"
              />
              <circle
                cx="18"
                cy="18"
                r="15"
                fill="none"
                stroke="#1B7A4A"
                strokeWidth="3"
                strokeDasharray="47 100"
              />
              <circle
                cx="18"
                cy="18"
                r="15"
                fill="none"
                stroke="#B8860B"
                strokeWidth="3"
                strokeDasharray="28 100"
                strokeDashoffset="-47"
              />
              <circle
                cx="18"
                cy="18"
                r="15"
                fill="none"
                stroke="#5D8A66"
                strokeWidth="3"
                strokeDasharray="25 100"
                strokeDashoffset="-75"
              />
            </svg>
          </div>
          <div className="space-y-1 text-sm font-body">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-primary" />
              <span>Rice 47%</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent" />
              <span>Black Gram 28%</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#5D8A66]" />
              <span>Sesame 25%</span>
            </div>
          </div>
        </div>
      </div>
    ),
  },
  {
    number: "04",
    title: "Simulate 1,000 Seasons",
    description: "Monte Carlo simulation proves the diversification benefit",
    icon: Shuffle,
    mockUI: (
      <div className="bg-surface-elevated border border-border rounded-lg p-4 space-y-3">
        <div className="text-xs text-text-tertiary font-body uppercase tracking-wide">
          Monte Carlo Results
        </div>
        <div className="h-16 flex items-end gap-0.5">
          {[12, 18, 35, 58, 72, 85, 92, 88, 75, 52, 35, 20, 10, 5, 3].map(
            (h, i) => (
              <div
                key={i}
                className="flex-1 bg-primary/60 rounded-t"
                style={{ height: `${h}%` }}
              />
            ),
          )}
        </div>
        <div className="flex justify-between text-xs text-text-tertiary font-body">
          <span>Low Income</span>
          <span>Expected</span>
          <span>High Income</span>
        </div>
      </div>
    ),
  },
];

/**
 * "How It Works" section with 4 steps,
 * each showing a mock UI preview.
 */
export function HowItWorksSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.1 });

  return (
    <section
      id="how-it-works"
      ref={ref}
      className="bg-surface py-24 sm:py-32 px-6"
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div
          className={`text-center mb-16 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-4 font-body">
            The Process
          </p>
          <h2 className="font-display text-4xl sm:text-5xl text-text-primary leading-tight text-balance">
            Four Steps to Resilience
          </h2>
        </div>

        {/* Steps */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className={`transition-all duration-700 ${
                isInView
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{ transitionDelay: `${index * 100 + 200}ms` }}
            >
              {/* Step number */}
              <div className="flex items-center gap-3 mb-4">
                <span className="font-data text-5xl text-border font-bold">
                  {step.number}
                </span>
                <step.icon className="w-6 h-6 text-primary" />
              </div>

              {/* Step content */}
              <h3 className="font-display text-xl text-text-primary mb-2">
                {step.title}
              </h3>
              <p className="text-text-secondary font-body text-sm mb-4 leading-relaxed">
                {step.description}
              </p>

              {/* Mock UI */}
              <div className="transform transition-transform hover:scale-[1.02]">
                {step.mockUI}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
