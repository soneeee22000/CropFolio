import { useInView } from "./use-in-view";
import { VolatilityVisualization } from "./volatility-visualization";
import { TrendingUp, Sprout, Award } from "./icons";

/** Correlation values computed from real FAOSTAT data. */
const CORRELATIONS = [
  { pair: "Rice × Sesame", corr: "-0.49", color: "text-primary" },
  { pair: "Rice × Groundnut", corr: "-0.05", color: "text-text-tertiary" },
  { pair: "Rice × Chickpea", corr: "+0.13", color: "text-accent" },
];

/**
 * "The Insight" — merged section combining the problem statement,
 * cross-domain portfolio theory bridge, and research-backed correlations.
 */
export function InsightSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.15 });

  return (
    <section
      id="insight"
      ref={ref}
      className="bg-surface text-text-primary py-12 sm:py-16 px-6"
    >
      <div className="max-w-6xl mx-auto">
        {/* Row 1: Problem text + Volatility Viz */}
        <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center mb-12">
          <div
            className={`transition-all duration-700 ${
              isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            <p className="text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-4 font-body">
              The Insight
            </p>

            <h2 className="font-display text-4xl sm:text-5xl lg:text-6xl text-text-primary mb-6 leading-tight text-balance">
              One Crop. One Risk.
              <br />
              <span className="text-accent">We Have the Data to Fix It.</span>
            </h2>

            <div className="space-y-6 text-text-secondary font-body text-lg leading-relaxed">
              <p>
                <span className="text-text-primary font-medium">
                  70% of Myanmar&apos;s farmers
                </span>{" "}
                grow rice as their only crop. When the monsoon fails, they lose
                everything. When it floods, they lose everything.
              </p>

              <p>There is no hedge. No safety net. No diversification.</p>

              <p className="text-accent font-medium">
                But rice isn&apos;t the only option.
              </p>
            </div>
          </div>

          <div
            className={`transition-all duration-700 delay-200 ${
              isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            <div className="bg-surface-elevated border border-border rounded-2xl p-8 shadow-sm">
              <p className="text-sm text-text-tertiary mb-6 font-body text-center">
                Income volatility comparison
              </p>
              <VolatilityVisualization isInView={isInView} />
            </div>
          </div>
        </div>

        {/* Row 2: Finance ↔ Agriculture cards */}
        <div
          className={`text-center mb-8 transition-all duration-700 delay-300 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <h3 className="font-display text-3xl sm:text-4xl leading-tight text-balance">
            Portfolio Theory for Farms
          </h3>
        </div>

        <div className="grid md:grid-cols-2 gap-8 relative mb-10">
          {/* Connecting line */}
          <div className="hidden md:block absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-px">
            <svg className="w-full h-8 overflow-visible">
              <defs>
                <linearGradient
                  id="lineGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >
                  <stop offset="0%" stopColor="#B8860B" stopOpacity="0.5" />
                  <stop offset="50%" stopColor="#B8860B" stopOpacity="1" />
                  <stop offset="100%" stopColor="#1B7A4A" stopOpacity="0.5" />
                </linearGradient>
              </defs>
              <line
                x1="0"
                y1="4"
                x2="80"
                y2="4"
                stroke="url(#lineGradient)"
                strokeWidth="2"
                strokeDasharray="4 4"
                className={`transition-all duration-1000 delay-500 ${
                  isInView ? "opacity-100" : "opacity-0"
                }`}
              />
              <circle
                cx="40"
                cy="4"
                r="6"
                fill="#B8860B"
                className={`transition-all duration-700 delay-700 ${
                  isInView ? "opacity-100 scale-100" : "opacity-0 scale-0"
                }`}
                style={{ transformOrigin: "40px 4px" }}
              />
            </svg>
          </div>

          {/* Finance Card */}
          <div
            className={`bg-surface-elevated border border-border rounded-2xl p-8 transition-all duration-700 delay-400 ${
              isInView
                ? "opacity-100 translate-x-0"
                : "opacity-0 -translate-x-8"
            }`}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-accent" />
              </div>
              <h3 className="font-display text-2xl">In Finance</h3>
            </div>
            <ul className="space-y-4 font-body text-text-secondary">
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                <span>Stocks have different risk profiles</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                <span>Negatively correlated assets reduce portfolio risk</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                <span className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-accent shrink-0" />
                  Markowitz won a Nobel Prize for proving this in 1952
                </span>
              </li>
            </ul>
          </div>

          {/* Agriculture Card */}
          <div
            className={`bg-surface-elevated border border-border rounded-2xl p-8 transition-all duration-700 delay-500 ${
              isInView ? "opacity-100 translate-x-0" : "opacity-0 translate-x-8"
            }`}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <Sprout className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-display text-2xl">In Agriculture</h3>
            </div>
            <ul className="space-y-4 font-body text-text-secondary">
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0" />
                <span>Crops have different climate tolerances</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0" />
                <span>
                  Rice &amp; sesame yield correlation:{" "}
                  <span className="font-data text-primary font-medium">
                    -0.49
                  </span>{" "}
                  (12 years of FAOSTAT data)
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0" />
                <span className="text-primary font-medium">
                  Real data. Real correlations. Real diversification.
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Row 3: Correlation grid + revenue insight */}
        <div
          className={`grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-2xl mx-auto transition-all duration-700 delay-600 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          {CORRELATIONS.map((item) => (
            <div
              key={item.pair}
              className="text-center bg-surface-elevated border border-border rounded-xl p-3"
            >
              <p className={`font-data text-lg font-medium ${item.color}`}>
                {item.corr}
              </p>
              <p className="text-[10px] text-text-tertiary mt-1">{item.pair}</p>
            </div>
          ))}
          {/* Revenue correlation — the key research insight */}
          <div className="text-center bg-surface-elevated border border-accent/30 rounded-xl p-3">
            <p className="font-data text-lg font-medium text-accent">0.00</p>
            <p className="text-[10px] text-text-tertiary mt-1">Revenue Corr.</p>
          </div>
        </div>

        <p className="text-center text-[10px] text-text-tertiary/60 mt-2">
          Yield correlations from FAOSTAT 2010–2021 · Revenue: yield × WFP price
        </p>

        {/* Bridge statement */}
        <div
          className={`text-center mt-6 transition-all duration-700 delay-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="font-display text-xl sm:text-2xl text-accent/90 italic">
            &ldquo;Not assumptions. 12 years of data.&rdquo;
          </p>
          <p className="text-sm text-text-tertiary font-body mt-2">
            Yield Risk ≠ Price Risk — our dual model captures both.
          </p>
        </div>
      </div>
    </section>
  );
}
