"""Build data/processed/chart_registry_staging/government_finance_banking.csv.

Reconciles the 4 already-harmonized government-finance/banking processed groups
(pahlavi_government_finance_series, majlis_budget_law_series, cbi_annual_review_series,
iran_banking_history_series -- all built by an earlier session, see
logs/downloads/government-finance-banking-harmonization.log) against the existing
data/processed/CHART_REGISTRY.csv (1,577 rows built by build_chart_registry.py from the
6 machine-readable sources: WDI, FAOSTAT, IMF WEO, OWID, Maddison, WID).

This script does NOT touch CHART_REGISTRY.csv, data/raw/, or any of the 4 source processed
folders -- it only WRITES the staging file. Every extends_chart_id value below was verified
by direct grep against CHART_REGISTRY.csv before being hardcoded here (see
logs/downloads/government-finance-banking-harmonization-staging.log [T+1] for the exact WDI
Iran-coverage-year queries that informed each extends-vs-new call).

Classification rule applied (per task brief): status=extends when a series covers the same
underlying concept as an existing chart_id for years that WDI's actual Iran data does NOT
reach (checked via macro_wdi.csv, not assumed); status=new when the series is a genuinely
distinct topic/granularity (money-supply composition detail, event logs, law-vs-outturn
concept mismatches, etc.) that no existing chart_id captures regardless of time overlap.
"""
import csv

OUT = "data/processed/chart_registry_staging/government_finance_banking.csv"
FIELDNAMES = ["chart_id", "title", "category", "primary_source", "alt_sources",
              "underlying_codes", "status", "extends_chart_id", "time_range", "notes"]

PAHLAVI_SRC = "pahlavi-era-primary-extraction"
MAJLIS_SRC = "majlis-historical-budget-laws"
CBI_SRC = "cbi-iran-annual-review"
GFDD_SRC = "worldbank-gfdd"
BANKHIST_SRC = "iran-banking-history"

rows = []

# ============================================================
# 1. pahlavi_government_finance_series/  (15 files -> 16 rows)
# ============================================================

rows.append({
    "chart_id": "pahlavi__actual_budget_revenues_1958_59",
    "title": "Government Revenue by Tax Category, Actuals (FY1958/59)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/actual_budget_revenues_1958_59.csv|wb1960-table12-actual-budget-revenues",
    "status": "extends",
    "extends_chart_id": "wdi__GC.REV.XGRT",
    "time_range": "FY1958/59 (single year)",
    "notes": "WDI's Iran GC.* government-finance series (incl. GC.REV.XGRT) only starts 1972 -- "
             "this single actual-revenue year sits 14 years before WDI's own Iran coverage begins. "
             "Direct/indirect tax and oil-transfer breakdown by category, actuals not budget. "
             "Unit: million rials, 1958/59 exchange rate -- do not convert to USD without checking "
             "the source table's own stated rate (see pahlavi_government_finance_series/README.md).",
})

rows.append({
    "chart_id": "pahlavi__actual_treasury_expenditures_1958_59",
    "title": "Government Expenditure by Ministry, Actuals (FY1958/59)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/actual_treasury_expenditures_1958_59.csv|wb1960-table11-actual-treasury-expenditures",
    "status": "extends",
    "extends_chart_id": "wdi__GC.XPN.TOTL",
    "time_range": "FY1958/59 (single year)",
    "notes": "Same pre-1972 WDI-gap logic as actual_budget_revenues_1958_59. Ministry-level "
             "granularity (Ministry of War, Education, Finance, Health, etc.) -- WDI's GC.XPN.TOTL "
             "is a single national aggregate with no ministry breakdown at any year, so this is "
             "also strictly more granular than the chart it extends, not just an earlier point on "
             "the same line.",
})

rows.append({
    "chart_id": "pahlavi__balance_of_payments_summary_1963_70",
    "title": "Balance of Payments Summary (FY1963/64-1969/70)",
    "category": "Balance of Payments (Net)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/balance_of_payments_summary_1963_70.csv|wb1971-appendix1-balance-of-payments-summary",
    "status": "extends",
    "extends_chart_id": "wdi__BN.CAB.XOKA",
    "time_range": "FY1963/64-1969/70 (+ 7-year CAGR summary rows)",
    "notes": "WDI's Iran balance-of-payments series (BN.CAB.XOKA.CD, BX.GSR.TOTL.CD, "
             "BM.GSR.TOTL.CD) only start 1976 -- this table covers 1963/64-1969/70, well before "
             "that gap. Covers exports (oil vs non-oil split), imports (goods vs services), "
             "current account, capital account, and monetary movements -- broader than just the "
             "current-account-balance chart it is mapped to; also touches BX.GSR.TOTL/BM.GSR.TOTL "
             "concepts. One illegible cell (1964/65 errors-and-omissions) left blank per "
             "no-fabrication rule -- see README caveats before charting.",
})

