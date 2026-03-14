"use client"

import { useState, useEffect } from "react"
import { AnimatedCounter } from "./animated-counter"
import { Button } from "@/components/ui/button"
import { ArrowRight, ChevronDown } from "lucide-react"

export function HeroSection() {
  const [showCounter, setShowCounter] = useState(false)
  const [showStrikethrough, setShowStrikethrough] = useState(false)
  const [showNewStat, setShowNewStat] = useState(false)

  useEffect(() => {
    // Start counter animation after component mounts
    const timer = setTimeout(() => setShowCounter(true), 300)
    return () => clearTimeout(timer)
  }, [])

  const handleCounterComplete = () => {
    setTimeout(() => setShowStrikethrough(true), 800)
    setTimeout(() => setShowNewStat(true), 1300)
  }

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center bg-[#1A1A18] text-[#FAFAF8] px-6 py-20 overflow-hidden">
      {/* Subtle background pattern */}
      <div className="absolute inset-0 opacity-[0.03]">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, #FAFAF8 1px, transparent 1px)`,
          backgroundSize: '48px 48px'
        }} />
      </div>
      
      {/* Ambient glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-primary/10 rounded-full blur-[120px] pointer-events-none" />
      
      <div className="relative z-10 max-w-4xl mx-auto text-center">
        {/* Overline */}
        <p 
          className={`text-[11px] uppercase tracking-[0.25em] text-muted-foreground mb-8 font-sans transition-all duration-700 ${
            showCounter ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          Modern Portfolio Theory for Agriculture
        </p>

        {/* Hero Stat */}
        <div className="mb-6">
          <div className="relative inline-block">
            <span 
              className={`font-serif text-[120px] sm:text-[160px] lg:text-[200px] leading-none font-normal tracking-tight transition-colors duration-500 ${
                showStrikethrough ? 'text-muted-foreground/40' : 'text-[#FAFAF8]'
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
            
            {/* Strikethrough line */}
            {showStrikethrough && (
              <div 
                className="absolute left-0 top-1/2 h-1 sm:h-1.5 bg-[#FAFAF8]/50 origin-left"
                style={{ 
                  width: '100%',
                  animation: 'strike-through 0.4s ease-out forwards'
                }}
              />
            )}
          </div>

          {/* New stat reveal */}
          {showNewStat && (
            <span 
              className="font-serif text-[60px] sm:text-[80px] lg:text-[100px] leading-none text-accent ml-4 sm:ml-8 animate-fade-in-up inline-block"
              style={{ animationDuration: '0.6s' }}
            >
              10%
            </span>
          )}
        </div>

        {/* Subtext */}
        <p 
          className={`text-lg sm:text-xl text-[#FAFAF8]/80 max-w-xl mx-auto mb-4 font-sans leading-relaxed transition-all duration-700 delay-200 ${
            showCounter ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          of Myanmar&apos;s rice farmers face catastrophic income loss
          in any given season.
        </p>

        {showNewStat && (
          <p 
            className="text-lg sm:text-xl text-accent/90 max-w-xl mx-auto mb-12 font-sans animate-fade-in-up"
            style={{ animationDuration: '0.6s', animationDelay: '0.2s', animationFillMode: 'both' }}
          >
            CropFolio reduces that to 10%.
          </p>
        )}

        {/* CTA Buttons */}
        <div 
          className={`flex flex-col sm:flex-row items-center justify-center gap-4 transition-all duration-700 delay-300 ${
            showCounter ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          <Button 
            size="lg" 
            className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-6 text-lg font-sans group"
          >
            Try CropFolio
            <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
          </Button>
          
          <a 
            href="#insight"
            className="text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors flex items-center gap-2 text-sm font-sans"
          >
            See how it works
            <ChevronDown className="h-4 w-4" />
          </a>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2">
        <div className="w-6 h-10 rounded-full border-2 border-[#FAFAF8]/30 flex items-start justify-center p-2">
          <div className="w-1 h-2 bg-[#FAFAF8]/50 rounded-full animate-bounce" />
        </div>
      </div>
    </section>
  )
}
