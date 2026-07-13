# Spain — Historical GDP & Price Series (Carreras & Tafunell compendium)

Extracted 2026-07-13 from `data/raw/banco-espana-historical/carreras-tafunell-historical-statistics/`
(immutable, unchanged) — *Estadísticas Históricas de España: Siglos XIX-XX* (Carreras & Tafunell,
eds., 2nd edition), the definitive academic compendium of Spanish historical statistics,
distributed by the Fundación BBVA / Banco de España network. **This source is enormous: 1,438
pages, 17 chapters** (climate, population, education, agriculture, industry, housing, transport,
external sector, money & banking, business, patents, public sector, government, elections, labor,
consumption & prices, income & wealth) covering roughly two centuries. Deliberately, **only a
thin, headline slice was extracted** — extracting this source exhaustively would dwarf every
other country in this batch; the brief was breadth across the country list, not depth in any one.

## File

`carreras_tafunell_gdp_cpi_1800_2000.csv` — 2,157 rows, columns: `country_iso3, source_table,
table_title, series, year, value`.

Five tables ("Cuadros") were selected from Chapter 17 ("Renta y riqueza" — Income & Wealth, by
Albert Carreras, Leandro Prados de la Escosura & Joan R. Rosés) and Chapter 16 ("Consumo y
precios" — Consumption & Prices, by Jordi Maluquer de Motes):

| Cuadro | Title | Years | Series |
|---|---|---|---|
| 17.6 | El PIB a precios constantes (real GDP, millones de pesetas de 1995) | 1850–2000 | GDP at factor cost & at market prices, in constant 1995 pesetas + as % of 1995 level |
| 17.7 | El PIB a precios corrientes (nominal GDP, millones de pesetas) | 1850–2000 | GDP at factor cost & at market prices, current pesetas |
| 17.8 | El PIB per cápita (miles de pesetas de 1995) | 1850–2000 | GDP per capita at factor cost & market prices, constant 1995 pesetas + as % of 1995 level |
| 16.19 | Índices de precios (1913=100) | 1800–1958 | Five independent economic historians' alternative price-index estimates (Reher/Ballesteros, Ballesteros, Alcaide, Prados de la Escosura, Maluquer de Motes) — sparse, not every column populated every year |
| 16.20 | Índice de Precios de Consumo (base 1983) | 1939–2000 | CPI: urban ("Conjunto urbano"), non-urban ("Conjunto no urbano"), and general index |

This gives a genuinely long-run GDP series (150 years, 1850-2000) and a price-index series that,
combined across the two Cuadros, spans 1800-2000 — two centuries of Spanish prices.

## Method and verification

This 1,438-page PDF is encrypted (print allowed, copy disallowed) but born-digital
(Adobe InDesign/PDF Library output) — `pdftotext -layout` extracts it cleanly despite the
encryption flag (Xpdf ignores the copy restriction, standard behavior for this tool). Spanish
number formatting uses `.` as the thousands separator and `,` as the decimal separator (opposite
of the English convention); the parser normalizes every numeric token by stripping periods then
converting the remaining comma to a decimal point.

Spot-checked against the source text: GDP at market prices, 1850 = 4,252 million pesetas; 2000 =
100,872,726 million pesetas. CPI general index, 1961 = 9.119 (base 1983=100) — all exact matches.

## What was NOT extracted (a deliberate, large scope cut)

Every other chapter and the other ~1,370 pages of this compendium — climate, detailed
demographics, education, agricultural production series, industrial output/prices, housing stock,
transport, the full external-sector (trade/balance-of-payments) chapter, the full money-and
-banking chapter (interest rates, monetary aggregates), business/stock-market history, patents,
the full public-sector chapter (revenue/expenditure/debt detail beyond what's implicit in the GDP
figures), government/administration, elections, and labor-market series. Within Chapter 17 itself,
several more Cuadros (17.1-17.5, 17.9-17.15: alternative pre-1958 GDP estimate comparisons, sector
-composition-of-GDP tables, expenditure-composition tables, GDP deflators) were also left
unextracted. This is flagged explicitly so a future pass knows exactly where to pick up — this
source alone could support a much deeper harmonization effort if ever prioritized.
