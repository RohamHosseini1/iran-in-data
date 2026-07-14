# iran-industry-energy-enrich progress log

## 2026-07-14T11:00Z — start
Read `_shared-context.md` and `docs/bookkeeping.md`. Cluster: Iran industrial & energy
production (motor vehicles; natural gas / oil-product production & consumption;
cigarette/sugar/tea/textile-cloth manufacturing output). No sub-agents used, all work
done directly in this session.

## 2026-07-14T12:30Z — inventory of existing raw data
Found substantial *already-downloaded but not yet mined* primary-source material from
earlier sessions:
- `data/raw/sci-amar/sci-cpi-yearbook/` — SCI Statistical Yearbook 1399 (2020/21), 6
  chapters, retrieved via Wayback (amar.org.ir direct access confirmed still SSL-blocked).
- `data/raw/cbi-iran/cbi-annual-review-wayback/` — CBI (Central Bank of Iran) Annual
  Review, English edition, 23 fiscal years 1379-1401 (2000/01-2022/23), full PDFs,
  properly manifested by a prior agent.
- `data/raw/mimt-iran/statistics-reports/` — MIMT daily bulletins: CONFIRMED (again) to
  contain only licensing/permit counts + stock-exchange + trade-price data, NO physical
  production statistics. Not useful for this cluster; not re-downloaded further.
- `data/raw/iran-data-portal/energy-environment-tables/` — oil production/exports,
  energy balance sheet, natural gas consumption 1991-2006, oil-product imports
  1991-2006, NPC petrochemical production 1996-2006 (the exact thin chart this task
  targets for extension).

## 2026-07-14T13:05Z — new SCI yearbook chapters downloaded
Downloaded chapters 6 (Mining & Quarrying), 7 (Oil & Gas), 8 (Manufacturing
Industries) of SCI Statistical Yearbook 1399 via the same Wayback pattern as the
already-held chapters (amar.org.ir/Portals/1/yearbook/1399/{6,7,8}.pdf).
-> `data/raw/sci-amar/yearbook-industry-mining-oilgas/`
FINDING: Chapter 8 (Manufacturing Industries) is an ISIC-classified LARGE-ESTABLISHMENT
SURVEY (establishment counts, employment, value-added, investment) — it does NOT
publish physical production quantities of specific consumer products (no cigarette/
sugar/tea/cloth physical-unit table exists in the modern SCI yearbook, confirmed by
grep across the full chapter text). Chapter 7 (Oil & Gas) DOES have exactly the
physical-quantity tables needed: 7.3 (oil-product production by refinery),
7.4 (oil-product consumption), 7.7 (natural gas production), 7.10/7.12 (gas
consumers/petrochemical production) — but as a single yearbook edition these show only
a sparse ~6-year window (1380/1385/1390/1394-1399) with the newest 2-3 years blank
("000"/not yet finalized).

## 2026-07-14T13:45Z — CBI Annual Review mined for a continuous annual series (KEY FIND)
Extracted (via `pdftotext -layout` + a custom Python table parser, all locally, no
sub-agents) two statistical-appendix tables that appear in EVERY edition of the CBI
Annual Review with a 5-year rolling window, giving near-full annual coverage once all
23 editions are combined:
- **Table 8 "Domestic Consumption of Oil Products"** (source: Ministry of Petroleum) —
  gas oil, fuel oil, gasoline, kerosene, LPG, other, total, thousand barrels/day.
  Continuous annual coverage **1996/97-2017/18** (22 years). GENUINE GAP, not a
  retrieval failure: every edition from 1398 (2019/20) onward shows ".." (not
  available) for 2018/19 onward — Ministry of Petroleum evidently stopped/paused
  publishing this granular series in CBI's own appendix from that point; documented,
  not fabricated.
- **Table 10 "Consumption of Natural Gas"** (source: National Iranian Gas Company/NIGC)
  — residential+commercial+industrial, power plants, major industries, transportation,
  total, billion cubic meters. Coverage **2005/06-2011/12 and 2015/16-2022/23** (gap
  2012/13-2014/15: those 3 editions' appendices do not contain this exact table,
  confirmed by direct grep, not an extraction bug).
- Also captured Table 7 "Iran Oil Export" (crude oil / oil products / total, thousand
  b/d) as a bonus, most years 1996/97-2021/22.
- **Motor vehicle production**: CBI's "Selected Products and Industrial Exports"
  narrative section, sourced to SAPCO (Supplying Automotive Parts Co.) through 2018/19
  and to the Ministry of Industry, Mine & Trade from 2019/20 on, gives a total
  motor-vehicle-manufactured figure (thousand units, light+heavy) nearly every year
  2009/10-2022/23, plus a passenger-car sub-count most years. From 2021/22 onward CBI
  also publishes a dedicated "Table 24/22 Production Performance of Selected
  Industries" (source: MIMT) with Passenger cars (thousand) alongside petrochemicals/
  crude steel/steel products/cement — all physical Iranian-government production data.
- Wrote tidy long-format CSVs to `data/processed/iran_industry_energy_enrich_series/`.

## 2026-07-14T14:15Z — cigarette / refined sugar / processed tea / textile cloth: BLOCKED
Checked every avenue available: SCI Yearbook Ch.8 (no physical-quantity table, see
above), CBI Annual Review appendix (only agricultural raw sugar-cane/sugar-beet/
green-tea-leaf tonnage under "Estimated Production of Major Farming Crops" — a
different, already-FAOSTAT-covered concept, NOT manufactured/refined output; "Sale of
cigarettes" appears only as an excise-tax REVENUE line, not a physical unit),
Iran Data Portal (no Industry/Manufacturing topic page exists; checked
Economic & Financial Affairs page directly — no such table), MIMT daily bulletins (no
production data of any kind, confirmed again), IranOpenData (targeted web search, no
hit). Conclusion: no continuous Iranian-government physical-production series for
these four specific manufactured commodities was found via any available route in this
session. Reporting as genuinely blocked, not fabricating or substituting.

## 2026-07-14T14:30Z — writing staging + processed outputs
Writing tidy CSVs to `data/processed/iran_industry_energy_enrich_series/` (derived data,
correctly placed in data/processed/ not data/raw/ since it's a table-extraction from
already-manifested raw PDFs, not a new download of its own), with the derivation method
documented in that folder's README.md rather than a separate raw manifest, plus
`data/processed/chart_registry_staging/enrichment_industry_energy.csv`.

## 2026-07-14T14:45Z — done, all deliverables written
- `data/raw/sci-amar/yearbook-industry-mining-oilgas/` (3 new PDFs + manifest.json)
- `data/processed/iran_industry_energy_enrich_series/` (4 CSVs, 289 data rows total + README.md)
- `data/processed/chart_registry_staging/enrichment_industry_energy.csv` (4 proposal rows: 1 extends
  motor-vehicle-production, 1 extends natural-gas production+consumption, 2 new oil-product
  production/consumption charts)
- `SOURCES.md` — appended dated section
- `logs/downloads/iran-industry-energy-enrich.log` — full attempt trail written incrementally
No sub-agents spawned at any point. Cigarette/refined-sugar/processed-tea/textile-cloth cluster
explicitly reported as blocked (not fabricated) — see README "What was NOT found" section and the
SOURCES.md entry above.
