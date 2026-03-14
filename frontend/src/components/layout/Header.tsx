import { STEP_LABELS } from "@/constants";

interface HeaderProps {
  currentStep: number;
}

/** Premium sticky header with backdrop blur and line-based step indicator. */
export function Header({ currentStep }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-surface-elevated/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <h1 className="font-display text-2xl text-text-primary tracking-tight">
          CropFolio
        </h1>
        <nav className="hidden sm:flex items-center gap-1">
          {STEP_LABELS.map((label, i) => (
            <div key={label} className="flex items-center">
              <div className="flex flex-col items-center gap-1">
                <div
                  className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    i === currentStep
                      ? "bg-primary scale-125"
                      : i < currentStep
                        ? "bg-primary/40"
                        : "bg-border"
                  }`}
                />
                <span
                  className={`text-[11px] tracking-wide transition-colors duration-300 ${
                    i === currentStep
                      ? "text-text-primary font-medium"
                      : "text-text-tertiary"
                  }`}
                >
                  {label}
                </span>
              </div>
              {i < STEP_LABELS.length - 1 && (
                <div
                  className={`w-12 h-px mx-2 mt-[-14px] transition-colors duration-300 ${
                    i < currentStep ? "bg-primary/30" : "bg-border"
                  }`}
                />
              )}
            </div>
          ))}
        </nav>
      </div>
    </header>
  );
}
