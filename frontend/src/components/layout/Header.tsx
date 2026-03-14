import { STEP_LABELS } from "@/constants";

interface HeaderProps {
  currentStep: number;
}

/** App header with logo and step indicator. */
export function Header({ currentStep }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900 tracking-tight">
            CropFolio
          </h1>
          <p className="text-xs text-gray-500">
            Portfolio Theory for Climate-Resilient Farming
          </p>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-sm">
          {STEP_LABELS.map((label, i) => (
            <div key={label} className="flex items-center gap-2">
              <span
                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                  i === currentStep
                    ? "bg-primary text-white"
                    : i < currentStep
                      ? "bg-green-100 text-green-700"
                      : "bg-gray-100 text-gray-400"
                }`}
              >
                {i + 1}
              </span>
              <span
                className={`${
                  i === currentStep
                    ? "text-gray-900 font-medium"
                    : "text-gray-400"
                }`}
              >
                {label}
              </span>
              {i < STEP_LABELS.length - 1 && (
                <span className="text-gray-300 mx-1">—</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}
