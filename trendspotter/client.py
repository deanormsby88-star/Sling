"""Client-facing PDF of the weekly report, in Just Imagine Consulting's look.

What goes in, and what stays out:
- Only positive, forward-looking material: trends, why they fit ages 5-9, when they should
  peak in South Africa, upcoming entertainment releases and key retail dates.
- Left out: red-flagged trends, risk alerts, recalls and safety notes, anything about
  sourcing, factories, prices paid, margins, imports, freight, quotes, samples or testing,
  the internal scores for sourcing, margin and runway, next steps, data gaps and the
  SA market pulse (exchange rate, port delays).

The client's name and logo are passed in at build time and never stored in this
repository, which is public.
"""

from __future__ import annotations

import base64
import mimetypes
import re
from datetime import date
from html import escape
from pathlib import Path

import calendar_events
import scoring
from models import Report, Trend

HERE = Path(__file__).parent

# Client "trend strength" uses only the demand-side factors, so nothing about our
# sourcing or margins can be read back from it.
CLIENT_WEIGHTS = {"velocity": 20, "cross_platform": 20, "age_fit": 15, "longevity": 10}
LABELS = [(70, "Hot now", "hot"), (50, "Rising", "rising"), (35, "On the radar", "radar")]

NEGATIVE = re.compile(
    r"recall|warn|counterfeit|fake|lookalike|look-alike|knock-?off|injur|burn|lawsuit|class action|"
    r"\bban|hazard|unsafe|\brisk|complain|chok|water bead|magnet|batter|seiz|raid|declin|\bfell\b|"
    r"\bfall|\bdrop|crash|slump|\bdown\b|weak|delay|congest|shortage|restrict|red flag|\bfad\b|"
    r"lower than|slow|criticis|controvers|negative|problem|concern|dried out|mixed|clearance|matur|fading|\bfade|"
    r"peaked|no spike|no new|no fresh|no separate|quiet|flat\b|stall|cool(ing|ed)|saturat|discount|markdown|"
    r"too close|too late|uncertain|unclear|not found|unknown",
    re.I,
)
SENSITIVE = re.compile(
    r"factor(y|ies)|1688|alibaba|temu|aliexpress|\bmoq|supplier|sourc|import|\bduty|freight|quote|"
    r"sample|sans\b|sans 8124|\btest|nrcs|margin|landed|distributor|allocation|wholesale|\bstock|"
    r"\border|just imagine|dean|our range|we should|request",
    re.I,
)
INTERNAL_CALENDAR = re.compile(r"order|ship|freeze|flag|durban|stock|canton|congest", re.I)


def _clean(text: str) -> str:
    """Keep only sentences with no negative or sensitive content."""
    parts = re.split(r"(?<=[.;])\s+", (text or "").strip())
    # Keep the positive half of "X, but Y" sentences.
    parts = [re.split(r",?\s+but\s+|,?\s+although\s+|,?\s+though\s+|,?\s+however\b", p, maxsplit=1, flags=re.I)[0] for p in parts]
    kept = [p for p in parts if p and not NEGATIVE.search(p) and not SENSITIVE.search(p)]
    out = " ".join(kept).strip()
    return out.rstrip(";") + ("" if not out or out.endswith(".") else ".")


def _ok(text: str) -> bool:
    return bool(text) and not NEGATIVE.search(text) and not SENSITIVE.search(text)


def strength(t: Trend) -> int:
    s = t.scores.model_dump()
    total = sum(max(0, min(5, s[f])) / 5 * w for f, w in CLIENT_WEIGHTS.items())
    return round(total / sum(CLIENT_WEIGHTS.values()) * 100)


def label(value: int) -> tuple[str, str] | None:
    for floor, name, cls in LABELS:
        if value >= floor:
            return name, cls
    return None


def client_trends(report: Report) -> list[tuple[Trend, int, str, str]]:
    out = []
    for t in report.trends:
        if t.safety_recall_active or t.only_ip_lookalikes_sourceable or t.ip_status == "proprietary":
            continue
        if scoring.band(t, scoring.total_score(t))[0] == "RED FLAG":
            continue
        v = strength(t)
        lab = label(v)
        if lab:
            out.append((t, v, *lab))
    return sorted(out, key=lambda x: -x[1])


def _data_uri(path: str | Path) -> str:
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def _blocks(value: int) -> str:
    filled = max(1, round(value / 20))
    cells = "".join(f'<i class="{"on" if i < filled else ""}"></i>' for i in range(5))
    return f'<span class="blocks" aria-label="Trend strength {value} out of 100">{cells}</span>'


def _peak(t: Trend) -> str:
    return t.projected_sa_peak if t.projected_sa_peak and t.projected_sa_peak.lower() != "unknown" else "To be confirmed"


