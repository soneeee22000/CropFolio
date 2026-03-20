import { Header } from "./header";
import { HeroSection } from "./hero-section";
import { InsightSection } from "./insight-section";
import { HowItWorksSection } from "./how-it-works-section";
import { MetricsSection } from "./metrics-section";
import { MoatSection } from "./moat-section";
import { FaqSection } from "./faq-section";
import { CTAFooter } from "./cta-footer";

/**
 * CropFolio landing page — 7-section editorial flow.
 * Header → Hero → Insight → How It Works → Impact → FAQ → CTA
 */
export function LandingPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <HeroSection />
      <InsightSection />
      <HowItWorksSection />
      <MetricsSection />
      <MoatSection />
      <FaqSection />
      <CTAFooter />
    </main>
  );
}
