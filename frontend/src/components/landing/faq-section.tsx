import { useState } from "react";
import { useInView } from "./use-in-view";

interface FaqItem {
  question: string;
  answer: string;
}

const faqs: FaqItem[] = [
  {
    question: "How does Myanmar's post-2021 situation affect the simulation?",
    answer:
      "This is our biggest limitation, honestly. Our yield correlations come from FAOSTAT 2010-2021 — essentially pre-coup data. Post-2021 Myanmar has a fundamentally different agricultural economy: 60% currency devaluation, banking collapse, supply chain disruption, fertilizer cost spikes, and active conflict in some regions. CropFolio models CLIMATE risk well (drought, flood, yield correlation), but it does NOT model political risk, economic disruption, input cost inflation, or supply chain breakdowns — which for farmers in 2026 may be bigger threats than weather. The yield hedging insight (rice-sesame = -0.49) remains physically valid regardless of politics, but the price and income projections should be treated as directional, not precise.",
  },
  {
    question: "Is the data actually real?",
    answer:
      "Yield correlations: Yes — 12 years of FAOSTAT data (2010-2021, element code 5419, country code 28). Price data: Based on WFP-published ranges but generated synthetically for the hackathon prototype. Climate data: NASA POWER + Open-Meteo with regional fallback. Crop profiles: Updated to FAOSTAT 2019-2021 means with cited sources. The covariance matrix — the core of the optimizer — uses real FAOSTAT yield correlations. This is our strongest data asset.",
  },
  {
    question: "Can individual farmers use this?",
    answer:
      "Not directly. CropFolio targets agricultural extension workers and cooperative managers — intermediaries who advise 500+ farmers each. They have the digital literacy, smartphones, and mandate to translate portfolio recommendations into planting advice. The tool speaks their language (literally — it supports Burmese), not the farmer's.",
  },
  {
    question: "What's the AI actually doing?",
    answer:
      "Gemini 2.5 Flash generates natural language analysis of the optimization results — translating numbers into actionable advice in English and Burmese. It does not perform the optimization itself. The portfolio math is pure scipy/numpy. The AI adds a layer of contextual interpretation: 'Given Magway's 30% drought probability, sesame's drought tolerance makes it the strongest hedge in your portfolio.' Without the API key, the app works fully — AI is additive, not essential.",
  },
  {
    question: "Why sesame? Why not just diversify with any crop?",
    answer:
      "Because the data says so. We computed yield correlations from 12 years of FAOSTAT data and found that rice-sesame has a -0.49 correlation — the only strong negative correlation among Myanmar's major crops. Rice-chickpea is +0.13 (slightly positive, NOT a hedge). Pulses correlate with each other at +0.5 to +0.9. Diversification only works when crops respond differently to the same climate stress. Sesame is the one crop that genuinely hedges rice.",
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
