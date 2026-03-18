import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { AnimatedCounter } from "./animated-counter";
import { ArrowRight, ChevronDown } from "./icons";

/**
 * Hero section — warm, welcoming, editorial.
 * Dark background with subtle grain texture and warm light wash.
 * The 40% -> 10% counter is the centerpiece.
 */
export function HeroSection() {
  const [showCounter, setShowCounter] = useState(false);
  const [showStrikethrough, setShowStrikethrough] = useState(false);
  const [showNewStat, setShowNewStat] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowCounter(true), 300);
    return () => clearTimeout(timer);
  }, []);

  const handleCounterComplete = () => {
    setTimeout(() => setShowStrikethrough(true), 800);
    setTimeout(() => setShowNewStat(true), 1300);
  };

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-6 py-20 overflow-hidden bg-surface">
      {/* Warm ambient light — soft, diffused, no harsh edges */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `
            radial-gradient(ellipse 80% 50% at 50% 0%, rgba(27, 122, 74, 0.06) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 70% 80%, rgba(184, 134, 11, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse 50% 50% at 20% 60%, rgba(27, 122, 74, 0.03) 0%, transparent 50%)
          `,
        }}
      />

      {/* Subtle grain texture */}
      <div
        className="absolute inset-0 opacity-[0.015] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='1'/%3E%3C/svg%3E")`,
          backgroundRepeat: "repeat",
          backgroundSize: "256px 256px",
        }}
      />

      {/* Thin horizontal lines for depth */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03]">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="absolute left-0 right-0 h-px bg-text-primary"
            style={{ top: `${15 + i * 14}%` }}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-4xl mx-auto text-center">
        {/* Overline with warm fade-in */}
        <p
          className={`text-[11px] uppercase tracking-[0.3em] text-text-tertiary mb-10 font-body transition-all duration-1000 ${
            showCounter
              ? "opacity-100 translate-y-0"
              : "opacity-0 translate-y-4"
          }`}
        >
          Modern Portfolio Theory for Agriculture
        </p>

        {/* The Number — the entire pitch */}
        <div className="mb-8">
          <div className="relative inline-flex items-baseline gap-2 sm:gap-6">
            <span
              className={`font-display text-[100px] sm:text-[140px] lg:text-[180px] leading-none tracking-tight transition-all duration-700 ${
                showStrikethrough
                  ? "text-text-tertiary/30"
                  : "text-text-primary"
              }`}
            >
              <AnimatedCounter
                end={40}
                duration={1500}
                suffix="%"
                shouldStart={showCounter}
                onComplete={handleCounterComplete}
              />
            </span>

            {/* Strikethrough */}
            {showStrikethrough && (
              <div
                className="absolute left-0 top-1/2 -translate-y-1/2 h-[2px] sm:h-[3px] bg-text-primary/40 origin-left"
                style={{
                  width: showNewStat ? "45%" : "100%",
                  animation: "strike-through 0.4s ease-out forwards",
                }}
              />
            )}

            {/* The answer */}
            {showNewStat && (
              <span
                className="font-display text-[60px] sm:text-[80px] lg:text-[100px] leading-none animate-fade-in-up"
                style={{
                  color: "#B8860B",
                  animationDuration: "0.6s",
                }}
              >
                10%
              </span>
            )}
          </div>
        </div>

        {/* Story text */}
        <p
          className={`text-lg sm:text-xl text-text-secondary max-w-lg mx-auto mb-3 font-body leading-relaxed transition-all duration-1000 delay-200 ${
            showCounter
              ? "opacity-100 translate-y-0"
              : "opacity-0 translate-y-4"
          }`}
        >
          of Myanmar&apos;s rice farmers face catastrophic income loss in any
          given season.
        </p>

        {showNewStat && (
          <p
            className="text-lg sm:text-xl font-body mb-14 animate-fade-in-up"
            style={{
              color: "rgba(184, 134, 11, 0.85)",
              animationDuration: "0.6s",
              animationDelay: "0.2s",
              animationFillMode: "both",
            }}
          >
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

        {/* CTA — warm, inviting */}
        <div
          className={`flex flex-col sm:flex-row items-center justify-center gap-5 transition-all duration-1000 delay-500 ${
            showCounter
              ? "opacity-100 translate-y-0"
              : "opacity-0 translate-y-6"
          }`}
        >
          <Link
            to="/dashboard"
            className="group px-8 py-4 bg-primary text-white rounded-xl text-base font-body font-medium inline-flex items-center gap-2 hover:bg-primary-dark transition-all duration-300 hover:shadow-lg hover:shadow-primary/20"
          >
            Try CropFolio
            <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
          </Link>

          <a
            href="#problem"
            className="text-text-tertiary hover:text-text-secondary transition-colors duration-300 flex items-center gap-2 text-sm font-body"
          >
            See how it works
            <ChevronDown className="h-4 w-4" />
          </a>
        </div>
      </div>

      {/* Scroll indicator — minimal, barely there */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 opacity-30">
        <div className="w-5 h-8 rounded-full border border-text-primary/30 flex items-start justify-center pt-1.5">
          <div className="w-0.5 h-1.5 bg-text-primary/50 rounded-full animate-bounce" />
        </div>
      </div>

      {/* Bottom edge fade — smooth transition to next section */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-surface to-transparent pointer-events-none" />
    </section>
  );
}
