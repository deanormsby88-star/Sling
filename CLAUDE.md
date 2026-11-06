# Sling website: project rules

This repository is the marketing website for **Sling**, a South African company that builds dedicated, managed teams of skilled professionals (finance and accounting first) for UK, US and Israeli firms. Brand line: "Small stone. Giant impact."

## Read first, in this order

1. `docs/BRIEF.md`: audiences, sitemap, page content, functional and technical requirements, build plan.
2. `design-system/README.md`: brand book covering voice, logo, colour, type, layout and components.
3. `design-system/tokens.css` and `design-system/tokens.json`: every colour, font, spacing and radius value.
4. `design-system/components/`: component guidelines plus React reference versions.

`docs/reference/Sling_Teaser_Deck_v3.pdf` is the private investor deck the brand came from. Use it for context and tone only. Never copy its competitor names, pricing benchmarks or investor content onto the site.

## Working agreement

- Build in the four passes in the brief, and **stop for review after each pass**. Begin by proposing the project structure and waiting for approval.
- Keep `docs/OPEN-ITEMS.md` up to date with every placeholder you use and every decision Dean still needs to make.
- Ask before adding a paid service, a new dependency over ~50 kB, or any third-party script.

## Brand rules (non-negotiable)

- Use only values from `tokens.css`. Never hard-code a hex colour, font or pixel size in components.
- **Dark theme is the default** (`data-theme="dark"` on `<html>`). The light theme is for Careers detail and Legal pages.
- Cyan (`--accent`) is for fills, dots and rules. Cyan **text** uses `--accent-text`. Text on cyan uses `--on-accent`, never white.
- Logos come from `assets/logos/*.svg` only. Never retype the wordmark in a font, recolour the dot, or place the logo on cyan.
- Headings use Poppins (`--font-display`) and text uses Lato (`--font-body`), both from Google Fonts with `display=swap`.
- No drop shadows, gradients, emoji, stock photos or icon-on-every-card layouts.
- Every external statistic shows its source and date. Savings figures are "indicative" ranges.
- Copy is en-GB, plain and specific, with no exclamation marks or hype words.
- Do not name clients or competitors anywhere on the site.

## Engineering rules

- WCAG 2.2 AA: semantic HTML, a visible focus ring (`--focus-ring`, 2 px, 3 px offset), labelled form fields, and `prefers-reduced-motion` respected.
- Validate forms on the server, keep secrets in environment variables with an `.env.example`, and rate-limit form routes.
- Aim for Lighthouse 90+ on mobile. Images in AVIF or WebP with dimensions set.
- Keep the brand name and domain in one config constant, because the name may change after a trademark check.
