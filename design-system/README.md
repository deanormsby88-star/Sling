# Sling

Sling recruits, employs and runs skilled South African teams for companies in the UK, the US and Israel. Clients pay one monthly fee per team member, and Sling owns recruitment, employment, workspace and quality. The first teams are in finance and accounting, then skilled operations, then customer experience.

The brand line is **Small stone. Giant impact.** It comes from David's sling: a small, well-aimed stone that does something much larger than itself. The brand should feel the same. It is compact, precise and confident, and it backs claims with evidence instead of volume.

This system is the source for Sling's website and every other screen. It was built from the Sling teaser deck (v3, October 2026): its logo, palette, type and layout habits. Anything the deck did not cover is marked as a decision made here.

## The brand idea

- **The cyan dot is the stone.** The dot over the "i" in the wordmark is the brand's one bright note. Use it the same way everywhere: one small, bright point on a calm charcoal ground. It appears as the eyebrow marker (see Eyebrow), in the cover pattern, and as the active state in navigation. It never becomes a background wash.
- **Work, not charity.** Sling's story starts in a community that wants to create jobs at home, but the product is a commercial service. Lead with what the client gets (skilled people, managed teams, time-zone overlap, savings) and let the jobs story support it.
- **Proof before promise.** The deck's ask was "Approve the proof, not the promise." Every page should show evidence: a number, a source, a named process, a clear next step.

## Voice

Sling writes the way a capable operator talks to another operator: short, plain and specific.

**Principles**

1. **Short declarative headlines, ending in a full stop.** Two beats work well: "Small stone. Giant impact." "One client. Three to five roles. Ninety days."
2. **Numbers do the persuading.** Prefer "40–55% below equivalent US/UK hiring" to "huge savings." Every statistic carries its source and date, shown where it appears.
3. **Name the work.** Bookkeeping, management accounts, AP/AR, audit support, paraplanning, claims, client success. Avoid vague categories like "solutions" or "services."
4. **Talk to one reader at a time.** Clients, candidates and supporters each get their own page and their own tone (below).
5. **No hype.** No exclamation marks, no "world-class," "cutting-edge," "seamless" or "revolutionary," and no emoji.

**By audience**

| Audience | What they need to hear | Tone |
| --- | --- | --- |
| Clients (finance leaders, COOs, partners at UK/US/Israeli firms) | Which roles, what it costs, how quality and security are managed, how fast it starts | Commercial, exact, unhurried |
| Candidates (South African professionals and graduates) | Real roles with international firms, a career path, fair pay, where they will work | Warm, direct, respectful; hiring is merit-based and open to all South Africans |
| Supporters and partners (alumni networks, foundations) | How an introduction becomes jobs at home, and how impact is measured | Grounded and specific; impact reported in jobs and roles, not adjectives |

**Examples**

- Do: "Dedicated finance teams in Johannesburg. Working your hours, on your systems."
- Do: "Your first shortlist in under 30 days."
- Do: "South Africa has 8.5 million people without work. We bring the work here." (with source line)
- Don't: "Revolutionising global talent with cutting-edge offshore solutions!"
- Don't: "Join our amazing family."

## Logo

The masters are vector SVGs in `assets/logos/` at the root of this kit. Use them everywhere.

- `sling-logo-white.svg`: white wordmark with cyan dot, for dark grounds (`surface` in the dark theme, `brand-charcoal`, `brand-black`). This is the primary logo.
- `sling-logo-charcoal.svg`: charcoal wordmark with cyan dot, for light grounds (`surface` in the light theme).
- `sling-logo-mono-white.svg` and `sling-logo-mono-charcoal.svg`: single-colour versions, dot included, for embossing, engraving, one-colour print, or wherever cyan can't be reproduced.
- `legacy-sling-logo-white.png` and `legacy-sling-logo-charcoal.png`: the original raster extracts from the deck, kept for reference only.

**How the logo is built:** the wordmark is "sl", a dotless "i", and "ng", set in Poppins Bold, the same family the system uses for headings. The SVGs were rebuilt from Poppins Bold's own outlines and match the deck artwork to within a pixel. The dot is a perfect circle centred on the "i" stem. Its diameter is 1.24 times the stem width, and it floats above the stem. Never retype the logo in a live font. Always use the SVG files.

Rules:

- **Clear space:** keep a margin at least the diameter of the dot on every side, with nothing inside it.
- **Minimum size:** 72 px wide on screen (the dot must stay a visible disc).
- **Do not** recolour the dot, put the logo on cyan, outline it, add effects, stretch it, or set "sling" in another typeface as a substitute.
- **Header placement:** top left on the website, at 96–120 px wide. The deck places it top right on slides, but that is a slide convention only.
- **Favicon:** `assets/favicon.svg`, the cyan dot on a `brand-charcoal` square. The full wordmark is unreadable at 16–32 px.

## Colour

The palette is charcoal, white and one cyan. In the deck, cyan does all the emphasis work: the logo dot, eyebrow labels, big numbers and key rules.

