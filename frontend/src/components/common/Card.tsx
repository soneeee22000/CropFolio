import type { ReactNode } from "react";

interface CardProps {
  title?: string;
  children: ReactNode;
  className?: string;
}

/** Premium card container with warm border and generous padding. */
export function Card({ title, children, className = "" }: CardProps) {
  return (
    <div
      className={`bg-surface-elevated rounded-xl border border-border p-8 animate-fade-in-up ${className}`}
    >
      {title && (
        <h3 className="font-display text-[22px] text-text-primary mb-6">
          {title}
        </h3>
      )}
      {children}
    </div>
  );
}
