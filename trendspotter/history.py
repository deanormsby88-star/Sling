"""Score history, so each report can show change since yesterday and over 7 days.

Stored as JSON: {"trends": {name: {"aliases": [...], "ip": str, "scores": {"YYYY-MM-DD": int}}}}
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import config

STATE_FILE = Path(__file__).parent / "state" / "history.json"


def load() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"trends": {
        t["name"]: {"aliases": t["aliases"], "ip": t["ip"], "scores": {}} for t in config.SEED_WATCHLIST
    }}


def save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=1, sort_keys=True, ensure_ascii=False))


def last_score(state: dict, name: str, before: date) -> int | None:
    scores = state["trends"].get(name, {}).get("scores", {})
    earlier = sorted(d for d in scores if d < before.isoformat())
    return scores[earlier[-1]] if earlier else None


def score_on_or_before(state: dict, name: str, day: date) -> int | None:
    scores = state["trends"].get(name, {}).get("scores", {})
    earlier = sorted(d for d in scores if d <= day.isoformat())
    return scores[earlier[-1]] if earlier else None


def change_7d(state: dict, name: str, today: date, score: int) -> int | None:
    prev = score_on_or_before(state, name, today - timedelta(days=7))
    return None if prev is None else score - prev


def record(state: dict, name: str, aliases: list[str], ip: str, today: date, score: int, seen: bool) -> None:
    entry = state["trends"].setdefault(name, {"aliases": [], "ip": ip, "scores": {}})
    entry["aliases"] = sorted(set(entry.get("aliases", [])) | set(aliases))
    entry["ip"] = ip
    entry["scores"][today.isoformat()] = score
    if seen:
        entry["last_seen"] = today.isoformat()
    # Keep a year of history.
    cutoff = (today - timedelta(days=365)).isoformat()
    entry["scores"] = {d: s for d, s in entry["scores"].items() if d >= cutoff}


def retire_dead(state: dict, today: date) -> list[str]:
    """Monthly: drop trends not seen for RETIRE_AFTER_DAYS that score under 35."""
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
