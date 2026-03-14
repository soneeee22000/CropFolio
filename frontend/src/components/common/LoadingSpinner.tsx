interface LoadingSpinnerProps {
  message?: string;
}

/** Centered loading spinner with optional message. */
export function LoadingSpinner({
  message = "Loading...",
}: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-8 h-8 border-3 border-gray-200 border-t-primary rounded-full animate-spin" />
      <p className="text-sm text-gray-500 mt-3">{message}</p>
    </div>
  );
}
