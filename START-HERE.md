# Sling website kit: start here

This folder has everything Claude Code needs to build the Sling website.

| Path | What it is |
| --- | --- |
| `CLAUDE.md` | Project rules. Claude Code reads this automatically. |
| `docs/BRIEF.md` | The website brief: goals, audiences, sitemap, page content, requirements, build plan |
| `docs/reference/Sling_Teaser_Deck_v3.pdf` | The source deck, for context only (private: not for the website) |
| `design-system/README.md` | Brand book: voice, logo, colour, type, layout, imagery |
| `design-system/tokens.css` | Ready-to-use CSS variables for both themes |
| `design-system/tokens.json` | The same tokens as data |
| `design-system/components/` | Guidelines plus React versions of Button, Eyebrow, Stat, FeatureCard, PhaseStep |
| `design-system/reference/` | The trajectory motif (`cover.svg`) and a component preview page |
| `assets/logos/` | Vector logos (SVG) for dark, light and one-colour use, plus the original PNGs |
| `assets/favicon.svg` | The cyan dot on charcoal |

## How to start

1. Unzip this folder and rename it to your project name (for example `sling-website`).
2. Open the folder in Claude Code.
3. Paste this prompt:

```text
You are building the Sling marketing website. Read CLAUDE.md, then docs/BRIEF.md in full, then design-system/README.md and design-system/tokens.css.

Then propose the project structure and stack (the brief recommends Next.js + TypeScript on Vercel), list any questions, and wait for my approval. After I approve, build pass 1 only (foundations plus a /styleguide page that shows the logo, colours, type and all five components in both themes) and stop for review.
```

Things only you can supply are listed under "Content still needed" in the brief. Claude Code will use placeholders and keep a list in `docs/OPEN-ITEMS.md`.
