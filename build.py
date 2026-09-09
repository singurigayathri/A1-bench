#!/usr/bin/env python3
"""Generate a single-file dashboard prototype with data embedded, so it opens
by double-click without a local server. Re-run after editing data/data.sample.csv."""
import csv, json, pathlib

root = pathlib.Path(__file__).parent
peers = json.loads((root / "data/peers.json").read_text())
metrics = json.loads((root / "data/metrics.json").read_text())
with open(root / "data/data.sample.csv") as f:
    rows = list(csv.DictReader(f))

payload = json.dumps({"peers": peers, "metrics": metrics, "rows": rows}, separators=(",", ":"))
tpl = (root / "template.html").read_text()
(root / "index.html").write_text(tpl.replace("/*__DATA__*/null", payload))
print("wrote index.html")
