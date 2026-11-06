# Components

Five components cover the site's signature patterns. React reference versions are in `react/`, with their styles in `react/sling-components.css` (which reads `tokens.css`). Types and props are in `react/index.ts`.

## Button

Buttons start one clear action: booking a call, applying for a role or reading on.

- **primary**: cyan fill with `on-accent` text. Use one per view, for the main next step ("Book a pilot call", "Apply").
- **secondary**: outline in `ink`. For a second, equal-weight route ("See open roles").
- **ghost**: `accent-text` link with an arrow, for reading on ("How the pilot works →").

Labels say exactly what happens, in two to four words and sentence case. Avoid "Submit," "Click here" and "Learn more." Pass `href` to render a link. All variants are at least 44 px tall and show the `focus-ring` on keyboard focus. Text on cyan is always `on-accent`, never white.

## Eyebrow

The eyebrow is a small uppercase label with the cyan dot, placed above a section headline. It is the brand's main signpost, taken from the deck's slide labels ("THE PROBLEM", "THE PILOT").

Write the label in sentence case and let the CSS uppercase it. Keep it to one to three words, with one per section. It sits `space-3` above the headline. The dot is the "stone" from the logo, so do not swap it for an icon or change its colour.

## Stat

A stat is a big number in `accent-text` with a bold label, an optional note and a source line. It is the deck's signature layout. Use two to four in a row on a 12-column grid, collapsing to one column on phones.

Every external figure needs a `source` giving the publisher, dataset and date. Sling's own targets (such as "40–55% below US/UK hiring") are marked "Indicative" in the note instead. Pre-format the value with its unit ("R2.3bn", "<30 days"). Keep labels to one line, and never put a stat inside a FeatureCard.

## FeatureCard

A FeatureCard is a panel on `surface-raised` with a hairline border and `radius-sm`. It holds an optional eyebrow, a `heading-3` title and a short body. Use cards in rows of two to four for service lines, role families or proof points.

The consumer provides the body content, a sentence or a short list. Keep cards in a row the same length. Avoid icons on every card, left-edge accent bars and shadows. Depth comes only from the surface step and the border.

## PhaseStep

A PhaseStep is one stage in a real sequence. It shows a two-digit number in `accent-text`, a time window, a title and up to four items, with a hairline above. Render PhaseSteps inside an `<ol>` in a grid of three or four.

Use it only where order matters: the 90-day pilot (Design, Build, Prove), onboarding, or the hiring process. Do not use numbered phases for unordered features. Use FeatureCard for those.
