"""Render the weekly report as a self-contained artifact page (HTML + inline CSS, no JS)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from html import escape

import config
from models import Report, Trend

BAND_TOKEN = {"ACT": "act", "PREPARE": "prepare", "WATCH": "watch", "IGNORE": "ignore", "RED FLAG": "flag"}
BAND_NOTE = {
    "ACT": "Request samples now",
    "PREPARE": "Get quotes, line up a test lab",
    "WATCH": "Keep watching",
    "IGNORE": "Not worth tracking",
    "RED FLAG": "Do not stock",
}


@dataclass
class Scored:
    trend: Trend
    score: int
    band: str
    band_reason: str
    since_last: int | None  # change since last week's report; None = new
    change_4w: int | None
    history: list[int] = field(default_factory=list)


def _note(text: str) -> str:
    return f'<br><span class="muted">{escape(text)}</span>' if text else ""


NO_NEW_DATA = "<br><span class='muted small'>no new data this week</span>"


def _delta(d: int | None, none_label: str = "new") -> str:
    if d is None:
        return f'<span class="delta new">{none_label}</span>'
    cls = "up" if d > 0 else "down" if d < 0 else "flat"
    txt = f"+{d}" if d > 0 else ("±0" if d == 0 else f"−{abs(d)}")
    return f'<span class="delta {cls}">{txt}</span>'


def _link(text: str, url: str) -> str:
    if url and url.startswith(("http://", "https://")):
        return f'<a href="{escape(url)}" target="_blank" rel="noopener">{escape(text)}</a>'
    return escape(text)


def _badge(band: str) -> str:
    return f'<span class="badge b-{BAND_TOKEN[band]}">{band}</span>'


def _spark(values: list[int]) -> str:
    if len(values) < 2:
        return '<span class="muted small">first week</span>'
    w, h, pad = 84, 24, 3
    step = (w - 2 * pad) / (len(values) - 1)
    pts = [(pad + i * step, h - pad - v / 100 * (h - 2 * pad)) for i, v in enumerate(values)]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ex, ey = pts[-1]
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="Score over the last {len(values)} weeks: {", ".join(map(str, values))}">'
            f'<line x1="0" x2="{w}" y1="{h - pad - 0.75 * (h - 2 * pad):.1f}" y2="{h - pad - 0.75 * (h - 2 * pad):.1f}" class="spark-75"/>'
            f'<polyline points="{path}" fill="none" class="spark-line"/>'
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="2.4" class="spark-dot"/></svg>')


def _factors(t: Trend) -> str:
    s = t.scores.model_dump()
    cells = []
    for f, wgt in config.WEIGHTS.items():
        v = max(0, min(5, s[f]))
        cells.append(
            f'<div class="factor" title="{config.FACTOR_LABELS[f]}: {v}/5 (weight {wgt})">'
            f'<div class="factor-bar"><span style="width:{v * 20}%"></span></div>'
            f'<div class="factor-label">{config.FACTOR_LABELS[f]} <b>{v}</b></div></div>')
    return f'<div class="factors" aria-label="Factor scores out of 5">{"".join(cells)}</div>'


def _runway(t: Trend) -> str:
    m = t.months_to_sa_peak
    if m < 0:
        return f'<p class="runway warn">Projected SA peak: {escape(t.projected_sa_peak)}. Timing unknown, so confirm runway before ordering.</p>'
    weeks = round(m * 4.33)
    ok = m >= config.MIN_MONTHS_TO_SA_PEAK_FOR_ACT
    verdict = ("enough time for a 10-16 week import" if ok
               else "too close for a 10-16 week import from China")
    return (f'<p class="runway {"ok" if ok else "warn"}">Projected SA peak <b>{escape(t.projected_sa_peak)}</b>, '
            f'about {weeks} weeks away: {verdict}.</p>')


def _card(s: Scored) -> str:
    t = s.trend
    ev = "".join(f"<li><span class=\"src\">{escape(e.source)}</span> {_link(e.finding, e.url)}</li>" for e in t.evidence[:5])
    reason = f'<p class="reason">{escape(s.band_reason)}</p>' if s.band_reason else ""
    return f"""<article class="card c-{BAND_TOKEN[s.band]}">
  <header class="card-head">
    <h3>{escape(t.name)}</h3>
    <div class="score"><span class="num">{s.score}</span><span class="of">/100</span> {_delta(s.since_last)}</div>
  </header>
  <div class="meta">{_badge(s.band)} <span class="chip">{escape(t.ip_status)}</span></div>
  {reason}
  <p class="why">{escape(t.why_now)}</p>
  {_factors(t)}
  <ul class="evidence">{ev}</ul>
  <dl class="facts">
    <div><dt>5-9 fit</dt><dd>{escape(t.age_fit_note)}</dd></div>
    <div><dt>Sourcing</dt><dd>{escape(t.sourcing_route)}</dd></div>
    <div><dt>Next step</dt><dd>{escape(t.next_step)}</dd></div>
  </dl>
  {_runway(t)}
