# Iran Prices & Inflation deep-dive — progress log

Mission: build the deepest, best-sourced IRAN PRICES & INFLATION layer from Iranian
primary sources (CPI incl. by-group and urban/rural, WPI, PPI). See
logs/downloads/iran-prices-inflation.log for the full download/access-attempt trail.

- [2026-07-14T12:38Z] Surveyed existing assets: inflation_rate_1937_2014.csv (rate
  only, 1937-2014, iran-data-portal), cpi_by_group_1390_1399.csv (SCI Yearbook 1399
  Table 22.2, national by-group, 2011-2020), 23 CBI Annual Review PDFs already on
  disk (1379-1401 SH / 2000-2023), SCI Yearbook 1399 Ch.22 PDF already on disk.
  Confirmed via grep of CHART_REGISTRY.csv that inflation_rate_1937_2014.csv is
  ALREADY registered as an alt_source on wdi__FP.CPI.TOTL (prior pass), but no
  chart carries CPI index LEVELS, WPI, PPI, or urban/rural CPI for Iran.
- [2026-07-14T13:00Z] amar.org.ir and cbi.ir's live inflation dashboard confirmed
  unreachable (see download log for full attempt trail); worked around via Wayback
  CDX API, recovering 5 monthly CPI snapshots + 1 dashboard snapshot spanning
  Mar 2022 - Feb 2025 (bridges past the newest CBI Annual Review on disk).
- [2026-07-14T13:20-14:10Z] Transcribed CPI (Urban)/PPI/WPI tables from a
  non-overlapping 6-edition ladder of CBI Annual Reviews (1379, 1384, 1386[WPI
  only], 1389, 1394, 1399, 1401), covering SH1375-1401 (1996/97-2022/23) with zero
  gaps for CPI and PPI; WPI ends SH1386 (2007/08, CBI's own table discontinued
  after that edition — confirmed via table-of-contents inspection of the 1387
  edition). Extracted SCI Yearbook 1399 Ch.22 Tables 22.4 (Urban) and 22.7 (Rural)
  general CPI index, base 1395=100, 7 year-points (1385/1390/1395-1399) — first
  urban-vs-rural extraction in this project.
- [2026-07-14T14:15Z] Wrote 5 harmonized CSVs to
  data/processed/iran_prices_inflation_series/ (604 total data rows) + README.md
  documenting method, cross-validation (incl. one genuine unresolved discrepancy
  between two CBI-attributed sources for SH1384 inflation: 12.1% vs 10.4%), and
  honest gaps (pre-1996 index levels not recovered; post-1401 coverage thin/sparse).
- [2026-07-14T14:25Z] Wrote data/processed/chart_registry_staging/enrichment_iran_prices.csv
  (5 proposal rows: 3 extends onto wdi__FP.CPI / wdi__FP.WPI, 2 new [PPI sectoral
  series, urban-vs-rural CPI]).
- [2026-07-14T14:30Z] Catalogued new raw downloads (6 Wayback HTML snapshots) into
  data/raw/sci-amar/cpi-monthly-pointintime-wayback/manifest.json and appended to
  catalog/manifests/sci-amar.jsonl. Updating SOURCES.md next.

## Status: essentially complete for this pass

Remaining honest gaps for a future agent (all documented in the README):
1. Pre-1996 CPI index LEVELS (as opposed to the existing 1937-2014 rate-only
   series) — would need Bank Melli bulletins or pre-1996 CBI Annual Reviews, not
   currently on disk.
2. Post-1401 (2023-2026) continuous coverage — amar.org.ir/cbi.ir both unreachable
   this session; only 5 sparse Wayback-sourced monthly points recovered. A fresh
   Wayback CDX crawl (query documented in the manifest) by an agent running later
   (closer to "now") would likely surface more recent snapshots.
