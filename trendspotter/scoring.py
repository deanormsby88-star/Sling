"""Turn factor scores into a 0-100 score and a decision band, per the brief.

Done in code, not by the model, so the maths is consistent day to day.
"""

from __future__ import annotations

import config
from models import Trend


def total_score(trend: Trend) -> int:
    s = trend.scores.model_dump()
    return round(sum(max(0, min(5, s[f])) / 5 * w for f, w in config.WEIGHTS.items()))


def red_flags(trend: Trend) -> list[str]:
    flags = []
    if trend.safety_recall_active:
        flags.append("active safety recall or warning")
    if trend.only_ip_lookalikes_sourceable or trend.ip_status == "proprietary":
        flags.append("only sourceable product is an IP lookalike")
    return flags


def band(trend: Trend, score: int) -> tuple[str, str]:
    """Return (band, reason). Red flags override the score."""
    flags = red_flags(trend)
    if flags:
        return "RED FLAG", "; ".join(flags)
    label = next(name for floor, name in config.BANDS if score >= floor)
    if label == "ACT" and 0 <= trend.months_to_sa_peak < config.MIN_MONTHS_TO_SA_PEAK_FOR_ACT:
        return "PREPARE", f"scores {score} but projected SA peak is under {config.MIN_MONTHS_TO_SA_PEAK_FOR_ACT} months away"
    if label == "ACT" and trend.months_to_sa_peak < 0:
        return "PREPARE", f"scores {score} but SA peak timing is unknown; confirm runway before ordering"
    return label, ""
