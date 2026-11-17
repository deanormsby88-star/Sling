"""Render the daily report as an HTML email (inline styles) and a plain-text version."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from html import escape

import config
from models import Report, Trend

STALE = ' <span style="color:#999">(no new data)</span>'
BAND_COLOURS = {"ACT": "#0a7d3b", "PREPARE": "#1f5fa8", "WATCH": "#8a6d00", "IGNORE": "#777777", "RED FLAG": "#b00020"}


@dataclass
class Scored:
    trend: Trend
    score: int
    band: str
    band_reason: str
    since_last: int | None  # change since the previous report; None = new
    change_7d: int | None


def _fmt_delta(d: int | None, new_label: str = "new") -> str:
    if d is None:
        return new_label
    return f"+{d}" if d > 0 else str(d)


def rising(scored: list[Scored]) -> list[Scored]:
    up = [s for s in scored if s.band != "RED FLAG" and s.trend.seen_today and (
        s.since_last is None or s.since_last > config.RISING_THRESHOLD)]
    return sorted(up, key=lambda s: (s.since_last is not None, -(s.since_last or 0), -s.score))[:5]


def _link(text: str, url: str) -> str:
    return f'<a href="{escape(url)}" style="color:#1f5fa8">{escape(text)}</a>' if url else escape(text)


def _badge(band: str) -> str:
    return (f'<span style="background:{BAND_COLOURS[band]};color:#fff;padding:1px 6px;border-radius:3px;'
            f'font-size:11px;font-weight:bold">{band}</span>')


def _h2(title: str) -> str:
    return f'<h2 style="font-size:16px;margin:24px 0 8px;border-bottom:2px solid #ddd;padding-bottom:4px">{title}</h2>'


def _trend_card(s: Scored) -> str:
    t = s.trend
    ev = "".join(f"<li>{escape(e.source)}: {_link(e.finding, e.url)}</li>" for e in t.evidence[:3])
    note = f"<br><em>{escape(s.band_reason)}</em>" if s.band_reason else ""
    return f"""<div style="border:1px solid #ddd;border-radius:4px;padding:10px 12px;margin:8px 0">
<strong>{escape(t.name)}</strong> {_badge(s.band)} <strong>{s.score}</strong>/100 ({_fmt_delta(s.since_last)} since last report){note}
<p style="margin:6px 0"><strong>Why now:</strong> {escape(t.why_now)}</p>
<ul style="margin:4px 0 4px 18px;padding:0">{ev}</ul>
<p style="margin:4px 0"><strong>5-9 fit:</strong> {escape(t.age_fit_note)}<br>
<strong>Sourcing:</strong> {escape(t.ip_status)}; {escape(t.sourcing_route)}<br>
<strong>Projected SA peak:</strong> {escape(t.projected_sa_peak)}<br>
<strong>Next step:</strong> {escape(t.next_step)}</p></div>"""


def html(report: Report, scored: list[Scored], today: date, mode: str,
         calendar: list[tuple[str, str, str]], health: dict[str, str]) -> str:
    act = [s for s in scored if s.band == "ACT"]
    prep = [s for s in scored if s.band == "PREPARE"]
    flagged = [s for s in scored if s.band == "RED FLAG"]
    parts = [f"""<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.45;color:#222;max-width:760px">
