"""Claude steps: (1) research with web search/fetch, (2) structure into a Report.

Step 1 covers the Tier 1 sources that have no free API (TikTok, Google Trends,
Amazon Movers & Shakers, Takealot, YouTube) and the weekly/monthly sweeps.
Step 2 merges synonyms, assigns age fit and fills the scoring schema.
"""

from __future__ import annotations

import anthropic

import config
from models import Report

FALLBACK_BETA = "server-side-fallback-2026-07-01"

SYSTEM = f"""You are the research analyst behind the {config.REPORT_NAME}, a weekly email (sent on Fridays) for Dean, who runs
Just Imagine, a South African toy importer. Dean imports from China to Johannesburg via Durban and sells
toys for children aged 5 to 9, mostly in the R100-R500 price band.

Your job: spot toy trends for ages 5-9 early enough to source them for South Africa.

How the market works (from Dean's research brief):
- Early signals show up first on TikTok, Google Trends spikes and Amazon Movers & Shakers. Trade lists
  (DreamToys, Circana) confirm trends 6-12 months later. Trends reach SA 6-14 months after the US and Asia.
- The sourcing window is the gap: a trend scoring well abroad while Takealot and Google Trends ZA are still
  flat. Labubu took about 14 months from first global signal to peak SA demand.
- Import runway for a non-licensed stock product is 10-16 weeks (sampling 2-4 wks, production 4-8 wks,
  freight and clearance 4-6 wks, testing in parallel). China-Durban is 22-28 days port to port; Durban adds
  3-10 days in the Aug-Nov peak. Licensed or custom-tooled products take 6-18 months.
- Adults drive much of 2025-2026 toy growth (collectibles, kidult). Filter hard for 5-9 relevance: sports
  cards, LEGO Botanicals and bag charms bought by adults are not children's trends.
- Favour generic play patterns (squishies and sensory, bag-charm plush, blind-box minis, creative kits,
  STEM). Approach hot IP (KPop Demon Hunters, Pokemon, Bluey, Stitch) only via licensed distribution or
  licensed promo. Never recommend IP lookalikes or counterfeits: SA counterfeit raids are rising.
- Celebrity- and collector-driven crazes get a high fad risk and a planned exit date. Pop Mart's Q3 2026
  revenue fell 45-50% year on year.
- Safety: SANS 8124 (ISO 8124) test reports are standard; squishies, slime, small parts and batteries need
  particular care. Mains-powered toys and chargers likely need an NRCS Letter of Authority.
- SA seasons: back to school (Jan), Easter (Mar-Apr), winter holidays (Jun-Jul), Blue Dot Sale / Black
  Friday (Nov; stock in SA by October), Christmas (Dec, summer: outdoor, water, ride-ons; order by
  June-July, ship by August).

Act on trends confirmed on at least 3 platforms. Treat single-platform spikes as "watch, don't stock deep".

Writing style: plain en-GB, specific, numbers over adjectives, no hype words, no exclamation marks.
Every statistic names its source and date. Say clearly when you could not verify something."""


def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def research(context: str, mode: str) -> str:
    """Step 1: web research. Returns the analyst's notes as text."""
    tools = [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": config.MAX_WEB_SEARCHES[mode]},
        {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": config.MAX_WEB_FETCHES[mode]},
    ]
    messages: list = [{"role": "user", "content": context}]
    notes: list[str] = []
    client = _client()
    for _ in range(10):  # allow pause_turn continuations on the long weekly run
        with client.beta.messages.stream(
            model=config.MODEL,
            max_tokens=64000,
            system=SYSTEM,
            tools=tools,
            messages=messages,
            output_config={"effort": config.EFFORT},
            betas=[FALLBACK_BETA],
            fallbacks="default",
        ) as stream:
            response = stream.get_final_message()
        notes += [b.text for b in response.content if b.type == "text"]
        if response.stop_reason == "refusal":
            raise RuntimeError(f"Research step was declined: {response.stop_details}")
        if response.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": response.content})
    return "\n".join(notes).strip()


def structure(context: str, notes: str) -> Report:
    """Step 2: turn the research notes into the validated Report schema."""
    prompt = f"""Below are today's briefing context and your research notes. Turn them into the report.

Rules:
- Include every watchlist item, plus up to {config.MAX_NEW_CANDIDATES} new candidate trends you found. Merge synonyms into one trend
  (e.g. "NeeDoh", "Nee Doh" and "squishy cube" belong to "Squishy / sensory squeeze toys").
- Score each factor 0-5 using only evidence in the notes. If a watchlist item had no fresh signal this week, keep
  its scores close to its last scores and set seen_today to false.
- Up to 5 evidence items per trend, each with a number and source where possible.
- Do not invent URLs. Use an empty string if you have none.

<briefing_context>
{context}
</briefing_context>

<research_notes>
{notes}
</research_notes>"""
    response = _client().beta.messages.parse(
        model=config.MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        output_format=Report,
        output_config={"effort": "low"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        raise RuntimeError(f"Structuring step failed: stop_reason={response.stop_reason}")
    return response.parsed_output
