"""Weekly sales summary for the Wimpy email, from Shamain's daily "Stock & Sales" emails.

The Friday session reads the emails and writes one record per trading day to a JSON file:
  [{"date": "2026-11-24", "toys": {"Squishy dumplings": 19}, "lp_boys": 6, "lp_girls": 4}, ...]
(toys = "Daily sales of the current toy", one entry per toy named; lp = "Daily sales of the
current L/P" in cases.) This script does the maths so it is the same every week:

  python sales.py --records out/sales.json --end 2026-11-26

- Week: the 7 days ending --end, against the same dates one month earlier.
- Month to date: the 1st to --end, against the same dates one month earlier.
- Promotion: the toy(s) with sales in each period, and whether they match.
Prints JSON (for checking) and writes out/sales.html, the block for the email.
"""

from __future__ import annotations

import argparse
import calendar
import json
from datetime import date, timedelta
from html import escape
from pathlib import Path

HERE = Path(__file__).parent


def month_back(d: date) -> date:
    """Same day one month earlier, clamped to the month's last day (31 Mar -> 28/29 Feb)."""
    y, m = (d.year, d.month - 1) if d.month > 1 else (d.year - 1, 12)
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def summarise(records: list[dict], start: date, end: date) -> dict:
    rows = [r for r in records if start <= date.fromisoformat(r["date"]) <= end]
    toys: dict[str, int] = {}
    for r in rows:
        for name, n in r.get("toys", {}).items():
            toys[name.strip()] = toys.get(name.strip(), 0) + int(n)
    boys = sum(int(r.get("lp_boys", 0)) for r in rows)
    girls = sum(int(r.get("lp_girls", 0)) for r in rows)
    return {
        "start": start.isoformat(), "end": end.isoformat(), "days_reported": len(rows),
        "toys": toys, "toy_total": sum(toys.values()),
        "lp_boys": boys, "lp_girls": girls, "lp_total": boys + girls,
        "promotion": [n for n, v in sorted(toys.items(), key=lambda x: -x[1]) if v > 0],
    }


def change(now: int, before: int) -> str:
    if before == 0:
        return "n/a" if now == 0 else "new"
    pct = round((now - before) / before * 100)
    return f"+{pct}%" if pct > 0 else f"{pct}%"


def same_promotion(a: list[str], b: list[str]) -> str:
    sa, sb = {x.lower() for x in a}, {x.lower() for x in b}
    if sa == sb:
        return "Same promotion"
    if sa & sb:
        return "Partly the same"
    return "Different promotion"


def fmt_range(s: str, e: str) -> str:
    ds, de = date.fromisoformat(s), date.fromisoformat(e)
    return f"{ds.day} {ds:%b} to {de.day} {de:%b}" if ds != de else f"{ds.day} {ds:%b}"


def build(records: list[dict], end: date) -> dict:
    week = summarise(records, end - timedelta(days=6), end)
    week_prev = summarise(records, month_back(end - timedelta(days=6)), month_back(end))
    mtd = summarise(records, end.replace(day=1), end)
    mtd_prev = summarise(records, month_back(end.replace(day=1)), month_back(end))
    return {"week": week, "week_prev": week_prev, "mtd": mtd, "mtd_prev": mtd_prev}


def html(s: dict) -> str:
    def row(label: str, now: dict, prev: dict) -> str:
        return (f"<tr><td><b>{escape(label)}</b><br>{fmt_range(now['start'], now['end'])} vs "
                f"{fmt_range(prev['start'], prev['end'])}</td>"
                f"<td>{now['toy_total']} vs {prev['toy_total']} ({change(now['toy_total'], prev['toy_total'])})</td>"
                f"<td>{now['lp_total']} vs {prev['lp_total']} ({change(now['lp_total'], prev['lp_total'])})</td></tr>")

    w, wp, m, mp = s["week"], s["week_prev"], s["mtd"], s["mtd_prev"]
    promo_now = ", ".join(w["promotion"]) or "none recorded"
    promo_prev = ", ".join(wp["promotion"]) or "none recorded"
    return f"""<table>
<tr><th></th><th>Toy sales (units)</th><th>Lucky packets (cases)</th></tr>
{row("This week", w, wp)}
{row("Month to date", m, mp)}
</table>
<p><b>Promotion running:</b> {escape(promo_now)}. Same week last month: {escape(promo_prev)} ({same_promotion(w['promotion'], wp['promotion']).lower()}).</p>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--end", required=True, help="last day included, YYYY-MM-DD")
    ap.add_argument("--out", default=str(HERE / "out" / "sales.html"))
    a = ap.parse_args()
    records = json.loads(Path(a.records).read_text())
    s = build(records, date.fromisoformat(a.end))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(html(s))
    print(json.dumps(s, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
