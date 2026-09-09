# AI Studio build prompt — seven markets, live data

Replace `YOURNAME/a1-bench` below with your actual repo path before pasting.

The repo must be **public** for the raw URL to work without authentication. If it has to
be private you need a token and a server-side route, which is a harder build — start public.

Your data URLs will be:

```
https://raw.githubusercontent.com/YOURNAME/a1-bench/main/data/peers.json
https://raw.githubusercontent.com/YOURNAME/a1-bench/main/data/metrics.json
https://raw.githubusercontent.com/YOURNAME/a1-bench/main/data/data.sample.csv
```

Open one in a browser first. If you can see the file, AI Studio will be able to fetch it.

---

## Pass 1 — paste this into AI Studio Build

```
Build a competitive benchmarking dashboard for A1 Telekom Austria Group, which operates
in seven markets: Austria, Bulgaria, Croatia, Belarus, Slovenia, Serbia and North
Macedonia.

DATA — fetch all three of these at load time. Do not hardcode any figure anywhere in the
source code. Every number rendered must come from these files.
  https://raw.githubusercontent.com/YOURNAME/a1-bench/main/data/peers.json
  https://raw.githubusercontent.com/YOURNAME/a1-bench/main/data/metrics.json
  https://raw.githubusercontent.com/YOURNAME/a1-bench/main/data/data.sample.csv

peers.json has a markets array. Each market has an operators list where exactly one
operator has is_us true, and a primary_peer object naming that market's number one
competitor, with a phase field of phase1 or phase2.

metrics.json has a metrics array: id, label, unit, higher_is_better, definition,
watch_out, and sometimes group_level_only true.

The CSV is long format, one row per observation: quarter, market, operator_id, metric_id,
value, basis_matches_dictionary, basis_note, source_type, source_url, source_page,
entered_on, status.

VIEW 1 — the landing view, a matrix.
Rows are the seven markets. Columns are the metrics where group_level_only is not true.
Each cell shows A1's gap to that market's primary_peer:
  gap = (a1_value - peer_value) * (higher_is_better ? 1 : -1)
so positive always means A1 ahead. Colour on a diverging scale, one hue for ahead and a
different hue for behind, near-neutral when the gap is close to zero. Scale colour
intensity per metric, not globally. Show A1's rank within the market as a small second
line inside each cell.

Markets with phase2 have almost no peer data yet. Render those cells as "no peer data"
in a muted style — not as zero, not as an error. Sort phase1 markets to the top.

VIEW 2 — clicking a market row expands a detail panel beneath it showing every
operator's raw value for every metric, with the basis_note beside each.

CONTROLS: a period selector built from the distinct quarter values present in the CSV.

DATA HONESTY — requirements, not nice-to-haves:
- Where basis_matches_dictionary is not "yes", show a warning marker on that value and put
  basis_note in the tooltip. Several peers report ADJUSTED figures while A1 reports
  including restructuring. The dashboard must make that visible, never smooth it over.
- Show each metric's definition and watch_out on hover over its column header.
- Never compare values whose quarter fields differ. If A1 has FY2025 and the peer has
  9M2025, show both with their period labels and suppress the computed gap.
- Missing data renders as "n/a". Never interpolate, never carry forward, never average.
- Show a "data as of" line using the newest entered_on value in the CSV.
- If any row has status ILLUSTRATIVE, show a persistent banner saying the figures are
  placeholders.

STYLE: a dense analyst tool for an executive audience, not a marketing page. Cool neutral
background, white cards, one typeface with tabular numerals. No gradients, no shadows, no
icons. The matrix colour should be the only strong colour on the page. Responsive down to
mobile, visible keyboard focus.
```

## Pass 2 — send these one at a time, only after pass 1 renders correctly

```
Add a like-for-like toggle. When on, adjust A1's figures to match the peer reporting
basis: add back restructuring where a restructuring_addback value exists in the data, and
exclude international transit revenue where an excl_international value exists. Label the
active basis clearly above the matrix. Never apply the adjustment silently.
```

```
Add a trend view. Select a market and a metric, then show A1 against that market's primary
peer across all available periods as a line chart. Mark any period where the reporting
basis differs between the two operators.
```

```
Add a group-level view as a separate tab: A1 Group against Deutsche Telekom Group and
United Group on free cash flow, net debt to EBITDA, and capex intensity. Label it clearly
as group level, because free cash flow is not published per market by any operator,
including A1.
```

```
Add an export button that downloads the current view as .xlsx, with one sheet for the
matrix and one for the underlying observations including source_url and source_page.
```

## Notes

- If AI Studio invents sample data, tell it plainly: "read values only from the fetched
  CSV, render n/a when a value is absent."
- Use annotation mode for fixes — highlight the element and describe the change.
  Re-prompting from scratch tends to regenerate the parts that already worked.
- The app needs no API key. It reads a public file. Keys live only in the GitHub Action.
