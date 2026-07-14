# iran-primary-agriculture — progress log

- [2026-07-14T00:00Z] Read shared context + bookkeeping. Confirmed hard rules: never edit
  CHART_REGISTRY.csv/data/charts/catalog directly, no sub-agents, staging-file-only output.
- [2026-07-14T00:05Z] maj.ir and amar.org.ir both unreachable (curl/WebFetch both fail) --
  consistent with prior SOURCES.md notes. cbi.ir reachable via curl but not via WebFetch tool.
  23 CBI Annual Review PDFs (1379-1401 / 2000-2023) already present locally from a prior agent
  at data/raw/cbi-iran/cbi-annual-review-wayback/ -- mined those instead of re-downloading.
- [2026-07-14T00:15Z] Found and downloaded 8 xlsx files from Iran Data Portal (Syracuse University),
  mirroring SCI Statistical Yearbook agriculture-chapter tables sourced to Ministry of Agriculture.
  Wheat-Production.xlsx is the standout: 1356-1392 (1977/78-2013/14), 37 annual points -- longest
  single-crop series found. Manifest written to
  data/raw/iran-data-portal-agriculture/sci-yearbook-agriculture-tables/manifest.json.
- [2026-07-14T00:30Z] pdftotext -layout on all 23 CBI PDFs. Confirmed every edition carries two
  structured appendix tables ("Estimated Production and Area under Cultivation of Major Crops" and
  "Livestock Products"), sourced Ministry of (Jihad-e-)Agriculture, spanning 1999-2021 for most
  crops (2010-2021 for the horticultural group added later) and 1996-2022 for livestock products.
- [2026-07-14T01:00Z] Wrote/iterated a positional-token PDF-table parser (handled '..'/theta
  placeholder cells and footnote-marker digits correctly after a first-pass bug was caught by
  cross-checking wheat against FAOSTAT and finding 73/339 implausible values -- fixed, 0 remain).
- [2026-07-14T01:15Z] Harmonized 4 CSVs to data/processed/iran_primary_agriculture_series/:
  cbi_annual_review_crop_production_area.csv (598 rows, 16 crops), cbi_annual_review_livestock_products.csv
  (127 rows, 5 products), iran_data_portal_sci_yearbook_series.csv (149 rows), and
  faostat_vs_cbi_comparison.csv (423 rows, the FAO-vs-Iran cross-validation table). README.md written
  with the full comparison table and methodology/caveats discussion.
- [2026-07-14T01:30Z] Wrote data/processed/chart_registry_staging/enrichment_iran_agriculture.csv
  (19 rows, all status=extends, all extends_chart_id values validated against CHART_REGISTRY.csv).
  16 crop charts (wheat, barley, rice, cotton, sugar beet, sugar cane, tea, tobacco, potatoes, onions,
  pistachios, citrus fruit total, grapes, apples, maize) + 4 livestock charts (chicken meat, milk,
  eggs, honey) get a genuine second Iranian-primary source with 12-37 years of independent data each.
  oilseeds/pulses/red-meat data extracted and kept in the harmonized CSVs but NOT proposed for chart
  extension (no clean 1:1 FAOSTAT item match -- would need adjudication this project's rules forbid).
- [2026-07-14T01:35Z] Updated logs/downloads/iran-primary-agriculture.log (written early + appended
  incrementally throughout, per bookkeeping rule) and catalog/manifests/iran-data-portal-agriculture.jsonl.
  SOURCES.md updated to record the two new/upgraded source rows.
  TASK COMPLETE. No further row slice remains -- this was a single self-contained mission, not a
  fixed row-range assignment.
