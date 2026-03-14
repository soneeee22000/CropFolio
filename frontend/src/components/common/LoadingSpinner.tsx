interface LoadingSpinnerProps {
  message?: string;
}

/** Premium pulsing dots loading indicator. */
export function LoadingSpinner({
  message = "Loading...",
}: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="flex gap-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full bg-primary"
            style={{
              animation: `pulsingDot 1.2s ease-in-out ${i * 150}ms infinite`,
            }}
          />
        ))}
      </div>
      <p className="text-sm text-text-tertiary mt-4 italic">{message}</p>
    </div>
  );
}
