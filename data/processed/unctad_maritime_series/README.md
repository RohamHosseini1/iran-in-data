# UNCTAD Maritime Country Profile — Iran (2026-07-13)

Extracted from `data/raw/unctad-maritime/irn/MaritimeProfile364.pdf` (immutable, unchanged) — a
4-page UNCTADstat auto-generated country profile (country code 364 = UN M49 numeric code for
Iran), born-digital (Microsoft Reporting Services PDF, not scanned), fully `pdftotext -layout`
extractable, no OCR needed.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `iran_maritime_snapshot_2024.csv` | 2024 single-year snapshot | Population, GDP, GDP growth, merchandise/transport-services trade totals, coast/area ratio, ship building/recycling, national-flag fleet tonnage & ship count, fleet-by-ownership tonnage, seafarer count |
| `iran_merchandise_trade_2005_2024.csv` | 2005, 2010, 2015, 2024 | Merchandise exports, imports, trade balance, millions current US$ |
| `iran_transport_services_trade_2005_2024.csv` | 2005, 2010, 2015 (2024 mostly unavailable) | Transport/travel/other-services export shares (%) and transport-services export/import/balance values (millions US$) |
| `iran_national_fleet_by_type_2005_2024.csv` | 2005, 2010, 2015, 2024 | National-flag fleet carrying capacity (thousand DWT) by ship type: oil tankers, bulk carriers, general cargo, container ships, other |

## Caveats — read before charting

- **Port-call/performance detail (arrivals, time in port, vessel age/size by ship category) and
  bilateral/port liner-shipping-connectivity-index tables were NOT extracted** — every cell in
  those specific tables is a "not publishable" (`-`) or "no value reported" (`..`) placeholder in
  this profile edition, genuinely empty in the source, not a extraction gap.
  `Container port throughput` and `Number of port calls` in the snapshot file are similarly
  `Not publishable` in the source and recorded as blank, not zero.
  `Ship recycling` for 2024 is `..` (no value reported), also left blank.
  `Ship building/recycling` under fleet-by-type-of-ship (number of ships, not tonnage) subsection
  had no populated table beneath its header in this PDF edition — not extracted.
- **2024 fleet growth rate (+0.3% y/y) and merchandise-export growth rate (+15.6% y/y) are
  UNCTAD's own printed headline figures**, not independently recalculated here — kept as text
  callouts in this README rather than a spurious CSV row, since they duplicate what's derivable
  directly from the trade/fleet CSVs' own year-over-year values.
- **This profile is Iran-only.** `data/raw/unctad-maritime/` also has already-downloaded Maritime
  Profile PDFs for all 10 comparator countries (ARG, DEU→via other folders, ESP, GRC, KOR, PRT,
  RUS, SAU, TUR, USA, VEN) from a prior round, none yet extracted/harmonized — a natural future
  addition using this exact same method (same-source multi-country win per this project's
  comparator-inclusion policy), deliberately left for a future pass to stay in scope for this
  task's Iran-first mandate.

## Sources

UNCTAD (UN Trade and Development), UNCTADstat Maritime Country Profile: Iran (Islamic Republic
of), generation date 2025-12-02 (data years 2005/2010/2015/2024 as tabulated in the profile;
several tables cite Clarksons Research, BIMCO-ICS, and MarineTraffic as UNCTAD's own underlying
data providers — see the PDF's own Notes section for full per-table attribution).
`data/raw/unctad-maritime/irn/manifest.json` for retrieval provenance.
