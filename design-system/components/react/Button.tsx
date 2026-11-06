import type { ReactNode, MouseEventHandler } from "react";

export interface ButtonProps {
  /** primary = cyan fill (one per view); secondary = outline; ghost = text link with arrow. */
  variant?: "primary" | "secondary" | "ghost";
  /** Renders an <a> when set, otherwise a <button>. */
  href?: string;
  type?: "button" | "submit";
  disabled?: boolean;
  onClick?: MouseEventHandler;
  className?: string;
  children: ReactNode;
}

export function Button({ variant = "primary", href, type = "button", disabled, onClick, className, children }: ButtonProps) {
  const cls = ["sl-btn", `sl-btn--${variant}`, className].filter(Boolean).join(" ");
  const arrow = variant === "ghost" ? <span className="sl-btn__arrow" aria-hidden="true"> →</span> : null;
  if (href) {
    return <a className={cls} href={href} onClick={onClick}>{children}{arrow}</a>;
  }
  return <button className={cls} type={type} disabled={disabled} onClick={onClick}>{children}{arrow}</button>;
}
