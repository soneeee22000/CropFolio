import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useScrollReveal } from "./useScrollReveal";
import { AnimatedCounter } from "./AnimatedCounter";

/** CropFolio landing page — editorial data story. */
export function LandingPage() {
  return (
    <div className="min-h-screen">
      <NavBar />
      <HeroSection />
      <ProblemSection />
      <InsightSection />
      <HowItWorksSection />
      <MetricsSection />
      <TechSection />
      <CTAFooter />
    </div>
  );
}

/** Sticky transparent → solid nav bar. */
function NavBar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-surface-elevated/90 backdrop-blur-md border-b border-border"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <span
          className={`font-display text-xl transition-colors ${
            scrolled ? "text-text-primary" : "text-white"
          }`}
        >
          CropFolio
        </span>
        <div className="flex items-center gap-6">
          {["How It Works", "Try App", "Admin"].map((label) => (
            <Link
              key={label}
              to={
                label === "Try App"
                  ? "/app"
                  : label === "Admin"
                    ? "/admin"
                    : "#how-it-works"
              }
              className={`text-sm transition-colors ${
                scrolled
                  ? "text-text-secondary hover:text-text-primary"
                  : "text-white/70 hover:text-white"
              }`}
            >
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

/** Hero: "40% → 10%" animated counter. */
function HeroSection() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 1800);
    const t2 = setTimeout(() => setPhase(2), 2800);
    const t3 = setTimeout(() => setPhase(3), 3400);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, []);

  return (
    <section className="min-h-screen flex flex-col items-center justify-center bg-[#1A1A18] text-white px-6 relative overflow-hidden">
      <div className="absolute inset-0 opacity-5">
        <div
          className="w-full h-full"
          style={{
            backgroundImage:
              "radial-gradient(circle at 50% 50%, #1B7A4A 1px, transparent 1px)",
            backgroundSize: "40px 40px",
          }}
        />
      </div>

      <div className="relative text-center">
        <p className="text-[11px] uppercase tracking-[0.3em] text-[#A3A29D] mb-8">
          Modern Portfolio Theory for Agriculture
        </p>

        <div className="flex items-baseline justify-center gap-4 mb-6">
          <span
            className={`font-display text-[120px] md:text-[160px] leading-none transition-all duration-500 ${
              phase >= 1 ? "line-through opacity-40" : ""
            }`}
          >
            <AnimatedCounter target={40} suffix="%" duration={1500} />
          </span>
          {phase >= 2 && (
            <span
              className="font-display text-[120px] md:text-[160px] leading-none animate-fade-in-up"
              style={{ color: "#B8860B" }}
            >
              10%
            </span>
          )}
        </div>

        <p className="text-lg md:text-xl text-[#A3A29D] max-w-xl mx-auto mb-4">
          of Myanmar's rice farmers face catastrophic income loss in any given
          season.
        </p>

        {phase >= 3 && (
          <p className="text-lg text-white/90 animate-fade-in-up mb-12">
            CropFolio reduces that to{" "}
            <span
              className="font-data font-medium"
              style={{ color: "#B8860B" }}
            >
              10%
            </span>
            .
          </p>
        )}

        <div className="flex flex-col items-center gap-4 mt-8">
          <Link
            to="/app"
            className="px-8 py-4 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors"
          >
            Try CropFolio
          </Link>
          <a
            href="#problem"
            className="text-sm text-[#A3A29D] hover:text-white transition-colors"
          >
            See how it works &darr;
          </a>
        </div>
      </div>
    </section>
  );
}

