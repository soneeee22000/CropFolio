import { useEffect, useState, useRef } from "react";

interface VolatilityVisualizationProps {
  isInView: boolean;
}

/**
 * Animated SVG visualization comparing income volatility
 * between monocrop (rice only) and a diversified portfolio.
 */
export function VolatilityVisualization({
  isInView,
}: VolatilityVisualizationProps) {
  const [progress, setProgress] = useState(0);
  const frameRef = useRef<number>(undefined);

  useEffect(() => {
    if (!isInView) return;

    let startTime: number | null = null;
    const duration = 4000; // 4 second loop

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const newProgress = (elapsed % duration) / duration;
      setProgress(newProgress);
      frameRef.current = requestAnimationFrame(animate);
    };

    frameRef.current = requestAnimationFrame(animate);

    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, [isInView]);

  // Calculate wave values
  const monoHeight = 60 + Math.sin(progress * Math.PI * 4) * 35; // High volatility
  const riceHeight = 35 + Math.sin(progress * Math.PI * 4) * 12;
  const pulseHeight =
    30 + Math.sin(progress * Math.PI * 4 + Math.PI * 0.7) * 10;
  const oilseedHeight =
    35 + Math.sin(progress * Math.PI * 4 + Math.PI * 1.4) * 8;

  return (
    <div className="relative w-full max-w-md mx-auto h-64">
      <svg
        viewBox="0 0 300 200"
        className="w-full h-full"
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Grid lines */}
        <defs>
          <pattern
            id="grid"
            width="30"
            height="20"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 30 0 L 0 0 0 20"
              fill="none"
              stroke="#1A1A18"
              strokeOpacity="0.1"
              strokeWidth="0.5"
            />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        {/* Labels */}
        <text x="20" y="25" className="text-[10px] fill-[#A3A29D] font-body">
          Monocrop (Rice Only)
        </text>
        <text x="20" y="130" className="text-[10px] fill-[#A3A29D] font-body">
          Diversified Portfolio
        </text>

        {/* Monocrop bar - high volatility */}
        <g transform="translate(20, 35)">
          <rect
            x="0"
            y={80 - monoHeight}
            width="260"
            height={monoHeight}
            fill="#1B7A4A"
            opacity="0.8"
            rx="2"
          />
          <text
            x="130"
            y={80 - monoHeight - 8}
            textAnchor="middle"
            className="text-[11px] font-body font-medium fill-[#1A1A18]"
          >
            Rice: High Volatility
          </text>
        </g>

        {/* Diversified bars - lower combined volatility */}
        <g transform="translate(20, 140)">
          {/* Rice portion */}
          <rect
            x="0"
            y={50 - riceHeight}
            width="86"
            height={riceHeight}
            fill="#1B7A4A"
            rx="2"
          />

          {/* Pulse portion */}
          <rect
            x="88"
            y={50 - pulseHeight}
            width="86"
            height={pulseHeight}
            fill="#B8860B"
            rx="2"
          />

          {/* Oilseed portion */}
          <rect
            x="176"
            y={50 - oilseedHeight}
            width="84"
            height={oilseedHeight}
            fill="#5D8A66"
            rx="2"
          />
        </g>

        {/* Legend */}
        <g transform="translate(20, 195)">
          <rect x="0" y="-8" width="12" height="8" fill="#1B7A4A" rx="1" />
          <text x="16" y="0" className="text-[9px] fill-[#A3A29D] font-body">
            Rice
          </text>

          <rect x="60" y="-8" width="12" height="8" fill="#B8860B" rx="1" />
          <text x="76" y="0" className="text-[9px] fill-[#A3A29D] font-body">
            Black Gram
          </text>

          <rect x="150" y="-8" width="12" height="8" fill="#5D8A66" rx="1" />
          <text x="166" y="0" className="text-[9px] fill-[#A3A29D] font-body">
            Sesame
          </text>
        </g>
      </svg>

      {/* Volatility indicator */}
      <div className="absolute top-10 right-4 flex flex-col items-end gap-1">
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#A3A29D] font-body">Volatility</span>
          <div className="w-16 h-2 bg-[#E8E6E1] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#c43b3b] transition-all duration-100"
              style={{
                width: `${Math.abs(Math.sin(progress * Math.PI * 4)) * 100}%`,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
