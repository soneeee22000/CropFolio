"use client"

import { useInView } from "@/hooks/use-in-view"
import { VolatilityVisualization } from "./volatility-visualization"

export function InsightSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.3 })

  return (
    <section 
      id="insight"
      ref={ref}
      className="bg-background py-24 sm:py-32 px-6"
    >
      <div className="max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left: Text content */}
          <div 
            className={`transition-all duration-700 ${
              isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
            }`}
          >
            <p className="text-[11px] uppercase tracking-[0.25em] text-muted-foreground mb-4 font-sans">
              The Problem
            </p>
            
            <h2 className="font-serif text-4xl sm:text-5xl lg:text-6xl text-foreground mb-8 leading-tight text-balance">
              One Crop. One Risk.
            </h2>
            
            <div className="space-y-6 text-foreground/80 font-sans text-lg leading-relaxed">
              <p>
                <span className="text-foreground font-medium">70% of Myanmar&apos;s farmers</span> grow rice as their only crop.
                When the monsoon fails, they lose everything. When it floods, they lose everything.
              </p>
              
              <p>
                There is no hedge. No safety net. No diversification.
              </p>
              
              <p className="text-accent font-medium">
                But rice isn&apos;t the only option.
              </p>
            </div>
          </div>

          {/* Right: Animated visualization */}
          <div 
            className={`transition-all duration-700 delay-200 ${
              isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
            }`}
          >
            <div className="bg-card border border-border rounded-2xl p-8 shadow-sm">
              <p className="text-sm text-muted-foreground mb-6 font-sans text-center">
                Income volatility comparison
              </p>
              <VolatilityVisualization isInView={isInView} />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
