# AI Studio build prompt

Paste the block below into Google AI Studio → Build. Upload `data/peers.json`,
`data/metrics.json` and `data/data.template.csv` first so it builds against the real schema.

Build it in two passes. Pass 1 is the prompt below. Only after pass 1 renders correctly
do you send the pass-2 additions at the bottom — asking for everything at once produces
a shallower app.

---

## Pass 1 — paste this

```
Build a competitive benchmarking dashboard for a telecom group that operates in six
markets: Austria, Slovenia, Croatia, Serbia, Bulgaria and North Macedonia.

DATA MODEL — use exactly this, do not redesign it.
Three config/data files, which I am uploading:
- peers.json: markets, each with a list of operators. One operator per market has
  is_us: true. Each operator has a source_type and, if listed, a ticker.
- metrics.json: the metric dictionary. Each metric has id, label, unit,
  higher_is_better, definition, and a watch_out string. Some have
  group_level_only: true and must be excluded from per-market views.
- A CSV of observations in long format, one row per observation, columns:
  quarter, market, operator_id, metric_id, value, basis_matches_dictionary,
  basis_note, source_type, source_url, source_page, entered_on, status.

Do not invent a wide table. Every value is one row. Never hardcode figures in the
source code — all values come from the CSV.

MAIN VIEW — a matrix, and make this the hero of the page.
Rows are the six markets. Columns are the metrics from metrics.json where
group_level_only is not true. Each cell shows our gap to the strongest competitor in
that market for that metric, computed as:
  gap = (our_value - best_peer_value) * (higher_is_better ? 1 : -1)
so a positive gap always means we are ahead. Colour cells on a diverging scale, one
hue for ahead and a different hue for behind, with a near-neutral fill when the gap is
close to zero. Scale the colour intensity per metric, not globally, because a 5-point
margin gap and a 0.3-point churn gap are not the same size. Show our rank within the
market as a small second line inside each cell, like "2 of 3".

Clicking a market row expands an operator-level table underneath it, showing every
operator's raw value for every metric in that market and quarter.

CONTROLS: a quarter selector. Nothing else in pass 1.

DATA HONESTY — these are requirements, not nice-to-haves:
- If any operator's basis_matches_dictionary is not "yes" for a metric, show a small
  "basis differs" tag on that metric row in the detail table, with basis_note in the
  tooltip.
- Show a metric's definition and watch_out text on hover over its column header.
- If any row in the loaded data has status "ILLUSTRATIVE", show a persistent warning
  banner at the top of the page saying the figures are placeholders.
- Where a market is missing a value, render "n/a". Never interpolate, never carry
  forward a previous quarter, never fill a gap with an average.

STYLE: dense analyst tool, not a marketing page. Neutral cool background, white cards,
one typeface with tabular numerals, generous whitespace between blocks but tight inside
tables. No gradients, no drop shadows, no icons. The colour in the matrix should be the
only strong colour on the page.

Responsive down to mobile. Keyboard focus visible.
```

## Pass 2 — send these one at a time, after pass 1 works

```
Add a server-side route that fetches the latest share price and market cap from the
Twelve Data API for every operator in peers.json that has a ticker, using the API key
stored in secrets as TWELVEDATA_API_KEY. Cache the response for 15 minutes. Show the
results in a separate strip above the matrix, clearly labelled as market data rather
than reported fundamentals. Handle the case where a ticker returns nothing — show
"not covered" rather than failing the whole page.
```

```
Add a currency normalisation layer. Values in RSD, MKD and BGN must be converted to
EUR before comparison. Fetch reference rates from the European Central Bank's public
euro reference rate feed. Add a toggle for spot rate versus period-average rate, and
show which one is active. Never silently mix the two.
```

```
Add an upload panel where I can drop a quarterly investor-relations PDF. Use Gemini to
extract the metrics defined in metrics.json into rows matching the CSV schema, and for
each extracted value also capture the page number and the operator's own stated
definition of that metric. Show the extracted rows in an editable review table with the
source page beside each value. Nothing is written to the dataset until I click Confirm.
Any value Gemini is not confident about must be flagged, not guessed.
```

```
Add an export button that downloads the current matrix as an .xlsx file with one sheet
for the matrix and one sheet for the underlying observations including source_url and
source_page.
```

## Prompting notes

- Give it the schema, not a description of the schema. It follows uploaded files far
  more reliably than prose.
- When it gets something wrong, use annotation mode — highlight the element and describe
  the fix — rather than re-prompting from scratch. Re-prompting tends to regenerate
  working parts too.
- If it starts inventing sample data, tell it explicitly: "read values only from the
  uploaded CSV, render n/a when absent."
