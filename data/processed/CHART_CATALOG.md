# Chart Catalog

The content plan for this database, before any frontend work. Every entry below is a candidate
chart backed by data that actually exists in `data/processed/` (or is being added right now) —
nothing here is aspirational. Organized by theme; within each theme, ordered roughly by how well
it serves the project's stated priority: **the Pahlavi era, especially 1941–1979 under Mohammad
Reza Shah, is the focal point** — comparator-country data matters only insofar as it illuminates
an Iran series we actually have.

**Pahlavi-coverage rating**, used throughout:
- 🟢 **Excellent** — continuous or near-continuous data spanning most/all of 1925–1979
- 🟡 **Good** — solid coverage for 1961–1979 (18 of the 38 Pahlavi years) via WDI/FAOSTAT's 1960/61
  start, but 1925–1960 is thin or missing
- 🟠 **Thin** — only sparse benchmark-year or narrative data pre-1979, being actively filled by the
  primary-source extraction effort (see below)
- 🔴 **None yet** — no Pahlavi-era data currently in the database (either a genuine gap to hunt, or
  a category that's inherently modern — noted per-item)

---

## 1. Macro fundamentals

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| **GDP per capita, deep history** | `macro_maddison.csv` | all 17 | annual 1950–2022, sparse benchmarks back to year 1 | 🟢 Excellent — this is the flagship "long run" chart, entire Second Pahlavi era covered annually |
| GDP per capita, modern detail | `macro_wdi.csv` (NY.GDP.PCAP.CD etc.) | all 17 | 1960–2025 | 🟡 Good (1961–79 only) |
| GDP growth, inflation (CPI + deflator), unemployment | `macro_wdi.csv` | all 17 | **1960–2025** (verified: WDI's inflation & FX-rate series both start 1960, not later as initially assumed) | 🟡 Good |
| Official exchange rate (rial/USD) | `macro_wdi.csv` (PA.NUS.FCRF) | all 17 | 1960–2025 | 🟡 Good, **plus** one hand-extracted 1960 snapshot (75.75 rials/$, from the WB report's currency-equivalents page) anchoring pre-1960 |
| **Government budget (revenue vs. expenditure)** | `pahlavi-era-primary-extraction` — budgeted expenditures (1955–60), actual revenues/expenditures (1958–59), government revenue summary (1962/63–71/72), ordinary budget current expenditure (1962/63–71/72), summary of central govt. operations incl. deficit financing (1962–1973) | IRN only | **1955–1974, near-continuous** across three overlapping WB report vintages | 🟢 Excellent — now reaches the 1972 prelim actuals/1973 budget estimate, i.e. the opening of the oil-price-shock years; updated from the earlier 5-year-window rating now that the 1971 and 1974 WB statistical appendices have also been extracted |
| Money supply / banking aggregates | `pahlavi-era-primary-extraction` — changes in money supply (1957–59), banking statistics of the private sector (1957–59), monetary survey/stock levels (1963/64–69/70), changes in money & quasi-money/flow (1964/65–70/71), movements in monetary aggregates (1963–1973) + `macro_wdi.csv` | IRN + comparators | **1957–1974, near-continuous** (extraction) + 1960– (WDI) | 🟢 Excellent — five overlapping WB tables now cover both stock levels and flow/factor decomposition through the early oil-boom years |
| Cost-of-living index, 7 major cities | `pahlavi-era-primary-extraction/wb1960-cost-of-living-index-1955-1959` | IRN only | **Dec 1955–Sept 1959, real Bank Melli data** | 🟢 Excellent for its narrow window — the earliest genuine Iran price index in the database |
| Income/wealth inequality (Gini, top shares) | `wid-world`, `swiid-inequality` (not yet harmonized into `data/processed/`) | all 17 | WID has Iran 1900–2025; SWIID has 55 years, 1969–2023 | 🟡 Good once harmonized — WID's 1900+ coverage is a genuine Pahlavi-era win, worth prioritizing in the next harmonization pass |
| Sovereign debt / external debt | `pahlavi-era-primary-extraction/wb1960-external-public-debt-summary-1959` (stock as of Sept 1959 + service schedule projected 1960/61–1973/74) + `macro_wdi.csv` (1970–) | IRN + comparators | 1959 snapshot + projected schedule, then WDI 1970– | 🟠 Thin→🟡 improving — the Table 20 extraction that was flagged as "not reached" is now done (single snapshot + forward schedule, not an annual actuals series, so still short of a true time series) |
| Fiscal narrative, long-run context | `pahlavi-era-primary-extraction/iranica-fiscal-system-narrative-series-1921-1979` | IRN only | 1921–1979, irregular (single years/periods/decade-averages) | 🟡 Good as narrative scaffolding, not a chartable annual series on its own — best used as text annotations alongside the WB point-series above |
| Government budget, primary Persian legal texts | `data/raw/majlis-historical-budget-laws/lamtakam-mirror-1301-1363` | IRN only | FY1301, 1341, 1357–1363 — **not continuous**, large gap years remain (1302–1340, 1342–1356, 1359, 1364–1370) | 🟠 Thin, real primary documents but sparse; a good target for a further lamtakam.com gap-filling pass |

## 2. Food & agriculture micro — the founding theme of this project

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| **Citrus production (oranges, tangerines)** | `bridged_series/citrus_production_iran_1950_2024.csv` + `agriculture_qcl_production.csv` | IRN (+ all via QCL) | **1950–2024, near-continuous** — the flagship bridge, WB primary data joined to FAOSTAT | 🟢 Excellent |
| Chicken/poultry meat production | `agriculture_qcl_production.csv` | all with FAOSTAT | 1961–2024 | 🟡 Good (1961–79), but genuinely 🔴 for 1941–60 — the 1950 WB agricultural table has NO poultry line at all, which is itself a real historical finding (industrial poultry farming likely wasn't statistically tracked in Iran before the 1960s) rather than a gap in our search |
| Wheat, barley, rice, other grain production | `agriculture_qcl_production.csv` + `pahlavi-era-primary-extraction/wb1960-agricultural-production-1950-1958` | IRN (+ all via QCL) | **1950–2024, continuous** | 🟢 Excellent |
| Food supply per capita (consumption proxy, incl. poultry/citrus) | `agriculture_fbs_food_balances.csv`, `agriculture_fbsh_food_balances_historic.csv` | all with FAOSTAT | 1961–2023 | 🟡 Good |
| Producer prices (farm-gate, incl. specific crops) | `agriculture_pp_producer_prices.csv` (1991–) + `agriculture_pa_prices_archive_pre1991.csv` (1966–90) | all with FAOSTAT | **1966–2025, continuous** | 🟡 Good (starts 1966, still misses 1941–65) |
| Food CPI | `food_cpi_faostat.csv` | all with FAOSTAT | 2000–2025 only | 🔴 None yet for Pahlavi era from this source — but the 1955–59 cost-of-living index above (§1) already covers "Foodstuffs" as 54% of the 1950s basket, a usable proxy |
| Bread/flour, wheat subsidy history | `data/raw/iran-bread-subsidy` (notes, not yet a time series) | IRN only | Islamic Republic era only (2018–2022 reform events) | 🔴 Necessarily IRI-only — Iran's modern bread-subsidy *system* as such postdates the Pahlavi era; the 1950–58 wheat *production* series above is the right Pahlavi-era proxy for this theme |

## 3. Oil & energy

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| **Oil production** | `owid_indicators.csv` (`oil-production-by-country`) | all with OWID | **1900–2024, continuous** | 🟢 Excellent — covers the D'Arcy Concession era, both Pahlavi reigns, and today in one series |
| **Oil revenue to government** | `pahlavi-era-primary-extraction` (oil revenues 1955–1963 + oil exports/revenues 1963–1971) | IRN only | **1955–1971, near-continuous** | 🟢 Excellent — this was arguably the single most important Pahlavi-era series to get right (oil-revenue-funded state spending is the central story of the era), and it's now solid across the whole 1955–71 window |
| CO2 emissions per capita | `owid_indicators.csv` | all with OWID | 1900s–2024 (OWID's CO2 series is also very deep) | 🟢 Excellent, though of secondary interest for a 1940s-70s focus |
| Natural gas production | — | — | Not yet in `data/processed/`; NIGC's own site was unreachable this round | 🔴 Gap — NIGC (est. 1965) is itself a Second Pahlavi-era institution, worth another hunting pass |

## 4. Trade

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
Ocean trade (non-petroleum exports/imports) | `pahlavi-era-primary-extraction/wb1962-ocean-trade-1950-1960` | IRN only | 1950/51–1959/60 | 🟢 Good for the 1950s specifically |
| Balance of payments (full breakdown) | `pahlavi-era-primary-extraction/wb1971-balance-of-payments-summary-1963-1970` | IRN only | 1963/64–1969/70 | 🟢 Good |
| Exports/imports by detailed commodity | `pahlavi-era-primary-extraction/wb1960-exports-by-commodities-1956-1959` + `wb1960-imports-by-commodities-1956-1959` (1956/57–58/59) + FAOSTAT Trade Indices (1961–) | IRN (+ all via FAOSTAT) | **1956–present**, WB extraction bridges directly into the FAOSTAT 1961 start | 🟢 Excellent — the Tables 16–17 extraction flagged as a follow-up target is now done |
| International transactions (pre-BOP-format capital flows, oil, foreign aid) | `pahlavi-era-primary-extraction/wb1960-international-transactions-1953-1959` | IRN only | 1953–1959 | 🟢 Good — extends the trade/BOP picture 10 years earlier than the 1963–70 balance-of-payments summary above |
| Trade as % of GDP | `owid_indicators.csv` | all with OWID | check exact start year in file | 🟡 likely Good, not yet spot-checked |
| Maritime/port trade profile | `unctad-maritime/irn/` (not yet harmonized) | IRN + 10 comparators | modern only (UNCTAD profiles are current-day snapshots) | 🔴 Necessarily modern-only — no equivalent historical UNCTAD product exists |

## 5. Demographics

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| **Population** | `macro_maddison.csv`, `owid_indicators.csv` | all | annual from 1950 (Maddison), OWID even deeper | 🟢 Excellent |
| Life expectancy, child mortality | `owid_indicators.csv` | all with OWID | check exact start; OWID's Gapminder-sourced demographic series often run 1900+ | likely 🟢, not yet spot-checked |
| **Census data (1956, 1966, 1976)** | — | IRN only | **Confirmed unavailable via the two most obvious routes** — Iran Data Portal's census hub and year-specific pages are navigation-only with no linked files (double-checked directly, including one promising-looking file that turned out to be an unrelated modern yearbook mislabeled by URL); IPUMS International's Iran holdings are confirmed to start at 2006 (nothing for 1956/66/76/86/96) | 🔴 **Priority gap, genuinely hard.** All three of these censuses are pure Pahlavi-era (1976 is the last one before the revolution). Remaining untried avenues: UN Statistics Division's historical Demographic Yearbook print archive (pre-digital editions sometimes carry national census totals even without microdata), university census microfilm collections (Princeton/Michigan/LSE Middle East collections), and the SCI provincial compendium already in `data/raw/iran-provincial-statistics/` may have retrospective census-year comparison tables worth mining before searching further afield |
| Education (literacy, enrollment) | `owid_indicators.csv` (`mean-years-of-schooling-long-run`) | all with OWID | some pre-1979 rows exist (15 rows found in the pre-1941 scan) | 🟠 Thin — worth checking exact Iran years; the White Revolution's Literacy Corps (1963) is a natural policy-timeline anchor for this chart once coverage is confirmed |

## 6. Industry & mining

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| Industrial production (textiles, cement, sugar) | `pahlavi-era-primary-extraction` (industrial production 1954–59 + import-dependence by product ~1970) | IRN only | 1954–1959, plus a 1970 snapshot | 🟢 Good for the 1950s window |
| Mineral production by commodity | `usgs-minerals-yearbook/iran/` (not yet harmonized) | IRN + 4 comparators | **2016–2023 only** — USGS's modern digital archive; older (1960s-70s) USGS Minerals Yearbook editions were not checked this round | 🔴 for Pahlavi era — worth checking if USGS has pre-1990s Iran editions digitized, since USGS has published this series since the 1930s |

## 7. Labor

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| Minimum wage history | `ilo-minimum-wage`, `iran-labor-council` (not yet harmonized) | IRN + comparators | ILO series starts 1995; the hand-compiled Iran series starts even later (Nowruz decisions, recent years only) | 🔴 Necessarily IRI-only so far — Iran had no comparable statutory minimum-wage regime in the same form under the Pahlavis; worth checking the WB documents' banking/employment tables for a period-appropriate wage proxy instead |
| Employment structure, labor force participation | `ilostat` (comparators-trade-mopup), `owid_indicators.csv` | all | check exact Iran start year | not yet assessed |

## 8. Housing

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| Housing price index | `cbi-iran`, `sci-amar` | IRN only | modern decades only (housing price indices are a late-20th-century statistical practice everywhere, not an Iran-specific gap) | 🔴 Necessarily modern-only |

## 9. Modernization & infrastructure (new this round)

Encyclopaedia Iranica / Wikipedia / GFRAS / Encyclopedia.com narrative extraction — none yet
harmonized into `data/processed/`, but real, citation-backed, and pre-1970 in every case (filling
gaps WDI's own telephone/air-passenger series don't reach):

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| **Cinema — theaters & attendance, "before and after" 1979** | `data/raw/iran-media-history/iranica-cinema-history/` | IRN only | 1932–1988 | 🟢 Excellent — 142 (1959)→453 (1975)→255 burned/closed pre-revolution→198 (1979), a vivid single-chart story |
| Telecom buildout (telegraph, telephone, radio, TV, post) | `data/raw/iran-telecom-history/` | IRN only | 1858–1990, benchmark years (1913/14, 1953, 1965, 1975/76, 1979, 1988/89) | 🟢 Good — sparse but spans the full Pahlavi period |
| Press/newspapers & periodical count | `data/raw/iran-media-history/iranica-press-newspapers/` | IRN only | 1898–1988 | 🟢 Good |
| Iran Air passengers, employees, revenue | `data/raw/iran-aviation-history/encyclopedia-com-iranair-company-history/` | IRN only | 1946–2003 | 🟢 Good — fills the pre-1970 gap in WDI's air-passenger series directly |
| Civil aviation fleet & founding events | `data/raw/iran-aviation-history/iranica-aviation-history/` | IRN only | 1913–2007 | 🟢 Good |
| White Revolution — Literacy Corps reach & illiteracy rate | `data/raw/iran-white-revolution-corps/iranica-literacy-corps/` | IRN only | 1958–1979 | 🟢 Good — natural overlay for the 1963 White Revolution timeline anchor |
| White Revolution — Health Corps & health spending | `data/raw/iran-white-revolution-corps/iranica-behdari-health-system/` | IRN only | 1920–1978 | 🟢 Good |
| White Revolution — Extension/Development Corps | `data/raw/iran-white-revolution-corps/gfras-extension-development-corps/` | IRN only | 1964–1979 | 🟡 Good, thinner (single source) |

## 10. Specialty exports & consumption goods (new this round)

FAOSTAT has zero caviar/sturgeon and zero carpet data at any date (confirmed absence, not a gap in
search) — these charts exist only via Encyclopaedia Iranica narrative extraction plus modern
trade-press/official compilations. Also not yet harmonized:

| Chart | Data | Countries | Iran coverage | Pahlavi rating |
|---|---|---|---|---|
| **Carpet export value, long run** | `data/raw/iran-carpet-exports/iranica-carpet-export-narrative-series-1960-1988/` + `carpet-export-value-post1990-compiled/` | IRN only | 1960/61–1988, then non-continuous headline years 1994–2025 | 🟢 Good for Pahlavi window, 🔴 gap 1989–1993 and no continuous 1995–2016 run (see Known Gaps) |
| Tobacco monopoly revenue & scale | `data/raw/iran-tobacco-monopoly/iranica-tobacco-monopoly-narrative-series-1890-1995/` | IRN only | 1890–1995, non-continuous | 🟢 Good — includes a genuine pre-Pahlavi (Qajar-era 1890 Tobacco Régie) anchor point |
| Sugar consumption & import origin | `data/raw/iran-sugar-tea-history/iranica-sugar-narrative-and-table1/` | IRN + 8 historical trade partners (incl. Russia, France, UK, British India) | 1890–2002, non-continuous; one real 1906/07–1913/14 embedded table | 🟢 Good — the 1906–1914 table is pre-Pahlavi (Qajar era) |
| Tea cultivation area, production, imports | `data/raw/iran-sugar-tea-history/iranica-tea-cultivation-narrative-series-1895-1984/` | IRN only | 1895–1984, non-continuous | 🟢 Good |
| Caviar/sturgeon production & exports | `data/raw/iran-caviar-exports/` (3 sources: CITES 2006, EUMOFA 2010–18, Shilat 2013/14–2024/25) | IRN (+ CHN/ARM/RUS/USA/VNM/EU via EUMOFA) | modern only, 2006–2025 | 🔴 None yet for Pahlavi era — genuinely modern-only phenomenon (Caspian aquaculture pivot postdates wild-catch collapse) |

---

## The policy-timeline link (correlation/causation scaffolding)

Every `timeline/*.csv` row already carries an `economic_domains` tag (`fx`, `inflation`, `oil`,
`trade`, `housing`, `food`, `banking`, `fiscal`, `labor`). `scripts/harmonize/timeline_lookup.py`
(new) is the mechanical link between a chart and its overlay events: given a country + one or more
domain tags + a date range, it returns the matching timeline rows, ready to render as annotation
markers on that chart. This keeps the linkage systematic and low-maintenance — add a domain tag to
a timeline row once, and every chart tagged with that domain picks it up automatically, rather than
hand-maintaining a chart-to-event mapping that drifts out of date.

For the Pahlavi era specifically, `timeline/iran.csv` already has anchor events that should overlay
directly onto the charts above once they're chart-ready: 1951 oil nationalization → oil production/
revenue charts; 1953 coup → GDP/FX charts; 1963 White Revolution → agriculture production charts
(land reform) and education charts (Literacy Corps); 1973 oil price shock → oil revenue and GDP
charts; 1977 anti-profiteering campaign → the cost-of-living index chart.

## Data-quality notes (the "clean out low-quality data" pass)

- **FAOSTAT `Flag` column** (kept in `agriculture_qcl_production.csv` etc.) marks estimated ("E"),
  imputed ("I"), and official ("A"/blank) values. When charting, prefer surfacing this distinction
  rather than treating all FAOSTAT numbers as equally authoritative — e.g. Iran's 2024 orange
  production is flagged "I" (imputed), not an official reported figure.
- **IMF WEO's `is_actual` column** (in `macro_imf_weo.csv`) already distinguishes real outturns from
  the Fund's 5-year-ahead forecasts — make sure any chart using WEO data doesn't silently plot
  forecast years as if they were history.
- **The citrus bridge's 1958→1961 discontinuity** (documented in `bridged_series/README.md`) is a
  real, unresolved gap between two source methodologies — flagged, not smoothed over.
- No wholesale data-quality problems found yet in a first pass; the 2.8M-row processed layer hasn't
  had a systematic anomaly sweep (e.g. year-over-year outlier detection) — worth doing once the
  Pahlavi-era extraction settles, since that's when it'll be easiest to spot a bad join.

## Next actions, in priority order (Iran-first, Pahlavi-first)

1. **Done across rounds to date**: 33 primary-source tables now extracted and verified from the World
   Bank archives (39-document pool), Encyclopaedia Iranica, and Esfahani-Pesaran/Mohaddes-Pesaran —
   government budget and money supply/banking are now near-continuous 1955–1974 (see §1 above);
   trade-by-commodity, international transactions, and external debt (the previously-flagged
   Tables 14–17/20 follow-up batch) are all done; new modernization/infrastructure (§9) and
   specialty-export-goods (§10) themes added; Majlis primary budget-law texts and the Stanford
   "Iran in Charts" budget dashboard added. See `DATA_INVENTORY.md` §2, §8, §17, §18 for full detail.
2. Hunt specifically for the 1956/1966/1976 census data — still the single highest-value known gap,
   confirmed genuinely hard rather than just unsearched (see `DATA_INVENTORY.md` §9).
3. Fill Majlis budget-law year-gaps via the proven lamtakam.com search-plus-pagination method (current
   gaps: 1302–1340, 1342–1356, 1359, 1364–1370) — same methodology, high probability of more finds.
4. Harmonize WID.world (1900+ Iran inequality coverage), the modernization/specialty-goods raw finds
   (§9–§10, all still **[R]** not **[P]**), and the USGS/UNCTAD comparator-matched sources.
5. Extract the companion tables flagged in the 1971/1974 WB statistical-appendix manifests as
   known follow-ups (revenue detail, expenditure functional breakdown, banking-system balance
   sheets) — same documents already in hand, same proven methodology.
6. Check whether USGS has pre-1990s Iran Minerals Yearbook editions.
7. Spot-check OWID's exact Iran start years for life expectancy, education, and trade-share-of-GDP
   (flagged above as "not yet assessed") to finish rating every row in this catalog.
