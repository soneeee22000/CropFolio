import { useInView } from "./use-in-view";

const techStack = [
  { name: "Python", category: "Backend" },
  { name: "FastAPI", category: "Backend" },
  { name: "React", category: "Frontend" },
  { name: "D3.js", category: "Visualization" },
  { name: "scipy", category: "Optimization" },
  { name: "Gemini AI", category: "AI" },
  { name: "FAOSTAT", category: "Data" },
  { name: "NASA POWER", category: "Data" },
  { name: "Open-Meteo", category: "Data" },
];

const stats = [
  { value: "89", label: "Automated Tests" },
  { value: "12yr", label: "FAOSTAT Yield Data" },
  { value: "10", label: "API Endpoints" },
  { value: "$0", label: "AI Costs (Gemini Free)" },
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
      className="bg-[#1A1A18] text-[#FAFAF8] border-t border-[#333330] py-10 sm:py-12 px-6"
    >
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <p
          className={`text-[11px] uppercase tracking-[0.25em] text-[#A3A29D] mb-8 text-center font-body transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          Built With
        </p>

        {/* Tech badges */}
        <div
          className={`flex flex-wrap justify-center gap-3 mb-6 transition-all duration-700 delay-100 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          }`}
        >
          {techStack.map((tech, index) => (
            <div
              key={tech.name}
              className="px-4 py-2 bg-[#242422] border border-[#333330] rounded-full font-data text-sm text-[#FAFAF8] transition-all hover:border-primary/30 hover:bg-primary/10"
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
              <div className="font-data text-2xl text-[#FAFAF8] font-medium">
                {stat.value}
              </div>
              <div className="text-sm text-[#A3A29D] font-body">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
