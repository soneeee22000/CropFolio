import { useState } from "react";
import { useInView } from "./use-in-view";

interface FaqItem {
  question: string;
  answer: string;
}

const faqs: FaqItem[] = [
  {
    question: "Who is CropFolio built for?",
    answer:
      "Agricultural distributors and fertilizer companies — not individual farmers. In Myanmar, distributors like Awba control the entire value chain: they recommend crops, supply fertilizers, and even grow demo plots at their own expense to convince farmers. When a distributor recommends a crop, entire regions follow. CropFolio gives these decision-makers data-driven confidence in their crop-fertilizer recommendations, reducing their risk when advising hundreds of farmers at once.",
  },
  {
    question: "Is the data actually real?",
    answer:
      "Yield correlations: Yes — 12 years of FAOSTAT data (2010-2021, element code 5419, country code 28). Price data: Based on WFP-published ranges but generated synthetically for the hackathon prototype. Climate data: NASA POWER + Open-Meteo with regional fallback. Soil coverage: 50 townships across 14 regions with real soil property data. The covariance matrix — the core of the optimizer — uses real FAOSTAT yield correlations. This is our strongest data asset.",
  },
  {
    question: "How does Myanmar's post-2021 situation affect the simulation?",
    answer:
      "This is our biggest limitation, honestly. Our yield correlations come from FAOSTAT 2010-2021 — essentially pre-coup data. Post-2021 Myanmar has a fundamentally different agricultural economy: 60% currency devaluation, fertilizer cost spikes, and supply chain disruption. CropFolio models CLIMATE risk well (drought, flood, yield correlation), but it does NOT model political risk or economic disruption. The yield hedging insight (rice-sesame = -0.49) remains physically valid regardless of politics, but the price and income projections should be treated as directional, not precise. For distributors, the relative crop-risk ranking matters more than absolute numbers.",
  },
  {
    question: "What's the AI actually doing?",
    answer:
      "Gemini 2.5 Flash generates natural language analysis of optimization results — translating numbers into actionable crop-fertilizer advice in English and Burmese. It does not perform the optimization itself. The portfolio math is pure scipy/numpy. The AI adds contextual interpretation: 'Given Magway's 30% drought probability and sandy loam soil, sesame with balanced NPK is your strongest recommendation.' Without the API key, the app works fully — AI is additive, not essential.",
  },
  {
    question: "Why sesame? Why not just diversify with any crop?",
    answer:
      "Because the data says so. We computed yield correlations from 12 years of FAOSTAT data and found that rice-sesame has a -0.49 correlation — the only strong negative correlation among Myanmar's 11 major crops. Rice-chickpea is +0.13 (slightly positive, NOT a hedge). Diversification only works when crops respond differently to the same climate stress. For distributors, this means recommending sesame alongside rice actually reduces the risk of their farmers failing — and that means fewer reimbursements.",
  },
];

/** FAQ section with expandable accordion — 5 honest answers. */
export function FaqSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.1 });

  return (
    <section id="faq" ref={ref} className="bg-surface py-12 sm:py-16 px-6">
      <div className="max-w-3xl mx-auto">
        <div
          className={`text-center mb-8 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-4 font-body">
            Frequently Asked
          </p>
          <h2 className="font-display text-3xl sm:text-4xl text-text-primary">
            Honest Answers
          </h2>
        </div>

        <div className="space-y-2">
          {faqs.map((faq, i) => (
            <FaqAccordion key={i} faq={faq} index={i} isInView={isInView} />
          ))}
        </div>
      </div>
    </section>
  );
}

/** Single FAQ accordion item. */
function FaqAccordion({
  faq,
  index,
  isInView,
}: {
  faq: FaqItem;
  index: number;
  isInView: boolean;
}) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className={`border border-border rounded-xl overflow-hidden transition-all duration-700 ${
        isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      }`}
      style={{ transitionDelay: `${index * 60}ms` }}
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full text-left px-6 py-4 flex items-center justify-between gap-4 hover:bg-surface-subtle transition-colors"
      >
        <span className="font-body text-sm text-text-primary font-medium">
          {faq.question}
        </span>
        <span
          className={`text-text-tertiary transition-transform duration-200 shrink-0 ${
            isOpen ? "rotate-45" : ""
          }`}
        >
          +
        </span>
      </button>
      {isOpen && (
        <div className="px-6 pb-4">
          <p className="text-sm text-text-secondary leading-relaxed font-body">
            {faq.answer}
          </p>
        </div>
      )}
    </div>
  );
}
