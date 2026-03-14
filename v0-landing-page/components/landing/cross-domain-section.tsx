"use client"

import { useInView } from "@/hooks/use-in-view"
import { TrendingUp, Sprout, Award } from "lucide-react"

export function CrossDomainSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.2 })

  return (
    <section 
      ref={ref}
      className="bg-[#1A1A18] text-[#FAFAF8] py-24 sm:py-32 px-6 overflow-hidden"
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div 
          className={`text-center mb-16 transition-all duration-700 ${
            isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <p className="text-[11px] uppercase tracking-[0.25em] text-[#A3A29D] mb-4 font-sans">
            The Insight
          </p>
          <h2 className="font-serif text-4xl sm:text-5xl lg:text-6xl leading-tight text-balance">
            Portfolio Theory for Farms
          </h2>
        </div>

        {/* Cards */}
        <div className="grid md:grid-cols-2 gap-8 relative">
          {/* Connecting line */}
          <div className="hidden md:block absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-px">
            <svg className="w-full h-8 overflow-visible">
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#B8860B" stopOpacity="0.5" />
                  <stop offset="50%" stopColor="#B8860B" stopOpacity="1" />
                  <stop offset="100%" stopColor="#1B7A4A" stopOpacity="0.5" />
                </linearGradient>
              </defs>
              <line 
                x1="0" y1="4" x2="80" y2="4" 
                stroke="url(#lineGradient)" 
                strokeWidth="2"
                strokeDasharray="4 4"
                className={`transition-all duration-1000 delay-500 ${
                  isInView ? 'opacity-100' : 'opacity-0'
                }`}
              />
              <circle 
                cx="40" cy="4" r="6" 
                fill="#B8860B"
                className={`transition-all duration-700 delay-700 ${
                  isInView ? 'opacity-100 scale-100' : 'opacity-0 scale-0'
                }`}
                style={{ transformOrigin: '40px 4px' }}
              />
            </svg>
          </div>

          {/* Finance Card */}
          <div 
            className={`bg-[#242422] border border-[#333330] rounded-2xl p-8 transition-all duration-700 delay-100 ${
              isInView ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'
            }`}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-accent" />
              </div>
              <h3 className="font-serif text-2xl">In Finance</h3>
            </div>
            
            <ul className="space-y-4 font-sans text-[#FAFAF8]/80">
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                <span>Stocks have different risk profiles</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                <span>Negatively correlated assets reduce portfolio risk</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                <span className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-accent shrink-0" />
                  Markowitz won a Nobel Prize for proving this in 1952
                </span>
              </li>
            </ul>
          </div>

          {/* Agriculture Card */}
          <div 
            className={`bg-[#242422] border border-[#333330] rounded-2xl p-8 transition-all duration-700 delay-300 ${
              isInView ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8'
            }`}
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <Sprout className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-serif text-2xl">In Agriculture</h3>
            </div>
            
            <ul className="space-y-4 font-sans text-[#FAFAF8]/80">
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0" />
                <span>Crops have different climate tolerances</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0" />
                <span>Rice survives floods; sesame survives drought</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0" />
                <span className="text-primary font-medium">
                  CropFolio applies the same math to crop selection
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bridge statement */}
        <div 
          className={`text-center mt-16 transition-all duration-700 delay-500 ${
            isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <p className="font-serif text-xl sm:text-2xl text-accent/90 italic">
            &ldquo;What if we gave farmers the same tools as hedge funds?&rdquo;
          </p>
        </div>
      </div>
    </section>
  )
}
