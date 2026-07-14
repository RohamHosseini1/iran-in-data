# Iran primary agriculture series (CBI Annual Review + SCI/Iran Data Portal)

Independent Iranian-official second source for FAOSTAT's Iran (IRN) agriculture charts, per the
project's "same measure => multi-source" rule. Two source families, both ultimately attributed to
the **Ministry of (Jihad-e-)Agriculture** and/or the **Statistical Centre of Iran (SCI)**:

1. **CBI Annual Review appendix tables** (`cbi_annual_review_*.csv`) — mined from the 23 editions of
   the Central Bank of Iran's English-language Annual Review already sitting in
   `data/raw/cbi-iran/cbi-annual-review-wayback/` (editions 1379-1401 / 2000/01-2022/23, retrieved via
   Wayback Machine by a prior agent). Every single edition carries two structured appendix tables:
   - **"Estimated Production and Area under Cultivation of Major (Farming and Horticultural)
     Crops/Products"** — area (thousand ha) + production (thousand tons), two years per edition
     (current + prior), for wheat, barley, rice, corn, cotton, sugar beet, sugar cane, tea, oilseeds,
     tobacco, pulses, potatoes, onions, pistachio, and (from ~2010 editions onward) citrus fruits,
     grapes, apples.
   - **"Livestock Products"** — red meat, milk, poultry, eggs, honey (thousand tons), five years per
     edition (rolling window).
   Both are explicitly sourced "Ministry of Agriculture Jihad" / "Deputy of Livestock Affairs" in
   every edition. Because editions overlap (each year typically appears in 2+ editions for the crop
   table, up to 5 for the livestock table), the series is internally cross-checked, not a single
   blind transcription.

2. **SCI Statistical Yearbook chapter tables, mirrored by Iran Data Portal (Syracuse University)**
   (`iran_data_portal_sci_yearbook_series.csv`) — `Wheat-Production.xlsx` gives a **1977/78-2013/14
   (Iranian year 1356-1392), 37-point** wheat production series sourced in-file to "Ministry of
   Agriculture" — the longest single-crop time series found in this hunt, extending 22 years earlier
   than the CBI table's 1999 start. Three more files give 8-point (1991,1996,2001-2006) national
   totals for red meat/milk, chicken meat/egg, and livestock slaughtered by species.

## What was NOT reachable

`maj.ir` (Ministry of Agriculture Jihad) and `amar.org.ir` (Statistical Centre of Iran) were both
unreachable directly from this environment (connection refused / immediate failure), consistent with
prior agents' notes in `SOURCES.md`. No Wayback Machine snapshot of a maj.ir "آمارنامه کشاورزی"
(Agricultural Statistics Yearbook) page was found via web search in the time available. See
`logs/downloads/iran-primary-agriculture.log` for the full attempt log.

## Schema