CSS = """
/* Layout: A4 portrait. Logo-led cover band, then trend cards in a two-column grid, then reference lists. */
:root {
  --ink: #141414; --orange: #f58220; --red: #e2231a; --yellow: #ffd200;
  --paper: #ffffff; --mist: #f3f3f1; --muted: #5d5d5a; --line: #e1e1dd;
  --display: "Inter", "Helvetica Neue", Arial, sans-serif;
  --body: "Inter", "Helvetica Neue", Arial, sans-serif;
}
@page { size: A4; margin: 14mm 14mm 18mm }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact }
html, body { margin: 0; background: var(--paper); color: var(--ink); font: 9.6pt/1.45 var(--body) }
h1, h2, h3 { font-family: var(--display); margin: 0; text-wrap: balance }
.cover { display: grid; grid-template-columns: 1fr auto; align-items: start; gap: 8mm; padding-bottom: 6mm; border-bottom: 3px solid var(--ink) }
.cover .ji { height: 26mm }
.prepared { text-align: right; display: grid; gap: 2mm; justify-items: end }
.prepared small { font: 600 7.5pt var(--body); letter-spacing: .12em; text-transform: uppercase; color: var(--muted) }
.prepared img { height: 20mm }
.title { margin: 8mm 0 3mm; display: grid; gap: 1mm }
.title h1 { font-size: 34pt; line-height: .95; font-weight: 900; letter-spacing: -.01em; text-transform: uppercase }
.title h1 em { font-style: normal; color: var(--orange) }
.title p { margin: 2mm 0 0; font: 600 10pt var(--body); color: var(--muted) }
.squares { display: inline-flex; gap: 1.6mm; vertical-align: middle; margin-right: 2.5mm }
.squares i { width: 3.2mm; height: 3.2mm; border: .5mm solid var(--ink); border-radius: .6mm; display: block }
.squares i:nth-child(1) { background: var(--red) } .squares i:nth-child(2) { background: var(--yellow) } .squares i:nth-child(3) { background: var(--orange) }
.brief { display: grid; grid-template-columns: 1fr auto; gap: 8mm; align-items: center; background: var(--mist); border-left: 2mm solid var(--orange); padding: 5mm 6mm; margin: 5mm 0 2mm }
.brief p { margin: 0; font-size: 11pt; line-height: 1.45; max-width: 120mm }
.stats { display: flex; gap: 6mm }
.stat { text-align: center } .stat b { display: block; font: 900 22pt/1 var(--display) }
.stat span { font: 600 7pt var(--body); text-transform: uppercase; letter-spacing: .1em; color: var(--muted) }
section { margin-top: 8mm }
h2 { font-size: 14pt; font-weight: 900; text-transform: uppercase; letter-spacing: .02em; display: flex; align-items: center; margin-bottom: 4mm }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm }
.card { border: .35mm solid var(--line); border-radius: 2mm; padding: 4mm 4.5mm; break-inside: avoid; display: grid; gap: 2mm; align-content: start }
.card-head { display: flex; justify-content: space-between; gap: 3mm; align-items: start }
.card h3 { font-size: 11.5pt; font-weight: 800; line-height: 1.2 }
.chip { font: 800 6.8pt/1 var(--body); text-transform: uppercase; letter-spacing: .1em; padding: 1.4mm 2mm; border-radius: 1mm; white-space: nowrap }
.chip.hot { background: var(--orange); color: var(--ink) } .chip.rising { background: var(--yellow); color: var(--ink) } .chip.radar { background: var(--mist); color: var(--muted); border: .3mm solid var(--line) }
.blocks { display: inline-flex; gap: 1mm } .blocks i { width: 3mm; height: 3mm; border-radius: .5mm; border: .4mm solid var(--ink); background: var(--paper) }
.blocks i.on { background: var(--orange) }
.meter { display: flex; align-items: center; gap: 2mm; font: 700 7.5pt var(--body); color: var(--muted) }
.card p { margin: 0 }
.fit { color: var(--muted) }
.peak { font-weight: 700 } .peak span { color: var(--orange) }
.evidence { margin: 0; padding-left: 4mm; display: grid; gap: 1mm; font-size: 8.6pt }
.evidence b { font-weight: 700 }
table { width: 100%; border-collapse: collapse; font-size: 9pt }
th { text-align: left; font: 700 7pt var(--body); text-transform: uppercase; letter-spacing: .1em; color: var(--muted); padding: 2mm; border-bottom: .5mm solid var(--ink) }
td { padding: 2.2mm 2mm; border-bottom: .3mm solid var(--line); vertical-align: top }
tr { break-inside: avoid }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 8mm }
.list { margin: 0; padding: 0; list-style: none; display: grid; gap: 2mm }
.list li { display: grid; grid-template-columns: 26mm 1fr; gap: 3mm; break-inside: avoid }
.list time { font-weight: 800; color: var(--orange) }
.method { margin-top: 8mm; padding-top: 3mm; border-top: .3mm solid var(--line); color: var(--muted); font-size: 7.8pt; max-width: 170mm }
"""


