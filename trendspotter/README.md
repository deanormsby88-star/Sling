# Just Imagine Trendspotter

A weekly report on toy trends for children aged 5 to 9, scored for sourcing into South Africa. It follows the
research brief *Just Imagine Trendspotter: Daily Source Map for Ages 5-9 Toy Trends*.

- **Report page:** https://claude.ai/artifact/TqAfEGvM5SQzEJPpoYHL3G (private to you; share it from its Share menu)
- **When:** every Friday morning, SAST. A push notification arrives when it is ready.
- **Cost:** runs on your Claude subscription as a scheduled Claude task. There is no API bill and no API key; each
  run uses part of your plan's usage allowance.

This folder is separate from the Sling website and can be moved to its own repository as it is.

## How a run works

A scheduled Claude session follows `RUNBOOK.md`:

1. Reads last week's report page. The page carries the score history in a hidden JSON block, so nothing else
   needs storing.
2. `python build.py context` prints the week's brief: sources, the watchlist with last week's scores, and the
   SA calendar.
3. Researches with web search: TikTok, Google Trends (ZA, US, UK), Amazon Movers & Shakers, Takealot, YouTube,
   trade news, US/UK/SA retailers, Temu/AliExpress/1688, Reddit, safety recalls, the streaming and licensing slate,
   and Durban freight. The first Friday of each month adds Circana, company investor updates, trade fairs and SA
   market data.
4. Writes `out/report.json` in the shape of `models.py`.
5. `python build.py page` scores every trend, carries the history forward and writes the page, which is then
   republished to the same link.

## Scoring

Each trend is scored 0-5 on seven factors: velocity 20, cross-platform 20, 5-9 fit 15, sourcing and IP 15,
SA runway 10, margin 10, longevity 10. The code, not the model, turns those into a score out of 100 and a band:
75+ ACT, 55-74 PREPARE, 35-54 WATCH, under 35 IGNORE. ACT also needs the projected SA peak to be at least 4 months
away. Active safety recalls and IP-lookalike-only trends are red-flagged whatever the score.

## Changing what it watches

Everything is in `config.py`: the seed watchlist, TikTok hashtags, sources, trigger words, weights, bands and the
SA calendar. The Friday run reads it from the `claude/daily-trendspotter-email-ckgq0l` branch until this folder
is merged into the default branch.

## Client PDF

`python build.py client-pdf` turns the latest report into a branded PDF for a client, with only positive,
client-safe content on generic products only (see `client.py` for exactly what is filtered out). The client's name and logos are set in
`config.py` and `brand/`. Steps are in RUNBOOK.md. The PDF's last page
is a fixed "Key dates" block (SA public holidays and school terms for public, private and 3-term schools), set in
`config.py`: update `KEY_DATES_YEAR`, `PUBLIC_HOLIDAYS`, `SCHOOL_TERMS` and `SCHOOL_HOLIDAYS` once a year.

## Local checks

```bash
cd trendspotter
python -m pip install -r requirements.txt
python build.py sample        # renders sample_report.json to out/sample.html
```

## Limits to know

- TikTok, Google Trends and Amazon have no free official API. Their numbers come from web search, so treat them
  as direction rather than exact counts.
- A deep run uses a fair share of your plan's usage. If it runs into your usage limit, that week's report may be
  late or missing.
- Treat anything at ACT as a prompt for your own review, not as an order. The brief requires a SANS 8124 test
  report before stocking anything.