</article>"""


def rising(scored: list[Scored]) -> list[Scored]:
    up = [s for s in scored if s.band != "RED FLAG" and s.trend.seen_today and (
        s.since_last is None or s.since_last > config.RISING_THRESHOLD)]
    return sorted(up, key=lambda s: (s.since_last is not None, -(s.since_last or 0), -s.score))[:5]


CSS = """
/* Layout: one reading column; band-coloured trend cards up top, then the watchlist table, then reference sections. */
:root {
  --bg: #f6f6f9; --surface: #ffffff; --fg: #1a1b26; --muted: #5c5f73; --line: #e2e3eb;
  --accent: #4a3ad0; --act: #0d7a45; --prepare: #1d62b3; --watch: #9a6200; --ignore: #73768a; --flag: #bf2530;
  --display: "Bricolage Grotesque", "Inter", system-ui, sans-serif;
  --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #12131a; --surface: #1b1c26; --fg: #ecedf3; --muted: #a3a6b9; --line: #2d2f3e;
  --accent: #a99cff; --act: #46c488; --prepare: #6ea7f0; --watch: #e2ad48; --ignore: #8f92a5; --flag: #f06b72; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #12131a; --surface: #1b1c26; --fg: #ecedf3; --muted: #a3a6b9; --line: #2d2f3e;
  --accent: #a99cff; --act: #46c488; --prepare: #6ea7f0; --watch: #e2ad48; --ignore: #8f92a5; --flag: #f06b72; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }
.wrap { max-width: 980px; margin: 0 auto; padding-block: 28px 56px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
a { color: var(--accent); text-underline-offset: 2px }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px }
h1, h2, h3 { font-family: var(--display); text-wrap: balance; margin: 0 }
.eyebrow { font: 600 12px/1 var(--body); letter-spacing: .08em; text-transform: uppercase; color: var(--muted) }
.masthead { display: grid; gap: 10px; margin-bottom: 22px }
.masthead h1 { font-size: clamp(28px, 5vw, 40px); font-weight: 700; letter-spacing: -.01em }
.headline { font-size: 18px; line-height: 1.5; margin: 6px 0 0; max-width: 68ch; border-left: 3px solid var(--accent); padding-left: 14px }
.tally { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 8px }
.tally span { font: 600 13px/1 var(--body); padding: 7px 10px; border-radius: 999px; background: var(--surface); border: 1px solid var(--line) }
.tally b { font-family: var(--mono); margin-right: 4px }
section { margin-top: 38px }
section > h2 { font-size: 21px; font-weight: 650; display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; margin-bottom: 14px }
section > h2 small { font: 400 14px var(--body); color: var(--muted) }
.cards { display: grid; gap: 14px }
.card { background: var(--surface); border: 1px solid var(--line); border-top: 4px solid var(--band); border-radius: 10px; padding: 16px 18px; display: grid; gap: 10px; min-width: 0 }
.c-act { --band: var(--act) } .c-prepare { --band: var(--prepare) } .c-watch { --band: var(--watch) } .c-ignore { --band: var(--ignore) } .c-flag { --band: var(--flag) }
.card-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap }
.card-head h3 { font-size: 19px; font-weight: 650 }
.score { font-family: var(--mono); white-space: nowrap }
.score .num { font-size: 26px; font-weight: 700 } .score .of { color: var(--muted); font-size: 13px; margin-right: 6px }
.meta { display: flex; gap: 6px; flex-wrap: wrap }
.badge, .chip { white-space: nowrap; font: 700 11px/1 var(--body); letter-spacing: .06em; padding: 5px 8px; border-radius: 4px }
.chip { font-weight: 600; text-transform: capitalize; letter-spacing: .02em; color: var(--muted); border: 1px solid var(--line) }
.b-act { color: var(--act); background: color-mix(in srgb, var(--act) 14%, transparent) }
.b-prepare { color: var(--prepare); background: color-mix(in srgb, var(--prepare) 14%, transparent) }
.b-watch { color: var(--watch); background: color-mix(in srgb, var(--watch) 16%, transparent) }
.b-ignore { color: var(--ignore); background: color-mix(in srgb, var(--ignore) 16%, transparent) }
.b-flag { color: var(--flag); background: color-mix(in srgb, var(--flag) 14%, transparent) }
.why { margin: 0; max-width: 70ch } .reason { margin: 0; font-style: italic; color: var(--muted) }
.factors { display: grid; grid-template-columns: repeat(auto-fill, minmax(118px, 1fr)); gap: 8px 10px }
.factor { min-width: 0 } .factor-bar { height: 6px; border-radius: 3px; background: var(--line); overflow: hidden }
.factor-bar span { display: block; height: 100%; background: var(--band) }
.factor-label { font-size: 11.5px; color: var(--muted); margin-top: 3px } .factor-label b { color: var(--fg); font-family: var(--mono) }
.evidence { margin: 0; padding-left: 18px; display: grid; gap: 4px }
.src { font-weight: 600; margin-right: 4px } .src::after { content: ":" }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px 18px; margin: 0 }
.facts dt { font: 600 11px/1.4 var(--body); text-transform: uppercase; letter-spacing: .07em; color: var(--muted) }
.facts dd { margin: 0 }
.runway { margin: 0; font-size: 13.5px; padding: 8px 10px; border-radius: 6px; background: color-mix(in srgb, var(--fg) 4%, transparent) }
.runway.ok::before { content: "On time. "; font-weight: 700; color: var(--act) }
.runway.warn::before { content: "Tight. "; font-weight: 700; color: var(--watch) }
.delta { font: 600 13px var(--mono) } .up { color: var(--act) } .down { color: var(--flag) } .flat, .new { color: var(--muted) }
.list { margin: 0; padding-left: 18px; display: grid; gap: 8px; max-width: 76ch }
.table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--surface) }
table { border-collapse: collapse; width: 100%; min-width: 820px; font-size: 13.5px }
th { text-align: left; font: 600 11px/1.3 var(--body); text-transform: uppercase; letter-spacing: .07em; color: var(--muted); padding: 10px; border-bottom: 1px solid var(--line) }
td { padding: 9px 10px; border-top: 1px solid var(--line); vertical-align: top }
tr:first-child td { border-top: 0 }
td.n { font-family: var(--mono); font-weight: 700; font-variant-numeric: tabular-nums }
.muted { color: var(--muted) } .small { font-size: 12px }
.spark-line { stroke: var(--accent); stroke-width: 1.6 } .spark-dot { fill: var(--accent) } .spark-75 { stroke: var(--line); stroke-dasharray: 2 2 }
.cal { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none }
.cal li { display: grid; grid-template-columns: 110px 1fr; gap: 12px }
.cal time { font: 600 13px var(--mono); color: var(--muted) }
.cols { margin-top: 38px; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px }
.cols section { margin-top: 0 }
footer { margin-top: 44px; padding-top: 16px; border-top: 1px solid var(--line); color: var(--muted); font-size: 13px; display: grid; gap: 10px }
footer p { margin: 0; max-width: 80ch }
@media (max-width: 520px) { .cal li { grid-template-columns: 1fr; gap: 0 } }
"""


def page(report: Report, scored: list[Scored], today: date, mode: str,
         calendar: list[tuple[str, str, str]], archive: list[dict], state_script: str) -> str:
    groups = {b: [s for s in scored if s.band == b] for b in BAND_TOKEN}
    tally = "".join(f'<span><b>{len(groups[b])}</b>{b.title() if b != "RED FLAG" else "Red flag"}</span>' for b in BAND_TOKEN)

    def cards(band: str) -> str:
        return "".join(_card(s) for s in groups[band])

    act = cards("ACT") or '<p class="muted">Nothing scores 75 or more with enough runway this week.</p>'
    prepare = (f'<section><h2>Prepare <small>55-74: {BAND_NOTE["PREPARE"].lower()}</small></h2><div class="cards">{cards("PREPARE")}</div></section>'
               if groups["PREPARE"] else "")

    rows = rising(scored)
    rising_html = ('<ul class="list">' + "".join(
        f'<li><b>{escape(s.trend.name)}</b> {_badge(s.band)} <span class="delta">{s.score}</span> {_delta(s.since_last)}: {escape(s.trend.why_now)}</li>'
        for s in rows) + "</ul>") if rows else '<p class="muted">No new or fast-rising trends this week.</p>'

    body_rows = "".join(
        f'<tr><td><b>{escape(s.trend.name)}</b>{"" if s.trend.seen_today else NO_NEW_DATA}</td>'
        f'<td>{_badge(s.band)}</td><td class="n">{s.score}</td><td>{_delta(s.since_last)}</td><td>{_delta(s.change_4w, "n/a")}</td>'
        f'<td>{_spark(s.history)}</td><td>{escape(s.trend.tiktok_change)}</td><td>{escape(s.trend.google_trends_change)}</td>'
        f'<td>{escape(s.trend.amazon_rank_change)}</td><td>{escape(s.trend.takealot_status)}</td></tr>'
        for s in scored)

    pipeline = ('<ul class="list">' + "".join(
        f'<li><b>{_link(p.item, p.url)}</b> <span class="muted">({escape(p.date)})</span><br>{escape(p.note)}</li>'
        for p in report.licensing_pipeline) + "</ul>") if report.licensing_pipeline else '<p class="muted">No new deals or releases found this week.</p>'
    pulse = ('<ul class="list">' + "".join(f"<li>{escape(x)}</li>" for x in report.sa_market_pulse) + "</ul>"
             ) if report.sa_market_pulse else '<p class="muted">No SA movements found this week.</p>'
    risk_items = [f"<li>{_link(a.alert, a.url)}</li>" for a in report.risk_alerts]
    risk_items += [f"<li><b>{escape(s.trend.name)}</b>: {escape(s.band_reason)}. Do not stock.</li>" for s in groups["RED FLAG"]]
    risks = ('<ul class="list">' + "".join(risk_items) + "</ul>") if risk_items else '<p class="muted">No new risk alerts.</p>'
    cal = ('<ul class="cal">' + "".join(
        f'<li><time>{escape(w)}</time><span><b>{escape(e)}</b>{_note(n)}</span></li>'
        for w, e, n in calendar) + "</ul>") if calendar else '<p class="muted">Nothing in the next 60 days.</p>'
    gaps = ("<p><b>Not checked this week:</b> " + escape("; ".join(report.data_gaps)) + "</p>") if report.data_gaps else ""
    past = [a for a in archive if a["date"] != today.isoformat()][:8]
    past_html = ('<section><h2>Previous weeks</h2><ul class="cal">' + "".join(
        f'<li><time>{escape(date.fromisoformat(a["date"]).strftime("%d %b %Y"))}</time><span>{escape(a["headline"])}</span></li>'
        for a in past) + "</ul></section>") if past else ""
    sweep = " with the monthly sweep" if mode == "monthly" else ""

    return f"""<title>Just Imagine Trendspotter</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header class="masthead">
  <span class="eyebrow">Toy trends for ages 5-9 · South Africa · week ending {today.strftime('%a %d %b %Y')}{sweep}</span>
  <h1>{escape(config.REPORT_NAME)}</h1>
  <p class="headline">{escape(report.headline)}</p>
  <div class="tally">{tally}</div>