rows.append({
    "chart_id": "pahlavi__bank_deposits_private_sector_1963_70",
    "title": "Private-Sector Bank Deposits by Type (Sight/Saving/Time), FY1963/64-1969/70",
    "category": "Financial Sector (Monetary)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/bank_deposits_private_sector_1963_70.csv|wb1971-table6.5-bank-deposits-private-sector",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "FY1963/64-1969/70 (+ 2 rolling 12-month periods)",
    "notes": "Money-supply/deposit-composition DETAIL (sight vs. saving vs. time deposits, level + "
             "% of total) -- WDI's broad-money chart (wdi__FM.LBL.BMNY) already covers this exact "
             "period (Iran coverage 1960-2016) as a single aggregate with no deposit-type "
             "breakdown, so this does not extend WDI's time range, it adds granularity WDI never "
             "had. Per task brief's own 'money supply detail' new-topic example. README flags one "
             "column (FY1964/65) with a ~2.0bn-rial Total-vs-components discrepancy in the ORIGINAL "
             "1971 typescript, preserved as printed, not corrected.",
})

rows.append({
    "chart_id": "pahlavi__banking_statistics_private_sector_1957_59",
    "title": "Deposit Banks vs. National Bank Private-Sector Deposits/Advances, 1957-1959",
    "category": "Financial Sector (Monetary)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/banking_statistics_private_sector_1957_59.csv|wb1960-table14-banking-statistics-private-sector",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "June 20 snapshots, 1957-1959",
    "notes": "Deposit-bank-vs-National-Bank institutional split, plus an advances/deposits ratio -- "
             "not tracked by WDI or any existing chart_id at any granularity. README flags the "
             "'Excess Cash' row's ambiguous parenthetical sign convention, preserved as a positive "
             "magnitude per the original manifest's interpretation.",
})

rows.append({
    "chart_id": "pahlavi__budgeted_vs_actual_expenditures_1955_60",
    "title": "Budgeted vs. Actual Government Expenditure by Ministry (FY1955/56-1959/60)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/budgeted_vs_actual_expenditures_1955_60.csv|wb1960-table10-budgeted-expenditures",
    "status": "extends",
    "extends_chart_id": "wdi__GC.XPN.TOTL",
    "time_range": "FY1955/56-1959/60",
    "notes": "Pre-1972 WDI-gap extension for government expenditure, same as the other Pahlavi "
             "expenditure tables. Distinctive extra angle no WDI chart carries at any year: "
             "BUDGETED figure side-by-side with ACTUAL figure by ministry, i.e. budget-execution "
             "variance -- a structurally different question ('did they spend what they planned') "
             "from a simple expenditure-level time series. Flagging this bonus dimension rather "
             "than treating the file as pure duplicate-of-level-series.",
})

rows.append({
    "chart_id": "pahlavi__central_govt_operations_summary_1962_73",
    "title": "Central Government Fiscal Operations: Revenue, Expenditure, Deficit & Financing (FY1962-1973)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/central_govt_operations_summary_1962_73.csv|wb1974-table6.1-central-govt-operations-summary",
    "status": "extends",
    "extends_chart_id": "wdi__GC.NLD.TOTL",
    "time_range": "FY1962-1973 (incl. preliminary actuals 1972, budget estimate 1973)",
    "notes": "Full IMF-GFS-style fiscal-operations statement: total revenue, current + capital "
             "expenditure, deficit, savings, and a FINANCING breakdown by source (net borrowing "
             "abroad / net borrowing from the banking system / nonbank holdings of government "
             "securities). The financing-by-source split has no equivalent in WDI's GC.* group at "
             "any year -- genuinely more granular than the net-lending/borrowing chart it is mapped "
             "to, not just an earlier data point. Also jointly extends wdi__GC.REV.XGRT (Total "
             "Revenues row) and wdi__GC.XPN.TOTL (Current+Capital Expenditure rows); one "
             "extends_chart_id per staging row, so those two are noted here rather than given "
             "separate rows since this is one integrated statement in the source. This is the only "
             "one of the Pahlavi expenditure tables with a CAPITAL expenditure line (others are "
             "current/ordinary-budget only) -- not directly comparable to the ministry-level "
             "current-only breakdowns without accounting for that scope difference (see README).",
})

