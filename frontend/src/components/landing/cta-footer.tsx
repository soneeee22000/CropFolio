import { Link } from "react-router-dom";
import { useInView } from "./use-in-view";
import { ArrowRight, Sprout } from "./icons";

/**
 * Final CTA footer section with launch button
 * and hackathon attribution.
 */
export function CTAFooter() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.3 });

  return (
    <footer
      ref={ref}
      className="bg-surface text-text-primary py-12 sm:py-16 px-6"
    >
      <div className="max-w-3xl mx-auto text-center">
        {/* Logo mark */}
        <div
          className={`flex justify-center mb-6 transition-all duration-700 ${
            isInView ? "opacity-100 scale-100" : "opacity-0 scale-90"
          }`}
        >
          <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center">
            <Sprout className="w-8 h-8 text-primary" />
          </div>
        </div>

        {/* Heading */}
        <h2
          className={`font-display text-4xl sm:text-5xl lg:text-6xl mb-6 leading-tight transition-all duration-700 delay-100 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          See it for yourself.
        </h2>

        {/* CTA Button */}
        <div
          className={`mb-8 transition-all duration-700 delay-200 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <Link
            to="/app"
            className="inline-flex items-center px-10 py-4 bg-primary text-white rounded-lg text-lg font-body group hover:bg-primary-dark transition-colors"
          >
            Launch CropFolio
            <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
          </Link>
        </div>

        {/* Hackathon credit */}
        <div
          className={`transition-all duration-700 delay-300 ${
            isInView ? "opacity-100" : "opacity-0"
          }`}
        >
          <p className="text-sm text-text-tertiary font-body mb-2">
            Built for the AI for Climate-Resilient Agriculture Hackathon 2026
          </p>
          <p className="text-sm text-text-tertiary font-body">
            Impact Hub Yangon x UNDP Myanmar
          </p>
        </div>

        {/* Decorative line */}
        <div
          className={`mt-10 pt-6 border-t border-border transition-all duration-700 delay-400 ${
            isInView ? "opacity-100" : "opacity-0"
          }`}
        >
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-text-tertiary font-body">
            <div className="flex items-center gap-2">
              <Sprout className="w-4 h-4 text-primary" />
              <span className="font-display text-base text-text-primary">
                CropFolio
              </span>
            </div>
            <p>Modern Portfolio Theory for Agriculture</p>
            <p>&copy; 2026 All rights reserved</p>
          </div>
        </div>
      </div>
    </footer>
  );
}
