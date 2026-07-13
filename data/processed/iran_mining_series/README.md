# Iran mining & minerals series (1961–2022)

Harmonized 2026-07-13 from four raw source folders (`data/raw/usgs-minerals-yearbook/`,
`data/raw/bgs-world-mineral-statistics/`, `data/raw/imidro-iran/`; all immutable, unchanged)
into one combined folder, mirroring the `specialty_goods_series/` pattern. Six of the seven
files here re-copy already-transcribed raw `data.csv` tables through Python's `csv` module
(normalizing quoting only, no numeric changes); one file (`bgs_wms_iran_crosscheck_1970_1974.csv`)
is newly extracted from a previously-unmined 216-page scanned BGS PDF, then **extended the same
day in a second pass** from 5 to 17 commodity sections checked for an Iran row (see the dedicated
BGS section below) as part of a project-wide backlog-clearing round.

## Files

### Pahlavi-to-revolution era (USGS Minerals Yearbook, primary Cold-War-era US government source)

| File | Coverage | What it covers |
|---|---|---|
| `usgs_iran_mineral_production_1961_1980.csv` | 1961–1965, 1968–1970, 1973–1980 (near-continuous; 1966/67 and 1971/72 are real gaps — those two Minerals Yearbook volumes were not in this project's download set) | Iran's annual production of 9 metals (chromite, copper at 4 stages of processing, iron ore, pig iron, crude steel, aluminum, lead at 2 stages, manganese, zinc), 5 nonmetals (barite, cement, gypsum, salt, sulfur) and 2 non-oil mineral fuels (coal, coke). Crude/refined petroleum deliberately excluded — already covered elsewhere in this project. |
| `usgs_iran_commodity_narrative_highlights_1965_1980.csv` | 1965, 1970, 1975, 1980 (one narrative snapshot per USGS volume) | The qualitative "Commodity Review" narrative behind the numbers: Sar Cheshmeh copper deposit's formal 1971 approval ($330M, 30% Iranian Selection Trust/70% Kerman Mining Co.) through its 1980 status (cost ballooned to $1.4B, construction suspended after the Revolution, output redirected to domestic market only); the Isfahan/Aryamehr steel complex's Soviet-financed construction (1965 planning → 1971 trial production → 1975 operational at 750,000 t/yr → 1980 running at less than half capacity on coking-coal supply problems); Qaleh Zari and Minakan copper mines; SIMIRAN's Angouran/Khursk lead-zinc complex; Iralco's Arak aluminum smelter (82.5% IDRO / 12.5% Reynolds US / 5% Pakistan Government); post-revolution chromite export collapse (>230,000t 1977 peak → ~80,000t 1980). |
| `usgs_comparator_argentina_turkey_metals_1968_1970.csv` | 1968–1970 | Argentina and Turkey production of the same core metals (chromite, copper, iron/steel, lead, zinc, manganese, cement), extracted opportunistically from the *same already-downloaded 1970 USGS volume* used for the Iran extraction — zero extra fetch cost, per this project's comparator-inclusion policy. |
| `bgs_wms_iran_crosscheck_1970_1974.csv` | 1970–1974 | British Geological Survey's independent "World Mineral Statistics 1970-74" country-production tables, checked for an Iran row across 17 commodity sections (Chromite, Copper, Iron ore, Lead, Zinc, plus 12 more added in a 2026-07-13 extension: Bauxite, Primary Aluminium, Barium/barite, Coal, Gold, Gypsum, Pig-Iron/Ferro-alloys, Manganese, Molybdenum, Phosphate Rock, Salt, Silver, Sulphur & Pyrites). Iran **has** a row in Chromite, Lead, Barium, Coal, Gypsum, Manganese, Salt, and Sulphur & Pyrites; Iran is **confirmed absent** from Copper, Iron ore, Zinc, Bauxite, Primary Aluminium, Gold, Pig-Iron/Ferro-alloys, Molybdenum, Phosphate Rock, and Silver (logged as genuine BGS coverage/production gaps, not search failures — see caveats and the dedicated section below). |

### Modern bridge (IMIDRO — Iran Mines and Mining Industries Development and Renovation Organization)

| File | Coverage | What it covers |
|---|---|---|
| `imidro_capacity_growth_since_2002.csv` | 2002/03 vs. 2021/22 | Two-point national capacity comparison since IMIDRO's founding: steel production capacity 8 → 43.5 million t/yr (5.4x), copper cathode capacity 190,000 → 450,000 t/yr (2.4x), aluminium billet capacity 216,000 → 770,000 t/yr (3.5x). |
| `imidro_sarcheshmeh_monthly_production_snapshot_2021_22.csv` | one recent Iranian-fiscal-year month + year-to-date vs. prior-year (exact calendar month not labeled in source) | Sarcheshmeh copper complex production by stage — concentrate, anode (at both Sarcheshmeh and its Khatounabad smelter), cathode (refinery and leaching), casting, plus by-products molybdenum and gold/silver refinery sludge. This is the modern-era continuation of the Sar Cheshmeh deposit first described in `usgs_iran_commodity_narrative_highlights_1965_1980.csv`'s 1971/1975/1980 entries. |
| `imidro_new_mineral_reserves_value_2014_2021.csv` | cumulative 2014/15–2021/22 | IMIDRO's own valuation of newly discovered mineral reserves by commodity (gold, iron ore, bauxite, barite, antimony, coal, rare earths, copper, salt, lead+zinc) — quantity, assumed unit price, and total USD value; copper (14 million tons, $16.6B) and iron ore ($5.86B) dominate the $27.8B cumulative total. |
| `imidro_production_performance_2011_2015.csv` | **New 2026-07-13 pass.** FY2011/12–2014/15 (performance, budget, and one-year-ahead plan figures) | Production volume (thousand tons) of Crude Steel, Final Steel Products, Copper Cathode, Aluminum, Coal, and Iron Ore, extracted from IMIDRO's `annual-report-2012-2013.pdf` and `annual-report-2013-2014.pdf` (both cleanly text-extractable, bilingual English/Persian). The two reports' overlapping FY2012/13 "performance" figures match exactly (e.g. Crude Steel 13,422 thousand tons in both), a useful cross-validation. Fills the gap between the Pahlavi-era USGS series (ending 1980) and the previously-extracted 2002/03 and 2021/22 IMIDRO snapshots. |
| `imidro_sales_export_by_group_2011_2015.csv` | **New 2026-07-13 pass.** FY2011/12–2013/14 | Sales and export volume/value by industrial group (Steel, Copper, Aluminum, Mine, Cement, Other), same two source reports. See Caveats below for a real source-side unit-labeling inconsistency between the two editions' export tables. |

## Caveats for the new 2026-07-13 IMIDRO tables

- **A genuine unit-labeling inconsistency in IMIDRO's own source PDFs, preserved not resolved**:
  the `annual-report-2012-2013.pdf` export table labels its value column "(million Dollars)" for
  FY2011/12-2012/13 export data, while `annual-report-2013-2014.pdf`'s export table — covering
  the *same* FY2012/13 figures plus FY2013/14 — labels the identical numbers "(billion IRR)".
  Since the actual printed numbers for the overlapping FY2012/13 column are identical between the
  two editions (Steel: 893 thousand tons / 543 value; Copper: 51 / 839; Aluminum: 140 / 310;
  Mine: 827 / 99 — all match exactly), this is almost certainly a copy-paste unit-label error in
  one of IMIDRO's own report editions (most likely the 2013-14 edition, since 543 million USD is
  a far more plausible steel-export value than 543 billion IRR at that period's exchange rate),
  but **this project does not silently correct a primary source's own labeling error** — both
  `value_unit` labels are preserved exactly as printed in their respective `source_report`-tagged
  rows. Flag this explicitly to any future user before treating the export-value column as
  USD-comparable across both editions.
- **Only 2 of IMIDRO's 11 downloaded raw PDFs contributed structured tables this pass** (the two
  annual reports with clean bilingual text and a repeated "Production/Sales/Export Performance"
  table format). The remaining 8 (2 identical copies of `performance-report-2013-2014`, confirmed
  byte-for-byte identical via `diff` on their extracted text; `actions-report-2015-2016`;
  `exploration-department`; `extensive-exploration-operations`; `exploration-activities-strategy`;
  `imidro-development-last-three-years`; `annual-report-2017-2018`) are narrative-heavy (project
  histories, exploration-strategy prose, 20-year sectoral vision targets) rather than tabular, or
  present their numbers as bar-chart data-labels rather than clean text tables (`annual-report-2017-2018`'s
  Financial Highlights) — reviewed but not converted to CSV this pass, a real logged
  incompleteness rather than an oversight. `annual-report-2021-2022.pdf` was already mined in a
  prior round (see `imidro_capacity_growth_since_2002.csv` etc. above).