rows.append({
    "chart_id": "pahlavi__century_indicators_bookend_1900_2006",
    "title": "Macro/Demographic Bookend Snapshot: Population, Income, Life Expectancy, Literacy, Urbanization, Agriculture Share, Trade Ratio (1900 vs. 2006)",
    "category": "Demographics & Population",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/century_indicators_1900_2006.csv|esfahani-pesaran-2008-century-indicators",
    "status": "extends",
    "extends_chart_id": "wdi__SP.POP",
    "time_range": "1900 (rough estimate) vs. 2006",
    "notes": "Bundles 7 different macro/demographic concepts as a single two-point (1900, 2006) "
             "bookend table (Esfahani & Pesaran 2008, Table 1); this row's single extends_chart_id "
             "captures Population (wdi__SP.POP) as primary, but the file equally extends: "
             "wdi__NY.GDP.PCAP (per-capita income), wdi__SP.DYN.LE00 (life expectancy), "
             "wdi__SE.ADT.LITR (literacy rate, pop. 15+), wdi__SP.URB.TOTL.IN (urbanization rate), "
             "wdi__NV.AGR.TOTL (agriculture share of GDP), and wdi__NE.TRD.GNFS (trade/GDP ratio) "
             "-- all confirmed present in CHART_REGISTRY.csv. The unique contribution is the single "
             "1900 anchor point, decades before WDI/Maddison's own Iran coverage begins for most of "
             "these series (WDI Population/GDP-per-capita start 1960). 1900 values are explicitly "
             "labeled rough estimates by the source (several carry a '?' or '<' marker, preserved "
             "in notes) -- treat as order-of-magnitude anchors, not precise data points. See "
             "pahlavi__century_indicators_world_rank_1900_2006 (this file's other row) for the "
             "world-rank sub-statistics, split out as status=new.",
})

rows.append({
    "chart_id": "pahlavi__century_indicators_world_rank_1900_2006",
    "title": "Iran's World Rank in Population, Per-Capita Income & Life Expectancy (1900 vs. 2006)",
    "category": "Demographics & Population",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/century_indicators_1900_2006.csv|esfahani-pesaran-2008-century-indicators",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "1900 (rough estimate) vs. 2006",
    "notes": "The same source file's 'rank in the world' and 'out of (N countries ranked)' rows -- "
             "a fundamentally different statistic TYPE (Iran's relative cross-country standing, not "
             "a level or growth rate) that no existing chart_id in CHART_REGISTRY.csv tracks at any "
             "granularity. Split out from the level-bookend row above because it doesn't extend any "
             "existing chart's time range or concept -- it's a new angle entirely.",
})

rows.append({
    "chart_id": "pahlavi__fiscal_system_narrative_indicators_1921_79",
    "title": "Fiscal-Structure Narrative Indicators: Tax Mix, Oil-Revenue Share, Expenditure Shares (1920-1977)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/fiscal_system_narrative_indicators_1921_79.csv|iranica-fiscal-system-narrative-1921-1979",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "1920-1977 (irregular: single years, multi-year periods, decade averages as stated in source prose)",
    "notes": "Iran-specific fiscal-structure indicators transcribed from Encyclopaedia Iranica's "
             "narrative prose (citing Bharier 1971, Karshenas 1990): direct/indirect tax shares of "
             "revenue, CUSTOMS-REVENUE-AS-RATIO-OF-DUTIABLE-IMPORTS, OIL-REVENUE SHARE OF BUDGET, "
             "effective tax rates on property/corporate income and on wages, development-project "
             "share of expenditure, First Seven-Year Plan financing splits. None of these are "
             "tracked by any existing chart_id, WDI's GC.* group included -- WDI has no 'oil "
             "revenue as % of government budget' indicator for Iran at any year, which is arguably "
             "the single most economically important fiscal fact about 20th-century Iran. NOT an "
             "annual series (irregular points, several values are themselves ranges e.g. "
             "'10-16 percent' or approximate e.g. '~100' exactly as Iranica states them) -- do not "
             "average a stated range to a point estimate.",
})

