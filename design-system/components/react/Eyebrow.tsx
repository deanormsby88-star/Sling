import type { ReactNode } from "react";

export interface EyebrowProps {
  as?: "p" | "span" | "div";
  className?: string;
  /** Short label in sentence case; CSS uppercases it. */
  children: ReactNode;
}

export function Eyebrow({ as: Tag = "p", className, children }: EyebrowProps) {
  return (
    <Tag className={["sl-eyebrow", className].filter(Boolean).join(" ")}>
      <span className="sl-eyebrow__dot" aria-hidden="true" />
      {children}
    </Tag>
  );
}
