import { useEffect, useState, useRef } from "react";

interface AnimatedCounterProps {
  end: number;
  duration?: number;
  suffix?: string;
  prefix?: string;
  decimals?: number;
  className?: string;
  shouldStart?: boolean;
  onComplete?: () => void;
}

/**
 * Animated number counter with easeOutQuart easing.
 * Counts from 0 to `end` over `duration` milliseconds.
 */
export function AnimatedCounter({
  end,
  duration = 1500,
  suffix = "",
  prefix = "",
  decimals = 0,
  className = "",
  shouldStart = true,
  onComplete,
}: AnimatedCounterProps) {
  const [count, setCount] = useState(0);
  const countRef = useRef(0);
  const frameRef = useRef<number>(undefined);
  const startTimeRef = useRef<number>(undefined);
  const hasCompleted = useRef(false);

  useEffect(() => {
    if (!shouldStart) {
      setCount(0);
      countRef.current = 0;
      hasCompleted.current = false;
      return;
    }

    const easeOutQuart = (t: number): number => {
      return 1 - Math.pow(1 - t, 4);
    };

    const animate = (timestamp: number) => {
      if (!startTimeRef.current) {
        startTimeRef.current = timestamp;
      }

      const elapsed = timestamp - startTimeRef.current;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOutQuart(progress);

      countRef.current = easedProgress * end;
      setCount(countRef.current);

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate);
      } else {
        if (!hasCompleted.current) {
          hasCompleted.current = true;
          onComplete?.();
        }
      }
    };

    frameRef.current = requestAnimationFrame(animate);

    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, [end, duration, shouldStart, onComplete]);

  const displayValue =
    decimals > 0 ? count.toFixed(decimals) : Math.round(count).toString();

  return (
    <span className={className}>
      {prefix}
      {displayValue}
      {suffix}
    </span>
  );
}
