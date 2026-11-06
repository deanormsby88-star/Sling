# Sling Website Brief

Version 1, 6 November 2026. Owner: Dean Ormsby.

## How to use this brief

This brief tells you what to build for Sling's first website. The design system in `/design-system` is the source for every colour, font, spacing step, component and logo file. Where the two disagree, the design system wins on look and feel, and this brief wins on content and function.

## Purpose and goals

The site has one job: turn warm introductions into booked pilot conversations. Most clients will arrive from a personal referral, so the site must confirm that Sling is credible and specific, and make it easy to book a call. It also gives South African candidates a place to register for roles.

| Goal | Measure | Year-one target |
| --- | --- | --- |
| Convert referred visitors into conversations | Pilot call requests from the Contact form | 20 qualified requests |
| Build a candidate pipeline before roles open | Talent pool sign-ups | 300 registered candidates in finance and accounting |
| Look credible to a sceptical CFO or partner | Time on the How it works and Security pages | Average over 60 seconds |
| Load fast in the UK, US, Israel and SA | Core Web Vitals on mobile | All three metrics in the green band |

## Audiences

Three audiences use the site, in this order of priority. Each gets its own route from the home page.

| Audience | Who they are | What they need to find | Main action |
| --- | --- | --- | --- |
| 1. Clients | CFOs, COOs, finance directors and partners at UK and US accounting, wealth and law firms, and at Israeli tech companies | Which roles Sling covers, how the pilot works, rough cost, how data and quality are managed | Book a pilot call |
| 2. Candidates | South African finance and accounting professionals and graduates, open to all South Africans | Real roles with international firms, pay and benefits, where they will work, how to apply | Join the talent pool |
| 3. Supporters | Alumni networks, foundations, community leaders and potential investors | How an introduction becomes jobs at home, and how impact is reported | Make an introduction |

## Positioning and key messages

**Positioning:** Sling builds dedicated, managed teams of skilled South African professionals for UK, US and Israeli firms. The first teams are in finance and accounting. Each team works the client's hours on the client's systems, for one monthly fee per person.

**Line:** Small stone. Giant impact.

**Hero headline options** (Dean to pick one; use the first until then):