`cbi_annual_review_crop_production_area.csv`: `country_iso3, indicator_id, item, element, crop_slug,
year, value, unit, source_dataset, source_edition, source_column, notes`. `year` is the Gregorian
start-year of the Iranian farming year as printed in the CBI table (e.g. CBI's "2020/21" -> `year =
2020`). Where multiple CBI editions report a different value for the same (crop, year) — i.e. a
revision between the "current" and a later "prior" printing — the earliest-reported ("current
column, earliest edition") value is used as the primary `value`, and **all** reported variants are
preserved verbatim in `notes` for auditability. 128 of the ~300 (crop, year) cells have such a
revision note; most are small (<5%) and a handful are large (see Known divergences below).

`cbi_annual_review_livestock_products.csv`: same idea, `product_slug` instead of `crop_slug`, `value`
= median of all editions reporting that (product, year), `n_editions_reporting` records how many
editions concur, `notes` lists all reported variants when they disagree.

`iran_data_portal_sci_yearbook_series.csv`: `country_iso3, indicator_id, item, element, year, value,
unit, source_dataset, year_iranian, notes`.

`faostat_vs_cbi_comparison.csv`: `category, commodity_slug, year, faostat_value_t,
iran_official_value_t, diff_pct` — every (commodity, year) where both this dataset and
`data/processed/agriculture_qcl_production.csv` (FAOSTAT QCL, already in this repo) have a value.

All values are converted to base units (`ha` for area, `t` for production/weight) to match FAOSTAT's
own units, multiplying the CBI table's thousand-ha/thousand-ton figures by 1,000.

## FAOSTAT vs. Iran-official cross-validation

Median absolute difference (`|iran_official - faostat| / faostat`, percent) across all overlapping
years, computed by `faostat_vs_cbi_comparison.csv`:

| Commodity | Years compared | Median \|diff\| % | Read |
|---|---:|---:|---|
| eggs | 27 | 0.0 | agree |
| poultry_meat | 27 | 0.0 | agree |
| potatoes | 23 | 2.0 | agree |
| honey | 19 | 0.9 | agree |
| milk | 27 | 0.8 | agree |
| red_meat | 27 | 2.9 | agree |
| onions | 23 | 4.0 | agree |
| sugar_beet | 23 | 4.0 | agree |
| sugar_cane | 23 | 4.3 | agree |
| wheat | 23 | 4.8 | agree |
| rice | 23 | 5.8 | agree |
| tobacco | 20 | 6.4 | agree |
| barley | 23 | 5.0 | agree |
| cotton | 23 | 8.2 | agree (seed-cotton basis) |
| tea | 15 | 12.7 | mild divergence |
| corn_maize | 18 | 16.4 | mild divergence |
| pistachios | 23 | 21.8 | **notable divergence, non-monotonic** |
| citrus_fruits | 12 | 33.5 | **large, systematic divergence** |
| apples | 12 | 40.6 | **large, systematic divergence** |
| grapes | 12 | 48.7 | **large, systematic divergence** |

**Agreement (12 of 19 commodities, most row/field crops and all livestock products):** wheat,
barley, rice, cotton, sugar beet, sugar cane, tobacco, potatoes, onions, plus red meat, milk, poultry
meat, eggs, and honey all show <10% median divergence from FAOSTAT — strong independent confirmation
of FAOSTAT's Iran numbers for exactly the commodities where Iran is a globally significant producer
and where a bad Iran estimate would most distort FAOSTAT's world totals.

**Known divergences (not adjudicated, both series kept):**
- **Apples, grapes, citrus fruits**: CBI's figures run systematically *higher* than FAOSTAT's, and
  the gap *widens over time* — near 0% in 2010-2013, growing to 40-95% by 2018-2021. This is a
  striking, real, and reportable pattern (not noise): either Iran's own reporting methodology
  changed (CBI's own 2020/21 table footnote notes "a change in methods of data collection" for that
  year, though the widening trend clearly predates it), or FAOSTAT's IRN horticultural estimates have
  not been revised at the same pace as Iran's official figures. Flagging for the frontend as a
  genuine cross-source disagreement, not a data-entry error.
- **Pistachios**: divergence swings both directions across years (from -73% to +134%), unlike the
  fruits above which diverge in one consistent direction. This pattern (adjacent years alternating
  sign) is consistent with pistachio's well-known **alternate bearing** (biennial high/low yield
  cycle) combined with the two sources plausibly attributing a given harvest to different calendar
  years at the margin — flagged, not corrected, since untangling which source's year-attribution is
  "right" would require a primary source neither this project nor the two inputs currently has.
- **Corn/maize and tea**: moderate (13-16%) divergence, no strong trend — ordinary estimate
  variance between an FAO model-adjusted figure and a national administrative figure.

## Known data-quality caveats

- The CBI table's own **2020/21 footnote** (appearing in the 1399 and 1400 editions) states: "Due to
  the change in methods of data collection resulting in notable changes in data on 'production' and
  'area under cultivation'... the performance in the farming year 2020/21 may not be compared with
  previous years." This is Iran's own methodology-break admission, not a reading error.
- Iran's "farming year" (سال زراعی) spans two Gregorian calendar years (roughly autumn-to-late-summer)
  and different Iranian sources are not perfectly consistent in which Gregorian year they attribute a
  given crop year to at the margin — see the pistachio note above. `year` in these CSVs is always the
  Gregorian **start**-year of the Iranian year as printed by the source (CBI's own dual-format
  "2020/21" labels, or a straight +621 conversion of a bare Iranian calendar year where the PDF only
  printed the Iranian numeral) — never inferred or shifted by this agent.
- `oilseeds` and `pulses` are extracted and included in `cbi_annual_review_crop_production_area.csv`
  for completeness but were **not** proposed as chart extensions in
  `chart_registry_staging/enrichment_iran_agriculture.csv`, because they are basket/aggregate
  categories without a single unambiguous 1:1 FAOSTAT item match.
- The 8 producer-price/production-cost xlsx files in `data/raw/iran-data-portal-agriculture/` were
  downloaded but not harmonized in this pass (production/area was prioritized per the mission brief);
  a future pass could extend this to the "prices" angle FAOSTAT also covers (Producer Prices PP).
