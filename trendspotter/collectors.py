"""Free, automated Tier 1 collectors: trade RSS, Google News, Reddit, YouTube.

Every collector fails soft. A dead source is recorded in `health` so it shows
in the email footer instead of stopping the run.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import config

USER_AGENT = "Mozilla/5.0 (compatible; JustImagineTrendspotter/1.0)"
TIMEOUT = 20
ATOM = "{http://www.w3.org/2005/Atom}"


@dataclass
class Item:
    source: str
    title: str
    url: str
    published: datetime | None = None
    extra: str = ""

    def line(self) -> str:
        when = self.published.strftime("%d %b") if self.published else "undated"
        extra = f" ({self.extra})" if self.extra else ""
        return f"- [{self.source}, {when}] {self.title}{extra} <{self.url}>"


@dataclass
class Collected:
    items: list[Item] = field(default_factory=list)
    health: dict[str, str] = field(default_factory=dict)  # source -> "ok (n)" or error

    def keyword_hits(self) -> list[Item]:
        return [i for i in self.items if any(k in i.title.lower() for k in config.KEYWORD_TRIGGERS)]

    def as_prompt_text(self, limit: int = 150) -> str:
        if not self.items:
            return "(No items collected from feeds today.)"
        return "\n".join(i.line() for i in self.items[:limit])


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def _parse_date(text: str | None) -> datetime | None:
    if not text:
        return None
    text = text.strip()
    try:
        dt = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def parse_feed(data: bytes, source: str) -> list[Item]:
    """Parse RSS 2.0 or Atom into Items."""
    root = ET.fromstring(data)
    items: list[Item] = []
    for node in root.iter("item"):  # RSS
        items.append(Item(
            source=source,
            title=(node.findtext("title") or "").strip(),
            url=(node.findtext("link") or "").strip(),
            published=_parse_date(node.findtext("pubDate")),
        ))
    for node in root.iter(f"{ATOM}entry"):  # Atom (YouTube, some blogs)
        link = node.find(f"{ATOM}link")
        items.append(Item(
            source=source,
            title=(node.findtext(f"{ATOM}title") or "").strip(),
            url=link.get("href", "") if link is not None else "",
            published=_parse_date(node.findtext(f"{ATOM}published") or node.findtext(f"{ATOM}updated")),
        ))
    return [i for i in items if i.title]


def _recent(items: list[Item], hours: int) -> list[Item]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return [i for i in items if i.published is None or i.published >= cutoff]


def _collect_feeds(out: Collected, feeds: dict[str, str], hours: int, per_feed: int = 15) -> None:
    for name, url in feeds.items():
        try:
            items = _recent(parse_feed(_get(url), name), hours)[:per_feed]
            out.items.extend(items)
            out.health[name] = f"ok ({len(items)})"
        except Exception as exc:  # noqa: BLE001 - fail soft, report in email
            out.health[name] = f"failed: {type(exc).__name__}"


def google_news_url(query: str, lang: str, country: str) -> str:
    q = urllib.parse.quote(f"{query} when:2d")
    return f"https://news.google.com/rss/search?q={q}&hl={lang}&gl={country}&ceid={country}:{lang.split('-')[0]}"


def collect_reddit(out: Collected, period: str) -> None:
    for sub in config.SUBREDDITS:
        name = f"r/{sub}"
        try:
            data = json.loads(_get(f"https://www.reddit.com/r/{sub}/top.json?t={period}&limit=15"))
            posts = [c["data"] for c in data["data"]["children"]]
            for p in posts:
                out.items.append(Item(
                    source=name,
                    title=p.get("title", ""),
                    url="https://www.reddit.com" + p.get("permalink", ""),
                    published=datetime.fromtimestamp(p.get("created_utc", 0), timezone.utc),
                    extra=f"{p.get('score', 0)} upvotes, {p.get('num_comments', 0)} comments",
                ))
            out.health[name] = f"ok ({len(posts)})"
        except Exception as exc:  # noqa: BLE001
            out.health[name] = f"failed: {type(exc).__name__}"


def collect(mode: str) -> Collected:
    """Run the collectors for this cadence. mode is daily, weekly or monthly."""
    out = Collected()
    window = 48 if mode == "daily" else 24 * 8
    _collect_feeds(out, config.TRADE_FEEDS, window)
    _collect_feeds(out, {n: google_news_url(*q) for n, q in config.NEWS_QUERIES.items()}, window, per_feed=10)
    _collect_feeds(out, {
        n: f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}" for n, cid in config.YOUTUBE_CHANNELS.items()
    }, window, per_feed=5)
    collect_reddit(out, "day" if mode == "daily" else "week")
    if mode != "daily":
        _collect_feeds(out, config.SAFETY_FEEDS, 24 * 8)
    # Keyword hits first so they survive the prompt limit.
    hits = out.keyword_hits()
    out.items = hits + [i for i in out.items if i not in hits]
    return out