rows.append({
    "chart_id": "pahlavi__government_revenue_summary_1962_72",
    "title": "Government Revenue by Category (FY1962/63-1971/72)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/government_revenue_summary_1962_72.csv|wb1971-table5.2-government-revenue-summary",
    "status": "extends",
    "extends_chart_id": "wdi__GC.REV.XGRT",
    "time_range": "FY1962/63-1971/72 (incl. budget-estimate/revised-estimate/draft-budget columns for 1970/71-1971/72)",
    "notes": "Almost entirely fills the pre-1972 gap in WDI's Iran GC.REV.XGRT coverage (WDI starts "
             "1972; this table runs through FY1971/72, ending exactly at the WDI boundary). Overlaps "
             "in time with pahlavi__central_govt_operations_summary_1962_73's 'Total Revenues' rows "
             "(1962-1971) but the two multi-year tables' totals do NOT agree exactly (e.g. FY1969/70: "
             "143.9bn vs 150.4bn rials for the same nominal year, per README) -- kept as two distinct "
             "report vintages, not merged into one reconciled figure. Direct/indirect tax and oil "
             "revenue breakdown by category.",
})

rows.append({
    "chart_id": "pahlavi__monetary_aggregates_movements_1963_73",
    "title": "Money & Quasi-Money Component Movements, Year-over-Year Flows (FY1963-1973)",
    "category": "Financial Sector (Monetary)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/monetary_aggregates_movements_1963_73.csv|wb1974-table7.1-movements-monetary-aggregates",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "FY1963-1973",
    "notes": "Money-supply FLOW (year-over-year change) detail by component (domestic assets net, "
             "foreign assets net, other items net) -- not a level series, so not directly comparable "
             "to WDI's FM.LBL.BMNY level chart even where the years overlap (WDI Iran coverage "
             "1960-2016, fully overlapping this file's span). Per README, this is the 1974-vintage "
             "'later/extended re-run of the same flow concept' as "
             "pahlavi__money_quasi_money_changes_1965_71 below -- the two overlap 1965-1971 and "
             "should be treated as two vintages of the same underlying flow concept, not summed or "
             "reconciled to one number.",
})

rows.append({
    "chart_id": "pahlavi__monetary_survey_1963_70",
    "title": "Consolidated Banking-System Balance Sheet, Year-End Stock Levels (FY1963/64-1969/70)",
    "category": "Financial Sector (Monetary)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/monetary_survey_1963_70.csv|wb1971-table6.1-monetary-survey",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "FY1963/64-1969/70",
    "notes": "Full consolidated banking-system balance sheet (foreign assets net, claims on public/ "
             "private sector, money supply, time & savings deposits, SDR allocation, capital "
             "accounts) at year-end STOCK levels -- far more granular than WDI's single "
             "FM.LBL.BMNY broad-money aggregate for the same 1960-2016 window. Level-series "
             "counterpart to the flow-series files above; do NOT mix the two families on one chart "
             "without labeling (per README).",
})

rows.append({
    "chart_id": "pahlavi__money_quasi_money_changes_1965_71",
    "title": "Money & Quasi-Money Component Changes, Year-over-Year Flows (FY1964/65-1970/71)",
    "category": "Financial Sector (Monetary)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/money_quasi_money_changes_1965_71.csv|wb1971-table6.2-changes-money-quasi-money",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "FY1964/65-1970/71 projection + 2 first-half-year figures",
    "notes": "Earlier (1971-vintage) sibling of pahlavi__monetary_aggregates_movements_1963_73 -- "
             "same flow concept, overlapping years 1965-1971, values are close but distinct report "
             "vintages per README ('never merged into one winning number'). Money-supply flow "
             "detail, not tracked by WDI at this granularity regardless of time overlap.",
})

rows.append({
    "chart_id": "pahlavi__money_supply_changes_1957_59",
    "title": "Money Supply & Claims Composition, Semi-Annual Changes (1957-1959)",
    "category": "Financial Sector (Monetary)",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/money_supply_changes_1957_59.csv|wb1960-table8-changes-in-money-supply",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "June/Dec snapshots, 1957-1959",
    "notes": "Money-supply composition detail (claims on government, official entities, and private "
             "sector split Bank Melli vs. deposit banks; both period-over-period and June-on-June "
             "changes) -- classified new per the task brief's money-supply-detail example, though "
             "worth flagging that this 1957-1959 window also slightly PREDATES WDI's Iran "
             "FM.LBL.BMNY broad-money series start (1960), so it has a minor extends-like character "
             "too; not given extends status because the file's real content (claims/composition "
             "breakdown) has no counterpart in WDI at any year, not just the 2-3 pre-1960 years.",
})

