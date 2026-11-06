import type { ReactNode } from "react";
import { Eyebrow } from "./Eyebrow";

export interface FeatureCardProps {
  eyebrow?: ReactNode;
  title: ReactNode;
  className?: string;
  children?: ReactNode;
}

export function FeatureCard({ eyebrow, title, className, children }: FeatureCardProps) {
  return (
    <article className={["sl-card", className].filter(Boolean).join(" ")}>
      {eyebrow ? <Eyebrow>{eyebrow}</Eyebrow> : null}
      <h3 className="sl-card__title">{title}</h3>
      <div className="sl-card__body">{children}</div>
    </article>
  );
}