## Sar Cheshmeh — no separate narrative dataset exists; folded into the USGS file

The task brief for this harmonization pass referenced "the Sar Cheshmeh copper mine narrative
dataset" as a distinct raw source. No such standalone folder exists in `data/raw/` — Sar
Cheshmeh's narrative history (1965 exploration → 1971 approval → 1975 construction →
1980 revolution-halted status) is embedded directly in
`usgs_iran_commodity_narrative_highlights_1965_1980.csv`'s four Sar Cheshmeh rows, and its
modern-era continuation is in `imidro_sarcheshmeh_monthly_production_snapshot_2021_22.csv`.
Together these two files ARE the Sar Cheshmeh narrative arc across 55+ years; no gap.

## BGS World Mineral Statistics — what was checked and what wasn't

The raw source (`data/raw/bgs-world-mineral-statistics/wms-1970-1974/WMS_1970_1974.pdf`, 216
pages) has **no extractable text layer** (`pdftotext` returns essentially nothing) — every value
in `bgs_wms_iran_crosscheck_1970_1974.csv` was read directly from a `pdftoppm -r 150`/`-r 200`
page render, not OCR'd. A first pass (2026-07-13, earlier round) checked only the 5 highest-value
commodity "Production of X" tables for an Iran row: Chromium (printed p.29), Copper (p.41), Iron
ore (p.74), Lead (p.99), Zinc (p.194).

