interface ErrorAlertProps {
  message: string;
  onRetry?: () => void;
}

/** Left-accented error alert. */
export function ErrorAlert({ message, onRetry }: ErrorAlertProps) {
  return (
    <div className="bg-danger-subtle border-l-4 border-danger rounded-r-lg p-4">
      <p className="text-sm text-danger">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 text-sm text-danger underline hover:text-danger/80 transition-colors"
        >
          Try again
        </button>
      )}
    </div>
  );
}
