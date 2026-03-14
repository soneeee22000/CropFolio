"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Sprout, Menu, X } from "lucide-react"

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }

    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled 
          ? 'bg-[#1A1A18]/95 backdrop-blur-md border-b border-[#333330]' 
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center gap-2 group">
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${
            isScrolled ? 'bg-primary/10' : 'bg-[#FAFAF8]/10'
          }`}>
            <Sprout className="w-4 h-4 text-primary" />
          </div>
          <span className="font-serif text-lg text-[#FAFAF8] group-hover:text-primary transition-colors">
            CropFolio
          </span>
        </a>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <a 
            href="#insight" 
            className="text-sm text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-sans"
          >
            How It Works
          </a>
          <a 
            href="#" 
            className="text-sm text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-sans"
          >
            About
          </a>
          <Button 
            size="sm" 
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-sans"
          >
            Try CropFolio
          </Button>
        </nav>

        {/* Mobile menu button */}
        <button 
          className="md:hidden p-2 text-[#FAFAF8]"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-[#1A1A18] border-t border-[#333330]">
          <nav className="flex flex-col p-6 gap-4">
            <a 
              href="#insight" 
              className="text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-sans py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              How It Works
            </a>
            <a 
              href="#" 
              className="text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-sans py-2"
            >
              About
            </a>
            <Button 
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-sans w-full mt-2"
            >
              Try CropFolio
            </Button>
          </nav>
        </div>
      )}
    </header>
  )
}