**Extended 2026-07-13 (later round)**: 12 more commodity "Production of X" tables were checked —
Aluminium & Bauxite (both the Bauxite and Primary Aluminium tables, printed p.1-2), Barium
(barite, p.22), Coal (p.33), Gold (p.62), Gypsum (p.69), Iron/Steel/Ferro-alloys (Pig-Iron table,
p.78), Manganese (p.107), Molybdenum (p.117), Phosphates (p.131), Salt (p.147-148), Silver
(p.158), and Sulphur & Pyrites (p.162-163). Iran has a row (new data added) in **6** of these 12:
Barium, Coal, Gypsum, Manganese, Salt, and Sulphur & Pyrites (two sub-lines: recovered/byproduct
and mined ore). Iran is **confirmed absent** from the other **6**: Bauxite, Primary Aluminium,
Gold, Pig-Iron & Ferro-alloys, Molybdenum, Phosphate Rock, and Silver (7 tables, since Aluminium
& Bauxite covers two) — each absence is plausible and consistent with independent evidence (e.g.
Iralco's aluminium smelter and the Isfahan steel complex hadn't reached production yet in this
window per the USGS commodity narrative; Sar Cheshmeh's molybdenum byproduct stream postdates
1970-74), not a search failure. PDF-page-to-printed-page offset re-confirmed as +6 throughout
(e.g. printed p.147 Salt = PDF p.153).

Combined, **17 of ~35 commodity sections** in this volume have now been checked for an Iran row.
The remaining ~18 (Antimony, Arsenic, Asbestos, Cadmium, Cobalt, Diamond, Diatomite, Feldspar,
Fluorspar, Graphite, Kaolin, Mercury, Mica, Nickel, Platinum, Potash, Sillimanite, Talc,
Tantalum/niobium, Tin, Titanium, Tungsten, Vanadium, Zirconium, and the 10 "Other minerals") were
**not checked** — a real, logged incompleteness, flagged as a next-pass target, though most are
lower-priority given Iran has no known major historical production in most of them. Export/import
tables (the other two-thirds of this publication's title) were not checked at all.

### Chromite disagreement — investigated, not resolved

Per the task brief, the BGS-vs-USGS chromite disagreement flagged in a prior round (BGS's 1970
figure of 220,000t vs. USGS's 120,000t; 1974's 140,000t vs. 175,000t) was re-examined at higher
resolution (`pdftoppm -r 200`) specifically looking for an explanatory footnote (unit basis,
fiscal-year convention, ore-grade adjustment, etc.). **None was found** — Iran's row in BGS's
Chrome Ore production table carries only the generic "*" (estimated) marker applied to roughly
half the countries in that table, with no country-specific footnote (unlike, e.g., Brazil's
"(a) Concentrate" annotation on the same page). The one relevant observation: **every single
Iran chromite value in BGS's table, for all 5 years 1970-74, is marked "estimated"** — meaning
BGS was not working from a direct Iranian customs/production return either, just as USGS's own
"preliminary"/"revised" flags on its Iran chromite figures signal an external estimate. Two
independent external estimates diverging by up to ~1.8x is therefore unsurprising and points to
genuine data scarcity at the source (Iran) rather than a transcription error in either compiling
institution. This does not resolve which number is closer to the truth — both remain in the
CSV as separate rows, consistent with this project's no-silent-resolution rule for disagreeing
sources.

## Caveats — read before charting

- **A genuine cross-source disagreement, preserved not resolved**: BGS's 1970 chromite figure
  for Iran (220,000 tonnes, marked estimate) is nearly double USGS's 1970 figure (120,000
  tonnes, preliminary, from the MYB1970v3 edition); 1974 similarly diverges (BGS 140,000 vs.
  USGS 175,000). Per this project's overlapping-disagreeing-sources rule, both are kept as
  separate lines — do not silently pick one. 1971–1973 chromite and all lead-mine-output years
  are close/consistent between the two sources (1970 lead matches exactly: 22,940 tonnes both
  sources), which is a reassuring cross-validation for the years that DO agree.