rows.append({
    "chart_id": "pahlavi__ordinary_budget_expenditure_1962_72",
    "title": "Ordinary (Current) Budget Expenditure by Category (FY1962/63-1971/72)",
    "category": "Government Finance",
    "primary_source": PAHLAVI_SRC,
    "alt_sources": "",
    "underlying_codes": "pahlavi_government_finance_series/ordinary_budget_expenditure_1962_72.csv|wb1971-table5.1-ordinary-budget-expenditure",
    "status": "extends",
    "extends_chart_id": "wdi__GC.XPN.TOTL",
    "time_range": "FY1962/63-1971/72 (incl. estimate/draft columns)",
    "notes": "Fills the pre-1972 gap in WDI's Iran GC.XPN.TOTL coverage, ending exactly at WDI's own "
             "start year. CURRENT/ordinary-budget expenditure only (Defense & Security, General "
             "Services, Social & Economic Services, Interest Payments) -- narrower scope than "
             "pahlavi__central_govt_operations_summary_1962_73's Current+Capital split for the same "
             "overlapping years (1962-1972); the two are not directly comparable without accounting "
             "for that scope difference, per README.",
})

# ============================================================
# 2. majlis_budget_law_series/  (4 files -> 4 rows)
# ============================================================

rows.append({
    "chart_id": "majlis__national_budget_totals_by_fiscal_year",
    "title": "Whole-Country Enacted Budget Law Totals: Revenue & Expenditure (FY1341-1370)",
    "category": "Government Finance",
    "primary_source": MAJLIS_SRC,
    "alt_sources": "",
    "underlying_codes": "majlis_budget_law_series/national_budget_totals_by_fiscal_year.csv",
    "status": "extends",
    "extends_chart_id": "wdi__GC.XPN.TOTL",
    "time_range": "FY1341-1370 (1963-1992 Western fiscal-year-end; 16 discontinuous fiscal years, 21 with any figure)",
    "notes": "Jointly extends wdi__GC.XPN.TOTL (expenditure_rials column, primary) and "
             "wdi__GC.REV.XGRT (revenue_rials column, co-extended -- both figures appear together "
             "in every row since Iran budget law traditionally sets revenue=expenditure by design "
             "pre-FY1355, see README). IMPORTANT CONCEPT CAVEAT: this is ENACTED-LAW (ex-ante) "
             "figures from the Majlis's own gazetted text, NOT audited outturns -- WDI's GC.* "
             "series and this project's own pahlavi_government_finance_series/ (World-Bank-sourced, "
             "1962/63-1971/72) are outturn/actuals-based. The 1963-1972 span in this file OVERLAPS "
             "pahlavi_government_finance_series's government_revenue_summary_1962_72.csv and "
             "ordinary_budget_expenditure_1962_72.csv, but per majlis_budget_law_series/README.md "
             "('this folder does not yet reconcile against pahlavi_government_finance_series'), NO "
             "cross-check between law-vs-actual figures has been performed -- flagging as an open "
             "reconciliation item, not resolved here. Also carries FY1358's law-vs-component-sum gap "
             "(22.86bn rial), FY1368/FY1370's component-sum-exceeds-total gaps (451bn / 1.24tn rial), "
             "and FY1344's deficit-consistency mismatch -- all preserved exactly as printed per "
             "README, never resolved to one number.",
})

rows.append({
    "chart_id": "majlis__ministry_level_appropriations_1301",
    "title": "Pre-Consolidated Ministry-Level Budget Appropriations (FY1301, Public Works/Justice/Foreign Affairs)",
    "category": "Government Finance",
    "primary_source": MAJLIS_SRC,
    "alt_sources": "",
    "underlying_codes": "majlis_budget_law_series/ministry_level_appropriations_1301.csv",
    "status": "extends",
    "extends_chart_id": "wdi__GC.XPN.TOTL",
    "time_range": "FY1301 (1922/23)",
    "notes": "Earliest government-expenditure data point in this database's government-finance "
             "collection (1922/23, 50 years before WDI's Iran GC.* coverage begins) -- but flagged "
             "as NOT directly comparable in magnitude to any later Rial-denominated series: FY1301 "
             "figures are in TOMANS (Iran's currency until the 1932 conversion, 1 toman = 10 rials), "
             "transcribed in original denomination with no retroactive conversion applied. Also "
             "carries the README's documented raw-filename mislabeling: the 'foreign-ministry' and "
             "'public-works-ministry' raw HTML filenames are SWAPPED relative to actual body-text "
             "content -- this processed CSV uses the CORRECT ministry attribution, raw files left "
             "untouched per bookkeeping policy.",
})

