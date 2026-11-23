# Weekly Trendspotter run

Instructions for the scheduled Claude session that runs every Friday morning (SAST). Follow them in order,
without asking questions: nobody is watching the run. The Sling website rules in the repository's CLAUDE.md
apply to `site/`, not to this folder.

Report page: https://claude.ai/artifact/TqAfEGvM5SQzEJPpoYHL3G

## 1. Get the code and last week's page

Work on the trendspotter branch itself, so the checkout stays clean. `out/` is git-ignored, so the run leaves
nothing uncommitted. If an earlier step copied `trendspotter/` onto another branch with
`git checkout FETCH_HEAD -- trendspotter`, the `git cat-file` line undoes that before switching.

```bash
cd "$(git rev-parse --show-toplevel)"     # the Sling repository checkout
# Undo a copied-in trendspotter/ folder, but only when the current branch does not track it:
git cat-file -e HEAD:trendspotter/build.py 2>/dev/null || { git rm -r -q --cached --ignore-unmatch trendspotter; rm -rf trendspotter; }
git fetch -q origin claude/daily-trendspotter-email-ckgq0l:refs/remotes/origin/claude/daily-trendspotter-email-ckgq0l
git switch -q -C claude/daily-trendspotter-email-ckgq0l origin/claude/daily-trendspotter-email-ckgq0l
cd trendspotter
python -m pip install -q -r requirements.txt   # "python -m pip" so packages go to the same Python that runs build.py
mkdir -p out
```

The code runs on Python 3.10 or later. Always call it as `python` and install with `python -m pip`: a bare `pip`
can belong to a different Python version.

Read the report page with the Artifact tool (`action: "read"`, `url` above). Then write
`trendspotter/out/previous.html`:

- If the result names a local file that holds the full page, copy that file.
- If it names no file (this happens when the page is small), write the
  `<script type="application/json" id="trendspotter-state">...</script>` block from the returned HTML into
  `out/previous.html`, copied character for character. Nothing else from the page is needed.

Check it with `grep -c 'id="trendspotter-state"' out/previous.html` (it must print 1). The block carries the
score history, so never skip this step: without it, history resets.

## 2. Print this week's brief

```bash
python build.py context --previous out/previous.html
```

This prints the sources to check, the watchlist with last week's scores, and the SA calendar.

## 3. Research

Use web search and web fetch to work through every source in the brief. Do the searches in parallel batches.
Aim for about 30 to 45 searches plus page reads where a page holds the numbers. Spend the effort where it
changes a decision: confirm promising trends on more platforms, rather than re-checking flat ones.

If web fetch fails for a site because the host does not resolve or is not allowed, the session's network policy
is blocking page reads. Stop trying further sites after two such failures and carry on with web search alone.
Add one `data_gaps` entry saying page reads were blocked, and mention it in the final summary so the network
setting can be changed.

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

End with a three-line summary: the headline, how many trends are at ACT and PREPARE, and any source that could
not be checked. Do not commit or push anything.

A stop hook in the cloud environment may ask for uncommitted changes to be committed and pushed. Do not do it.
Run `git status --short`: after step 1 it should print nothing, because `out/` is git-ignored. If it shows files,
say which in the summary and leave them uncommitted.
