"""Daily run: collect -> research -> structure -> score -> email.

Usage:
  python main.py                 # full run, sends the email
  python main.py --no-email      # full run, writes the report to out/ only
  python main.py --sample        # no API calls: renders a sample report to out/ (for checking the layout)
  python main.py --mode monthly  # force a cadence (default: weekly; the first Friday of the month = monthly)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import calendar_events
import config
import history
import render
import scoring
from models import Report

SAST = ZoneInfo("Africa/Johannesburg")
OUT = Path(__file__).parent / "out"


def pick_mode(today) -> str:
    """The report runs weekly; the first run of each month also does the monthly sweep."""
    return "monthly" if today.day <= 7 else "weekly"


def build_context(today, mode: str, state: dict, collected_text: str, calendar) -> str:
    sources = config.WEB_SOURCES["daily"] + (config.WEB_SOURCES["weekly"] if mode in ("weekly", "monthly") else [])
    if mode == "monthly":
        sources += config.WEB_SOURCES["monthly"]
    cal = "\n".join(f"- {w}: {e}" for w, e, _ in calendar) or "(none)"
    return f"""Today is {today.strftime('%A %d %B %Y')} (SAST). This is the {mode} run.

This is a once-a-week deep dive, so be thorough: check every source below, follow up promising leads with
web fetch, and confirm each trend on as many independent platforms as you can. Prioritise signals from the
last 7 days, and give 4-week context (direction of travel) where you can find it.

Research these sources with web search and web fetch:
{chr(10).join('- ' + s for s in sources)}

Current watchlist (re-check each one, then look for new candidates for ages 5-9):
{history.watchlist_text(state, today)}

Headlines from the last 8 days, collected automatically from trade RSS, Google News and Reddit (use as leads; verify what matters):
{collected_text}

SA calendar, next 60 days:
{cal}

Look actively for new candidate trends for ages 5-9 (up to {config.MAX_NEW_CANDIDATES}), not just the watchlist.

Write research notes covering, for each watchlist item and each new candidate: the signals you found with numbers,
dates and URLs (TikTok, Google Trends ZA/US/UK, Amazon, Takealot, YouTube, trade press, retailers), the 5-9 age fit,
IP status and sourcing route, projected SA peak, and safety or counterfeit issues. Then notes on the licensing and
entertainment pipeline, SA market pulse (retailers, Durban port and freight, ZAR), and risk alerts. Finish with a list
of sources you could not check and why."""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["daily", "weekly", "monthly"])
    ap.add_argument("--no-email", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    today = datetime.now(SAST).date()
    mode = args.mode or pick_mode(today)
    state = history.load()
    calendar = calendar_events.upcoming(today)

    if args.sample:
        report = Report.model_validate_json((Path(__file__).parent / "sample_report.json").read_text())
        health = {"sample": "ok (0)"}
    else:
        import analyst
        import collectors

        collected = collectors.collect(mode)
        health = collected.health
        print(f"Collected {len(collected.items)} items; feed health: {json.dumps(health)}", file=sys.stderr)
        context = build_context(today, mode, state, collected.as_prompt_text(), calendar)
        notes = analyst.research(context, mode)
        OUT.mkdir(exist_ok=True)
        (OUT / f"notes-{today}.md").write_text(notes)
        report = analyst.structure(context, notes)

    scored: list[render.Scored] = []
    for t in report.trends:
        s = scoring.total_score(t)
        band, reason = scoring.band(t, s)
        scored.append(render.Scored(
            trend=t, score=s, band=band, band_reason=reason,
            since_last=history.last_score(state, t.name, today),
            change_4w=history.change_4w(state, t.name, today, s),
        ))
        if scored[-1].since_last is not None:
            scored[-1].since_last = s - scored[-1].since_last
    order = {"ACT": 0, "PREPARE": 1, "WATCH": 2, "IGNORE": 3, "RED FLAG": 4}
    scored.sort(key=lambda x: (order[x.band], -x.score))

    html_body = render.html(report, scored, today, mode, calendar, health)
    text_body = render.text(report, scored, today)
    OUT.mkdir(exist_ok=True)
    (OUT / f"report-{today}.html").write_text(html_body)

    if args.sample:
        print(f"Sample report written to {OUT / f'report-{today}.html'}")
        return 0

    for x in scored:
        history.record(state, x.trend.name, x.trend.aliases, x.trend.ip_status, today, x.score, x.trend.seen_today)
    if mode == "monthly":
        retired = history.retire_dead(state, today)
        if retired:
            print(f"Retired: {', '.join(retired)}", file=sys.stderr)
    history.save(state)

    if not args.no_email:
        import mailer

        n_act = sum(1 for x in scored if x.band == "ACT")
        subject = f"{config.REPORT_NAME}: {today.strftime('%d %b %Y')}" + (f" ({n_act} to act on)" if n_act else "")
        mailer.send(subject, html_body, text_body)
        print("Email sent.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
