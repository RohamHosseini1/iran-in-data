# Pahlavi-era government finance, money supply & banking series (1900–1979)

Fifteen archival tables — already hand-extracted and visually verified (rendered to PNG via
`pdftoppm -r 200` and read directly off the page image, per this project's established method for
scanned World Bank/Encyclopaedia Iranica sources) to `data/raw/pahlavi-era-primary-extraction/*/
data.csv` by earlier rounds of this project — reshaped here from each source's own wide (one
column per year) layout into one uniform tidy long format for charting. **No value was
recalculated, interpolated, or fabricated in this reshaping step** — every cell is copied through
exactly as it sits in the raw `data.csv`; the only transformation applied is melting year-columns
into rows and attaching a sortable `year` integer. Raw files are untouched.
Built by `scripts/harmonize/harmonize_pahlavi_government_finance.py`.

## Schema (uniform across all 15 files)

`fiscal_year_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset`

- **`fiscal_year_label`** — the period exactly as the source printed it (e.g. `"1958/59"`,
  `"1957-06-20"`, `"Sept1968-Aug1969"`, `"budget_estimate_1970/71"`).
- **`year`** — a single sortable integer for charting. **Convention: Iran's fiscal year historically
  ran ~March 21 to March 20 the following Western year; a dual-year label like `"1969/70"` is mapped
  to its LATER Western year (1970)** — i.e. the year in which the fiscal year *ends*. This matches
  how the source documents themselves transition to single-year notation in later tables (e.g. the
  1974 World Bank report labels the fiscal year ending March 20 1972 simply `"1972"`). Snapshot
  dates (e.g. `1957_06_20`) use the year read directly off the date. Rows tagged as a budget
  estimate/revised estimate/draft budget/projection still get a `year` (so they place correctly on
  a chart) but `notes` always states explicitly that the row is not an actual — filter or style
  those out before treating a series as "actuals only."
- **`category` / `subcategory`** — preserves each source table's own row hierarchy exactly (ministry
  names, monetary-aggregate components, etc.).
- **`value`** — blank means the source cell was blank, illegible, or marked "n.a." — never filled in.
- **`unit`**, **`notes`**, **`country_iso3`** (always `IRN`), **`source_dataset`** (the raw dataset_id,
  for tracing back to the manifest with the full extraction/verification method).

## Files

