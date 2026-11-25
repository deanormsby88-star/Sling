"""Product photos for the client PDF.

Step 1 (script): collect candidate photos for each trend in the client PDF.
  python images.py candidates --previous out/previous.html      (or --report report.json)
  Downloads each evidence page's preview image (og:image) into out/candidates/<n>-<trend>/,
  resized to a JPEG, and prints the list with each image's source site.

Step 2 (the person or Claude session): look at the candidates and write out/images.json:
  {"<trend name>": {"file": "out/candidates/1-slime/2.jpg", "credit": "The Toy Insider"}, ...}
  If no candidate fits, search the web for a shop or brand product page showing a typical
  example and try it:  python images.py fetch --trend "<trend name>" --url <product page>
  (big-box sites such as Walmart, Target and Amazon usually block this; specialist shops work).
  Pick a clear photo of the product itself: no people, no screenshots or collages, no
  licensed characters (the report covers generic products only). Leave a trend out if
  nothing suitable was found. Then: python build.py client-pdf --images out/images.json
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import client
import history
from models import Report

HERE = Path(__file__).parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
OG = [re.compile(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]+content=["\']([^"\']+)', re.I),
      re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\']', re.I)]


def _get(url: str, limit: int = 3_000_000) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(limit)


def og_image(page_url: str) -> str | None:
    html = _get(page_url, 600_000).decode("utf-8", "ignore")
    for rx in OG:
        m = rx.search(html)
        if m:
            return urllib.parse.urljoin(page_url, m.group(1).replace("&amp;", "&"))
    return None


def site_name(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    return host


def to_jpeg(src: Path, dst: Path, width: int = 700) -> bool:
    """Resize to a modest JPEG so the PDF stays small. Uses ImageMagick when present."""
    if shutil.which("convert"):
        r = subprocess.run(["convert", f"{src}[0]", "-fuzz", "4%", "-trim", "+repage", "-resize", f"{width}x{width}>", "-background", "white",
                            "-flatten", "-quality", "82", str(dst)], capture_output=True)
        return r.returncode == 0 and dst.exists()
    shutil.copy(src, dst)
    return True


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def candidates(report: Report, out: Path) -> list[dict]:
    found = []
    for i, (t, *_rest) in enumerate(client.client_trends(report), 1):
        folder = out / f"{i}-{slug(t.name)}"
        folder.mkdir(parents=True, exist_ok=True)
        n = 0
        for e in t.evidence:
            if not e.url.startswith("http"):
                continue
            try:
                img = og_image(e.url)
                if not img:
                    continue
                raw = folder / f"raw-{n + 1}"
                raw.write_bytes(_get(img))
                jpg = folder / f"{n + 1}.jpg"
                if to_jpeg(raw, jpg):
                    n += 1
                    found.append({"trend": t.name, "file": str(jpg.relative_to(HERE)), "credit": site_name(e.url),
                                  "page": e.url})
                raw.unlink(missing_ok=True)
            except Exception as exc:  # noqa: BLE001 - a failed source just means one fewer candidate
                print(f"  skipped {e.url[:70]}: {type(exc).__name__}", file=sys.stderr)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["candidates", "fetch"])
    ap.add_argument("--trend", help="fetch: trend name")
    ap.add_argument("--url", help="fetch: product page URL")
    ap.add_argument("--previous")
    ap.add_argument("--report")
    ap.add_argument("--out", default=str(HERE / "out" / "candidates"))
    a = ap.parse_args()
    if a.command == "fetch":
        folder = Path(a.out) / f"extra-{slug(a.trend)}"
        folder.mkdir(parents=True, exist_ok=True)
        try:
            img = og_image(a.url)
            if not img:
                print("No preview image on that page.", file=sys.stderr)
                return 1
            raw = folder / "raw"
            raw.write_bytes(_get(img.replace("http://", "https://", 1)))
        except Exception as exc:  # noqa: BLE001
            print(f"Could not fetch {a.url[:70]}: {exc}", file=sys.stderr)
            return 1
        jpg = folder / f"{len(list(folder.glob('*.jpg'))) + 1}.jpg"
        ok = to_jpeg(raw, jpg)
        raw.unlink(missing_ok=True)
        print(f"{a.trend} | {jpg.relative_to(HERE) if ok else 'failed'} | {site_name(a.url)}")
        return 0 if ok else 1
    if a.report:
        report_json = Path(a.report).read_text()
    else:
        report_json = history.report_from_page(Path(a.previous).read_text()) if a.previous else None
    if not report_json:
        print("No report data found.", file=sys.stderr)
        return 1
    out = Path(a.out)
    shutil.rmtree(out, ignore_errors=True)
    found = candidates(Report.model_validate_json(report_json), out)
    (out / "candidates.json").write_text(json.dumps(found, indent=1))
    for f in found:
        print(f"{f['trend']} | {f['file']} | {f['credit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
