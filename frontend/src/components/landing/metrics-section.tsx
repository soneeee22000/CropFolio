import { useInView } from "./use-in-view";
import { AnimatedCounter } from "./animated-counter";

const metrics = [
  {
    value: 51.3,
    suffix: "%",
    label: "Risk Reduction",
    sublabel: "vs Monocrop",
    decimals: 1,
  },
  {
    value: 1.5,
    suffix: "M",
    prefix: "",
    label: "Expected Income",
    sublabel: "MMK per Hectare",
    decimals: 1,
  },
  {
    value: 10,
    suffix: "%",
    label: "Catastrophic Loss",
    sublabel: "Probability",
    decimals: 0,
  },
];

/**
 * Metrics section with animated counters showing
 * key portfolio optimization results.
 */
export function MetricsSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.3 });

  return (
    <section
      ref={ref}
      className="relative py-12 sm:py-16 px-6 overflow-hidden"
      style={{
        background:
          "linear-gradient(180deg, #1A1A18 0%, #1E1E1C 50%, #1A1A18 100%)",
      }}
    >
      {/* Decorative elements */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
      </div>

      <div className="max-w-5xl mx-auto relative">
        {/* Header */}
        <div
          className={`text-center mb-8 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-[#A3A29D] mb-4 font-body">
            The Results
          </p>
          <h2 className="font-display text-4xl sm:text-5xl text-[#FAFAF8] leading-tight text-balance">
            Real Impact, Real Numbers
          </h2>
        </div>

        {/* Metrics cards */}
        <div className="grid sm:grid-cols-3 gap-6 sm:gap-8">
          {metrics.map((metric, index) => (
            <div
              key={metric.label}
              className={`bg-[#242422] border border-[#333330] rounded-2xl p-8 text-center shadow-sm transition-all duration-700 hover:shadow-md ${
                isInView
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{ transitionDelay: `${index * 150 + 200}ms` }}
            >
              <div className="font-display text-5xl sm:text-6xl lg:text-7xl text-[#FAFAF8] mb-2">
                <AnimatedCounter
                  end={metric.value}
                  duration={1500}
                  suffix={metric.suffix}
                  prefix={metric.prefix || ""}
                  decimals={metric.decimals}
                  shouldStart={isInView}
                />
              </div>
              <div className="text-lg font-body text-[#FAFAF8] font-medium mb-1">
                {metric.label}
              </div>
              <div className="text-sm font-body text-[#A3A29D]">
                {metric.sublabel}
              </div>
            </div>
          ))}
        </div>

        {/* Context note */}
        <p
          className={`text-center text-sm text-[#A3A29D] font-body mt-8 transition-all duration-700 delay-700 ${
            isInView ? "opacity-100" : "opacity-0"
          }`}
        >
          Based on Magway township, monsoon season, rice + black gram + sesame
          portfolio
        </p>
      </div>
    </section>
  );
}
