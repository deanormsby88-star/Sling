# Just Imagine Trendspotter

A weekly email, every Friday at about 06:00 SAST, that tracks toy trends for children aged 5 to 9 and scores each one for
sourcing into South Africa. It follows the research brief *Just Imagine Trendspotter: Daily Source Map for
Ages 5-9 Toy Trends*.

This folder is separate from the Sling website. It can be moved to its own private repository as it is.

## What it does each Friday

1. **Collects** free signals from the past 8 days: trade RSS (The Toy Book, Toy World, Toy News, License Global,
   Kidscreen, Toys n Playthings), Google News searches (SA toys, licensing, sell-outs, recalls, Durban port),
   Reddit parent and toy communities, and any YouTube channels listed in `config.py`. Headlines that contain
   a trigger word ("master toy licence", "sold out", "shortage", "recall", "viral") go first.
2. **Researches in depth** using Claude with web search (up to 45 searches and 25 page reads, at high effort).
   It covers every Tier 1 and Tier 2 source in the brief in one pass:
   - TikTok Creative Center and toy hashtags, Google Trends (ZA, US, UK), Amazon Movers & Shakers and Hot New
     Releases, Takealot best sellers, YouTube toy channels.
   - US/UK/SA retailer bestsellers, Temu/AliExpress/1688 copy counts and price floors, Reddit and parent
     communities, a safety and recall sweep, and the streaming and licensing slate.
   - It looks for up to 10 new candidate trends each week, as well as re-checking the watchlist.
   - **The first Friday of each month** adds Circana, company investor updates, trade fairs and SA market data
     (up to 55 searches). It also retires trends that have not been seen for 30 days and score under 35.
3. **Scores** every trend 0-5 on the brief's seven factors. The code, not the model, turns those into a
   score out of 100 and a band: 75+ ACT, 55-74 PREPARE, 35-54 WATCH, under 35 IGNORE. ACT also needs the
   projected SA peak to be at least 4 months away (the import runway). Active safety recalls and
   IP-lookalike-only trends are red-flagged, whatever the score.
4. **Emails** the report in the brief's template: headline, ACT list, rising, watchlist movement (with
   4-week change), licensing pipeline, SA market pulse, risk alerts and the next 60 days of the calendar. The
   footer lists any feeds that failed and any sources Claude could not check.

## Setup (about 10 minutes)

1. **Anthropic API key:** create one at console.anthropic.com.
2. **Gmail app password:** turn on 2-step verification, then create an app password at
   myaccount.google.com/apppasswords. Any other SMTP provider works too; set `SMTP_HOST` and `SMTP_PORT`.
3. **GitHub secrets:** in the repository, go to Settings > Secrets and variables > Actions, then add:
   `ANTHROPIC_API_KEY`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_TO` (comma-separate several addresses), and
   optionally `EMAIL_FROM`, `SMTP_HOST`, `SMTP_PORT`.
4. **Merge to the default branch.** GitHub only runs scheduled workflows from the default branch.
5. **Test it:** go to Actions > Trendspotter weekly email > Run workflow. If a run fails, GitHub emails you.

## Run it locally

```bash
cd trendspotter
pip install -r requirements.txt
python main.py --sample            # renders a sample to out/ with no API calls
cp .env.example .env               # fill in, then: set -a; . ./.env; set +a
python main.py --no-email          # full run, report saved to out/report-<date>.html
python main.py --mode monthly      # force the monthly sweep
```

## Changing what it watches

Everything is in `config.py`: the seed watchlist, TikTok hashtags, RSS feeds, Google News searches,
subreddits, YouTube channel IDs, trigger words, scoring weights, bands and the SA calendar.

## Cost

One run a week, using `claude-opus-5-5` at high effort with up to 45 web searches and 25 page reads. My
rough, unmeasured estimate is US$3-6 a run, so about US$15-25 a month. Check usage in the Anthropic console
after the first two runs. To spend less, set `TRENDSPOTTER_EFFORT=medium` or lower `MAX_WEB_SEARCHES` in
`config.py`. To go deeper, raise them.

The requests have refusal fallback turned on (`fallbacks: "default"`). If the model declines a request, the API
retries it on a fallback model in the same call, so the email still goes out.

## Limits to know

- TikTok, Google Trends and Amazon have no free official API (the brief explains why). Claude reads them through
  web search, so those numbers are directional. A paid data vendor would make them exact.
- Score history is kept in the GitHub Actions cache, not in the repository, so the watchlist stays private.
  GitHub deletes cache entries unused for 7 days, so a free Tuesday job (no API calls) touches the cache to keep
  it alive between Fridays.
- Treat anything at ACT as a prompt for your own review, not as an order. The brief requires a SANS 8124 test
  report before stocking anything.
