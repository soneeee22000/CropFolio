import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Sprout, Menu, X } from "./icons";

/**
 * Fixed header with transparent-to-solid scroll transition.
 * Includes mobile hamburger menu.
 */
export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-[#1A1A18]/95 backdrop-blur-md border-b border-[#333330]"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div
            className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${
              isScrolled ? "bg-primary/10" : "bg-[#FAFAF8]/10"
            }`}
          >
            <Sprout className="w-4 h-4 text-primary" />
          </div>
          <span className="font-display text-lg text-[#FAFAF8] group-hover:text-primary transition-colors">
            CropFolio
          </span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#about"
            className="text-sm text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-body"
          >
            About
          </a>
          <a
            href="#the-science"
            className="text-sm text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-body"
          >
            The Science
          </a>
          <a
            href="#how-it-works"
            className="text-sm text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-body"
          >
            How It Works
          </a>
          <Link
            to="/app"
            className="px-6 py-2 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors"
          >
            Try CropFolio
          </Link>
        </nav>

        {/* Mobile menu button */}
        <button
          className="md:hidden p-2 text-[#FAFAF8]"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {isMobileMenuOpen ? (
            <X className="w-5 h-5" />
          ) : (
            <Menu className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-[#1A1A18] border-t border-[#333330]">
          <nav className="flex flex-col p-6 gap-4">
            <a
              href="#about"
              className="text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              About
            </a>
            <a
              href="#the-science"
              className="text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              The Science
            </a>
            <a
              href="#how-it-works"
              className="text-[#FAFAF8]/70 hover:text-[#FAFAF8] transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              How It Works
            </a>
            <Link
              to="/app"
              className="px-6 py-3 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors text-center w-full mt-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Try CropFolio
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
