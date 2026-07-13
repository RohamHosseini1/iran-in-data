# OPEC Annual Statistical Bulletin 2025 — Iran series (2026-07-13)

Extracted from `data/raw/opec-asb/asb-2025-pdf/asb-2025.pdf` (immutable, unchanged) — a 92-page,
born-digital (Adobe InDesign) PDF, fully `pdftotext -layout` extractable, no OCR needed. This is
the OPEC Secretariat's flagship annual statistical publication (data through end-2024), and the
single richest present-day Iran extension found in this backlog-clearing round: it brings this
project's oil/gas/macro series for Iran up to 2024 in one document.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `iran_opec_facts_2024_snapshot.csv` | 2024, single cross-section | 21 headline metrics in one table: population, land area, GDP per capita, nominal GDP, GDP growth, exports/imports of goods & services, current account balance, petroleum export value, crude reserves, gas reserves, crude production, gas marketed production, refinery capacity/throughput, petroleum product output, oil demand, crude/product exports & imports, gas exports |
| `iran_opec_macro_2020_2024.csv` | 2020–2024 annual | Population, nominal GDP, real GDP growth (PPP-weighted), exports of goods & services, petroleum export value, imports of goods & services, current account balance — from OPEC's Tables 2.1–2.7 |
| `iran_opec_oil_reserves_production_2020_2024.csv` | 2020–2024 annual | Proven crude oil reserves (flat at 208,600 million barrels every year) and crude oil production (Table 3.5's world-production series for Iran) |
| `iran_opec_crude_production_historical_1980_2024.csv` | 1980, 1990, 2000, 2010, 2023, 2024 (sparse anchor years, exactly as OPEC itself publishes them in Table 3.4) | Long-run crude oil production bridge — directly extends this project's Pahlavi-era and IMF/USGS-era oil series to the present |
| `iran_opec_natural_gas_2020_2024.csv` | 2020–2024 annual | Natural gas reserves (flat), marketed production, exports, imports (near-zero), and domestic demand |
| `iran_heavy_crude_spot_price_2020_2024.csv` | 2020–2024 annual average | "Iran Heavy" spot price, Iran's representative crude stream within the OPEC Reference Basket (ORB) |

## Caveats — read before charting

- **Table 3.4's historical crude-production anchors (1980/1990/2000/2010) are OPEC's own
  published sparse years, not a project-imposed subsample** — this table exists specifically to
  show long-run comparison points, so intervening years are genuinely not published here. This
  project's existing Pahlavi-era/IMF-era Iran oil series (see `pahlavi_oil_energy_series/` and
  related) should be used to fill the gaps between these anchor points; do not assume linear
  interpolation.
  - Cross-check: 2023/2024 values are identical across `iran_opec_crude_production_historical_1980_2024.csv`
    (Table 3.4) and `iran_opec_oil_reserves_production_2020_2024.csv` (Table 3.5) — 2,884 and
    3,257 thousand b/d respectively — a reassuring internal consistency check within the same
    OPEC publication.
- **`iran_opec_natural_gas_2020_2024.csv`: 2024 marketed production (277,611 million scm) exactly
  matches the same figure in `iran_opec_facts_2024_snapshot.csv`'s Table-1.1-derived row** —
  cross-validated within the same document.
- **Reserves figures (crude oil 208,600 mb; natural gas 33,988 bcm) are reported flat/unchanged
  across all 5 years 2020-2024** — this is exactly as published by OPEC (no year-to-year revision
  in this edition), not a repeated-value extraction error.
- **Nominal, not inflation-adjusted**: GDP, trade, and petroleum-export values are current US$;
  the sharp jump in `iran_opec_macro_2020_2024.csv`'s nominal GDP (195,528 → 401,357 million US$,
  2020→2024) reflects some combination of real growth, exchange-rate movements, and inflation —
  do not read as pure real economic growth without cross-referencing the GDP-growth-rate row
  (3.3–5.0% real per year) separately.
- **This extraction covers only Iran's own rows/columns** from tables that list all OPEC members
  (and, for reserves/production/gas tables, all world countries) — the full OPEC-wide and
  world-wide tables in the source PDF are far larger; only Iran was pulled out per this project's
  Iran-first policy. Section 4 (downstream refining detail by product), Section 5 (bilateral
  trade-partner-level oil trade), Section 6 (tanker freight rates), and Section 8 (OECD tax
  composite-barrel breakdown) were not extracted at all this round — lower priority for an
  Iran-specific database, flagged as a scoped future addition from the same PDF if ever needed.
- **OPEC's own historical production-quota table (Table 1.2, "OPEC Members' crude oil production
  allocations")** — a decades-long series of OPEC-negotiated quotas for Iran going back to 1982 —
  was noticed in the source but NOT extracted this round (it is a quota/allocation series, not an
  actual-production series, and would need careful labeling to avoid being confused with actual
  output; flagged here as a genuinely interesting future addition, distinct from the actual
  production figures already captured in `iran_opec_crude_production_historical_1980_2024.csv`
  and `iran_opec_oil_reserves_production_2020_2024.csv`).

## Sources

OPEC Secretariat, *Annual Statistical Bulletin 2025* (data through end-2024) —
`data/raw/opec-asb/asb-2025-pdf/asb-2025.pdf`. Full manifest:
`data/raw/opec-asb/asb-2025-pdf/manifest.json` (raw PDF left untouched per
`docs/bookkeeping.md`'s immutability rule). Extraction method: `pdftotext -layout` (clean,
born-digital PDF; no OCR needed).
