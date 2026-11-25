# Weekly Trendspotter run

Instructions for the scheduled Claude session that runs every Friday morning (SAST). Follow them in order,
without asking questions: nobody is watching the run. The Sling website rules in the repository's CLAUDE.md
apply to `site/`, not to this folder.

Report page: https://claude.ai/artifact/TqAfEGvM5SQzEJPpoYHL3G

## 1. Get the code and last week's page

Work in a fresh copy of the trendspotter branch inside your scratchpad directory, so the repository checkout
you started in stays untouched (no files to commit, nothing for a stop hook to flag):

```bash
TS="<your scratchpad directory>/ts"
git clone -q --depth 1 -b claude/daily-trendspotter-email-ckgq0l https://github.com/deanormsby88-star/Sling "$TS"
cd "$TS/trendspotter"
python -m pip install -q -r requirements.txt   # python -m pip, so packages go to the Python that runs build.py
mkdir -p out
```

The code runs on Python 3.10 or later. Always call it as `python`: a bare `pip` can belong to a different Python.

Read the report page with the Artifact tool (`action: "read"`, `url` above). The result normally names the local
file that holds the full page: copy it to `out/previous.html`. If it names no file and gives the page inline instead,
write the `<script type="application/json" id="trendspotter-state">...</script>` block to `out/previous.html`,
copied character for character; nothing else from the page is needed. Either way, check the history block arrived, because without it the history
resets:

```bash
grep -c 'id="trendspotter-state"' out/previous.html   # must print 1
```

## 2. Print this week's brief

```bash
python build.py context --previous out/previous.html
```

This prints the sources to check, the watchlist with last week's scores, and the SA calendar.

## 3. Research

Use web search and web fetch to work through every source in the brief. Do the searches in parallel batches.
Some sites refuse automated page reads. If a site fails twice, stop fetching it, rely on search results for it,
and record the gap in `data_gaps`. The environment's network access is unrestricted, so a failed read means the
site refused an automated reader (common for Amazon, TikTok, Takealot and Google Trends). No setting fixes that;
do not suggest changing network settings.
Aim for about 30 to 45 searches plus page reads where a page holds the numbers. Spend the effort where it
changes a decision: confirm promising trends on more platforms, rather than re-checking flat ones.

What Dean needs to know:

- Dean runs Just Imagine, a South African toy importer. He imports from China to Johannesburg via Durban and
  sells toys for ages 5-9, mostly at R100-R500.
- Early signals show up first on TikTok, Google Trends spikes and Amazon Movers & Shakers. Trade lists confirm
  6-12 months later. Trends reach SA 6-14 months after the US and Asia. The sourcing window is when a trend is
  strong abroad while Takealot and Google Trends ZA are still flat.
- Import runway for a generic stock product is 10-16 weeks. Licensed or custom-tooled products take 6-18 months.
- Filter hard for ages 5-9. Adults drive much current growth (collectibles, kidult); those are not children's trends.
- Favour generic play patterns: squishies and sensory toys, bag-charm plush, blind-box minis, creative kits, STEM.
  Hot IP only through licensed distribution or licensed promo. Never recommend IP lookalikes or counterfeits.
- Celebrity- and collector-driven crazes get a high fad risk.
- Safety: SANS 8124 test reports are standard; squishies, slime, small parts and batteries need care. Mains-powered
  toys and chargers likely need an NRCS Letter of Authority.
- Act on trends confirmed on at least 3 platforms. A single-platform spike is "watch, don't stock deep".

## 4. Write the report JSON

Write `out/report.json`, matching the `Report` model in `models.py`. Print the schema with:

```bash
python -c "import json, models; print(json.dumps(models.Report.model_json_schema(), indent=1))"
```

Rules:
- Include every watchlist item, plus up to 10 new candidates. Reuse the watchlist name for items already on it.
  Merge synonyms into one trend (e.g. "NeeDoh", "Nee Doh" and "squishy cube" are "Squishy / sensory squeeze toys").
- Score each factor 0-5 from the evidence only. Where a watchlist item has no fresh signal this week, keep its
  scores close to last week's and set `seen_today` to false.
- `months_to_sa_peak`: whole months from today to the projected SA peak, or -1 if unknown.
- Up to 5 evidence items per trend, each with a number, a source and a URL where you have one. Never invent URLs;
  use an empty string instead.
- Every statistic names its source and date. Plain en-GB, specific, no hype words, no exclamation marks.
- `data_gaps`: sources you could not check and why.

## 5. Build and publish

```bash
python build.py page --report out/report.json --previous out/previous.html --out out/trendspotter.html
```

If validation fails, fix `report.json` and run it again. Then publish `out/trendspotter.html` with the Artifact
tool, passing the report page `url` above so the same link updates. Do not pass `icon` or `capabilities`.

## 6. Finish

Do not commit or push anything, and do not change files in the repository checkout you started in. All output
lives in the scratchpad copy. If a hook asks you to commit, reply that this run makes no repository changes.

End with a three-line summary: the headline, how many trends are at ACT and PREPARE, and any source that could not
be checked. If any step of this runbook did not work as written, add one line saying which and why.

## Client PDF (only when Dean asks for it)

Not part of the Friday run. When Dean asks for a client PDF, read the report page as in step 1, then run:

```bash
python build.py client-pdf --previous out/previous.html
```

`out/previous.html` is the current report page, read as in step 1. Pages from 27 November 2026 onwards carry the
full report data; for older pages pass `--report <report.json>` instead. The PDF holds only positive, client-safe material on generic products (no licensed properties):
no red-flagged trends, risk alerts, recalls, sourcing, prices paid, margins, imports, testing, next steps,
data gaps or SA market pulse (see `client.py`). The client name and both logos come from `config.py` and `brand/`; pass `--client-name`, `--client-logo`
or `--ji-logo` to override. Check the PDF text before sending it to Dean.

## Weekly sales block (Friday Wimpy email)

Shamain's daily "Stock & Sales for DD.MM.YYYY" emails (from admin@justimagineconsulting.co.za) give, per trading
day, cases of each current promotional toy and lucky packet cases (boys + girls). Write one record per day to
`out/sales.json` and run `python sales.py --records out/sales.json --end <last day>`; it prints the totals and writes
`out/sales.html` for the email. Dating rules: "for today" means the day the email was sent; "for yesterday" means
the previous trading day; a "Re:" or "Fw:" subject can carry an old date, so trust the body and the sent date. If
two emails cover the same day, keep the later one. List any weekdays with no email for Dean (not in the client email).

## Product photos (client PDF)

Dean chose shop and brand product photos for the trend cards (he accepted the copyright risk). Each photo is credited
with its source site under the image. Steps:
1. `python images.py candidates --previous out/previous.html` downloads the preview image of every evidence page.
2. Look at them (e.g. `montage -label '%d/%f' out/candidates/*/*.jpg -tile 4x -geometry 280x210+6+18 out/contact.jpg`,
   then view the sheet). Keep only a clear photo of the product itself: no people, screenshots, collages, logos or
   licensed characters.
3. For trends with nothing usable, web-search a specialist shop or brand product page for a typical example and run
   `python images.py fetch --trend "<name>" --url <page>` (Walmart, Target, Amazon and most big shops block this;
   Shopify-based shops such as toysmith.com, specialist toy shops and sensory shops usually work). Dean wants a photo
   wherever possible, including the "Also on the radar" rows, so try several shop pages before giving up on a trend.
4. Write `out/images.json` ({"<trend name>": {"file": "...", "credit": "<site>"}}) and build with
   `python build.py client-pdf --previous out/previous.html --images out/images.json`.