rows.append({
    "chart_id": "majlis__supplementary_budget_additions",
    "title": "Mid-Year Supplementary Budget Additions (FY1357, 1358, 1369)",
    "category": "Government Finance",
    "primary_source": MAJLIS_SRC,
    "alt_sources": "",
    "underlying_codes": "majlis_budget_law_series/supplementary_budget_additions.csv",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "FY1357/1358/1369 (1979, 1980, 1991)",
    "notes": "Mid-year top-up (متمم) appropriation DELTAS, not annual totals -- a structurally "
             "different concept from every level/aggregate series in this database, so classified "
             "new rather than as an extension of the expenditure-level charts despite covering "
             "years (1979/1980/1991) that fall inside WDI's own Iran GC.* window (1972-2009). For "
             "FY1357 and FY1369, this is the ONLY primary-source budget figure available at all in "
             "this collection (the main annual law was not located) -- must not be presented as a "
             "full-year budget total on any chart.",
})

rows.append({
    "chart_id": "majlis__forex_budget_law_1364",
    "title": "War-Economy Foreign-Exchange Allocation Ceiling Law (FY1364)",
    "category": "Government Finance",
    "primary_source": MAJLIS_SRC,
    "alt_sources": "",
    "underlying_codes": "majlis_budget_law_series/forex_budget_law_1364.csv",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "FY1364 (1985/86)",
    "notes": "USD 15 billion maximum foreign-currency allocation ceiling for the fiscal year "
             "(Iran-Iraq war FX rationing law) -- a distinct policy-instrument figure with no analog "
             "anywhere else in this database (not comparable to WDI's exchange-rate or reserves "
             "indicators, which measure market outcomes, not a legislated allocation ceiling). "
             "Single data point, one fiscal year only; the general RIAL-denominated FY1364 national "
             "budget law was not located in this collection (confirmed gap, see README) so this is "
             "a narrower, separate law, not a stand-in for the missing main budget.",
})

# ============================================================
# 3. cbi_annual_review_series/  (1 file -> 1 row)
# ============================================================

rows.append({
    "chart_id": "cbi__monetary_banking_aggregates_1379_1401",
    "title": "Liquidity (M2), Monetary Base & Inflation, CBI Annual Review Aggregates (FY1379-1401)",
    "category": "Financial Sector (Monetary)",
    "primary_source": CBI_SRC,
    "alt_sources": "wdi",
    "underlying_codes": "cbi_annual_review_series/monetary_banking_aggregates_1379_1401.csv",
    "status": "extends",
    "extends_chart_id": "wdi__FM.LBL.BMNY",
    "time_range": "FY1379-1401 (2000/01-2022/23)",
    "notes": "Primary driver of extends status: the Liquidity(M2) level+growth columns (23/23 years, "
             "full coverage) extend PAST WDI's Iran FM.LBL.BMNY cutoff (2016) through FY1401 "
             "(2022/23) -- 6-7 additional years no WDI chart reaches for Iran. For the OVERLAPPING "
             "years (2001-2016) this is an independent CBI-sourced alt vintage of the same broad-"
             "money concept, not previously cross-checked against WDI's own FM.LBL.BMNY figures for "
             "those years (flagging as an open reconciliation item, not performed here). Monetary "
             "base column (19/23 growth-rate years, 5/23 level years) has NO direct WDI Iran "
             "analog at any year -- a genuinely new sub-component bundled into this same row rather "
             "than split out, given its partial/secondary coverage. CPI/inflation column (6/23 "
             "years) is REDUNDANT with WDI's already-FULL Iran FP.CPI.TOTL.ZG coverage (1960-2025, "
             "no gap) -- explicitly NOT counted as an extension, included in this row only for "
             "completeness/traceability. Also carries README's documented FY1396 raw-filename "
             "Western-year mislabeling and the FY1383 inter-report revision example (both flagged, "
             "neither resolved to one number).",
})