def html(report: Report, today: date, client_name: str, client_logo: str | None, ji_logo: str) -> str:
    trends = client_trends(report)
    top = [x for x in trends if x[3] in ("hot", "rising")][:6]
    rest = [x for x in trends if x not in top]
    n_hot = sum(1 for x in trends if x[3] == "hot")
    n_rising = sum(1 for x in trends if x[3] == "rising")

    headline = _clean(report.headline)
    if not headline and top:
        headline = f"{top[0][0].name} leads this week's trends for children aged 5 to 9."

    def card(t: Trend, v: int, name: str, cls: str) -> str:
        ev = [e for e in t.evidence if _ok(e.finding) and _ok(e.source)][:3]
        ev_html = "".join(f"<li><b>{escape(e.source)}:</b> {escape(e.finding)}</li>" for e in ev)
        why, fit = _clean(t.why_now), _clean(t.age_fit_note)
        return f"""<article class="card">
  <div class="card-head"><h3>{escape(t.name)}</h3><span class="chip {cls}">{name}</span></div>
  <div class="meter">{_blocks(v)} Trend strength {v}/100</div>
  {f'<p>{escape(why)}</p>' if why else ''}
  {f'<p class="fit">{escape(fit)}</p>' if fit else ''}
  {f'<ul class="evidence">{ev_html}</ul>' if ev_html else ''}
  <p class="peak">Expected SA peak: <span>{escape(_peak(t))}</span></p>
</article>"""

    rows = "".join(
        f"<tr><td><b>{escape(t.name)}</b></td><td><span class='chip {cls}'>{name}</span></td>"
        f"<td>{_blocks(v)}</td><td>{escape(_clean(t.why_now))}</td><td>{escape(_peak(t))}</td></tr>"
        for t, v, name, cls in rest)
    pipeline = [p for p in report.licensing_pipeline if _ok(p.item)]
    pipe_html = "".join(f"<li><time>{escape(p.date)}</time><span>{escape(p.item)}</span></li>" for p in pipeline[:8])
    cal = [(w, e) for w, e, _ in calendar_events.upcoming(today, days=90) if not INTERNAL_CALENDAR.search(e)]
    cal_html = "".join(f"<li><time>{escape(w)}</time><span>{escape(e)}</span></li>" for w, e in cal)
    client_img = f'<img src="{_data_uri(client_logo)}" alt="{escape(client_name)}">' if client_logo else f"<b>{escape(client_name)}</b>"
    sq = '<span class="squares"><i></i><i></i><i></i></span>'

    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<title>Kids' Toy Trends: {escape(client_name)} · {today.strftime('%d %B %Y')}</title><style>{CSS}</style></head><body>
<header class="cover">
  <img class="ji" src="{_data_uri(ji_logo)}" alt="Just Imagine Consulting">
  <div class="prepared"><small>Prepared for</small>{client_img}</div>
</header>
<div class="title">
  <h1>Kids' toy <em>trends</em></h1>
  <p>Ages 5 to 9 · South Africa · Week ending {today.strftime('%d %B %Y')}</p>
</div>
<div class="brief">
  <p>{escape(headline)}</p>
  <div class="stats">
    <div class="stat"><b>{n_hot}</b><span>Hot now</span></div>
    <div class="stat"><b>{n_rising}</b><span>Rising</span></div>
    <div class="stat"><b>{len(trends)}</b><span>Tracked</span></div>
  </div>
</div>

<section><h2>{sq}Top trends this week</h2>
<div class="cards">{"".join(card(*x) for x in top) or '<p>No trends reach Rising strength this week.</p>'}</div></section>

{f'''<section><h2>{sq}Also on the radar</h2>
<table><thead><tr><th>Trend</th><th>Status</th><th>Strength</th><th>Why it's worth watching</th><th>SA peak</th></tr></thead>
<tbody>{rows}</tbody></table></section>''' if rows else ''}

<div class="two">
{f'<section><h2>{sq}Coming up on screen</h2><ul class="list">{pipe_html}</ul></section>' if pipe_html else ''}
{f'<section><h2>{sq}Key dates</h2><ul class="list">{cal_html}</ul></section>' if cal_html else ''}
</div>

<p class="method">How we track trends: each week we review social video, search interest, online bestseller charts,
retailer lists and trade news across South Africa, the US and the UK. Trend strength combines momentum, how many
independent channels confirm the trend, fit for children aged 5 to 9, and staying power. Expected SA peaks are
estimates based on how trends have spread from the US and Asia to South Africa in the past.</p>
</body></html>"""
