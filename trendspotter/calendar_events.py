"""Next-60-days calendar from config.CALENDAR plus Easter (computed)."""

from __future__ import annotations

from datetime import date, timedelta

import config


def easter(year: int) -> date:
    """Western Easter Sunday (anonymous Gregorian algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7  # noqa: E741
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def upcoming(today: date, days: int = 60, start_days: int = 0) -> list[tuple[str, str, str]]:
    """Return (when, event, note) for events from `start_days` to `days` days ahead."""
    end = today + timedelta(days=days)
    start = today + timedelta(days=start_days)
    out: list[tuple[date, str, str, str]] = []
    for year in (today.year, today.year + 1, today.year + 2):
        for (month, day), event, note in config.CALENDAR:
            if day:
                d = date(year, month, day)
                label = d.strftime("%d %b %Y")
                in_range = start <= d <= end
            else:
                d = date(year, month, 1)
                label = d.strftime("%b %Y")
                # Month-long items show while the month is current or starts in range.
                in_range = (start_days == 0 and (d.year, d.month) == (today.year, today.month)) or start <= d <= end
            if in_range:
                out.append((d, label, event, note))
        e = easter(year)
        if start <= e <= end:
            out.append((e, e.strftime("%d %b %Y"), "Easter", "Squishies and small collectibles were 2026 Easter-basket hits."))
    out.sort(key=lambda x: x[0])
    return [(label, event, note) for _, label, event, note in out]
