import type { ReactNode } from "react";

export interface StatProps {
  /** Pre-formatted number: "40–55%", "R2.3bn", "<30 days". */
  value: ReactNode;
  label: ReactNode;
  note?: ReactNode;
  /** Required for any external statistic: publisher, dataset and date. */
  source?: string;
  className?: string;
}

export function Stat({ value, label, note, source, className }: StatProps) {
  return (
    <figure className={["sl-stat", className].filter(Boolean).join(" ")}>
      <div className="sl-stat__value">{value}</div>
      <figcaption className="sl-stat__caption">
        <span className="sl-stat__label">{label}</span>
        {note ? <span className="sl-stat__note">{note}</span> : null}
        {source ? <cite className="sl-stat__source">Source: {source}</cite> : null}
      </figcaption>
    </figure>
  );
}
