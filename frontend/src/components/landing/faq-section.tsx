import { useState } from "react";
import { useInView } from "./use-in-view";

interface FaqItem {
  question: string;
  answer: string;
}

const faqs: FaqItem[] = [
  {
    question: "How does Myanmar's post-2021 inflation affect the simulation?",
    answer:
      "It's the biggest data challenge we face honestly. The MMK has lost ~60% of its value since 2021, meaning our WFP price data (2022-2025) reflects a fundamentally different economic regime than pre-coup prices. Our price correlations capture this inflationary period — all crop prices move together (+0.67 to +0.97 correlation) largely because of currency-driven inflation, not agricultural fundamentals. The yield data (FAOSTAT 2010-2021) is more stable because yields are measured in kg/ha, not currency. The optimizer's diversification benefit comes primarily from yield hedging (-0.49 rice-sesame), which is inflation-independent.",
  },
  {
    question: "Is the data actually real?",
    answer:
      "Yield correlations: Yes — 12 years of FAOSTAT data (2010-2021, element code 5419, country code 28). Price data: Based on WFP-published ranges but generated synthetically for the hackathon prototype. Climate data: NASA POWER + Open-Meteo with regional fallback. Crop profiles: Updated to FAOSTAT 2019-2021 means with cited sources. The covariance matrix — the core of the optimizer — uses real FAOSTAT yield correlations. This is our strongest data asset.",
  },
  {
    question: "Why does the simulation run so fast?",
    answer:
      "Because it's not machine learning. Monte Carlo simulation samples 1,000 scenarios from a multivariate normal distribution — a single matrix operation that takes ~50ms. The Markowitz optimizer solves a convex optimization with 6 variables. The value is in the statistical insight (stress-testing portfolios across 1,000 climate seasons), not in compute time. A simulation that takes 3 hours but produces the same distribution is not more valuable — it's just slower.",
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
  {
    question: "How accurate are the Burmese translations?",
    answer:
      "They're AI-generated and have not been reviewed by a native speaker. They may contain grammatical errors, overly formal register, or awkward phrasing. Native speaker review is a priority before any real deployment. The crop names (စပါး, မတ်ပဲ, နှမ်း, etc.) are standard and correct.",
  },
  {
    question:
      "What about crops not in the system? Myanmar grows hundreds of varieties.",
    answer:
      "The current prototype covers 6 major crops: rice, black gram, green gram, chickpea, sesame, and groundnut. These represent the bulk of Myanmar's agricultural output and the crops with available FAOSTAT yield data. Adding more crops requires historical yield time series to compute correlations — without data, the optimizer can't make meaningful recommendations.",
  },
];

/** FAQ section with expandable accordion. */
export function FaqSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.1 });

  return (
    <section ref={ref} className="bg-surface py-12 sm:py-16 px-6">
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