| File | Coverage | Topic | Raw source dataset |
|---|---|---|---|
| `actual_budget_revenues_1958_59.csv` | FY1958/59 (single year) | Government revenue by tax category (direct/indirect taxes, monopoly profits, oil transfers) | `wb1960-table12-actual-budget-revenues` |
| `actual_treasury_expenditures_1958_59.csv` | FY1958/59 (single year) | Government expenditure by ministry, actuals | `wb1960-table11-actual-treasury-expenditures` |
| `budgeted_vs_actual_expenditures_1955_60.csv` | FY1955/56–1959/60 | Budgeted expenditure by ministry + two summary rows (Total budgeted, Actual) | `wb1960-table10-budgeted-expenditures` |
| `banking_statistics_private_sector_1957_59.csv` | June 20 snapshots, 1957–1959 | Deposit-bank vs. National Bank private-sector deposits/advances | `wb1960-table14-banking-statistics-private-sector` |
| `bank_deposits_private_sector_1963_70.csv` | FY1963/64–1969/70 + 2 rolling 12-mo periods | Private-sector sight/saving/time deposits, level + % of total | `wb1971-table6.5-bank-deposits-private-sector` |
| `money_supply_changes_1957_59.csv` | June/Dec snapshots, 1957–1959 | Money supply, claims on government/private sector, period-over-period changes | `wb1960-table8-changes-in-money-supply` |
| `money_quasi_money_changes_1965_71.csv` | FY1964/65–1969/70 + 1970/71 projection + 2 first-half-year figures | Money & quasi-money components, year-over-year FLOWS (not levels) | `wb1971-table6.2-changes-money-quasi-money` |
| `monetary_survey_1963_70.csv` | FY1963/64–1969/70 | Consolidated banking-system balance sheet, year-end STOCK LEVELS | `wb1971-table6.1-monetary-survey` |
| `monetary_aggregates_movements_1963_73.csv` | FY1963–1973 | Money & quasi-money components, year-over-year FLOWS — later/extended vintage of the same concept as `money_quasi_money_changes_1965_71.csv` | `wb1974-table7.1-movements-monetary-aggregates` |
| `government_revenue_summary_1962_72.csv` | FY1962/63–1969/70 + budget-estimate/revised-estimate/draft-budget columns for 1970/71–1971/72 | Government revenue by category (direct/indirect taxes, oil revenue) | `wb1971-table5.2-government-revenue-summary` |
| `ordinary_budget_expenditure_1962_72.csv` | FY1962/63–1969/70 + estimate/draft columns | Ordinary-budget current expenditure by ministry/category | `wb1971-table5.1-ordinary-budget-expenditure` |
| `central_govt_operations_summary_1962_73.csv` | FY1962–1971 + preliminary-actuals-1972 + budget-estimate-1973 | Full fiscal balance: revenue, current+capital expenditure, deficit, financing breakdown | `wb1974-table6.1-central-govt-operations-summary` |
| `balance_of_payments_summary_1963_70.csv` | FY1963/64–1969/70 + 7-year CAGR rows | Exports/imports/current account/capital account/monetary movements | `wb1971-appendix1-balance-of-payments-summary` |
| `fiscal_system_narrative_indicators_1921_79.csv` | 1921–1979, irregular (single years, periods, decade-averages as stated in Iranica's prose) | Tax-mix shares, oil-revenue share of budget, expenditure-category shares — narrative-article statistics, each row carries its own underlying academic citation (mostly Bharier 1971, Karshenas 1990) | `iranica-fiscal-system-narrative-1921-1979` |
| `century_indicators_1900_2006.csv` | 1900 (rough estimate) vs. 2006 | Broad macro/demographic bookends: population, per-capita income, urbanization, life expectancy, literacy, agriculture share of GDP, trade/GDP ratio | `esfahani-pesaran-2008-century-indicators` |

## Relationships between these files — read before charting

**These 15 tables come from at least 4 different World Bank report vintages (1960, 1962, 1971,
1974) plus Encyclopaedia Iranica and one academic paper. Several genuinely overlap in time and
topic but were extracted from different original documents, and their overlapping years do NOT
always agree exactly** (most likely due to preliminary-vs-revised-vs-later-recompiled figures
across report vintages). Per this project's reconciliation policy, **overlapping disagreeing
sources are kept as separate files/lines, never merged into one "winning" number**:

- **Government revenue**: `actual_budget_revenues_1958_59.csv` (single year, most granular
  tax-category breakdown) → `government_revenue_summary_1962_72.csv` (1971 report, 1962/63-1971/72)
  → `central_govt_operations_summary_1962_73.csv`'s "Total Revenues" rows (1974 report, 1962-1973).
  The two multi-year tables overlap 1962-1971 and their TOTAL figures are close but not identical
  (e.g. FY1969/70: 143.9 vs 150.4 billion rials for the same nominal year) — treat as two distinct
  vintages of the same underlying concept, not a single reconciled series.
- **Government expenditure**: `actual_treasury_expenditures_1958_59.csv` (single year, actuals) and
  `budgeted_vs_actual_expenditures_1955_60.csv` (1955/56-1959/60, budgeted AND actual side by side)
  → `ordinary_budget_expenditure_1962_72.csv` (1962/63-1971/72, current expenditure only) →
  `central_govt_operations_summary_1962_73.csv`'s "Current Expenditure" + "Capital Expenditure" rows
  (1962-1973, both current and capital, a different split than the ordinary-budget table).
  `central_govt_operations_summary_1962_73.csv` is the only one of these with a **capital**
  expenditure line — the others are current/ordinary-budget only, so it is not directly comparable
  to the ministry-level breakdowns without accounting for that scope difference.
- **Money supply / monetary aggregates** form two parallel families that must not be mixed:
  **levels** (`money_supply_changes_1957_59.csv` snapshot levels, `monetary_survey_1963_70.csv`
  year-end stock levels) vs. **flows/year-over-year changes**
  (`money_quasi_money_changes_1965_71.csv` and `monetary_aggregates_movements_1963_73.csv`, the
  1974-vintage extended/later re-run of the same flow concept). `bank_deposits_private_sector_
  1963_70.csv` and `banking_statistics_private_sector_1957_59.csv` are deposit-composition detail
  tables, narrower in scope than the full monetary-survey balance sheets.
- **`century_indicators_1900_2006.csv`** is broader macro/demographic context (population, GDP per
  capita, life expectancy, etc.), not government-finance/banking specifically — included in this
  batch because it was part of the assigned raw-material list, but it is flagged in the chart-
  registry staging file as `status=extends` against existing WDI/Maddison population and GDP-per-
  capita charts (its unique contribution is the single 1900 anchor point, decades before WDI/
  Maddison's own Iran coverage begins in most series) rather than a new government-finance concept.

## Caveats — read before charting

- **Fiscal-year vs. calendar-year**: every `"NNNN/NN"`-style label is Iran's fiscal year (ends
  ~March 20); see the `year` convention above. Do not assume these align month-for-month with
  Western-calendar-year data from other sources (e.g. FAOSTAT) without accounting for the ~9-day-
  to-11.5-month offset.
- **`money_supply_changes_1957_59.csv`** preserves one column, "Foreign Assets and non-monetary
  factors," that is itself a flow/balancing item in the source with no separate level ever printed —
  do not try to compute a level for it.
- **`balance_of_payments_summary_1963_70.csv`** has one illegible cell (1964/65 errors-and-omissions)
  left blank per the no-fabrication rule, even though the BOP accounting identity would imply a
  value of -14 — the printed digits in the 1971 report scan could not be confidently read, so it
  was NOT back-calculated. Two rows (`net_capital_account`, `monetary_movements`) have their
  "7-year CAGR" cell replaced by a 7-year cumulative total instead (the source itself printed a
  total, not a growth rate, for these two rows specifically) — flagged in each row's `notes`.
- **`bank_deposits_private_sector_1963_70.csv`**: one column (FY1964/65) has a ~2.0 billion rial
  discrepancy between the printed Total and its own printed components in the *original 1971
  typescript* (confirmed not a transcription error on this project's end via arithmetic re-check) —
  transcribed exactly as printed, not corrected. The two `SeptYYYY-AugYYYY` rows are rolling 12-month
  periods, not aligned to the Iranian fiscal year — flagged per-row, do not chart interleaved with
  the FY columns without labeling.
- **`banking_statistics_private_sector_1957_59.csv`**: the "Excess Cash" row is printed in
  parentheses in the source with ambiguous sign convention (see the row's own `notes`) — preserved
  as a positive magnitude per the original manifest's interpretation, not silently resigned.
- **`fiscal_system_narrative_indicators_1921_79.csv`** is narrative-article prose, not a table —
  points are irregular (single years, multi-year periods, decade averages) and several values are
  themselves ranges (e.g. "10-16 percent") or approximate ("~100") exactly as Iranica's own text
  states them; do not treat as an annual series, and do not average a stated range down to a point
  estimate.
- **`century_indicators_1900_2006.csv`**'s 1900 column values are explicitly labeled by the source
  as rough estimates (several carry a `?` or `<` uncertainty marker in the original, preserved in
  `notes`) — treat as an order-of-magnitude anchor, not a precise data point.
- **Units**: almost all Pahlavi-era monetary figures are in **million or billion rials** (note which,
  per file — this project's own convention did not standardize million vs. billion across these WB
  report vintages because the SOURCE documents themselves don't; always check the `unit` column per
  row) at exchange rates that were themselves changing over this period (the 1971-vintage tables
  state "1 US$ = 75.7 rials" as of their report date; earlier/later tables may differ — do not
  convert to USD without checking each table's own stated rate).

## Sources

- International Bank for Reconstruction and Development (World Bank), *Current Economic Position
  and Prospects of Iran* (1960) — Tables 8, 10, 11, 12, 14.
- World Bank, *Economic Development of Iran* (1971) — Statistical Annex Tables 5.1, 5.2, 6.1, 6.2,
  6.5, Appendix 1.
- World Bank (1974) — Statistical Appendix Tables 6.1, 7.1.
- Encyclopaedia Iranica, "FISCAL SYSTEM v. Pahlavi Period" (iranicaonline.org), citing Bharier,
  *Economic Development in Iran 1900-1970* (1971) and Karshenas, *Oil, State and Industrialization
  in Iran* (1990) as underlying primary sources.
- Esfahani & Pesaran (2008), "The Iranian Economy in the Twentieth Century: A Global Perspective,"
  Table 1.

Full extraction methods (page numbers, visual-verification arithmetic cross-checks, exact scan
sources): `data/raw/pahlavi-era-primary-extraction/*/manifest.json` — see
`data/processed/pahlavi_era_tables_index.md` for the master index across all 43 Pahlavi-era tables
extracted by this project (of which these 15 are the government-finance/banking-relevant subset
harmonized here; the remainder cover agriculture, industry, transport, energy, and household-
consumption topics and are harmonized separately).
