# Just Imagine Trendspotter

A daily email at about 06:00 SAST that tracks toy trends for children aged 5 to 9 and scores each one for
sourcing into South Africa. It follows the research brief *Just Imagine Trendspotter: Daily Source Map for
Ages 5-9 Toy Trends*.

This folder is separate from the Sling website. It can be moved to its own private repository as it is.

## What it does each morning

1. **Collects** free Tier 1 signals: trade RSS (The Toy Book, Toy World, Toy News, License Global,
   Kidscreen, Toys n Playthings), Google News searches (SA toys, licensing, sell-outs, recalls, Durban port),
   Reddit parent and toy communities, and any YouTube channels listed in `config.py`. Headlines that contain
   a trigger word ("master toy licence", "sold out", "shortage", "recall", "viral") go first.
2. **Researches** the sources with no free API using Claude with web search: TikTok Creative Center and toy
   hashtags, Google Trends (ZA, US, UK), Amazon Movers & Shakers and Hot New Releases, Takealot best sellers
   and YouTube toy channels.
   - **Mondays** add the weekly deep-dive: US/UK/SA retailer bestsellers, Temu/AliExpress/1688 copy counts and
     price floors, a Reddit sweep, a safety and recall sweep, and the streaming and licensing slate.
   - **The 1st of each month** adds Circana, company investor updates, trade fairs and SA market data. It also
     retires trends that have not been seen for 30 days and score under 35.
3. **Scores** every trend 0-5 on the brief's seven factors. The code, not the model, turns those into a
   score out of 100 and a band: 75+ ACT, 55-74 PREPARE, 35-54 WATCH, under 35 IGNORE. ACT also needs the
   projected SA peak to be at least 4 months away (the import runway). Active safety recalls and
   IP-lookalike-only trends are red-flagged, whatever the score.
4. **Emails** the report in the brief's template: headline, ACT list, rising, watchlist movement (with
   7-day change), licensing pipeline, SA market pulse, risk alerts and the next 60 days of the calendar. The
   footer lists any feeds that failed and any sources Claude could not check.

## Setup (about 10 minutes)

1. **Anthropic API key:** create one at console.anthropic.com.
2. **Gmail app password:** turn on 2-step verification, then create an app password at
   myaccount.google.com/apppasswords. Any other SMTP provider works too; set `SMTP_HOST` and `SMTP_PORT`.
3. **GitHub secrets:** in the repository, go to Settings > Secrets and variables > Actions, then add:
   `ANTHROPIC_API_KEY`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_TO` (comma-separate several addresses), and
   optionally `EMAIL_FROM`, `SMTP_HOST`, `SMTP_PORT`.
4. **Merge to the default branch.** GitHub only runs scheduled workflows from the default branch.
5. **Test it:** go to Actions > Trendspotter daily email > Run workflow. If a run fails, GitHub emails you.

## Run it locally

```bash
cd trendspotter
pip install -r requirements.txt
python main.py --sample            # renders a sample to out/ with no API calls
cp .env.example .env               # fill in, then: set -a; . ./.env; set +a
python main.py --no-email          # full run, report saved to out/report-<date>.html
python main.py --mode weekly       # force the Monday deep-dive
```

## Changing what it watches

Everything is in `config.py`: the seed watchlist, TikTok hashtags, RSS feeds, Google News searches,
subreddits, YouTube channel IDs, trigger words, scoring weights, bands and the SA calendar.

## Cost

It uses `claude-opus-5-5` at medium effort, with up to 20 web searches a day (30 on Mondays) plus up to 10
page fetches. I estimate roughly US$1-2 a day, but this has not been measured yet. Check usage in the Anthropic
console after the first week. To spend less, set `TRENDSPOTTER_EFFORT=low` or lower `MAX_WEB_SEARCHES` in
`config.py`.

The requests have refusal fallback turned on (`fallbacks: "default"`). If the model declines a request, the API
retries it on a fallback model in the same call, so the email still goes out.

## Limits to know

- TikTok, Google Trends and Amazon have no free official API (the brief explains why). Claude reads them through
  web search, so those numbers are directional. A paid data vendor would make them exact.
- Score history is kept in the GitHub Actions cache, not in the repository, so the watchlist stays private. If
  the workflow does not run for 7 days the cache expires, and the history starts again.
- Treat anything at ACT as a prompt for your own review, not as an order. The brief requires a SANS 8124 test
  report before stocking anything.
