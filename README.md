# A1 competitive benchmarking dashboard

A working prototype plus the scaffold you need to build the real thing in AI Studio.

Open `index.html` in a browser to see it. It runs with no server and no keys, on
placeholder data.

```
data/peers.json         15 operators across 6 markets, with data source per operator
data/metrics.json       metric dictionary - your definitions and the comparability traps
data/data.template.csv  blank data file, correct schema
data/data.sample.csv    same schema filled with placeholder values, drives the prototype
template.html           the dashboard source
build.py                regenerates index.html with the CSV embedded
AISTUDIO_PROMPT.md      the prompt to paste into AI Studio Build
```

Everything in `data.sample.csv` is invented. Nothing in this repo is A1 or competitor data.

## Getting API keys

No key is needed for the prototype. You need them for the live version.

**Twelve Data** — twelvedata.com. Free tier gives roughly 800 calls a day, which is
plenty if you cache properly. This is the one provider that actually covers Wiener
Börse, Zagreb and Ljubljana. Sign up, copy the key from the dashboard. Verify each
ticker through their `/symbol_search` endpoint before trusting `peers.json` — the
tickers there are unverified guesses.

**EODHD** — eodhd.com. Around €60/month for fundamentals. Worth it only if Twelve
Data's coverage of the smaller exchanges turns out to be thin. Test the free tier
against Telekom Slovenije and Makedonski Telekom before you pay for anything.

**Gemini** — aistudio.google.com. If you build inside AI Studio, `GEMINI_API_KEY` is
configured for you automatically as a server-side secret. You only need to generate a
key manually if you run the app outside AI Studio.

**ECB reference rates** — no key, no signup. Public feed, use it for RSD, MKD and BGN
conversion rather than a commercial FX provider.

Put every key in the AI Studio Secrets panel, never in the code. If you ever see a key
in the browser's network tab or JS bundle, stop and move it server-side.

## Steps

1. Open `index.html`. Decide whether the matrix is the view you actually want before
   building anything real.
2. Fix `peers.json`. Verify the tickers, correct anything wrong about ownership, add
   or drop operators. Ticker confidence is marked `low` where I am guessing.
3. Review `metrics.json` and cut it down. Twelve metrics is already more than a first
   version needs — six is fine.
4. Fill `data.template.csv` for one market, one quarter, by hand. Austria, three
   operators, six metrics is 18 rows. Do it manually so you learn where the numbers
   actually live in each report.
5. Rename it to `data.sample.csv`, run `python3 build.py`, reopen `index.html`.
6. Show that to someone in Group Controlling. Ask them specifically whether the
   EBITDAaL treatment is right and whether the peer set is the one the CEO cares about.
7. Only then open AI Studio and follow `AISTUDIO_PROMPT.md`.
8. Push to GitHub from AI Studio's GitHub tab, deploy to Cloud Run.

## Two things that will decide whether this works

**Tower spin-off.** A1 spun off its tower business in September 2023. Tower costs now
sit in lease expense rather than above EBITDA. Peers that still own towers keep them
below the line. Comparing raw EBITDA margin across the two structures is wrong by
several points in every market — that is why the dictionary uses EBITDAaL. If a peer
only discloses EBITDA and no lease expense, mark the value `basis_matches_dictionary =
no` rather than converting it with an assumption.

**ARPU is not comparable off the shelf.** M2M inclusion, prepaid deactivation windows
and whether interconnect sits in the numerator all differ by operator. The
`basis_note` column exists for this. A dashboard that shows ARPU without the basis
note will get taken apart the first time someone senior challenges it.

## Licensing

Market data licences generally restrict redistribution. A prototype on your own machine
is fine. The moment it is an internal A1 tool with multiple viewers, that is a different
licence tier — worth checking the terms before it gets shared around.