/** Problem section: one crop = one risk. */
function ProblemSection() {
  const { ref, isVisible } = useScrollReveal();

  return (
    <section id="problem" className="bg-surface py-24 px-6" ref={ref}>
      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
        <div
          className={`transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-4">
            The Problem
          </p>
          <h2 className="font-display text-4xl text-text-primary mb-6">
            One Crop. One Risk.
          </h2>
          <p className="text-text-secondary leading-relaxed mb-4">
            70% of Myanmar's farmers grow rice as their only crop. When the
            monsoon fails — Loss. When it floods — Loss. No hedge. No safety
            net. No diversification.
          </p>
          <p className="text-text-primary font-medium">
            But what if crops could be managed like a financial portfolio?
          </p>
        </div>

        <div
          className={`transition-all duration-700 delay-200 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <VolatilityViz started={isVisible} />
        </div>
      </div>
    </section>
  );
}

/** Animated SVG showing income volatility: monocrop vs diversified. */
function VolatilityViz({ started }: { started: boolean }) {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    if (!started) return;
    const id = setInterval(() => setTick((t) => t + 1), 50);
    return () => clearInterval(id);
  }, [started]);

  const t = tick * 0.08;
  const monoH = 120 + Math.sin(t) * 60 + Math.sin(t * 2.3) * 30;
  const riceH = 60 + Math.sin(t) * 15 + Math.sin(t * 2.3) * 8;
  const pulseH = 40 + Math.sin(t * 1.5 + 1) * 8;
  const oilH = 30 + Math.sin(t * 0.7 + 2) * 6;

  return (
    <div className="bg-surface-subtle rounded-xl p-8">
      <div className="flex items-end justify-center gap-12 h-48">
        <div className="text-center">
          <div
            className="w-16 rounded-t-md transition-all duration-100"
            style={{
              height: `${monoH}px`,
              backgroundColor: "#C43B3B",
              opacity: 0.8,
            }}
          />
          <p className="text-[11px] text-text-tertiary mt-2 uppercase tracking-wide">
            Rice Only
          </p>
        </div>

        <div className="text-center">
          <div className="flex items-end gap-1 justify-center">
            <div
              className="w-5 rounded-t-sm transition-all duration-100"
              style={{ height: `${riceH}px`, backgroundColor: "#3A8F5C" }}
            />
            <div
              className="w-5 rounded-t-sm transition-all duration-100"
              style={{ height: `${pulseH}px`, backgroundColor: "#C4923A" }}
            />
            <div
              className="w-5 rounded-t-sm transition-all duration-100"
              style={{ height: `${oilH}px`, backgroundColor: "#B85A5A" }}
            />
          </div>
          <p className="text-[11px] text-text-tertiary mt-2 uppercase tracking-wide">
            Diversified
          </p>
        </div>
      </div>
      <p className="text-center text-xs text-text-tertiary mt-4">
        Income volatility comparison (simulated)
      </p>
    </div>
  );
}

/** Cross-domain insight: finance → agriculture. */
function InsightSection() {
  const { ref, isVisible } = useScrollReveal();

  return (
    <section className="bg-[#1A1A18] py-24 px-6" ref={ref}>
      <div className="max-w-5xl mx-auto text-center mb-16">
        <p className="text-[11px] uppercase tracking-[0.2em] text-[#A3A29D] mb-4">
          The Insight
        </p>
        <h2 className="font-display text-4xl text-white">
          Portfolio Theory for Farms
        </h2>
      </div>

      <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-8">
        {[
          {
            title: "In Finance",
            body: "Diversify stocks to reduce portfolio risk. Negatively correlated assets cancel out volatility. Nobel Prize, 1952.",
          },
          {
            title: "In Agriculture",
            body: "Diversify crops to reduce climate risk. Rice survives floods. Sesame survives drought. Same math. Different asset class.",
          },
        ].map((card, i) => (
          <div
            key={card.title}
            className={`border border-white/20 rounded-xl p-8 transition-all duration-700 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-8"
            }`}
            style={{ transitionDelay: `${i * 150}ms` }}
          >
            <h3 className="font-display text-xl text-white mb-4">
              {card.title}
            </h3>
            <p className="text-[#A3A29D] leading-relaxed">{card.body}</p>
          </div>
        ))}
      </div>

      <div className="flex justify-center mt-8">
        <div className="w-px h-12 bg-white/10" />
      </div>
      <p className="text-center text-[#A3A29D] text-sm">
        Same optimization. Different domain.
      </p>
    </section>
  );
}

