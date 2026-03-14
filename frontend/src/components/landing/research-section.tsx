import { useInView } from "./use-in-view";

/** Correlation values computed from real data. */
const RICE_SESAME_YIELD_CORR = "-0.49";
const RICE_CHICKPEA_YIELD_CORR = "+0.13";
const RICE_SESAME_REVENUE_CORR = "0.00";

interface FindingCard {
  /** Large stat number displayed prominently. */
  stat: string;
  /** Label below the stat. */
  label: string;
  /** Card heading. */
  title: string;
  /** Card body text. */
  body: string;
}

const findings: FindingCard[] = [
  {
    stat: RICE_SESAME_YIELD_CORR,
    label: "Yield correlation (FAOSTAT 2010\u20132021)",
    title: "The Rice-Sesame Hedge",
    body: "When drought hurts rice, sesame thrives. The strongest natural hedge among Myanmar crops.",
  },
  {
    stat: RICE_CHICKPEA_YIELD_CORR,
    label: "Rice-Chickpea correlation",
    title: "Not All Crops Hedge Rice",
    body: "Our data contradicted our assumptions. Chickpea is NOT a rice hedge. Only sesame is.",
  },
  {
    stat: RICE_SESAME_REVENUE_CORR,
    label: "Rice-Sesame revenue correlation",
    title: "Yield Risk \u2260 Price Risk",
    body: "Yield hedging works (\u20130.49) but prices co-move (+0.74). Our dual model captures both.",
  },
];

/**
 * "Research & Findings" section showcasing data-driven insights
 * from FAOSTAT yield and WFP price analysis.
 */
export function ResearchSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.1 });

  return (
    <section
      id="research"
      ref={ref}
      className="bg-surface text-text-primary py-12 sm:py-16 px-6"
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div
          className={`text-center mb-10 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-4 font-body">
            Research &amp; Findings
          </p>
          <h2 className="font-display text-4xl sm:text-5xl text-text-primary leading-tight text-balance">
            Built on 12 Years of Data, Not Assumptions
          </h2>
        </div>

        {/* Finding cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {findings.map((card, index) => (
            <div
              key={card.title}
              className={`bg-surface-elevated border border-border rounded-xl p-6 transition-all duration-700 ${
                isInView
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{ transitionDelay: `${index * 150 + 200}ms` }}
            >
              {/* Big stat */}
              <p className="font-data text-5xl sm:text-6xl text-text-primary tracking-tight leading-none mb-1">
                {card.stat}
              </p>
              <p className="text-xs text-text-tertiary font-body mb-4">
                {card.label}
              </p>

              {/* Title + body */}
              <h3 className="font-display text-lg text-text-primary mb-2">
                {card.title}
              </h3>
              <p className="font-body text-sm text-text-secondary leading-relaxed">
                {card.body}
              </p>
            </div>
          ))}
        </div>

        {/* Citation line */}
        <p
          className={`text-center text-xs text-text-tertiary font-body transition-all duration-700 delay-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          Source: FAOSTAT 2010&ndash;2021 &middot; WFP Myanmar 2022&ndash;2025
        </p>
      </div>
    </section>
  );
}
