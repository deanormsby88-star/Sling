"""Build the weekly Trendspotter page.

Two steps, run by the weekly scheduled Claude session (see RUNBOOK.md):

  python build.py context --previous out/previous.html
      Prints this week's research brief: sources to check, the watchlist with
      last week's scores, and the SA calendar.

  python build.py page --report out/report.json --previous out/previous.html --out out/trendspotter.html
      Validates the report, scores every trend, carries the history forward and
      writes the page to publish.

  python build.py sample
      Renders sample_report.json to out/sample.html (layout check, no history).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import calendar_events
import config
import history
import render
import scoring
from models import Report

HERE = Path(__file__).parent
SAST = ZoneInfo("Africa/Johannesburg")


def mode_for(today) -> str:
    """Every report is weekly; the first Friday of the month adds the monthly sweep."""
    return "monthly" if today.day <= 7 else "weekly"


def _read(path: str | None) -> str | None:
    if path and Path(path).exists():
        return Path(path).read_text()
    return None


def context(today, state: dict) -> str:
    mode = mode_for(today)
    sources = config.WEB_SOURCES["weekly"] + (config.WEB_SOURCES["monthly"] if mode == "monthly" else [])
    cal = "\n".join(f"- {w}: {e}" for w, e, _ in calendar_events.upcoming(today)) or "(none)"
    return f"""Week ending {today.strftime('%A %d %B %Y')} (SAST). Run type: {mode}.

Sources to research (signals from the last 7 days, with 4-week direction where you can find it):
{chr(10).join('- ' + s for s in sources)}

Watchlist (re-check every one; also find up to {config.MAX_NEW_CANDIDATES} new candidates for ages 5-9):
{history.watchlist_text(state, today)}

SA calendar, next 60 days:
{cal}"""


def build_page(report: Report, state: dict, today, mode: str) -> str:
    scored: list[render.Scored] = []
    for t in report.trends:
        s = scoring.total_score(t)
        band, reason = scoring.band(t, s)
        prev = history.last_score(state, t.name, today)
        scored.append(render.Scored(
            trend=t, score=s, band=band, band_reason=reason,
            since_last=None if prev is None else s - prev,
            change_4w=history.change_4w(state, t.name, today, s),
        ))
    for x in scored:
        history.record(state, x.trend.name, x.trend.aliases, x.trend.ip_status, today, x.score, x.trend.seen_today)
        x.history = history.series(state, x.trend.name)
    if mode == "monthly":
        retired = history.retire_dead(state, today)
        if retired:
            print(f"Retired: {', '.join(retired)}", file=sys.stderr)
    history.add_headline(state, today, report.headline)

    order = {"ACT": 0, "PREPARE": 1, "WATCH": 2, "IGNORE": 3, "RED FLAG": 4}
    scored.sort(key=lambda x: (order[x.band], -x.score))
    return render.page(report, scored, today, mode, calendar_events.upcoming(today),
                       state["archive"], history.to_script(state))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["context", "page", "sample", "placeholder"])
    ap.add_argument("--previous", help="last week's published page (HTML), if any")
    ap.add_argument("--report", help="this week's report JSON")
    ap.add_argument("--out", default=str(HERE / "out" / "trendspotter.html"))
    ap.add_argument("--date", help="report date YYYY-MM-DD (default: today in SAST)")
    args = ap.parse_args()

    today = datetime.fromisoformat(args.date).date() if args.date else datetime.now(SAST).date()
    state = history.from_page(_read(args.previous))

    if args.command == "context":
        print(context(today, state))
        return 0

    if args.command == "placeholder":
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        first = today + timedelta(days=(4 - today.weekday()) % 7)
        out.write_text(render.placeholder(first, calendar_events.upcoming(today), state, history.to_script(state)))
        print(f"Wrote {out}")
        return 0

    if args.command == "sample":
        report = Report.model_validate_json((HERE / "sample_report.json").read_text())
        out = HERE / "out" / "sample.html"
    else:
        if not args.report:
            ap.error("page needs --report")
        report = Report.model_validate_json(Path(args.report).read_text())
        out = Path(args.out)

    html_page = build_page(report, state, today, mode_for(today))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_page)
    print(f"Wrote {out} ({len(report.trends)} trends)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
