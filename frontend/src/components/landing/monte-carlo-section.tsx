import { useInView } from "./use-in-view";
import { Atom, Dice, Target } from "./icons";

const MAX_BAR_HEIGHT = 80;

const RICE_ONLY_HEIGHTS = [85, 40, 25, 15, 10, 8, 6, 5, 3, 2];
const OPTIMIZED_HEIGHTS = [3, 5, 12, 25, 35, 40, 35, 20, 10, 5];

interface CardData {
  icon: typeof Atom;
  title: string;
  body: string;
}

const cards: CardData[] = [
  {
    icon: Atom,
    title: "Born in Physics",
    body: "Monte Carlo simulation was invented during the Manhattan Project. When the math for neutron diffusion was intractable, scientists simulated millions of random scenarios instead.",
  },
  {
    icon: Dice,
    title: "Adopted by Wall Street",
    body: "Investment banks simulate 10,000+ market scenarios to stress-test portfolios before risking real capital. It\u2019s the gold standard for financial risk management.",
  },
  {
    icon: Target,
    title: "Applied to Farming",
    body: "CropFolio simulates 1,000 climate seasons for Myanmar. Each scenario tests your crop portfolio against a different combination of drought, flood, and price volatility.",
  },
];

/**
 * "The Science" section explaining Monte Carlo simulation
 * with origin cards and visual histogram comparison.
 */
export function MonteCarloSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.1 });

  return (
    <section
      id="the-science"
      ref={ref}
      className="bg-surface text-text-primary py-12 sm:py-16 px-6 border-t border-border"
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div
          className={`text-center mb-8 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-4 font-body">
            The Science
          </p>
          <h2 className="font-display text-4xl sm:text-5xl lg:text-6xl leading-tight text-balance">
            1,000 Stress Tests, Not One Guess
          </h2>
        </div>

        {/* 3-column card grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-10">
          {cards.map((card, index) => (
            <div
              key={card.title}
              className={`bg-surface-elevated border border-border rounded-2xl p-8 transition-all duration-700 ${
                isInView
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{ transitionDelay: `${index * 150 + 200}ms` }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center">
                  <card.icon className="w-6 h-6 text-accent" />
                </div>
                <h3 className="font-display text-xl">{card.title}</h3>
              </div>
              <p className="font-body text-text-secondary leading-relaxed">
                {card.body}
              </p>
            </div>
          ))}
        </div>

        {/* Visual comparison — two histograms */}
        <div
          className={`transition-all duration-700 delay-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <div className="grid sm:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Rice Only histogram */}
            <div className="bg-surface-elevated border border-border rounded-2xl p-6">
              <h4 className="font-display text-lg text-center mb-4">
                Rice Only
              </h4>
              <div
                className="flex items-end gap-1 justify-center"
                style={{ height: `${MAX_BAR_HEIGHT}px` }}
              >
                {RICE_ONLY_HEIGHTS.map((h, i) => (
                  <div
                    key={i}
                    className="flex-1 max-w-[24px] bg-[#C43B3B] rounded-t transition-all duration-700"
                    style={{
                      height: isInView
                        ? `${(h / 100) * MAX_BAR_HEIGHT}px`
                        : "0px",
                      transitionDelay: `${800 + i * 50}ms`,
                    }}
                  />
                ))}
              </div>
              <div className="flex justify-between text-xs text-text-tertiary font-body mt-3">
                <span>Loss</span>
                <span>Gain</span>
              </div>
              <p className="text-center text-sm text-[#C43B3B] font-body mt-4 font-medium">
                High loss probability, wide spread
              </p>
            </div>

            {/* Optimized Portfolio histogram */}
            <div className="bg-surface-elevated border border-border rounded-2xl p-6">
              <h4 className="font-display text-lg text-center mb-4">
                Optimized Portfolio
              </h4>
              <div
                className="flex items-end gap-1 justify-center"
                style={{ height: `${MAX_BAR_HEIGHT}px` }}
              >
                {OPTIMIZED_HEIGHTS.map((h, i) => (
                  <div
                    key={i}
                    className="flex-1 max-w-[24px] bg-[#1B7A4A] rounded-t transition-all duration-700"
                    style={{
                      height: isInView
                        ? `${(h / 100) * MAX_BAR_HEIGHT}px`
                        : "0px",
                      transitionDelay: `${800 + i * 50}ms`,
                    }}
                  />
                ))}
              </div>
              <div className="flex justify-between text-xs text-text-tertiary font-body mt-3">
                <span>Loss</span>
                <span>Gain</span>
              </div>
              <p className="text-center text-sm text-[#1B7A4A] font-body mt-4 font-medium">
                Tight distribution, shifted right
              </p>
            </div>
          </div>

          {/* Caption */}
          <p className="text-center text-sm text-text-tertiary font-body mt-6">
            Each bar represents outcomes from 1,000 simulated climate seasons
          </p>
        </div>

        {/* Closing statement */}
        <div
          className={`text-center mt-8 transition-all duration-700 delay-1000 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="font-display text-xl sm:text-2xl text-[#B8860B] italic">
            This isn&apos;t a guess. It&apos;s 1,000 stress tests.
          </p>
        </div>
      </div>
    </section>
  );
}