</header>

<section><h2>Act now <small>75+ and at least {config.MIN_MONTHS_TO_SA_PEAK_FOR_ACT} months to the SA peak: {BAND_NOTE["ACT"].lower()}</small></h2><div class="cards">{act}</div></section>
{prepare}
<section><h2>Rising <small>new, or up more than {config.RISING_THRESHOLD} points since last week</small></h2>{rising_html}</section>

<section><h2>Watchlist</h2>
<div class="table-wrap"><table>
<thead><tr><th>Trend</th><th>Band</th><th>Score</th><th>Week</th><th>4 weeks</th><th>Last 12 weeks</th><th>TikTok</th><th>Google Trends</th><th>Amazon</th><th>Takealot</th></tr></thead>
<tbody>{body_rows}</tbody></table></div></section>

<div class="cols">
<section><h2>Licensing and entertainment</h2>{pipeline}</section>
<section><h2>SA market pulse</h2>{pulse}</section>
</div>
<div class="cols">
<section><h2>Risk alerts</h2>{risks}</section>
<section><h2>Next 60 days</h2>{cal}</section>
</div>
{past_html}

<footer>
<p><b>How scores work.</b> Each trend is scored 0-5 on velocity (20), cross-platform confirmation (20), 5-9 age fit (15),
sourcing and IP freedom (15), SA runway (10), margin in the R100-R500 band (10) and longevity (10), out of 100.
75+ act, 55-74 prepare, 35-54 watch, under 35 ignore. Active safety recalls and trends where only an IP lookalike could be
sourced are red-flagged whatever the score. Anything at ACT still needs your review and a SANS 8124 test report.</p>
{gaps}
<p>Updated every Friday by a scheduled Claude task. TikTok, Google Trends and Amazon figures come from web search, so treat them as direction, not exact counts.</p>
</footer>
</div>
{state_script}
"""


def placeholder(first_run: date, calendar: list[tuple[str, str, str]], state: dict, state_script: str) -> str:
    """Page shown before the first weekly report has run."""
    seeds = "".join(
        f'<tr><td><b>{escape(n)}</b></td><td><span class="chip">{escape(e.get("ip", ""))}</span></td>'
        f'<td class="muted">{escape(", ".join(e.get("aliases", [])) or "none")}</td></tr>'
        for n, e in sorted(state["trends"].items()))
    cal = "".join(
        f"<li><time>{escape(w)}</time><span><b>{escape(e)}</b>" + (f"<br><span class='muted'>{escape(n)}</span>" if n else "") + "</span></li>"
        for w, e, n in calendar)
    return f"""<title>Just Imagine Trendspotter</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header class="masthead">
  <span class="eyebrow">Toy trends for ages 5-9 · South Africa · weekly</span>
  <h1>{escape(config.REPORT_NAME)}</h1>
  <p class="headline">The first report arrives on {first_run.strftime('%A %d %B %Y')}, and this page updates every Friday after that.</p>
</header>
<section><h2>Starting watchlist <small>re-scored each week, plus up to {config.MAX_NEW_CANDIDATES} new candidates</small></h2>
<div class="table-wrap"><table style="min-width:560px"><thead><tr><th>Trend</th><th>IP</th><th>Also tracked as</th></tr></thead><tbody>{seeds}</tbody></table></div></section>
<section><h2>Next 60 days</h2><ul class="cal">{cal}</ul></section>
<footer><p>Updated every Friday by a scheduled Claude task, following the Just Imagine trendspotter research brief.</p></footer>
</div>
{state_script}
"""
