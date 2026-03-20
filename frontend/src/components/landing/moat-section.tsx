import { useInView } from "./use-in-view";

interface MoatEngine {
  title: string;
  tag: string;
  description: string;
  detail: string;
}

const engines: MoatEngine[] = [
  {
    title: "Bayesian Belief Network",
    tag: "Inference",
    description: "Field observations update yield predictions in real time",
    detail:
      "Input drought, rainfall, or soil quality evidence and watch posterior probabilities shift per crop. Pure numpy — no heavy ML dependencies.",
  },
  {
    title: "Copula Tail Risk",
    tag: "Simulation",
    description: "Captures simultaneous crop failures that normal models miss",
    detail:
      "Gaussian copula replaces multivariate normal in Monte Carlo, revealing true tail dependence between crops under extreme climate stress.",
  },
  {
    title: "LP Fertilizer Optimizer",
    tag: "Optimization",
    description: "Growth-stage application plans with NPK delivery and ROI",
    detail:
      "Linear programming minimizes cost while meeting nutrient targets per growth stage. Includes micronutrient alerts and interaction flags.",
  },
  {
    title: "SAR Planting Verification",
    tag: "Remote Sensing",
    description: "Sentinel-1 radar confirms rice planting without field visits",
    detail:
      "VH/VV backscatter time series detect transplanting, vegetative growth, heading, and harvest phenology signals from space.",
  },
];

/** Technical moat section — 4 defensible engines. */
export function MoatSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.1 });

  return (
    <section
      id="moat"
      ref={ref}
      className="bg-surface text-text-primary py-12 sm:py-16 px-6"
    >
      <div className="max-w-6xl mx-auto">
        <div
          className={`text-center mb-8 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-4 font-body">
            Technical Moat
          </p>
          <h2 className="font-display text-4xl sm:text-5xl text-text-primary leading-tight text-balance">
            Four Engines. Hard to Replicate.
          </h2>
          <p className="text-text-secondary font-body mt-4 max-w-2xl mx-auto">
            Every engine answers: does this make us harder to copy?
          </p>
        </div>

        <div className="grid sm:grid-cols-2 gap-6">
          {engines.map((engine, index) => (
            <div
              key={engine.title}
              className={`bg-surface-elevated border border-border rounded-2xl p-8 transition-all duration-700 hover:border-primary/30 ${
                isInView
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{ transitionDelay: `${index * 100 + 200}ms` }}
            >
              <div className="flex items-center gap-3 mb-4">
                <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-primary/10 text-primary font-medium font-body">
                  {engine.tag}
                </span>
              </div>
              <h3 className="font-display text-xl text-text-primary mb-2">
                {engine.title}
              </h3>
              <p className="text-text-secondary font-body text-sm mb-3 leading-relaxed">
                {engine.description}
              </p>
              <p className="text-text-tertiary font-body text-xs leading-relaxed">
                {engine.detail}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
