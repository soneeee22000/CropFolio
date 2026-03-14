"use client"

import { useInView } from "@/hooks/use-in-view"
import { Button } from "@/components/ui/button"
import { ArrowRight, Sprout } from "lucide-react"

export function CTAFooter() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.3 })

  return (
    <footer 
      ref={ref}
      className="bg-[#1A1A18] text-[#FAFAF8] py-24 sm:py-32 px-6"
    >
      <div className="max-w-3xl mx-auto text-center">
        {/* Logo mark */}
        <div 
          className={`flex justify-center mb-8 transition-all duration-700 ${
            isInView ? 'opacity-100 scale-100' : 'opacity-0 scale-90'
          }`}
        >
          <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center">
            <Sprout className="w-8 h-8 text-primary" />
          </div>
        </div>

        {/* Heading */}
        <h2 
          className={`font-serif text-4xl sm:text-5xl lg:text-6xl mb-8 leading-tight transition-all duration-700 delay-100 ${
            isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          See it for yourself.
        </h2>

        {/* CTA Button */}
        <div 
          className={`mb-12 transition-all duration-700 delay-200 ${
            isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <Button 
            size="lg" 
            className="bg-primary hover:bg-primary/90 text-primary-foreground px-10 py-7 text-lg font-sans group"
          >
            Launch CropFolio
            <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
          </Button>
        </div>

        {/* Hackathon credit */}
        <div 
          className={`transition-all duration-700 delay-300 ${
            isInView ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <p className="text-sm text-[#A3A29D] font-sans mb-2">
            Built for the AI for Climate-Resilient Agriculture Hackathon 2026
          </p>
          <p className="text-sm text-[#A3A29D] font-sans">
            Impact Hub Yangon × UNDP Myanmar
          </p>
        </div>

        {/* Decorative line */}
        <div 
          className={`mt-16 pt-8 border-t border-[#333330] transition-all duration-700 delay-400 ${
            isInView ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[#A3A29D] font-sans">
            <div className="flex items-center gap-2">
              <Sprout className="w-4 h-4 text-primary" />
              <span className="font-serif text-base text-[#FAFAF8]">CropFolio</span>
            </div>
            <p>Modern Portfolio Theory for Agriculture</p>
            <p>© 2026 All rights reserved</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