# ============================================================
# 4. iran_banking_history_series/  (4 files -> 10 rows: GFDD split x7 + 3 others)
# ============================================================

GFDD_ROWS = [
    ("GFDD.DI.01", "Private Credit by Deposit Money Banks to GDP",
     "wdi__FD.AST.PRVT.GD", "1961", "2016",
     "Closest WDI analog is wdi__FD.AST.PRVT.GD (Domestic credit to private sector by banks, % "
     "of GDP), which covers the identical 1961-2016 Iran window -- so this does NOT extend WDI's "
     "time range, it is an independently-sourced (GFDD via FRED, not WDI's own bulk file) alt "
     "vintage of a near-identical concept. README confirms GFDD.* codes do not appear anywhere in "
     "macro_wdi.csv. Flagging the conceptual overlap for a future reconciliation pass rather than "
     "merging -- classified new per this project's policy of not silently resolving alt-source "
     "overlaps."),
    ("GFDD.DI.04", "Deposit Money Bank Assets to Deposit Money Bank Assets and Central Bank Assets",
     "", "1961", "2016",
     "No WDI Iran analog found for this specific structural ratio (deposit-money-bank share of "
     "total banking-system assets) -- genuinely new content, not just a new source for an existing "
     "concept."),
    ("GFDD.DI.05", "Liquid Liabilities to GDP",
     "wdi__FM.LBL.BMNY.GD", "1960", "2016",
     "Conceptually close to wdi__FM.LBL.BMNY.GD (Broad money, % of GDP) -- 'liquid liabilities' is "
     "the standard IFS/GFDD term for the same M2/M3 broad-money concept WDI calls broad money. "
     "Identical 1960-2016 Iran window as WDI, so not a time extension -- an alt-source vintage of "
     "the same underlying aggregate, flagged for future reconciliation, not merged."),
    ("GFDD.DI.06", "Central Bank Assets to GDP",
     "", "1960", "2016",
     "No WDI Iran analog found (WDI's FM.AST.* codes are net domestic credit / net foreign assets "
     "in current LCU levels, not a central-bank-assets-to-GDP ratio) -- genuinely new content."),
    ("GFDD.OI.02", "Bank Deposits to GDP",
     "", "1961", "2016",
     "No WDI Iran indicator for bank-deposits-to-GDP found -- genuinely new content, complements "
     "the deposit-composition detail in pahlavi__bank_deposits_private_sector_1963_70 (different "
     "era, different granularity: aggregate/GDP-ratio here vs. sight/saving/time composition "
     "there)."),
    ("GFDD.OI.07", "Liquid Liabilities (Broad Money)",
     "wdi__FM.LBL.BMNY", "1960", "2016",
     "Level-form counterpart to GFDD.DI.05 above; conceptually close to wdi__FM.LBL.BMNY (Broad "
     "money, current LCU) -- same 1960-2016 Iran window as WDI, so an alt-source vintage rather "
     "than a time extension. Check currency/unit basis (GFDD/FRED extract vs. WDI's own LCU "
     "series) before treating as directly comparable -- not verified equal in this pass."),
    ("GFDD.SI.04", "Bank Credit to Bank Deposits",
     "", "1961", "2016",
     "No WDI Iran analog -- genuinely new content, a banking-sector liquidity/leverage ratio not "
     "tracked elsewhere in this database."),
]

for code, label, alt_wdi, ymin, ymax, note in GFDD_ROWS:
    slug = code.lower().replace(".", "_")
    rows.append({
        "chart_id": f"gfdd__{slug}",
        "title": f"{label} (World Bank GFDD)",
        "category": "Financial Sector (Monetary)",
        "primary_source": "worldbank-gfdd-via-fred",
        "alt_sources": "wdi" if alt_wdi else "",
        "underlying_codes": f"iran_banking_history_series/worldbank_gfdd_banking_depth_1960_2016.csv|{code}",
        "status": "new",
        "extends_chart_id": "",
        "time_range": f"{ymin}-{ymax}",
        "notes": note + (f" (closest existing chart_id: {alt_wdi})" if alt_wdi else ""),
    })

