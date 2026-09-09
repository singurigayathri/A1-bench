# A1 competitive benchmarking dashboard
 
Compares A1 Telekom Austria Group against the number one operator in each of its seven
markets, using figures published in investor relations reports.
 
**Live dashboard: [index.html](./index.html)**
 
## What is in here
 
```
index.html          the dashboard - open this
austria.html        Austria detail view with a like-for-like basis toggle
data/peers.json     7 markets, each with its number one competitor and data source
data/metrics.json   metric definitions and the comparability traps for each
data/data.sample.csv the actual figures, long format, one row per observation
template.html       dashboard source
build.py            rebuilds index.html after the CSV changes
pipeline/fetch.py   checks IR sites for new reports and extracts with Gemini
COVERAGE.md         what data exists per market - read before designing anything
AISTUDIO_PROMPT.md  prompt for rebuilding this in Google AI Studio
```
 
## Data status
 
A1 figures for all seven markets are real, from the A1 Group Annual Financial Report 2025.
Peer figures exist for Austria and Croatia only. The other five markets are deliberately
empty rather than estimated.
 
Two known issues flagged in the data:
 
- The Croatia peer figure is **HT Group**, which includes Montenegro and Bosnia. Replace it
  with Hrvatski Telekom's Croatia segment before publishing.
- A1 Serbia's 2025 capex includes EUR 100 mn of 5G spectrum, so its capex intensity is an
  artefact rather than an investment surge.
## There is no financial data API for this
 
Country-segment telecom financials are not in any commercial data API at any price. Twelve
Data, EODHD and similar providers cover share prices and group-level fundamentals only, and
Vienna requires their Pro tier regardless. This was tested, not assumed.
 
The data lives in published PDFs and HTML pages, free and public:
 
| Source | Markets | What it gives |
|---|---|---|
| A1 Group IR | all 7 | revenue, service revenue, EBITDA, EBITDAaL, EBIT, capex, subscribers |
| Deutsche Telekom | AT, HR, MK | country revenue and adjusted EBITDA AL, quarterly, HTML |
| Hrvatski Telekom | HR | full quarterly accounts, separately listed |
| United Group | BG, HR, SI | revenue, adjusted EBITDAal, capex, RGUs per market |
| RTR / national regulators | per market | subscriber and market data, open data formats |
| ECB | — | reference exchange rates, no key |
 
The only API key in this project is a Gemini key, used by `pipeline/fetch.py` to read
documents. The dashboard itself needs no key.
 
## Two traps built into the metric dictionary
 
**Tower spin-off.** A1 spun off its towers in September 2023, so tower costs sit in lease
expense rather than above EBITDA. Peers that still own towers keep them below the line.
Raw EBITDA margin is not comparable across the two structures, which is why the dictionary
uses EBITDAaL throughout. Hrvatski Telekom separated its towers in September 2025, so
Croatia is the cleanest comparison available.
 
**Adjusted versus reported.** Deutsche Telekom and United Group publish *adjusted* figures
that strip special factors. A1's segment figures include restructuring - EUR 96 mn in
Austria in 2025 alone. On reported figures A1 Austria's EBITDAaL margin looks 12 points
behind Magenta; corrected for basis it is 6.5 points. Always check `basis_note`.
 
**ARPU is gone.** A1 stopped disclosing segment ARPU from FY2025, citing competition
sensitivity. Only a group figure including M2M remains, and that number falls when M2M
grows, which is dilution rather than pricing. Calculate revenue per subscriber yourself
and label it as derived.
 
## Licensing
 
Everything here comes from freely published investor relations material. Redistribution
terms still apply once this becomes an internal tool with multiple viewers.
 
