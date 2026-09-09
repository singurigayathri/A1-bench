# What is obtainable, market by market

Read this before designing any view. The dashboard can only show what exists.

## Your competitor is different in every market

Deutsche Telekom is in three of your seven markets. There is no Magenta Bulgaria,
no Magenta Serbia, no Magenta Slovenia, no DT in Belarus.

| Market | Main peer | Second peer | Peer's parent |
|---|---|---|---|
| Austria | Magenta Telekom | Drei | DT / CK Hutchison |
| Bulgaria | Vivacom | Yettel Bulgaria | United Group / PPF |
| Croatia | Hrvatski Telekom | Telemach Croatia | DT / United Group |
| Belarus | MTS Belarus | — | state / MTS |
| Slovenia | Telekom Slovenije | Telemach Slovenija | state / United Group |
| Serbia | Telekom Srbija | Yettel Serbia | state / PPF |
| North Macedonia | Makedonski Telekom | Telekabel | DT / private |

United Group divested its Serbian business (SBB) in 2025. Confirm who holds it now
before adding a Serbia peer row.

## What each source publishes PER MARKET

| Source | Markets | Revenue | EBITDA(aL) | Capex | EBIT | OPEX | Subs | ARPU | Freq |
|---|---|---|---|---|---|---|---|---|---|
| A1 Group | all 7 | yes | yes | yes | yes | derive | yes | NO from FY2025 | quarterly |
| Deutsche Telekom | AT, HR, MK | yes | adjusted only | no | no | no | no | no | quarterly |
| United Group | BG, HR, SI | yes | adjusted only | yes | no | derive | RGUs | growth % only | quarterly |
| Hrvatski Telekom | HR | yes | yes | yes | yes | yes | yes | yes | quarterly |
| Telekom Slovenije | SI | yes | yes | yes | yes | yes | yes | check | quarterly |
| PPF / Yettel | BG, RS | check bond reports | check | check | no | no | check | no | check |
| Telekom Srbija | RS | annual report | check | check | check | no | check | no | annual |
| Belarus peers | BY | realistically nothing | | | | | | | |

Hrvatski Telekom is separately listed on the Zagreb exchange and files full quarterly
accounts. It is by far your best-documented competitor. Build Croatia first, not Austria.

## The metrics you asked for, and where they actually live

**Free cash flow — group level only.** Nobody publishes segment FCF, including A1.
Your FCF comparison is A1 Group vs DT Group vs United Group. Not per market.

**OPEX — not published by anyone per market, but derivable.** Revenue minus EBITDA is a
usable OPEX proxy and is consistent across operators because both inputs are published.
Label it as derived, not reported.

**EBIT — A1 publishes it per market, most peers do not.** Only Croatia and Slovenia
will have a peer EBIT to compare against.

**Capex — A1 and United Group publish per market, DT does not.** So capex intensity works
in Bulgaria, Croatia and Slovenia, and not in Austria or North Macedonia.

**ARPU — effectively dead.** A1 stopped disclosing it per segment from FY2025. United Group
publishes growth percentages, not levels. Use revenue per subscriber that you calculate
yourself, from published revenue and published subscriber counts, and label it as derived.

## Design consequence: build two levels, not one

**Group level** — A1 Group vs DT Group vs United Group vs PPF. Full P&L, FCF, leverage,
capex intensity. Everything you asked for exists here.

**Market level** — seven markets, but only revenue, EBITDA(aL) and subscribers are
comparable, and only where a peer publishes at all. Capex in three markets. EBIT in two.

Trying to force a full P&L comparison into the market level is the one thing that will
sink this project. The data does not exist and no tooling creates it.

## Basis differences you must carry

- DT and United Group both report ADJUSTED EBITDA(aL), stripping special factors.
  A1's segment figures include restructuring — EUR 96 mn in Austria in 2025 alone.
- A1's Austrian revenue includes low-margin international transit, roughly EUR 155 mn,
  which peers do not carry. A1's own report separates this out.
- Serbia and North Macedonia report in local currency. Normalise to EUR and state
  whether you used spot or period-average.
- Reporting periods differ. DT and United Group publish 9M and H1 figures; A1 publishes
  quarterly. Never compare a nine-month figure to a full year.