<h1 style="font-size:20px;margin:0 0 4px">{escape(config.REPORT_NAME.upper())}: {today.strftime('%A %d %B %Y')}</h1>
<p style="color:#666;margin:0 0 12px">{mode.capitalize()} report. Ages 5-9, South Africa.</p>
<p style="font-size:16px;background:#f4f4f4;padding:10px 12px;border-left:4px solid #222">{escape(report.headline)}</p>"""]

    parts.append(_h2("Act now (score 75+)"))
    parts.append("".join(_trend_card(s) for s in act) or "<p>Nothing at ACT today.</p>")
    if prep:
        parts.append(_h2("Prepare (55-74): get quotes, line up a test lab"))
        parts.append("".join(_trend_card(s) for s in prep))

    parts.append(_h2(f"Rising (new or up more than {config.RISING_THRESHOLD} points)"))
    rows = rising(scored)
    parts.append("<ul>" + "".join(
        f"<li><strong>{escape(s.trend.name)}</strong> {_badge(s.band)} {s.score} ({_fmt_delta(s.since_last)}): "
        f"{escape(s.trend.why_now)}" + (f" Source: {_link(s.trend.evidence[0].source, s.trend.evidence[0].url)}" if s.trend.evidence else "")
        + "</li>" for s in rows) + "</ul>" if rows else "<p>No new or fast-rising trends today.</p>")

    parts.append(_h2("Watchlist movement"))
    th = 'style="text-align:left;padding:4px 6px;background:#f4f4f4;font-size:12px"'
    td = 'style="padding:4px 6px;border-top:1px solid #eee;font-size:12px;vertical-align:top"'
    head = "".join(f"<th {th}>{h}</th>" for h in ["Trend", "Band", "Score", "7-day", "TikTok", "Google Trends", "Amazon", "Takealot"])
    body = "".join(
        f"<tr><td {td}>{escape(s.trend.name)}{'' if s.trend.seen_today else STALE}</td>"
        f"<td {td}>{_badge(s.band)}</td><td {td}><strong>{s.score}</strong></td><td {td}>{_fmt_delta(s.change_7d, 'n/a')}</td>"
        f"<td {td}>{escape(s.trend.tiktok_change)}</td><td {td}>{escape(s.trend.google_trends_change)}</td>"
        f"<td {td}>{escape(s.trend.amazon_rank_change)}</td><td {td}>{escape(s.trend.takealot_status)}</td></tr>"
        for s in scored)
    parts.append(f'<table style="border-collapse:collapse;width:100%">{"<tr>" + head + "</tr>"}{body}</table>')

    parts.append(_h2("Licensing and entertainment pipeline"))
    parts.append("<ul>" + "".join(
        f"<li><strong>{_link(p.item, p.url)}</strong> ({escape(p.date)}): {escape(p.note)}</li>"
        for p in report.licensing_pipeline) + "</ul>" if report.licensing_pipeline else "<p>No new deals or releases found today.</p>")

    parts.append(_h2("SA market pulse"))
    parts.append("<ul>" + "".join(f"<li>{escape(x)}</li>" for x in report.sa_market_pulse) + "</ul>"
                 if report.sa_market_pulse else "<p>No SA movements found today.</p>")

    parts.append(_h2("Risk alerts"))
    risk = [f"<li>{_link(a.alert, a.url)}</li>" for a in report.risk_alerts]
    risk += [f"<li><strong>{escape(s.trend.name)}</strong>: red flag ({escape(s.band_reason)}). Do not stock.</li>" for s in flagged]
    parts.append("<ul>" + "".join(risk) + "</ul>" if risk else "<p>No new risk alerts.</p>")

    parts.append(_h2("Calendar: next 60 days"))
    parts.append("<ul>" + "".join(
        f"<li><strong>{escape(w)}</strong>: {escape(e)}{(' ' + chr(8212) + ' ' + escape(n)) if n else ''}</li>"
        for w, e, n in calendar) + "</ul>" if calendar else "<p>Nothing in the next 60 days.</p>")

    ok = [k for k, v in health.items() if v.startswith("ok")]
    bad = [f"{k} ({v})" for k, v in health.items() if not v.startswith("ok")]
    gaps = "".join(f"<li>{escape(g)}</li>" for g in report.data_gaps)
    parts.append(f"""<div style="margin-top:28px;padding-top:8px;border-top:1px solid #ddd;color:#777;font-size:12px">
<p><strong>Scoring:</strong> velocity 20, cross-platform 20, 5-9 fit 15, sourcing and IP 15, SA runway 10, margin 10, longevity 10.
75+ ACT, 55-74 PREPARE, 35-54 WATCH, under 35 IGNORE. ACT also needs the projected SA peak at least
{config.MIN_MONTHS_TO_SA_PEAK_FOR_ACT} months away. Safety recalls and IP-lookalike-only trends are red-flagged whatever the score.
Keep a human review step for anything at ACT.</p>
<p><strong>Feeds working:</strong> {escape(', '.join(ok)) or 'none'}<br>
<strong>Feeds failing:</strong> {escape(', '.join(bad)) or 'none'}</p>
{'<p><strong>Not checked today:</strong></p><ul>' + gaps + '</ul>' if gaps else ''}
</div></div>""")
    return "\n".join(parts)


def text(report: Report, scored: list[Scored], today: date) -> str:
    lines = [f"{config.REPORT_NAME.upper()}: {today.strftime('%d %B %Y')}", "", report.headline, ""]
    for label in ("ACT", "PREPARE", "WATCH", "RED FLAG"):
        group = [s for s in scored if s.band == label]
        if group:
            lines.append(label)
            lines += [f"  {s.score:>3}  {s.trend.name} ({_fmt_delta(s.since_last)}): {s.trend.next_step}" for s in group]
            lines.append("")
    lines.append("Open the HTML version for evidence, pipeline, SA pulse, risks and calendar.")
    return "\n".join(lines)
