# iran-trade-oil-enrich — progress log

Mission: deepen Iran's TRADE and OIL-EXPORT layer from Iranian primary sources
(docs/agent-briefs — trade/oil-export enrichment task).

- [2026-07-14T12:37Z] Read _shared-context.md and bookkeeping.md. Grepped SOURCES.md and
  CHART_REGISTRY.csv for existing trade/oil coverage. Confirmed: oil revenue 1910+
  (pahlavi_oil_energy_series/), Pahlavi-era oil/trade tables 1950s-70s
  (pahlavi_agriculture_trade_extensions/), OPEC ASB sparse production anchors 1980-2024,
  WDI merchandise trade 1960-2025 (macro_wdi.csv). No existing continuous IRI-era
  (1979-present) Iranian-primary trade/oil-export series found — genuine gap confirmed.
- [2026-07-14T12:42Z] Tested direct access: cbi.ir returns HTTP 200 but is an F5/TSPD bot-
  challenge page (blocked, consistent with docs/bookkeeping.md); irica.ir and amar.org.ir
  both connection-refused/unreachable. Wayback CDX search on irica.ir found ~30 archived
  PDFs under opaque CMS paths, no obvious statistics-yearbook page found in time budget —
  logged as an open lead, not pursued further this pass. Full trail:
  logs/downloads/iran-trade-oil.log.
- [2026-07-14T13:05Z] Pivoted to data/raw/cbi-iran/cbi-annual-review-wayback/ (23 CBI
  Annual Review PDFs already held, FY1379-1401). Confirmed native-text via pdftotext
  -layout (no OCR needed). Located "Balance of Payments" table (present in all 23 reports,
  Table 51/52/53/47/49 depending on year) and "Export of Crude Oil" table (Table 14,
  present ONLY in the 2 earliest reports).
- [2026-07-14T14:35Z] Manually transcribed each of the 23 reports' own-fiscal-year column
  of the Balance of Payments table (current account, trade/goods balance, exports total,
  oil exports, non-oil exports, imports total, and — FY1388+ only — imports oil/gas vs.
  other-goods split), plus the 6-year Export of Crude Oil volume table and the 5-year
  Geographical Distribution of Crude Oil Exports table. Wrote
  scripts/harmonize/harmonize_cbi_trade_oil.py with full per-year source citations and
  format-era documentation (Era A/B/C, BPM5 methodology revision). Ran it — produced:
  - data/processed/iran_trade_oil_enrich_series/cbi_balance_of_payments_trade_oil_1375_1401.csv (189 rows, 27 fiscal years)
  - data/processed/iran_trade_oil_enrich_series/cbi_crude_oil_export_volume_1375_1380.csv (18 rows, 6 fiscal years)
  - data/processed/iran_trade_oil_enrich_series/cbi_crude_oil_export_geographic_share_1376_1380.csv (25 rows, 5 fiscal years)
  - data/processed/iran_trade_oil_enrich_series/README.md (full methodology, gap
    disclosure, cross-validation)
- [2026-07-14T14:45Z] Cross-validated CBI exports/imports against this project's own WDI
  series (macro_wdi.csv, TX.VAL.MRCH.CD.WT / TM.VAL.MRCH.CD.WT) for 6 spot-check years
  with the fiscal/calendar-year offset correctly applied. Exports agree within ~5-10%;
  imports diverge more (up to ~28% in the most recent year) — documented as a genuine,
  unadjudicated divergence per project policy, both series kept.
- [2026-07-14T14:55Z] Wrote scripts/harmonize/build_iran_trade_oil_staging.py and ran it —
  produced data/processed/chart_registry_staging/enrichment_iran_trade_oil.csv (5 chart
  proposals: 1 extends onto iran_unctad_maritime__merchandise_trade_2005_2024 for the
  exports/imports/balance triad, 1 extends onto wdi__BN.CAB.XOKA for current account,
  3 new — oil-vs-non-oil export value, imports oil-gas-vs-other split, and the short
  1996/97-2001/02 oil-export-volume series). No CHART_REGISTRY.csv or catalog/ file
  edited directly, per hard rule #1.
- [2026-07-14T15:00Z] DONE for this pass. Scope explicitly NOT covered (see README's "What
  was NOT extracted this pass" section): by-commodity trade breakdown (present in source,
  not transcribed across all 23 years), IRICA/SCI direct downloads (both domains
  unreachable; IRICA has an unexplored Wayback lead), trade-by-partner-country beyond the
  5-year 1997/98-2001/02 fragment already captured.
