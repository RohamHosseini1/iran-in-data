# Iran provincial standing economic indicators (SCI "Jaygah-e Ostan-ha", FY1393-1402)

Harmonized 2026-07-13 from `data/raw/iran-provincial-statistics/sci-provincial-standing-indicators/`
(2 Excel workbooks, raw files unchanged). Each workbook is the Statistical Centre of Iran's
"Economic, Social and Cultural Standing of the Provinces" (جایگاه اقتصادی، اجتماعی و فرهنگی
استان‌ها) compendium — 24 chapters x 31 provinces, published as a rolling multi-year edition.
Two editions are in `data/raw/`: `jaygah_eght-ejt-farh_ostan_1398-1402.xlsx` (years mostly
1396-1402) and `NE_Jaygah_Ostan_1395-99.xlsx` (years mostly 1393-1397). This complements —
does not duplicate — this project's existing province-level **census/demographic** data in
`data/processed/iran_census_demographics_series/`; this folder focuses on the **economic**
chapters (national accounts, government budget, financial markets/insurance, industry, mining,
foreign investment) that were not previously mined from this source.

**Scope note (read before assuming exhaustive coverage)**: each workbook has 24 chapters
(climate, environment, population, labor, agriculture, mining, oil & gas, industry, water &
electricity, construction, commerce, transport, communications, financial markets, judicial
affairs, welfare, education, health, culture, government budget, household expenditure/income,
price indices, national accounts, political affairs), each with 8-13 separate numbered tables.
This pass extracted a **curated selection of the highest economic value**: the complete national-
accounts chapter (GDP/value-added by province, 6-7 tables) plus one or two headline tables each
from government budget, financial markets, industry, mining, and commerce. The remaining
tables/chapters (full detail on agriculture, water/electricity infrastructure, education, health,
welfare, judicial affairs, tax-by-type breakdowns beyond what's here, etc.) were **not**
extracted — a real, logged incompleteness, not a fabricated "nothing there." Every table in
both workbooks follows the same structure (province x year, with a paired share/rank or
value/rank column pair and a "کل کشور" whole-country reference row), so a future pass can reuse
the `parse_generic_table` pattern documented below to extend coverage cheaply.

## Files

| File | Chapter | Years (SH) | What it covers |
|---|---|---|---|
| `gdp_value_added_share_by_province_1393_1401.csv` | 23 - National Accounts | 1393-1401 (both editions, overlapping 1396-1397) | Province share of national GDP (current prices), GDP excluding oil, and value-added by sector (agriculture, mining incl. oil extraction, industry, services) — 6 indicators x 31 provinces + country total, both editions kept side by side (not reconciled) per this project's overlapping-source policy. |
| `gdp_per_capita_excl_oil_by_province_1393_1397.csv` | 23 | 1393-1397 | Non-oil GDP per capita by province, thousand rial (NE edition only; the newer edition does not repeat this specific table). |
| `government_budget_execution_share_by_province.csv` | 20 - Government Budget | 1397-1401 | Province share of national current (operating) and capital (development) budget-credit execution. |
| `financial_markets_insurance_by_province.csv` | 14 - Financial Markets | 1397-1401 | Bank loan-to-deposit ratio, insurance premium-written share, insurance claims-paid share (all percent), and insurance premium per capita (million rial) — directly complements this project's Bimeh Markazi national-level insurance-sector data with a provincial breakdown. |
| `industry_workshops_by_province.csv` | 8 - Industry | 1396-1400 | Province share of industrial production value and of workshop count, for workshops with 10+ employees. |
| `mining_production_value_share_by_province.csv` | 6 - Mining | 1397-1401 | Province share of the value of production from operating mines — complements `iran_mining_series/` (which is commodity-based, national-level) with a geographic breakdown. |
| `foreign_investment_by_province.csv` | 11 - Commerce | 1398-1400 | Foreign investment value by province, thousand USD. 1401-1402 rows dropped (source shows literal placeholder "000" for those years/provinces, i.e. data not yet available at publication time — not real zeros; excluded per this project's never-guess rule rather than kept as misleading zeros). |

## Extraction method

Both workbooks are digitally-produced modern `.xlsx` files (SCI's own internal publishing
system) — no OCR needed, read directly via `openpyxl`. Each chapter sheet packs multiple
numbered tables (title row -> year-header row, years spanning 2 columns each -> a subheader row
whose label varies by table: "سهم"/رتبه" = share/rank, "نسبت"/رتبه = ratio/rank, "ارزش"/رتبه =
value/rank, "شاخص"/رتبه = index/rank -> a "کل کشور" whole-country total row -> 31 province rows
-> footnotes). A generic Python parser (kept in this session's scratch area, not committed to
`scripts/` — flagged as a candidate to formalize if this source is revisited) locates each
table by its numbered-title regex, reads the actual subheader label into a `value_label_fa`
column (rather than assuming every table is a percent share — this caught and fixed a real bug,
see Caveats), and reads the table's own unit annotation (e.g. "(درصد)"=percent, "(هزار
دلار)"=thousand USD, "(میلیون ریال)"=million rial) into a `unit` column.

## Caveats — read before charting

- **A real bug was caught and fixed during this pass**: the first extraction pass assumed every
  table's value column was a percentage share (labeled `share_pct`), which is true for most
  tables (national accounts, budget, industry, mining) but **wrong** for three financial-markets
  tables (loan/deposit ratio is a ratio, insurance premium-per-capita is a million-rial amount)
  and the foreign-investment table (a thousand-USD value, not a share at all). Re-extracted with
  a generic `value`/`unit`/`value_label_fa` schema that reads each table's actual label instead
  of assuming — cross-checked against every table's own unit annotation before finalizing.
- **Both editions kept side by side, not reconciled**, per this project's standing policy for
  overlapping/disagreeing sources — where both workbooks cover the same year (1396-1397 in the
  GDP file), expect two rows tagged by `edition`, occasionally differing slightly (the source's
  own footnote says "figures revised by the relevant organization" between editions).
- **`کل کشور` (whole-country) rows are kept as a built-in validation reference** (share/ratio
  columns should sum player-provinces to ~100% net of the "cross-regional" residual the source's
  own footnotes describe) — not a 32nd province, filter out if only province-level rows are
  wanted for mapping.
- **`mining_production_value_share_by_province.csv`**: the whole-country reference row's value is
  stored as the literal string `"100/00"` in the source spreadsheet (a Persian-locale decimal
  formatting artifact using "/" instead of "." — this project's other tables in the same chapter
  print `100` as a plain number) — preserved exactly as found rather than silently reformatted;
  affects only the reference row, not actual province data.
- **`insurance_premium_per_capita_million_rial`**: the source's own subheader literally says
  "شاخص" (index) even though the title and unit ("11- حق بیمه سرانه", million rial) make clear
  this is a per-capita rial amount, not an index number — the raw label is preserved in
  `value_label_fa` for transparency rather than silently overridden.
- **Rank columns show `××`** for the whole-country row (not ranked against itself) and, in the
  foreign-investment table, for any province with zero/undisclosed investment in a given year —
  preserved as the literal source symbol, not converted to a numeric rank.

## Sources

Statistical Centre of Iran (SCI / مرکز آمار ایران), under the Plan and Budget Organization,
*Economic, Social and Cultural Standing of the Provinces* (جایگاه اقتصادی، اجتماعی و فرهنگی
استان‌ها), two editions:
- `data/raw/iran-provincial-statistics/sci-provincial-standing-indicators/jaygah_eght-ejt-farh_ostan_1398-1402.xlsx`
- `data/raw/iran-provincial-statistics/sci-provincial-standing-indicators/NE_Jaygah_Ostan_1395-99.xlsx`

Full manifest (both files, retrieved via Wayback Machine since amar.org.ir is unreachable
directly from this network): `data/raw/iran-provincial-statistics/sci-provincial-standing-indicators/manifest.json`.
The companion PDF narrative report in the same raw folder
(`N_Jaygah_Ostanha_IDAA_1400-06.pdf`, 193pp, Persian methodology/highlights companion) was
reviewed for context but not separately transcribed — its content is the underlying methodology
and narrative behind these same Excel tables, not additional data.
