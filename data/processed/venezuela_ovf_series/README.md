# Venezuela — OVF (Observatorio Venezolano de Finanzas) Macro Indicators

Extracted 2026-07-13 from `data/raw/ovf-venezuela/ovf-indicators/` (immutable, unchanged).

## Why this source, specifically

**OVF (Observatorio Venezolano de Finanzas) is an independent Venezuelan economic-monitoring
initiative** — specifically, the reports used here are published by the *Instituto de
Investigaciones Económicas y Sociales* (IIES) at the *Universidad Católica Andrés Bello* (UCAB),
an independent academic institution, not a government body. This matters because Venezuela's
official statistics agency (BCV — Banco Central de Venezuela) has well-documented credibility
problems in recent years: the BCV suspended regular publication of CPI and several other
macroeconomic series for extended periods during the country's hyperinflation crisis (2014-2019),
and independent researchers, the IMF, and international press have repeatedly noted gaps and
inconsistencies in official Venezuelan statistics since. OVF/UCAB's academic estimates — built
from independent price-basket surveys, household expenditure surveys (ENCOVI), and published
methodology — are widely cited by the IMF, World Bank, and financial press specifically *because*
the official alternative is compromised. This is a genuine, useful instance of this project's
general policy (see `docs/bookkeeping.md`, "Source reliability & neutrality principles") of
preferring a credible independent source over a compromised official one, applied deliberately
here rather than defaulting to BCV. Where OVF's own tables cite BCV as their underlying data
source (e.g. reserves, fiscal accounts), that's noted in the `variable`/`section` text as-is —
OVF's value-add in those cases is compiling and contextualizing BCV data, not replacing it, and is
flagged accordingly rather than presented as if fully independent.

## File

`ovf_macro_indicators_2012_2024.csv` — 309 rows, columns: `country_iso3, source_table, section,
variable, unit, year, value`. Source: `Informe-de-Coyuntura-Venezuela-abril-2024.pdf` (IIES-UCAB's
April 2024 quarterly situation report, 74 pages, born-digital, cleanly extractable).

Three tables ("Cuadros") were extracted — the ones containing real embedded text (most of this
report's ~20 other data tables are embedded as images/screenshots inside the PDF and were **not**
extractable as text; see below):

| Cuadro | Title | Coverage | Rows |
|---|---|---|---|
| 9 | Evolución y proyecciones de los agregados macroeconómicos (the headline table) | 2012–2024 (2022 estimated, 2023-2024 projected) | 168 |
| 1 | Perspectivas económicas globales: crecimiento económico (%) — includes Venezuela alongside World/regional/peer-country GDP growth rows | 2021–2024 | 73 |
| 2 | Perspectivas económicas globales: inflación (%) — same country set, inflation | 2021–2024 | 68 |

**Cuadro 9 is the centerpiece**: a single continuous 2012-2024 table spanning Real Sector (real
GDP growth), Monetary Sector (M2/liquidity growth, monetary base growth, **CPI inflation** —
20.1% in 2012 rising to a peak of **130,060.2% in 2018** during the hyperinflation crisis, then
falling to 31.7% projected for 2024), Public Sector (restricted-public-sector revenue/expenditure/
fiscal balance as % of GDP, external public debt as % of exports), and External Sector (exports,
imports, international reserves in billions US$, real official exchange-rate index, average Merey
16 crude oil price). This is exactly the kind of long-run, independently-compiled Venezuela series
this project needed, and it was sitting as real (non-image) text in the PDF.

Cuadro 1 and 2 add IMF-sourced comparative context: Venezuela's 2021-2024 real GDP growth (1.0%,
8.0%, 4.0%, 4.5%f) and inflation (686.4%, 234.1%, 189.8%, 31.7%f) alongside the World, developed
/developing-economy aggregates, and 12 individual comparator countries (including several already
in this project's country set — Argentina, Russia — plus regional Latin American peers).

**Verification**: all three tables' Venezuela rows were cross-checked internally — Cuadro 9's
2021-2024 inflation values (686.4/234.1/189.8/31.7) exactly match Cuadro 2's independently-printed
Venezuela inflation row, confirming consistent, correctly-parsed extraction across both tables.

## `Boletin-economico-y-Social-OVF-DIC-2023.pdf` — genuinely unusable, not a gap in this pass

The raw folder's second file could not be extracted at all: it is served by OVF's own CDN as an
**exactly 1,048,576-byte (1.0 MiB) truncated PDF with no `%%EOF` trailer**. This was already
diagnosed and documented in `data/raw/ovf-venezuela/ovf-indicators/manifest.json` by the
downloading agent (verified via two independent re-downloads plus a matching Cloudflare ETag
`W/"100000-..."` = exactly `0x100000` bytes, confirming this is what the source server actually
serves, not a fetch error on this project's end). Confirmed independently in this pass: neither
`pdftotext`, `pdftoppm`, nor Python's `pypdf` (with lenient/non-strict parsing) can recover any
content — the file is missing its trailer/xref table entirely and the object streams themselves
are truncated mid-stream. Per this project's "no fabricated data" rule, nothing was extracted from
it; it remains in `data/raw/` as a faithful (if useless) mirror of what the source actually serves.

## What was NOT extracted (scope discipline)

Roughly 20 other "Cuadro" tables and ~55 "Gráfico" charts in the Informe de Coyuntura were left
unextracted: most Cuadros beyond 1/2/9 (oil-sector variables, monetary-base/liquidity detail,
manufacturing-sector wages, bank foreign-currency deposits, household-expenditure-inequality
tables 10-13) are embedded as images in this particular PDF and are not text-extractable without
OCR; the Gráficos (oil prices, exchange-rate/inflation charts, labor-market survey results,
poverty/inequality figures) were judged lower headline-value relative to effort for this breadth
-oriented pass. A future pass with an OCR step could recover the image-based tables.
