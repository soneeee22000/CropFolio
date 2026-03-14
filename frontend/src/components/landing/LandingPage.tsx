import { Header } from "./header";
import { HeroSection } from "./hero-section";
import { InsightSection } from "./insight-section";
import { CrossDomainSection } from "./cross-domain-section";
import { MonteCarloSection } from "./monte-carlo-section";
import { ResearchSection } from "./research-section";
import { HowItWorksSection } from "./how-it-works-section";
import { MetricsSection } from "./metrics-section";
import { TechSection } from "./tech-section";
import { FaqSection } from "./faq-section";
import { CTAFooter } from "./cta-footer";

/**
 * CropFolio landing page composing all editorial sections
 * in presentation order.
 */
export function LandingPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <HeroSection />
      <InsightSection />
      <CrossDomainSection />
      <MonteCarloSection />
      <ResearchSection />
      <HowItWorksSection />
      <MetricsSection />
      <TechSection />
      <FaqSection />
      <CTAFooter />
    </main>
  );
}
