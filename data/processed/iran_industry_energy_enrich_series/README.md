# Iran industry & energy enrichment series (2026-07-14)

Produced by agent `iran-industry-energy-enrich` per the mission: find continuous
Iranian-government series to extend a set of thin (5-7 year) Iran industrial/energy
charts into decade-spanning series. All data below is derived from Iranian
government/central-bank sources, either fetched directly this session or re-mined
from PDFs already downloaded (and separately manifested) by earlier sessions of this
project. Schema for every file: `country_iso3, indicator_id, year, value, unit,
source_dataset, original_period_label, source_report_file[, notes]`. `year` is the
Gregorian start-year of the Iranian fiscal year (e.g. SH 1388 -> 2009); the exact
Iranian-calendar label is preserved in `original_period_label`.

## Files

### `motor_vehicle_production_cbi_2009_2022.csv` (19 rows)
Total light+heavy motor vehicle production and passenger-car sub-count, Iranian FY
2009/10-2022/23 (SH 1388-1401). Source: Central Bank of Iran (CBI) Annual Review,
"Selected Products and Industrial Exports" narrative section, itself sourced to SAPCO
(Supplying Automotive Parts Company) through the 2018/19 edition and to the Ministry
of Industry, Mine & Trade (MIMT) from the 2019/20 edition onward; cross-confirmed
where available against CBI's own "Table 24/22 Production Performance of Selected
Industries" appendix table (present in the 2021/22 and 2022/23 editions). Hand-
extracted and manually verified from `pdftotext -layout` output of each PDF (already
held at `data/raw/cbi-iran/cbi-annual-review-wayback/`) -- NOT run through an
unverified automated parser, given the narrative (non-tabular) format for most years.
Gaps: 2011 (SH1390) and 2013 (SH1392) have no stated total-vehicle figure in either
edition's narrative (checked directly, genuinely not printed as a plain number in
those two editions -- left blank rather than interpolated). See `notes` column per
row for the exact YoY context and any caveats (e.g. "preliminary figure per report's
own wording").

### `oil_product_domestic_consumption_2000_2022.csv` (153 rows)
Gas oil, fuel oil, gasoline, kerosene, LPG, other, and total domestic oil-product
consumption, thousand barrels/day. Source: Ministry of Petroleum, via CBI Annual
Review "Table 8 Domestic Consumption of Oil Products" (every edition carries a 5-year
rolling window; this file is the union across all 23 available editions, 1379-1401 SH
/ 2000/01-2022/23). Extracted programmatically (`parse_cbi_tables.py` in this
session's scratchpad, not committed to the repo) from the pdftotext output, with the
row-label -> indicator mapping done by hand and the numeric parsing spot-checked
against the raw `-layout` text for several editions. **Real annual coverage: 1996/97-
2017/18 (22 years).** From 2018/19 onward, every edition through the newest (2022/23)
prints ".." (not available) for this specific table -- i.e. Ministry of Petroleum
appears to have stopped or paused releasing this granular consumption breakdown in
CBI's own statistical appendix from that point on. This is a genuine, source-confirmed
gap (checked directly in two independent, non-adjacent editions), not a retrieval
failure.

### `natural_gas_consumption_2005_2022.csv` (53 rows)
Natural gas consumption by end-use sector (residential+commercial+industrial, power
plants, major industries, transportation, total), billion cubic meters. Source:
National Iranian Gas Company (NIGC), via CBI Annual Review "Table 10 Consumption of
Natural Gas". Same extraction method as the oil-product-consumption file above.
Coverage: 2005/06-2011/12 and 2015/16-2022/23. Gap 2012/13-2014/15: those three
editions' appendices do not contain this table at all (confirmed by direct grep, not
an extraction artifact) -- flagged as a genuine known gap, not fabricated/interpolated.

### `oil_and_gas_production_sci_yearbook_2001_2017.csv` (64 rows)
Two physical-production tables from the Statistical Centre of Iran (SCI) Statistical
Yearbook 1399 (2020/21 edition), Chapter 7 "Oil & Gas":
- Table 7.3 "Average Production of Different Types of Oil Products in Refineries" (cu
  m/day): liquefied gas, motor spirit, kerosene, gas oil, fuel oil, jet fuels,
  lubricants, bitumen, other products, total. Source: Ministry of Oil.
- Table 7.7 "Average Production of Enriched (Natural) Gas by Source of Production"
  (million cu m/day): total, associated gas, cap gas, gas of independent gas fields.
  Source: Ministry of Oil.
Both tables in this single yearbook edition show a sparse window: 1380, 1385, 1390,
1394, 1395, 1396 SH (2001, 2006, 2011, 2015, 2016, 2017). Values for 1397-1399 SH
(2018/19-2020/21) are printed as "000" in the source PDF, which in SCI's own
convention (cross-checked against the fact every single row across every product goes
to exactly "000" for exactly those three years, not a plausible real zero for e.g.
gasoline production) means "not yet available at time of publication", not an actual
zero -- excluded from this CSV rather than recorded as 0. `jet_fuels`, `lubricants`,
`bitumen`, `other_products`, and the refinery `total` line are additionally only
populated for 1380 and 1385 in the source table itself (blank/000 from 1390 onward for
those specific rows only -- a genuine source-table quirk, not a transcription error;
manually double-checked against the PDF's `-layout` text). Hand-transcribed (not
regex-parsed) directly from `pdftotext -layout` output of
`data/raw/sci-amar/yearbook-industry-mining-oilgas/sci_yearbook_1399_ch7.pdf` and
visually cross-checked against the source table twice.

## What was NOT found (honesty section)

**Cigarette production, refined sugar output, processed tea output, and textile cloth
output** (the four manufacturing-output measures named in the task brief) have **no
continuous Iranian-government physical-production series** discoverable via any route
checked this session:
- SCI Statistical Yearbook Chapter 8 ("Manufacturing Industries") is an ISIC-classified
  large-establishment survey (counts, employment, wages, value-added, investment) --
  confirmed via full-text search to contain zero physical-quantity tables for specific
  consumer products.
- CBI Annual Review's "Estimated Production of Major Farming Crops" table covers raw
  sugar cane / sugar beet / green tea leaf (agricultural, pre-processing tonnage --
  already FAOSTAT territory, a different concept from manufactured/refined output) and
  a "Sale of cigarettes" line that is an excise-tax REVENUE figure (billion rials), not
  a physical unit count.
- Iran Data Portal has no Industry/Manufacturing topic page; its Economic & Financial
  Affairs page's 22 tables include none of these four commodities.
- MIMT (Ministry of Industry, Mine & Trade) daily bulletins (already downloaded,
  re-checked this session) contain only licensing/permit counts, e-commerce
  trust-mark issuance, stock-exchange top-movers, and customs trade summaries -- no
  production data of any kind.
- IranOpenData: targeted search, no hit.

This is reported here rather than silently worked around. See
`logs/downloads/iran-industry-energy-enrich.log` for the full attempt-by-attempt trail.
