"""Score history and past headlines, carried from week to week inside the
published report page itself (a JSON block), so nothing else needs storing.

State shape:
  {"trends": {name: {"aliases": [...], "ip": str, "last_seen": "YYYY-MM-DD",
                     "scores": {"YYYY-MM-DD": int}}},
   "archive": [{"date": "YYYY-MM-DD", "headline": str}]}
"""

from __future__ import annotations

import json
import re
from datetime import date, timedelta

import config

STATE_ID = "trendspotter-state"
_STATE_RE = re.compile(r'<script type="application/json" id="' + STATE_ID + r'">(.*?)</script>', re.S)


def seed() -> dict:
    return {
        "trends": {t["name"]: {"aliases": t["aliases"], "ip": t["ip"], "scores": {}} for t in config.SEED_WATCHLIST},
        "archive": [],
    }


def from_page(page_html: str | None) -> dict:
    """Read the state block from last week's published page (or start fresh)."""
    if not page_html:
        return seed()
    m = _STATE_RE.search(page_html)
    if not m:
        return seed()
    state = json.loads(m.group(1))
    state.setdefault("archive", [])
    return state


REPORT_ID = "trendspotter-report"
_REPORT_RE = re.compile(r'<script type="application/json" id="' + REPORT_ID + r'">(.*?)</script>', re.S)


def report_to_script(report_json: str) -> str:
    """Embed this week's full report JSON so a client PDF can be built from the page later."""
    data = report_json.replace("<", "\\u003c")
    return f'<script type="application/json" id="{REPORT_ID}">{data}</script>'


def report_from_page(page_html: str) -> str | None:
    m = _REPORT_RE.search(page_html or "")
    return m.group(1) if m else None


def to_script(state: dict) -> str:
    """Embed state as JSON. Escape '<' so the JSON can never close the script tag."""
    data = json.dumps(state, sort_keys=True, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f'<script type="application/json" id="{STATE_ID}">{data}</script>'


def _scores(state: dict, name: str) -> dict:
    return state["trends"].get(name, {}).get("scores", {})


def last_score(state: dict, name: str, before: date) -> int | None:
    s = _scores(state, name)
    earlier = sorted(d for d in s if d < before.isoformat())
    return s[earlier[-1]] if earlier else None


def score_on_or_before(state: dict, name: str, day: date) -> int | None:
    s = _scores(state, name)
    earlier = sorted(d for d in s if d <= day.isoformat())
    return s[earlier[-1]] if earlier else None


def change_4w(state: dict, name: str, today: date, score: int) -> int | None:
    prev = score_on_or_before(state, name, today - timedelta(days=28))
    return None if prev is None else score - prev


def series(state: dict, name: str, weeks: int = 12) -> list[int]:
    s = _scores(state, name)
    return [s[d] for d in sorted(s)][-weeks:]


def record(state: dict, name: str, aliases: list[str], ip: str, today: date, score: int, seen: bool) -> None:
    entry = state["trends"].setdefault(name, {"aliases": [], "ip": ip, "scores": {}})
    entry["aliases"] = sorted(set(entry.get("aliases", [])) | set(aliases))
    entry["ip"] = ip
    entry["scores"][today.isoformat()] = score
    if seen:
        entry["last_seen"] = today.isoformat()
    cutoff = (today - timedelta(days=365)).isoformat()
    entry["scores"] = {d: v for d, v in entry["scores"].items() if d >= cutoff}


def add_headline(state: dict, today: date, headline: str) -> None:
    state["archive"] = [a for a in state["archive"] if a["date"] != today.isoformat()]
    state["archive"].insert(0, {"date": today.isoformat(), "headline": headline})
    state["archive"] = state["archive"][:52]


def retire_dead(state: dict, today: date) -> list[str]:
    """Monthly: drop non-seed trends not seen for RETIRE_AFTER_DAYS that score under 35."""
    cutoff = (today - timedelta(days=config.RETIRE_AFTER_DAYS)).isoformat()
    seeds = {t["name"] for t in config.SEED_WATCHLIST}
    retired = []
    for name, entry in list(state["trends"].items()):
        latest = score_on_or_before(state, name, today) or 0
        if name not in seeds and entry.get("last_seen", "") < cutoff and latest < 35:
            retired.append(name)
            del state["trends"][name]
    return retired


def watchlist_text(state: dict, today: date) -> str:
    lines = []
    for name, entry in sorted(state["trends"].items()):
        prev = last_score(state, name, today)
        aliases = ", ".join(entry.get("aliases", [])) or "none"
        lines.append(f"- {name} (IP: {entry.get('ip', '?')}; aliases: {aliases}; last score: {prev if prev is not None else 'new'})")
    return "\n".join(lines)
