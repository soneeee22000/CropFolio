import { useInView } from "./use-in-view";

const techStack = [
  { name: "Python", category: "Backend" },
  { name: "FastAPI", category: "Backend" },
  { name: "React", category: "Frontend" },
  { name: "D3.js", category: "Visualization" },
  { name: "scipy", category: "Optimization" },
  { name: "NASA POWER", category: "Data" },
  { name: "Open-Meteo", category: "Data" },
];

const stats = [
  { value: "63", label: "Automated Tests" },
  { value: "88%", label: "Backend Coverage" },
  { value: "0", label: "External AI Costs" },
];

/**
 * Tech credibility section showing the technology stack
 * and engineering quality metrics.
 */
export function TechSection() {
  const { ref, isInView } = useInView<HTMLElement>({ threshold: 0.3 });

  return (
    <section
      ref={ref}
      className="bg-surface border-t border-border py-16 sm:py-20 px-6"
    >
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <p
          className={`text-[11px] uppercase tracking-[0.25em] text-text-tertiary mb-8 text-center font-body transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          Built With
        </p>

        {/* Tech badges */}
        <div
          className={`flex flex-wrap justify-center gap-3 mb-12 transition-all duration-700 delay-100 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          {techStack.map((tech, index) => (
            <div
              key={tech.name}
              className="px-4 py-2 bg-surface-subtle border border-border rounded-full font-data text-sm text-text-primary transition-all hover:border-primary/30 hover:bg-primary/5"
              style={{ transitionDelay: `${index * 50}ms` }}
            >
              {tech.name}
            </div>
          ))}
        </div>

        {/* Stats row */}
        <div
          className={`flex flex-wrap justify-center gap-8 sm:gap-16 transition-all duration-700 delay-300 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="font-data text-2xl text-text-primary font-medium">
                {stat.value}
              </div>
              <div className="text-sm text-text-tertiary font-body">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
