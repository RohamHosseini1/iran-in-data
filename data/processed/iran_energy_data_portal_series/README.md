# Iran energy data — Iran Data Portal + national energy balance (1370-1394 SH / 1991-2016)

Harmonized 2026-07-13 from `data/raw/iran-data-portal/energy-environment-tables/` (5 files,
all immutable, unchanged). Four small Excel tables (already-tidy English-labeled SCI/CBI/NIOC
mirrors hosted by Syracuse University's Iran Data Portal) are re-copied with header/footnote
rows stripped; one large scanned-format PDF (Iran's official annual Energy Balance Sheet for
FY1394/2015-16, published by the Ministry of Energy) is newly extracted this pass — its
retrospective annex contains a full national energy balance table for **9 consecutive years**
(1386-1394), which is the highest-value find in this folder.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `national_energy_balance_1386_1394.csv` | FY1386-1394 (2007/08-2015/16), 9 years | **New extraction.** Iran's complete national energy balance sheet: primary energy Production/Imports/Exports/international bunkers/stock changes -> Total Primary Energy Supply (TPES) -> transformation losses (refineries, power plants, coking plants, blast furnaces, T&D losses) -> Total Final Consumption (TFC) -> consumption by end-use sector (residential/public/commercial, industry, transport, agriculture, other, non-energy uses). Broken out by 8-9 energy carriers: crude oil & petroleum products, natural gas, coal, combustible renewables, hydro, solar & wind, nuclear (from FY1390 onward only), electricity, and total. Unit: million barrels of crude-oil-equivalent (see Caveats — a parallel million-tons-of-oil-equivalent edition of the same 9 tables also exists in the source PDF but was not transcribed, to avoid a duplicate unit-converted copy of the same facts). |
| `oil_production_exports_quarterly_2000_2016.csv` | 2000q2-2016q3 (Iranian quarters 1379q1-1395q2), quarterly | Iran's crude oil production and exports in thousand barrels/day, Central Bank of Iran source, both Iranian and Western calendar quarters given. Complements (does not duplicate) the annual-frequency oil series elsewhere in this project — this is genuine quarterly granularity. |
| `natural_gas_consumption_1370_1385.csv` | 1370, 1375, 1380-1385 (1991-2006, gap years 1371-74/76-79 not in source) | Flared gas, gas delivered to National Iranian Gas Company, and gas injection (into oil fields for pressure maintenance), million cubic meters. |
| `oil_products_imports_1370_1385.csv` | 1370, 1375, 1380-1385 | Iran's oil-product imports by type (motor spirit/gasoline, burning oil/kerosene, gas oil/diesel, aviation spirit), million liters. Notable: burning-oil and most gas-oil imports drop to zero after 1375 (domestic refining caught up with demand), gasoline imports instead rise sharply from 1380 onward — an early visible marker of Iran's later gasoline-import/subsidy story. |
| `npc_petrochemical_production_1375_1385.csv` | 1375, 1380-1385 (1996-2006) | National Petrochemical Company total production by category (polymers, chemicals, aromatics, hydrocarbons, fertilizers/pesticides), thousand tons. |

## National energy balance — extraction method

Source: `data/raw/iran-data-portal/energy-environment-tables/energy_balance_sheet_1394_2015-16.pdf`
(596 pages, Ministry of Energy / Deputy for Electricity and Energy Affairs, "ترازنامه انرژی سال
۱۳۹۴"). This PDF's text layer exists but renders as reversed/reshaped Arabic-presentation-form
glyphs when extracted with `pdftotext` (a common artifact with older Persian PDF generators) —
per this project's standard method, every value here was read directly from
`pdftoppm -png -r 150` page renders (PDF pages 121, 123, 125, 127, 129, 131, 133, 135, 137,
corresponding to printed pages 93, 95, 97, 99, 101, 103, 105, 107, 109), not from the garbled
text layer. Each page is one of a run of 18 near-identical tables (`جدول (۱-۱)` through
`جدول (۱-۱۸)`, "Energy Balance Year X, whole country") in the report's Part 1 retrospective
section — the report publishes **each of the 9 years twice**, once in million-barrels-oil-
equivalent and once in million-tons-oil-equivalent (verified by visually inspecting the unit
line of both the first table, 1386/barrels, and the last, 1394/tons — total-energy figures
differ by a factor consistent with 1 tonne ≈ 7.3 barrels, confirming this is a real unit pair,
not a data error). Only the barrel-denominated (odd-numbered, 1-1/1-3/.../1-17) tables were
transcribed, to keep one consistent unit across the whole 9-year series; arithmetic
cross-checked (TPES total column = sum of its own fuel-column components) for every year and
matched exactly to one decimal place in every case checked.

## Caveats — read before charting

- **Column set changes mid-series**: a "nuclear energy" (انرژی هسته‌ای) column appears starting
  FY1390 (Bushehr plant era) and does not exist in FY1386-1389 — left as a genuinely absent
  (not zero) value for those years, per this project's blank-not-guessed rule.
- **FY1394 is explicitly marked preliminary/provisional** by the source itself (a "■" symbol
  next to the table title, with a footnote "figures are provisional") — flagged in the `note`
  column, not silently treated as final.
- **Row-level footnotes preserved as notes**, not silently absorbed: oil-product import figures
  exclude MTBE (no production/import data available for it, so total ≠ exact sum in some years);
  natural-gas export figures include NGL and gas condensate exports; the "energy sector own use
  and T&D losses" gas figure includes gas consumed at refineries, gas-processing facilities,
  pressure-boosting stations, and gas-lift diesel at oil fields — these are the source's own
  scope notes, reproduced verbatim in English rather than dropped.
- **`npc_petrochemical_production_1375_1385.csv`**: the FY1385 total (18,000 thousand tons)
  carries a source footnote "(2) including existing ceded complexes" — a scope change from prior
  years, preserved in the `note` column; the reported total does not equal the sum of the 5
  listed sub-categories in any year (source itself notes the categories are illustrative "main
  categories," not an exhaustive partition).
- **`oil_products_imports_1370_1385.csv`**: burning-oil and gas-oil imports collapsing to
  literal zero for years 1380-1382 most likely reflects Iran's refining capacity catching up
  with domestic demand for those specific products (imports of gasoline/motor-spirit rose
  sharply instead) — read as a real substitution, not a data gap, since the source explicitly
  reports "0" rather than leaving the cell blank.
- **Two small earlier extraction bugs caught and fixed during this pass** (both off-by-one row
  offsets from mis-locating the header row in a multi-row-preamble sheet): the petrochemical
  file was initially missing the "Fertilizers, pesticides and related materials" category row
  and had picked up a bogus "Category" pseudo-row; the oil-products-imports file was initially
  missing the "Aviation spirit" row entirely. Both re-extracted and verified against the raw
  `openpyxl` cell dump before being written here.

## Sources

- Iran Data Portal (Syracuse University Moynihan Institute), Energy & Environment topic page:
  `data/raw/iran-data-portal/energy-environment-tables/*.xlsx` — English-labeled mirrors of
  SCI/CBI/NIOC/NPC original tables.
- Islamic Republic of Iran Ministry of Energy, Deputy for Electricity and Energy Affairs,
  Office of Macro Electricity & Energy Planning, *Energy Balance Sheet 1394* (ترازنامه انرژی
  سال ۱۳۹۴), 596pp — `data/raw/iran-data-portal/energy-environment-tables/energy_balance_sheet_1394_2015-16.pdf`.

Full manifest: `data/raw/iran-data-portal/energy-environment-tables/manifest.json` (raw source,
untouched per this project's immutability rule; the manifest predates this extraction pass and
does not itself carry an `extraction_method` field for the balance-sheet PDF — documented here
instead).