rows.append({
    "chart_id": "banking_hist__branch_network_timeseries_1919_2016",
    "title": "Bank & Branch Network Counts (1919-2016)",
    "category": "Financial Sector (Banking Access)",
    "primary_source": BANKHIST_SRC,
    "alt_sources": "",
    "underlying_codes": "iran_banking_history_series/branch_network_timeseries_1919_2016.csv",
    "status": "extends",
    "extends_chart_id": "wdi__FB.CBK.BRCH",
    "time_range": "1919-2016 (9 sparse anchor points: 1919, 1940, 1954, 1977, 1978, 1982, 2004, 2005, 2016)",
    "notes": "WDI's Iran commercial-bank-branches series (FB.CBK.BRCH.P5) only covers 2004-2018 -- "
             "this table reaches back to 1919, 85 years earlier. UNIT-BASIS CAVEAT: this file "
             "reports raw bank/branch COUNTS and branches-per-MILLION-population, not WDI's "
             "branches-per-100,000-adults ratio -- not a drop-in splice, needs a unit-basis "
             "reconciliation before combining on one chart, not attempted here. SPARSE, not "
             "continuous (9 points across 97 years) -- do not interpolate between points without "
             "labeling gaps. Brackets a real discontinuity, not a data gap: the 1977->1982 span "
             "captures the 1979 bank-nationalization shock (36 banks/8,275 branches -> 9 banks/"
             "6,581 branches) -- see banking_hist__nationalization_1979_events for the paired "
             "event log. Source (Encyclopaedia Iranica) itself flags a confirmed digitization gap "
             "for 6 referenced-but-never-digitized data tables (Tables 25-30) -- a genuine "
             "source-side gap per README, not a search failure.",
})

rows.append({
    "chart_id": "banking_hist__nationalization_1979_events",
    "title": "1979 Bank Nationalization & Consolidation Event Log",
    "category": "Financial Sector (Banking Access)",
    "primary_source": BANKHIST_SRC,
    "alt_sources": "",
    "underlying_codes": "iran_banking_history_series/nationalization_1979_consolidation_events.csv",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "1979-1984 (16-row event log)",
    "notes": "Event log (nationalization decree, 5-bank consolidation into Ma'dan-va-San'at/Maskan/"
             "Keshavarzi/Tejarat/Mellat, which banks stayed unmerged, the sole non-nationalized bank "
             "Bank Iran-o-Rus, the 1983-84 Islamic-banking law) -- not a numeric time series, no "
             "existing chart_id concept applies. Preserves an unresolved date discrepancy (28 May "
             "1979 decree per Encyclopaedia Iranica vs. 8-9 June 1979 takeover per Western press "
             "archives) exactly as found, per this project's never-pick-a-winner policy for "
             "disagreeing sources -- flagged again here, not resolved.",
})

rows.append({
    "chart_id": "banking_hist__private_bank_reentry_2000_2025",
    "title": "Post-Privatization Private Bank Founding/Licensing Timeline (2000-2025)",
    "category": "Financial Sector (Banking Access)",
    "primary_source": BANKHIST_SRC,
    "alt_sources": "",
    "underlying_codes": "iran_banking_history_series/private_bank_reentry_2000_2025.csv",
    "status": "new",
    "extends_chart_id": "",
    "time_range": "2000-2025 (13 named banks + 2 summary rows for unidentified cohorts)",
    "notes": "Entity-level founding/licensing-date log for Iran's post-2000 private banking wave, "
             "ending with Ayandeh Bank's 2025 CBI-ordered dissolution/merger into Bank Melli -- not "
             "a numeric time series, no existing chart_id concept applies (WDI's banking-access "
             "indicators are aggregate ratios, not named-entity timelines). Two rows are explicit "
             "summary placeholders for unidentified bank cohorts ('seven unspecified banks' 2001-11, "
             "'eight unspecified banks' 2011) -- confirmed real gaps (source states the fact but not "
             "individual names), flagged as an open lead for a future continuation pass, not "
             "fabricated, per README.",
})

# ============================================================
# Write
# ============================================================

with open(OUT, "w", newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDNAMES)
    w.writeheader()
    for r in rows:
        w.writerow(r)

n_extends = sum(1 for r in rows if r["status"] == "extends")
n_new = sum(1 for r in rows if r["status"] == "new")
print(f"Wrote {len(rows)} rows to {OUT}")
print(f"  status=extends: {n_extends}")
print(f"  status=new:     {n_new}")
assert n_extends + n_new == len(rows)
