# UNCTAD Maritime Country Profiles — Comparator Countries (2024 snapshot)

Extracted 2026-07-13 from `data/raw/unctad-maritime/{usa,ven,esp,prt,grc,tur,arg,sau,rus,kor}/`
(10 immutable, unchanged single-file PDFs) — UNCTADstat's auto-generated "Maritime Country
Profile" for each country, born-digital (Microsoft Reporting Services PDF, not scanned), fully
`pdftotext -layout` extractable with no OCR needed. All 10 profiles share an identical template,
so one parser handled every country.

**Iran is deliberately excluded from this file** — another pass in this project already produced
a much richer Iran-specific extraction (4 files, including 2005-2024 multi-year trade/fleet time
series) at `data/processed/unctad_maritime_series/`. Cross-reference that folder for the Iran
side of any comparison; this folder is comparators-only.

## File

`unctad_maritime_comparators_2024.csv` — one long-format table, 150 rows (10 countries x 15
metrics), columns: `country_iso3, country_name, year, category, metric, metric_label, value,
value_raw_text, unit, estimate_flag`.

Metrics captured per country (all for the 2024 reference year unless a metric's own value was
reported for a different underlying year in the source):

- **general**: population, GDP (current US$), merchandise trade, land area, GDP growth,
  transport services trade
- **fleet**: national-flag registered fleet (deadweight tonnage and ship count), fleet under
  national ownership regardless of flag (deadweight tonnage)
- **maritime_key_figures**: coast/area ratio, ship building (gross tonnage), ship recycling
  (gross tonnage), container port throughput (TEU), number of seafarers, number of port calls

`value` is blank where the source itself printed `-` (not publishable) or `..` (no value
reported) — never guessed; the original printed text is preserved in `value_raw_text` for every
row so nothing is silently lost. `estimate_flag` decodes UNCTAD's footnote letters
((e)=estimate, (p)=provisional, (m)/(n)/(k)/(l)/(o)=ILO modeled estimate for seafarer counts).

## Verification

Text extraction was cross-checked against a `pdftoppm -r 150` PNG render of the United States
profile (`data/raw/unctad-maritime/usa/MaritimeProfile840.pdf`, page 1) — every number matched
exactly, confirming the born-digital text layer is reliable across this template family.

## What was NOT extracted (scope discipline, not a gap)

Each profile also contains a "World Shares" bar-chart page and a "Port Calls and Performance"
table (arrivals, median time in port, average vessel age/size by ship category, 2023 data) and,
for some countries, multi-year (2005/2010/2015/2024) time series for merchandise trade,
transport-services trade, and national-fleet-by-ship-type. Only the single-year 2024 headline
snapshot was extracted here for breadth across 10 countries; the multi-year time-series tables
were left unextracted in this pass (same trade-off Iran's own extraction made an exception for,
since Iran got a dedicated deeper pass — see `unctad_maritime_series/`).

## Headline figures at a glance (2024)

| Country | Fleet — national flag (000 DWT) | Fleet — national flag (ships) | Container throughput (TEU) | Port calls |
|---|---|---|---|---|
| USA | 13,268 | 3,513 | 54,282,705 | 267,937 |
| Venezuela | 1,300 | 268 | — | — |
| Spain | 1,691 | 480 | 16,379,282 | 142,103 |
| Portugal | 29,519 | 988 | 3,178,259 | — |
| Greece | 56,126 | 1,208 | 5,818,508 | 171,951 |
| Türkiye | 7,193 | 1,208 | 12,554,581 | 184,015 |
| Argentina | 880 | 199 | 1,490,437 | — |
| Saudi Arabia | 14,132 | 444 | 11,379,951 | — |
| Russian Federation | 12,087 | 2,935 | 4,586,171 | 61,175 |
| Republic of Korea | 21,192 | 2,161 | 30,003,141 | 105,500 |

Greece stands out with by far the largest fleet under national ownership regardless of flag
(394,963 thousand DWT — the well-known Greek-owned, foreign-flagged shipping phenomenon), while
its national-flag fleet is comparatively modest (56,126 thousand DWT). South Korea leads on
container throughput and shipbuilding (20.1 million GT built in 2024) among this set.
