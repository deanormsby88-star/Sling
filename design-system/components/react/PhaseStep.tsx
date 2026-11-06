import type { ReactNode } from "react";

export interface PhaseStepProps {
  /** Two-digit sequence marker, e.g. "01". Only for real sequences; render inside an <ol>. */
  number: string;
  /** Time window, e.g. "Days 0–30". */
  window?: string;
  title: ReactNode;
  items?: ReactNode[];
  className?: string;
}

export function PhaseStep({ number, window, title, items, className }: PhaseStepProps) {
  return (
    <li className={["sl-step", className].filter(Boolean).join(" ")}>
      <div className="sl-step__num" aria-hidden="true">{number}</div>
      {window ? <p className="sl-step__window">{window}</p> : null}
      <h3 className="sl-step__title">{title}</h3>
      {items && items.length ? <ul className="sl-step__list">{items.map((t, i) => <li key={i}>{t}</li>)}</ul> : null}
    </li>
  );
}
