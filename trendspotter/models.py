"""Structured report schema that Claude fills in (validated with Pydantic)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class FactorScores(BaseModel):
    """Each factor 0-5, per the brief's Signal Scoring Framework."""

    velocity: int = Field(description="0 = flat; 5 = more than 3x in 4 weeks (TikTok views, Google Trends, Amazon rank)")
    cross_platform: int = Field(description="0 = 1 platform; 5 = 4+ independent platforms (social + search + retail + trade)")
    age_fit: int = Field(description="0 = adult/kidult only; 5 = clearly 5-9 (parents asking, kid creators, school fad)")
    sourcing: int = Field(description="0 = proprietary IP, no licence route; 5 = generic, multiple factories on 1688/Alibaba")
    runway: int = Field(description="0 = SA peak under 10 weeks away; 5 = SA not saturated and seasonal peak 4-9 months away")
    margin: int = Field(description="0 = under 30% gross; 5 = over 55% gross after duty, VAT, freight, testing (R100-R500 band)")
    longevity: int = Field(description="0 = celebrity or single-SKU craze in decline; 5 = evergreen play pattern or multi-year IP")


class Evidence(BaseModel):
    source: str = Field(description="e.g. 'TikTok', 'Google Trends ZA', 'Amazon UK Movers & Shakers', 'Takealot'")
    finding: str = Field(description="The signal with a number where possible, e.g. '#needoh views +240% week on week'")
    url: str = Field(description="Source URL, or empty string if none")


class Trend(BaseModel):
    name: str = Field(description="Canonical trend name; reuse the watchlist name if it is already on the watchlist")
    aliases: list[str]
    ip_status: Literal["generic", "licensed", "proprietary"]
    scores: FactorScores
    evidence: list[Evidence] = Field(description="Strongest signals today, up to 4")
    why_now: str = Field(description="One sentence")
    age_fit_note: str = Field(description="Why this is (or is not) a 5-9 trend rather than kidult or toddler")
    sourcing_route: str = Field(description="e.g. 'generic: 1688 factories, SANS 8124 test report needed' or 'licensed distributor only'")
    projected_sa_peak: str = Field(description="Month and year, e.g. 'Mar 2027', or 'unknown'")
    months_to_sa_peak: int = Field(description="Whole months from today to projected SA peak; -1 if unknown")
    next_step: str = Field(description="Recommended next step: samples, quotes, test lab, watch, or drop")
    tiktok_change: str = Field(description="Short change note or 'n/a'")
    google_trends_change: str = Field(description="ZA/US/UK change note or 'n/a'")
    amazon_rank_change: str = Field(description="Short change note or 'n/a'")
    takealot_status: str = Field(description="e.g. 'not listed', 'listed R199', 'top 20 bestseller', or 'n/a'")
    safety_recall_active: bool = Field(description="True if there is an active recall or safety warning for this product type")
    only_ip_lookalikes_sourceable: bool = Field(description="True if the only sourceable product would be an IP lookalike or counterfeit")
    seen_today: bool = Field(description="True if you found a fresh signal today; False if carried over from the watchlist without new data")


class PipelineItem(BaseModel):
    item: str = Field(description="Deal, release or licence, e.g. 'Netflix X: Mattel named master toy licensee'")
    date: str = Field(description="Announcement or release date")
    note: str = Field(description="What it means for Just Imagine (licensed route or adjacent generic theme)")
    url: str


class Alert(BaseModel):
    alert: str
    url: str


class Report(BaseModel):
    headline: str = Field(description="1-2 lines: the single most important change since the last report")
    trends: list[Trend] = Field(description="Every watchlist item plus new candidates")
    licensing_pipeline: list[PipelineItem] = Field(description="New deals and releases in the next 3-12 months")
    sa_market_pulse: list[str] = Field(description="Takealot / Toys R Us SA / PEP movements, local press, Durban freight/port status, ZAR exchange rate")
    risk_alerts: list[Alert] = Field(description="Recalls, safety warnings, counterfeit crackdowns, fads in decline")
    data_gaps: list[str] = Field(description="Sources you could not check today and why")