| Role | Dark theme (primary) | Light theme |
| --- | --- | --- |
| `surface` page ground | #1D1D1D | #FFFFFF |
| `surface-raised` panels and cards | #131313 | #F4F7F7 |
| `surface-alt` bands and inputs | #2A2A2C | #EAEFEF |
| `ink` headings | #FFFFFF | #1D1D1D |
| `ink-body` running text | #E6E6E6 | #2B2B2B |
| `ink-muted` notes and sources | #9A9A9A | #5E6466 |
| `accent` cyan fills, dots, rules | #0ADBDE | #0ADBDE |
| `accent-text` cyan as text | #0ADBDE | #00777A |

Rules:

- **Proportion:** about 70% charcoal or white ground, 20% text, 10% cyan. If a screen looks cyan, there is too much of it.
- **Cyan text on light grounds uses `accent-text`**, the deep teal (#00777A). Bright cyan on white fails contrast. Cyan *fills* (buttons, dots, rules) stay `accent` in both themes.
- **Text on a cyan fill is `on-accent`** (#131313), never white.
- **Dark is the primary theme**, as in the deck: hero, navigation, client pages and footer. Use the light theme for long-reading pages (careers detail, legal, articles) and for printable material.
- Error states use `signal-error`. There is no green "success" colour in the brand. Confirmations use `ink` plus a cyan dot.

## Typography

The deck sets headings in **Century Gothic Bold** and text in **Calibri**. Neither can be served freely on the web, so the website uses close open-licence matches from Google Fonts:

- **Display:** Poppins (600, 700) in place of Century Gothic Bold. Both are geometric with round bowls and a single-storey "a." If Sling licenses Century Gothic as a web font later, put it first in `font-display`.
- **Text:** Lato (400, 700, italic). Carlito, the open Calibri clone, was built on Lato, so it is the natural web match for Calibri.

Load both from Google Fonts:
`https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Lato:ital,wght@0,400;0,700;1,400&display=swap`

Rules:

- Headlines in sentence case, ending with a full stop when they are statements.
- Eyebrows (small labels above headings) in uppercase, `eyebrow` style, letter-spaced, in `accent-text`, with the dot marker.
- Big numbers use the `stat` style in `accent-text`, with label and source beneath in `ink-body` and `ink-muted`.
- Keep running text to `measure` (about 68 characters per line).
- Use `display-xl` once per page at most.

## Layout and spacing

- **Grid:** 12 columns, `container` max width 1200 px, 24 px gutters (`space-6`), with side padding of at least 16 px on phones.
- **Section rhythm:** `space-24` (96 px) between major sections on desktop and `space-16` (64 px) on phones. Inside a section, `space-8` (32 px) between groups.
- **Composition from the deck:** left-aligned headline blocks, eyebrow then headline then one supporting line, then content in two to four equal columns. Avoid centring long text.
- **Panels:** `surface-raised` with a 1 px `hairline` border and `radius-sm`. There are no drop shadows. Depth comes from the step between `surface` and `surface-raised`.
- **Sources:** show a source line under every data block in `caption`, `ink-muted`, as the deck does under every chart.

## Brand devices

- **Eyebrow with dot:** the main way pages are signposted. Use one per section, at most.
- **Stat row:** two to four `Stat`s side by side, each with a source. This is the deck's most recognisable layout.
- **Numbered phases:** 01 / 02 / 03 markers only where the content is a real sequence, such as the 90-day pilot (Design, Build, Prove) or a hiring process. Never use them for unordered lists.
- **The trajectory:** a row of cyan discs rising along an arc, from small to large ("small stone, giant impact"). Use it once on the home hero or a key banner, never as wallpaper.

## Imagery

- Photograph real Sling people at work in Johannesburg or Cape Town, in natural light: desks, screens, conversations. Avoid stock images of handshakes, globes and headsets.
- Until there is a photo shoot, lead with type, stats and the trajectory device rather than generic stock.
- Photos sit full-bleed or in `radius-sm` frames, never in circles (circles belong to the dot).

## Icons

Use a line icon set with a 1.5 px stroke and rounded joins (Lucide fits). Icons are `ink-body` by default and `accent-text` only when active or selected. Use them sparingly, to mark navigation or form fields, not as decoration on every card.

## Accessibility

- All text pairs here meet WCAG 2.2 AA (4.5:1, or 3:1 for 24 px and above) in both themes. Check any new pair before using it.
- Keyboard focus is a 2 px `focus-ring` outline with a 3 px offset on every interactive element.
- Respect `prefers-reduced-motion`. The brand barely moves anyway, so a single fade or rise on scroll is the most to use.

## Using this system

- `tokens.css` defines every token as a CSS custom property. Dark is the default on `:root`; set `data-theme="light"` on any element to switch that subtree to the light theme. Import it once, globally.
- `tokens.json` holds the same values as data, with a usage note on every token.
- `components/` has a guideline file for each component and React reference implementations in `components/react/` (TypeScript, no dependencies beyond React), styled by `components/react/sling-components.css`.
- `reference/cover.svg` shows the trajectory motif. `reference/components-preview.html` renders every component in both themes. Open it in a browser.
- Load fonts with: `https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Lato:ital,wght@0,400;0,700;1,400&display=swap`, or self-host Poppins and Lato through `next/font/google`.