- **`usgs_iran_mineral_production_1961_1980.csv`** has one flagged unit ambiguity: "Iron ore
  (gross weight)" for 1968-1970 is recorded as "metric tons or thousand metric tons (unclear in
  source)" — the 1961-65 and 1973-80 entries for the same commodity are unambiguously in
  thousand metric tons, so the 1968-70 figures (1057, 1650, 1858) are almost certainly also
  thousand metric tons, but this was NOT silently assumed — the ambiguity is preserved in the
  `unit` column exactly as found. Several other rows carry `revised`/`estimate`/`preliminary`
  flags directly from the source in the `flag` column — these are the Bureau of Mines' own
  data-quality annotations, not this project's judgment calls.
- **Aluminum, lead-smelter, and sulfur rows have a mid-series naming/methodology shift**
  visible directly in the `commodity` column (e.g. "Aluminum, primary ingot" 1973-75 vs.
  "Aluminum metal, primary ingot" 1976-80; "Sulfur (all forms — refined from ores + elemental
  byproduct)" 1961-65/1973-75 vs. "Sulfur total (native + byproduct of petroleum/gas)"
  1976-1980) — these are the Bureau of Mines' own edition-to-edition terminology changes,
  preserved exactly as printed per-row rather than force-normalized into one label, since the
  underlying accounting basis may differ subtly across editions.
- **`imidro_new_mineral_reserves_value_2014_2021.csv`** is a *valuation* of newly discovered
  reserves (assumed unit price × quantity), not a production series and not a reserves-in-the-
  ground total — do not chart alongside the production tonnage series above without labeling
  the difference (discovered-reserve value vs. actual annual output).
- **State-linked source note**: IMIDRO is an Iranian state industrial-development
  organization; its self-reported capacity/production/reserve figures are used here as the
  best (and in most cases only) available modern data for these specific metrics, consistent
  with `docs/bookkeeping.md` rule 4 (official statistics from a state body are usable but
  should be cross-checked against independent data wherever available) — no independent
  cross-check was found for the 2021/22 IMIDRO figures specifically in this pass.

## Sources

- US Bureau of Mines, *Minerals Yearbook*, Volume III/IV (Area Reports: International),
  editions 1965, 1970, 1975, 1980 — `data/raw/usgs-minerals-yearbook/historical-pre1990-volumes/`
  (archive.org mirror of University of Wisconsin Ecology and Natural Resources Digital
  Collection). US Government publication, public domain.
- British Geological Survey / Institute of Geological Sciences, *World Mineral Statistics
  1970-74: Production, Exports, Imports* (HMSO, 1978) — `data/raw/bgs-world-mineral-statistics/
  wms-1970-1974/WMS_1970_1974.pdf`.
- IMIDRO (Iran Mines and Mining Industries Development and Renovation Organization), Annual
  Report 2021-22 — `data/raw/imidro-iran/statistical-reports/annual-report-2021-2022.pdf`.

Full manifests and extraction methods:
`data/raw/usgs-minerals-yearbook/historical-pre1990-volumes/*/manifest.json`,
`data/raw/imidro-iran/annual-report-2021-22-extraction/manifest.json`. The BGS manifest
(`data/raw/bgs-world-mineral-statistics/wms-1970-1974/manifest.json`) was left untouched per
this project's raw-data-immutability rule — its `extraction_method` field is blank because the
raw PDF had not previously been mined; the extraction method for
`bgs_wms_iran_crosscheck_1970_1974.csv` is instead documented here: `pdftoppm -png -r 100`
(first-round commodities) / `-r 150`–`-r 200` (2026-07-13 extension) page renders of each
commodity's "Production of X" table, read directly with the Read tool (no OCR — the source PDF
has no usable text layer). PDF-page-to-printed-page offset confirmed empirically as +6 (printed
p.25 = PDF p.31; re-confirmed on the extension batch, e.g. printed p.147 Salt = PDF p.153) before
locating each target page. PDF pages used this round: Bauxite/Aluminium 7-8, Barium 28, Coal 39,
Gold 68, Gypsum 75, Pig-Iron 84, Manganese 113, Molybdenum 123, Phosphates 137, Salt 153-154,
Silver 164, Sulphur & Pyrites 168-169.
