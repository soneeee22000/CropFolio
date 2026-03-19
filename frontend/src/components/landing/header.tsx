import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTheme } from "@/hooks/useTheme";
import { Menu, X } from "./icons";

/**
 * Fixed header with transparent-to-solid scroll transition.
 * Includes mobile hamburger menu and theme toggle.
 */
export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();

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
          ? "bg-surface/95 backdrop-blur-md border-b border-border"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <svg
            width="24"
            height="24"
            viewBox="0 0 32 32"
            fill="none"
            className="transition-transform duration-300 group-hover:scale-110"
          >
            <rect
              width="32"
              height="32"
              rx="8"
              fill={isScrolled ? "#1B7A4A" : "currentColor"}
              fillOpacity={isScrolled ? 0.15 : 0.1}
            />
            <rect x="6" y="20" width="5" height="6" rx="1" fill="#3A8F5C" />
            <rect x="13.5" y="14" width="5" height="12" rx="1" fill="#1B7A4A" />
            <rect x="21" y="8" width="5" height="18" rx="1" fill="#B8860B" />
            <path
              d="M25.5 7C25.5 7 23 4 20 5.5C21.5 6 23.5 6 25.5 7Z"
              fill="#3A8F5C"
              opacity="0.8"
            />
          </svg>
          <span className="font-display text-lg text-text-primary group-hover:text-primary transition-colors">
            CropFolio
          </span>
          <span className="text-[9px] uppercase tracking-widest text-accent font-medium -ml-1">
            Pro
          </span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#insight"
            className="text-sm text-text-secondary hover:text-text-primary transition-colors font-body"
          >
            The Insight
          </a>
          <a
            href="#how-it-works"
            className="text-sm text-text-secondary hover:text-text-primary transition-colors font-body"
          >
            How It Works
          </a>
          <a
            href="#impact"
            className="text-sm text-text-secondary hover:text-text-primary transition-colors font-body"
          >
            Impact
          </a>
          <a
            href="#faq"
            className="text-sm text-text-secondary hover:text-text-primary transition-colors font-body"
          >
            FAQ
          </a>
          <button
            onClick={toggleTheme}
            className="px-3 py-1 text-[11px] border border-border rounded-full text-text-secondary hover:text-text-primary hover:border-text-tertiary transition-colors duration-200"
            aria-label={
              theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
            }
          >
            {theme === "dark" ? "\u2600" : "\u263D"}
          </button>
          <Link
            to="/dashboard"
            className="px-6 py-2 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors"
          >
            Try CropFolio Pro
          </Link>
        </nav>

        {/* Mobile menu button */}
        <button
          className="md:hidden p-2 text-text-primary"
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
        <div className="md:hidden bg-surface border-t border-border">
          <nav className="flex flex-col p-6 gap-4">
            <a
              href="#insight"
              className="text-text-secondary hover:text-text-primary transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              The Insight
            </a>
            <a
              href="#how-it-works"
              className="text-text-secondary hover:text-text-primary transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              How It Works
            </a>
            <a
              href="#impact"
              className="text-text-secondary hover:text-text-primary transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Impact
            </a>
            <a
              href="#faq"
              className="text-text-secondary hover:text-text-primary transition-colors font-body py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              FAQ
            </a>
            <button
              onClick={() => {
                toggleTheme();
                setIsMobileMenuOpen(false);
              }}
              className="px-3 py-1 text-[11px] border border-border rounded-full text-text-secondary hover:text-text-primary hover:border-text-tertiary transition-colors duration-200 w-fit"
              aria-label={
                theme === "dark"
                  ? "Switch to light mode"
                  : "Switch to dark mode"
              }
            >
              {theme === "dark" ? "\u2600 Light" : "\u263D Dark"}
            </button>
            <Link
              to="/dashboard"
              className="px-6 py-3 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors text-center w-full mt-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Try CropFolio Pro
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
