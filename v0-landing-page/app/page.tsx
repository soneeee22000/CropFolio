import { HeroSection } from "@/components/landing/hero-section"
import { InsightSection } from "@/components/landing/insight-section"
import { CrossDomainSection } from "@/components/landing/cross-domain-section"
import { HowItWorksSection } from "@/components/landing/how-it-works-section"
import { MetricsSection } from "@/components/landing/metrics-section"
import { TechSection } from "@/components/landing/tech-section"
import { CTAFooter } from "@/components/landing/cta-footer"
import { Header } from "@/components/landing/header"

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <HeroSection />
      <InsightSection />
      <CrossDomainSection />
      <HowItWorksSection />
      <MetricsSection />
      <TechSection />
      <CTAFooter />
    </main>
  )
}
