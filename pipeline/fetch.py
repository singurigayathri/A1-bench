#!/usr/bin/env python3
"""Check each source for new publications, extract metrics with Gemini, and queue
the results for review. Nothing is written to data/data.csv automatically -
extractions land in data/pending_review.csv until you approve them.

Run locally:  GEMINI_API_KEY=... python3 pipeline/fetch.py
In CI:        see .github/workflows/update.yml (weekly cron)

NOT TESTED against the live endpoints - the selectors below are a starting point
and will need one debugging pass on first run.
"""
import csv, hashlib, json, os, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEEN = DATA / "seen.json"
PENDING = DATA / "pending_review.csv"
KEY = os.environ.get("GEMINI_API_KEY")

SOURCES = [
    {
        "id": "a1_results_center",
        "operator": "a1-at",
        "market": "AT",
        "url": "https://a1.com/investor-relations/results-center/",
        "kind": "pdf_index",
        "link_pattern": r'href="(https://a1\.com/wp-content/uploads/[^"]+\.pdf)"',
        "note": "Segment Austria table carries revenue, service revenue, EBITDA, EBITDAaL, subscribers, churn.",
    },
    {
        "id": "dt_europe_austria",
        "operator": "magenta-at",
        "market": "AT",
        "url": "https://report.telekom.com/interim-report-q3-2025/management-report/"
               "development-of-business-in-the-operating-segments/europe.html",
        "kind": "html",
        "note": "Austria paragraph gives revenue and adjusted EBITDA AL. Update the quarter in the URL each period.",
    },
]

METRIC_PROMPT = """You are extracting financial data from a telecom operator's published report.

Extract ONLY these metrics for the operator's AUSTRIA business (not group, not other countries):
- total_revenue (EUR mn)
- service_revenue (EUR mn)
- ebitdaal (EUR mn) - EBITDA after leases, or adjusted EBITDA AL
- capex (EUR mn, excluding spectrum if separable)
- mobile_subscribers (thousands)
- mobile_churn (percent)

Return a JSON array. One object per metric found, with these keys exactly:
  metric, value, period, basis_note, page_or_section, confidence

Rules, follow them strictly:
- period must be like "FY2025", "9M2025", "Q1 2026". If the figure covers nine
  months, say 9M - do NOT annualise it.
- basis_note: record the operator's own wording for what the figure includes or
  excludes. If it says "adjusted", say so. If restructuring is included, say so.
- confidence: "high" only if the number is stated explicitly in a table or
  sentence. "low" if you derived, inferred, or calculated it.
- If a metric is not present, omit it. Do NOT estimate. Do NOT calculate a
  missing value from other figures.
- Return the JSON array and nothing else. No markdown fences, no commentary.

Report text follows.
---
"""


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "a1-bench/1.0"})
    return urllib.request.urlopen(req, timeout=60).read()


def gemini(text):
    if not KEY:
        sys.exit("GEMINI_API_KEY not set")
    body = json.dumps({
        "contents": [{"parts": [{"text": METRIC_PROMPT + text[:400000]}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }).encode()
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent",
        data=body, headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    out = json.loads(urllib.request.urlopen(req, timeout=180).read())
    raw = out["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M))


def discover(src):
    """Return a list of (label, url) documents for this source."""
    page = get(src["url"]).decode("utf-8", "replace")
    if src["kind"] == "html":
        return [(src["id"], src["url"])]
    links = re.findall(src["link_pattern"], page)
    return [(l.rsplit("/", 1)[-1], l) for l in dict.fromkeys(links)][:4]


def main():
    seen = json.loads(SEEN.read_text()) if SEEN.exists() else {}
    new_rows, checked = [], 0

    for src in SOURCES:
        try:
            docs = discover(src)
        except Exception as e:
            print(f"  ! {src['id']}: discovery failed - {e}")
            continue

        for label, url in docs:
            key = hashlib.sha256(url.encode()).hexdigest()[:16]
            if seen.get(key):
                continue
            checked += 1
            print(f"  new: {src['id']} -> {label}")
            try:
                blob = get(url)
                text = blob.decode("utf-8", "replace")
                if url.endswith(".pdf"):
                    try:
                        import pypdf, io
                        text = "\n".join(
                            p.extract_text() or ""
                            for p in pypdf.PdfReader(io.BytesIO(blob)).pages[:40])
                    except ImportError:
                        print("    skipped: pip install pypdf")
                        continue
                else:
                    text = re.sub(r"<[^>]+>", " ", text)
                for m in gemini(text):
                    new_rows.append([
                        m.get("period", ""), src["market"], src["operator"],
                        m.get("metric", ""), m.get("value", ""),
                        "unknown", m.get("basis_note", ""), src["id"], url,
                        m.get("page_or_section", ""), m.get("confidence", ""),
                        "PENDING_REVIEW",
                    ])
                seen[key] = {"url": url, "source": src["id"]}
            except Exception as e:
                print(f"    ! extraction failed - {e}")

    if new_rows:
        first = not PENDING.exists()
        with open(PENDING, "a", newline="") as f:
            w = csv.writer(f)
            if first:
                w.writerow(["period", "market", "operator_id", "metric_id", "value",
                            "basis_matches_dictionary", "basis_note", "source_type",
                            "source_url", "source_page", "confidence", "status"])
            w.writerows(new_rows)
    SEEN.write_text(json.dumps(seen, indent=2))
    print(f"\n{checked} new documents, {len(new_rows)} rows queued in {PENDING.name}")
    print("Review them, then move approved rows into data/data.csv.")


if __name__ == "__main__":
    main()