/** How it works: 4 steps. */
function HowItWorksSection() {
  const { ref, isVisible } = useScrollReveal();

  const steps = [
    {
      n: "01",
      title: "Select Township",
      desc: "Choose from 25 Myanmar agricultural townships",
    },
    {
      n: "02",
      title: "Assess Climate Risk",
      desc: "NASA satellite data for drought and flood probability",
    },
    {
      n: "03",
      title: "Optimize Portfolio",
      desc: "Markowitz optimization finds the ideal crop mix",
    },
    {
      n: "04",
      title: "Simulate Seasons",
      desc: "Monte Carlo proves the diversification benefit",
    },
  ];

  return (
    <section id="how-it-works" className="bg-surface py-24 px-6" ref={ref}>
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-4">
            How It Works
          </p>
          <h2 className="font-display text-4xl text-text-primary">
            Four Steps to Climate Resilience
          </h2>
        </div>

        <div className="grid md:grid-cols-4 gap-8">
          {steps.map((step, i) => (
            <div
              key={step.n}
              className={`transition-all duration-700 ${
                isVisible
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{ transitionDelay: `${i * 100}ms` }}
            >
              <span className="font-display text-5xl text-border">
                {step.n}
              </span>
              <h3 className="font-medium text-text-primary mt-3 mb-2">
                {step.title}
              </h3>
              <p className="text-sm text-text-secondary">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/** Key metrics with animated counters. */
function MetricsSection() {
  const { ref, isVisible } = useScrollReveal();

  return (
    <section className="bg-surface py-24 px-6" ref={ref}>
      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-3 gap-6">
          {[
            {
              target: 51.3,
              suffix: "%",
              label: "Risk Reduction",
              sub: "vs Monocrop",
              decimals: 1,
            },
            {
              target: 1.5,
              suffix: "M",
              label: "Expected Income",
              sub: "MMK per Hectare",
              decimals: 1,
              gold: true,
            },
            {
              target: 10,
              suffix: "%",
              label: "Catastrophic Loss",
              sub: "Probability",
              decimals: 0,
            },
          ].map((m, i) => (
            <div
              key={m.label}
              className={`text-center p-8 rounded-xl transition-all duration-700 ${
                m.gold ? "border border-[#B8860B]/20" : ""
              } ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
              style={{ transitionDelay: `${i * 100}ms` }}
            >
              <div
                className={`font-data text-4xl md:text-5xl font-medium ${
                  m.gold ? "text-[#B8860B]" : "text-text-primary"
                }`}
              >
                <AnimatedCounter
                  target={m.target}
                  suffix={m.suffix}
                  decimals={m.decimals}
                  started={isVisible}
                  duration={1000}
                />
              </div>
              <p className="text-[11px] uppercase tracking-[0.1em] text-text-tertiary mt-3">
                {m.label}
              </p>
              <p className="text-xs text-text-tertiary mt-1">{m.sub}</p>
            </div>
          ))}
        </div>
        <p className="text-center text-xs text-text-tertiary mt-8">
          Based on Magway township, monsoon season, rice + black gram + sesame
        </p>
      </div>
    </section>
  );
}

/** Tech credibility badges. */
function TechSection() {
  return (
    <section className="bg-surface py-16 px-6 border-t border-border">
      <div className="max-w-4xl mx-auto text-center">
        <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-6">
          Built With
        </p>
        <p className="text-text-secondary mb-4">
          Python &middot; FastAPI &middot; React &middot; TypeScript &middot;
          D3.js &middot; scipy
        </p>
        <p className="font-data text-sm text-text-tertiary">
          63 Tests &middot; 88% Coverage &middot; 8 Endpoints &middot; Zero AI
          Costs
        </p>
      </div>
    </section>
  );
}

/** Final CTA. */
function CTAFooter() {
  return (
    <section className="bg-[#1A1A18] py-24 px-6">
      <div className="max-w-2xl mx-auto text-center">
        <h2 className="font-display text-4xl text-white mb-8">
          See it for yourself.
        </h2>
        <Link
          to="/app"
          className="inline-block px-10 py-4 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors"
        >
          Launch CropFolio
        </Link>
        <p className="text-[#A3A29D] text-xs mt-8">
          AI for Climate-Resilient Agriculture Hackathon 2026
          <br />
          Impact Hub Yangon &times; UNDP Myanmar
        </p>
      </div>
    </section>
  );
}
