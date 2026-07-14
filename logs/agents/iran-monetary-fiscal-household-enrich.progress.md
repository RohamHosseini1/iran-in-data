# Progress log — Iran monetary/fiscal/household-consumption enrichment agent

- [2026-07-14T11:02:00Z] Started. Read shared context + bookkeeping.md. Surveyed existing holdings
  before hunting further (per project convention: dig once, don't re-hunt what's already there).
  Found the cluster is NOT starting from zero — prior rounds already landed: CBI Annual Review
  monetary aggregates (M2/liquidity/monetary base, FY1379-1401 = 2000-2023, cbi_annual_review_series),
  government budget (iran_plan_budget_org annual_budget_law_totals FY1371-1401 = 1992-2023, near-
  continuous, + Majlis scattered pre-1979 fragments + SCI yearbook 1385-1400), Pahlavi-era money-
  supply/banking fragments (1955-1973, pahlavi_government_finance_series). [continuation below]
  Genuine remaining gaps
  identified: (a) a downloaded-but-never-harmonized IMF IFS historical Iran money-supply series
  (M1/quasi-money/reserve-money/domestic-credit, 1950-1971, 21 annual points,
  data/raw/imf-ifs-historical/iran-annual-series-extracted/data.csv) sitting unharmonized and
  unregistered; (b) a downloaded-but-never-harmonized Iran Data Portal quarterly "Government Debt to
  the Central Bank" series 1978-2016 (157 quarterly obs, direct monetary-financing proxy) at
  data/raw/iran-data-portal/government-finance-tables/; (c) a downloaded-but-never-harmonized SCI
  Statistical Yearbook 1399 household-expenditure-detail table 2001-2020 (data/raw/sci-amar/
  household-expenditure-detail-2001-2020/data.csv, 1089 rows) sitting as raw only, not registered in
  CHART_REGISTRY; (d) a downloaded-but-never-harmonized Iran Data Portal GDP-by-final-expenditure-
  component table 1991-2005 (includes household final consumption expenditure at the national-
  accounts level). Plan: harmonize (a)-(d) first since they are genuine continuity wins sitting
  already on disk, then do fresh web hunting for the still-open 1972-1999 M1/M2 gap and for
  HEIS/CBI updates beyond current coverage (forward to 2024-2025).
- [2026-07-14T11:20:00Z] Harmonized all 4 identified unharmonized local sources into
  data/processed/iran_monetary_fiscal_household_enrich_series/ (script:
  scripts/harmonize/enrich_monetary_fiscal_household.py): money_supply_banking_national_accounts_imf_ifs_1937_1971.csv
  (415 rows), government_debt_to_central_bank_quarterly_1978_2016.csv (462 rows, the biggest
  continuity win -- 154 quarters, direct bridge across the 1971-2000 money-supply gap),
  household_expenditure_detail_urban_rural_2001_2020.csv (1088 rows, first-ever registration path
  for the previously-orphaned SCI HEIS extraction), gdp_by_final_expenditure_component_1991_2005.csv
  (42 rows, national-accounts household consumption counterpart to HEIS). README.md written with
  full provenance + explicit "what's still a gap" section (1972-1999 M1/M2 genuinely still open;
  HEIS 2021-2025 not found; CBI Annual Review FY1402+ not found). Next: staging-file registration,
  then fresh web hunting for the 1972-1999 M1/M2 gap and CBI/SCI forward extension.
- [2026-07-14T11:35:00Z] Wrote staging file data/processed/chart_registry_staging/enrichment_monetary_fiscal_household.csv,
  6 rows (via csv.DictWriter): 2 new flagship registrations of previously-orphaned-but-fully-processed
  data found during the survey (cbi_annual_review monetary_banking_aggregates -> chart_id
  iran_monetary__liquidity_m2_monetary_base_2000_2023; iran_plan_budget_org annual_budget_law_totals ->
  chart_id iranplanbudgetorg__annual_budget_law_totals, confirmed via grep it was referenced by name in
  another row's notes but never itself registered), plus 4 rows from this pass's own harmonization work
  (2 new: government-debt-to-CBI quarterly 1978-2016; 3 extends: IMF IFS money-supply 1937-1971 onto
  pahlavi__money_supply_changes_1957_59, HEIS household-expenditure 2001-2020 onto
  pahlavi_hh__expenditure_levels_rials_1965_1971, GDP-by-expenditure 1991-2005 onto
  iran_sci1399__gdp_by_expenditure_component_1390_1397). Did NOT run merge_chart_registry_staging.py
  myself (per project convention: a human/coordinator merges staging files, confirmed in memory notes).
  Next: fresh web hunting for the still-open 1972-1999 M1/M2 gap and CBI/SCI forward extension
  (FY1402+/2023+, HEIS 2021-2025).
- [2026-07-14T12:10:00Z] Fresh web-hunting phase: (1) tsd.cbi.ir (CBI's own time-series database,
  "annual data from 1959") confirmed a genuine, permanent dead end -- it's an ASP.NET WebForms
  postback-driven query tool, not a static data page; Wayback only captured the image splash screen,
  never a query result. (2) Found and harmonized a genuinely new source not previously in this
  project: JHU Institute for Applied Economics' Haver-Analytics-sourced Iran monetary database
  (data/raw/jhu-iae-haver-iran-monetary/), 29 quarterly CBI-attributed monetary/credit-aggregate
  metrics 1998Q4-2016Q2, 2059 rows -- cross-validated exactly against the existing CBI Annual Review
  data (2001-Q1 M2 match to the decimal). (3) CBI's own "Economic Trends" bulletin checked via
  Wayback -- category page has no direct PDF links, and the one page/<id>.aspx link found was an
  uncaptured redirect; ruled out as a near-term route. (4) Confirmed via WebSearch that CBI's own
  M1/M2 series is only published by the Bank itself from 1999 onward -- the 1972-1997 gap (between
  IMF IFS's 1971 endpoint and Haver's 1998 start) is a genuine, real, searched-for-and-not-found hole,
  documented explicitly in the series README rather than papered over. (5) Found and harmonized
  Djavad Salehi-Isfahani's (Virginia Tech economist) published analysis of SCI's own HEIS microdata
  for SH1402-1403 (2023-2025) -- data/raw/salehi-isfahani-heis-analysis/, 12 rows of growth-rate/
  poverty/Gini figures, partially closing (not fully -- these are rates/indices, not absolute levels)
  the "HEIS post-2020" gap flagged earlier. Added 2 more staging rows for these (total staging file
  now 8 rows). Updated README.md with both new sources + revised gap-honesty section. All processed
  CSVs + the staging file + both new manifest.json files verified structurally valid (csv.DictReader
  parse + json.load, all pass) before finishing.