- "Skilled finance teams in South Africa. Working your hours."
- "Your next finance team is in Johannesburg."
- "Bringing the world's work home to South Africa." (the deck's line, which suits the Supporters page best)

**Four messages for clients, in order:**

1. **Dedicated, managed teams, not freelancers.** Sling recruits, employs, houses and quality-checks every person.
2. **Built for your time zone.** Full UK overlap, and US coverage by design.
3. **Meaningfully lower cost.** Indicative pricing is 40–55% below equivalent US/UK hiring, depending on role and scope. Show this as a range with that caveat, never as a promise.
4. **Proof before promise.** Start with one 90-day pilot of three to five roles, with KPIs agreed up front.

**For candidates:** real careers with international firms, without leaving South Africa.

**For supporters:** don't just send a donation, send the work. In the Maimonides tradition, a job is the highest form of giving.

**Public-site cautions:**

- Do not name other outsourcing providers as benchmarks or proof points. The deck in `docs/reference` does this, but it is a private document.
- Do not name clients until they agree in writing.
- Every external statistic carries its source and date (see the Stat component).
- Keep the community story on the Supporters and About pages. Client and candidate pages lead with the commercial offer, and candidate pages say hiring is merit-based and open to all South Africans.

## Sitemap

```
/                                  Home
├── For clients
│   ├── /services                  Services overview
│   │   ├── /services/finance-and-accounting    (launch: main page)
│   │   ├── /services/operations               (coming next: register interest)
│   │   └── /services/customer-experience      (coming next: register interest)
│   ├── /how-it-works              The 90-day pilot
│   ├── /security                  Security and quality
│   └── /contact                   Book a pilot call   ← primary conversion
├── For candidates
│   └── /careers                   Open roles + talent pool form
├── For supporters
│   ├── /supporters                Make an introduction
│   └── /about                     Story and team
└── Footer on every page: /privacy  /cookies  /terms  /paia
```

The main navigation is Services, How it works, Careers, About and a "Book a pilot call" button. Supporters and Security are linked from the home page and the footer.

## Page by page

Each page opens with an Eyebrow, a headline and one supporting line, then follows the order below. The copy shown is a working draft and can be refined.

### Home `/`

1. **Hero** (dark): eyebrow "Offshore teams, South Africa", the headline, a one-line explanation, and two buttons: "Book a pilot call" (primary) and "See how it works" (ghost). The trajectory device sits on the right.
2. **What we build**: three FeatureCards. Launch: Finance and accounting (bookkeeping, management accounts, AP/AR, audit support). Next: Skilled operations (claims, paralegal, executive support, analytics). Scale: Customer experience (premium support, sales, client success).
3. **Why clients say yes**: three Stats: "40–55%" below equivalent US/UK hiring (indicative), "1–2 hrs" ahead of the UK so the working day is almost fully shared, and "<30 days" to first shortlist (pilot target).
4. **The pilot**: three PhaseSteps (Design, Build, Prove) with a link to How it works.
5. **Why South Africa**: a Stat row from public data with sources. 115,000 new international jobs created in SA from 2019 to 2024, and 76.5% of new jobs coming from the US and UK (source: BPESA GBS Sector Job Creation Report, April–June 2025). Check the figures against the source before launch.
6. **Two audience panels**: "Hiring in South Africa?" linking to Careers, and "Want to help?" linking to Supporters.
7. **Closing call to action**: "One client. Three to five roles. Ninety days." with the Book a pilot call button.

### Services `/services`, with three child pages

- `/services/finance-and-accounting` is the main page at launch. List each role with what it covers, the systems the team works in (Xero, Sage, QuickBooks, NetSuite, Excel) and typical seniority. The system list needs confirming with Martin.
- `/services/operations` and `/services/customer-experience` start as short "coming next" pages with a register-interest form.

### How it works `/how-it-works`

The 90-day pilot in detail: Design (days 0–30: select the process; set scope, KPIs and security; agree pricing and governance), Build (days 31–60: recruit and shortlist; client interviews and selection; onboard people and systems) and Prove (days 61–90: go live with weekly QA; track quality, savings and uptime; decide whether to scale, refine or stop). Then what Sling owns (recruitment, employment, workspace, equipment, QA, retention) against what the client provides (process documentation, system access, a named manager). Then the pricing model: one monthly fee per team member, with no recruitment fees. Do not publish prices; say "from a pilot quote". Close with an FAQ of about eight questions: contracts, notice periods, IP, data, holidays, load-shedding backup, replacing a team member, and time zones.

### Security and quality `/security`

How client data is protected: POPIA and UK GDPR compliance, data processing agreements, device management, access control and backup power. State only what is in place at launch, and add ISO 27001 when it is real. Include the QA model: weekly quality reviews and KPIs agreed in the pilot.

### Careers `/careers`

Aimed at candidates. Cover what working at Sling is like, the roles being hired now and next, pay and benefits in general terms, where the team works, and the hiring steps as PhaseSteps (Apply, Assess, Interview with the client, Onboard). A talent pool form with CV upload. A clear line: "Hiring is merit-based and open to all South Africans." Use the light theme for long role descriptions.

### About `/about`

The story: South Africa's jobs emergency, shown as Stats with sources. Official unemployment is 33.6%, 8.5 million South Africans are without work, and youth unemployment is 47.4% (source: Statistics South Africa, Quarterly Labour Force Survey, Q2 2026). The idea, in the line "don't just send a donation, send the work". Then the team: Martin Smookler CA(SA), founder, plus the rest of the leadership once Dean confirms who is named at launch.

### Supporters `/supporters`

For alumni and community networks. How one introduction becomes a pod of three to five jobs, what to send (a name and a company), and how impact will be reported (jobs created, roles, retention). The "Make an introduction" form.

### Contact `/contact`

The Book a pilot call form (see Functional requirements), plus an email address shown as text, the Johannesburg location, and a note on response time ("we reply within one working day"). Use placeholders until Dean supplies the address.

### Legal

`/privacy`, `/cookies`, `/terms` and `/paia` (a PAIA manual is required for South African private bodies). Light theme, plain text pages, with placeholder copy clearly marked "Draft: legal review required".

## Look and feel

Follow `/design-system/README.md`. In summary:

- **Dark first.** Charcoal ground (#1D1D1D), white headings, and Sling cyan (#0ADBDE) used sparingly for the eyebrow dot, big numbers, primary buttons and rules. Long-reading pages (Careers detail, Legal) use the light theme.
- **Type.** Poppins for headings, standing in for Century Gothic Bold (the logo itself is Poppins Bold), and Lato for text, standing in for Calibri. Both load from Google Fonts.
- **Signature layouts.** Eyebrow, then headline, then one line. Stat rows with source lines. Numbered phases only for real sequences.
- **The trajectory.** Cyan discs rising along an arc from small to large, used once in the home hero. See `/design-system/reference/cover.svg` for the motif.
- **Restraint.** No drop shadows, gradients, stock handshake photos or emoji. Square-ish panels, round buttons.
- **Imagery.** Real Sling people once there is a photo shoot. Until then, the pages are led by type and data.

## Functional requirements

| Feature | What it does | Fields or details |
| --- | --- | --- |
| Book a pilot call form | Sends a qualified lead to Sling and an email confirmation to the sender | Name, work email, company, country (UK / US / Israel / other), role type (dropdown), team size (1–2, 3–5, 6+), "How did you hear about us?" including "Introduced by someone I know", message, consent tick box |
| Talent pool form | Registers candidates for current and future roles | Name, email, phone, city, role family, years of experience, qualification (CA(SA), CIMA, ACCA, degree, other), CV upload (PDF, up to 5 MB), consent to keep data for 12 months |
| Make an introduction form | Lets supporters pass on a contact | Your name and email, contact's name, company and role, how you know them, consent that the contact may be approached |
| Register-interest form | Collects interest for services not yet launched | Name, work email, company, service |
| Calendar booking (optional) | Lets qualified leads pick a time after submitting | Link to Calendly or Cal.com on the thank-you page |
| Lead routing | Forms deliver to a shared inbox and a simple CRM | Monday.com (already budgeted), through its form or email integration, or a webhook |
| Analytics | Measures the goals | A privacy-friendly tool (Plausible, or GA4 with consent mode), with an event for each form submission and each Book a pilot call click |
| Spam protection | Keeps forms clean without a visible CAPTCHA puzzle | Cloudflare Turnstile or a honeypot field |

The site does not need user accounts, payments or a blog at launch. An Insights section can be added later.

## Technical requirements

**Recommended stack** (you may propose an alternative, with reasons):

- **Framework:** Next.js (current stable, App Router) with TypeScript, mostly statically generated. React versions of the design system components are in `/design-system/components/react`.
- **Styling:** `/design-system/tokens.css` is the single source of CSS custom properties. Use CSS Modules or Tailwind mapped to those variables. Never hard-code a colour or size.
- **Content:** page copy in Markdown or MDX files in the repo, so copy changes don't need code changes.
- **Forms:** server-side route handlers that validate input, send email through Resend or Postmark, and post to Monday.com. Store CVs in private object storage, never in a public folder. Keep secrets in environment variables, and provide an `.env.example`.
- **Hosting:** Vercel or Netlify, with a global CDN for UK, US, Israel and SA visitors, and preview deployments for every change.

**Domain (GoDaddy):** the domain stays registered at GoDaddy and is pointed at the host. Use an A record for the root and a CNAME for `www`, per the host's instructions. Before changing DNS, record the existing MX and TXT records so business email is not broken. Add SPF, DKIM and DMARC records for the address the forms send from. Write these steps up for Dean in `docs/DEPLOY.md`.

**Performance:** a Lighthouse score of 90 or more on mobile for every page, images in AVIF or WebP with set dimensions, fonts loaded with `display=swap`, and no heavy animation libraries.

**SEO:** a unique title and description per page, Open Graph images in the brand style, `sitemap.xml`, `robots.txt`, schema.org Organization markup, and `en-GB` spelling throughout.

**Accessibility:** WCAG 2.2 AA. That means semantic headings, keyboard access to every control, the design system's focus ring, form labels and error messages, alt text, and support for reduced motion.

**Security:** HTTPS only, security headers (CSP, HSTS), rate-limited forms and no secrets in the client bundle.

## Legal and compliance

The site collects personal data from people in several countries, so it must meet South Africa's POPIA and the UK and EU GDPR from day one. A South African privacy lawyer will review the final wording.

- **Privacy notice:** who Sling is, what each form collects, why, how long it is kept, where it is stored (including any transfer outside South Africa), and how to ask for access or deletion. Name Sling's registered Information Officer.
- **Consent:** each form has an unticked consent box linked to the privacy notice. The talent pool states the 12-month retention period.
- **Cookies:** no non-essential cookies before consent. With a cookieless analytics tool, the cookie banner can be avoided entirely.
- **PAIA manual:** published at `/paia`.
- **Company details:** registered name, registration number and address in the footer, once the company exists (use placeholders until then).
- **Claims:** savings figures are shown as indicative ranges with a caveat, and third-party statistics keep their source lines.

## Risks, open decisions and content needed

**Risks**

- **The name "Sling" is crowded.** Sling by Toast (getsling.com) sells employee scheduling, and there is also Sling TV and Sling Money. Dean is checking trademarks, so keep the brand name easy to change (one constant for the name, no hard-coded domain).
- **SA–Israel politics.** Keep territory-specific content on client pages and out of careers content.
- **Claims without proof.** Until the pilot reports, keep savings and quality claims as indicative targets.

**Open decisions** (use placeholders and flag them in `docs/OPEN-ITEMS.md`)

- Domain: which .com to buy at GoDaddy
- Hero headline (three options above)
- Whether to name Martin and Dean on the About page at launch
- Whether Israel gets its own page now or later
- Analytics tool: Plausible (cookieless) or GA4 with consent

**Content still needed from Dean**

- Company registration details and Information Officer name
- Final role list and systems for Finance and accounting
- Team photos, or a photo shoot booked
- Contact email address and office location
- Privacy notice and PAIA manual from a lawyer

## Build plan

Build in four passes, and stop for Dean's review after each one, with a preview deployment where possible.

1. **Foundations:** project set-up, tokens, fonts, logo, favicon, header and footer, and the five components, all shown on one `/styleguide` page.
2. **Core pages:** Home, How it works, Services (Finance and accounting) and Contact, with a working Book a pilot call form.
3. **Audience pages:** Careers with the talent pool form, Supporters, About, Security, and the two "coming next" service pages.
4. **Launch:** legal pages, SEO, analytics, accessibility and performance checks, and `docs/DEPLOY.md` covering DNS from GoDaddy to the host.
