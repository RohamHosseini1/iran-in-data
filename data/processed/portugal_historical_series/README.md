# Portugal — Long-Run Historical Series (INE + Banco de Portugal)

Extracted 2026-07-13 from two immutable raw sources:
- `data/raw/ine-portugal/long-series-portuguese-economy/` — Portugal's national statistics
  institute (INE), "Séries Longas da Economia Portuguesa" (SLEP2020), a joint INE/Banco de
  Portugal product.
- `data/raw/banco-portugal/series-longas-pos-guerra/` — the 1997/1998-vintage predecessor
  publication (322-page PDF, "Séries Longas para a Economia Portuguesa — Pós II Guerra
  Mundial", extended to 1995), Banco de Portugal's own historical-series compendium.

## Files

### `ine_slep2020_headline_series.csv` (19,952 rows)

The raw folder already contains a companion `SLEP2020_tables.xlsx` (81 sheets: menu/navigation
tabs plus 66 numbered data tables "Q1.1" through "Q7.4") alongside the PDF report — using that
pre-existing structured spreadsheet was far more reliable than PDF extraction, so no OCR/PDF
parsing was needed here at all. Every "Qx.y" sheet shares one template (a `Código`/`Indicador`
label pair, then one column per year), so a single generic parser covered all of them.

13 headline tables were selected out of the 66 available, for breadth without over-investing in
any one domain — population/employment, GDP, prices, money, and government:

| Sheet | Title | Years | Rows |
|---|---|---|---|
| Q1.1 | Principais indicadores de população e emprego | 1941–2020 | 1,031 |
| Q1.2 | População residente e indicadores demográficos | 1941–2020 | 5,378 |
| Q1.11 | Taxa de desemprego por sexo e grupo etário | 1983–2020 | 684 |
| Q2.1 | Investimento (FBCF) a preços correntes por ativo fixo | 1953–2020 | 680 |
| Q3.1 | Principais indicadores da produção, despesa e rendimento (GDP headline) | 1953–2020 | 3,511 |
| Q3.6.1 | Despesa Nacional a preços correntes | 1953–2020 | 1,360 |
| Q4.1 | Índices anuais de preços no consumidor (CPI level) | 1948–2020 | 2,037 |
| Q4.2 | Taxas de variação anual de preços no consumidor (CPI, % y/y) | 1949–2020 | 2,009 |
| Q5.1 | Síntese Monetária (1947–1998) | 1947–1998 | 468 |
| Q5.2 | Agregados Monetários (pós 1998) | 1999–2020 | 66 |
| Q6.1 | Receitas e despesas das administrações públicas | 1947–2020 | 1,480 |
| Q6.3 | Dívida bruta consolidada das administrações públicas (Maastricht debt) | 1947–2020 | 883 |
| Q7.3 | Síntese da Balança de Pagamentos | 1948–2020 | 365 |

Columns: `country_iso3, source_table, table_title, category, code, indicator, unit, year, value`.
Labels are kept in the source's original Portuguese (official INE/BdP terminology); `category`
carries the table's row-group header (forward-filled), `code` is the source's own line-item code.

**53 further tables in the same workbook were intentionally left unextracted** — detailed sector
-by-sector value-added breakdowns (A10/A38 classifications), product-level export/import tables
(CPA10/CPA38), deflator series, quarterly consumption detail, interest-rate schedules, and
regional CPI — genuinely available in the source for a future deeper pass, not a gap in this one.

**Verification**: GDP at current prices, 2020 = €200,087.571 million (matches Portugal's known
actual 2020 nominal GDP of ~€200bn); Maastricht gross public debt, 2020 = €270,490.575 million
(matches the well-documented ~135%-of-GDP COVID-era debt spike). Both spot-checked against the
source spreadsheet cell-by-cell.

### `banco_portugal_balance_sheet_1947_1976.csv` (1,240 rows)

The predecessor Banco de Portugal PDF is organized as ~17 short "Balanço do Banco de Portugal"
(central bank balance sheet) tables, each covering a handful of years/quarters, printed serially
through the document. `pdftotext -layout` extracts this PDF cleanly despite it being encrypted
(print/copy-restricted; Xpdf ignores the restriction, as is normal behavior). A generic parser
located every occurrence of the exact page-header "BALANÇO DO BANCO DE PORTUGAL", read the
Activo/Passivo period-column headers, and matched a fixed, verified set of 11 Activo + 9 Passivo
line-item labels (net foreign assets, gold, credit to government, monetary base, banknotes and
coin, government deposits, etc.) against each period's values.

Columns: `country_iso3, section (Activo/Passivo), item, period, year, quarter, value_million_escudos`.
Coverage: **Dez 1947 through Set 1976** (annual Dec-only snapshots 1947-1965, then quarterly from
1966), 62 periods x 20 (section, item) pairs = a complete rectangle, no gaps.

**Stopped at Set 1976, not the full 1947-1995 the index promises** — the parser's exact-title
match (`"BALANÇO DO BANCO DE PORTUGAL"` alone on its own line) found only 7 real occurrences of
that literal running header before the document moves into a differently-titled "Reclassificação
das Operações Realizadas com o Ultramar no Balanço do Banco de Portugal" section (a colonial
-accounting adjustment table, correctly NOT parsed as if it were the main balance sheet — an
earlier draft of this parser accidentally ingested that section's near-all-zero values under the
same period labels before this was caught and fixed). The genuine continuation of this table
past 1976 (through 1995, per the source's own table of contents) evidently uses different page
-header text later in the document; chasing that down was judged not worth the marginal value
given `ine_slep2020_headline_series.csv` above already provides BdP/INE's own **revised and
extended successor** monetary-aggregates series (Q5.1/Q5.2) covering the same 1947-2020 span more
authoritatively. This 1947-1976 slice is kept because it is the only place in this project with a
genuine **central-bank balance sheet** (assets/liabilities, not just monetary aggregates) for
Portugal — a useful comparator to CBI (Central Bank of Iran) balance-sheet data if that exists
elsewhere in this project.

**Verification**: Total assets/liabilities, Dez 1973 = 89,619 million escudos; Set 1976 = 156,629
million escudos — both spot-checked against the source PDF text, exact match.

**The rest of this 322-page compendium was NOT extracted** (Balança de Pagamentos, Contas do
Sector Público Administrativo detail, interest-rate schedules, Treasury-bond issuance tables) —
deliberately, since it substantially overlaps ground the modern SLEP2020 workbook above already
covers more currently and more authoritatively (same institutions, revised methodology).
