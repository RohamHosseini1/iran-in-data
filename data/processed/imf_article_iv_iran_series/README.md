# IMF Article IV Consultation staff reports -- Iran (2015 and 2018)

The two Iran-specific IMF Article IV Country Reports found in `data/raw/policy-docs/imf-article-iv/`
mined table-by-table into one tidy long-format CSV. Both source PDFs are born-digital (no OCR
needed); most tables extracted cleanly via `pdftotext -layout`, and the handful that came through
as embedded images were transcribed via `pdftoppm -png -r 150` + visual read. **1,947 rows.**

## Overlap check against the existing IMF Article IV holdings (done first, per task instructions)

`data/raw/imf-article-iv-iran/consultation-history-2002-2025/imf_article_iv_iran_consultation_history.csv`
already exists in this project and covers every Article IV consultation from 2002-2025, including
2015 and 2018 -- but that file is a lightweight **metadata/headline-findings table** (one row per
consultation, sourced from IMF press releases and Public Information Notices), not the full
statistical content of the underlying Country Report PDFs. There is **no row-level overlap**: this
new file's ~1,947 rows are actual macro/fiscal/monetary/external-sector time series pulled from the
full Staff Reports, which the existing consultation-history file does not contain at all. Both
files can coexist and serve different purposes -- consult the older file for a quick chronological
narrative of each consultation's headline conclusion, and this file for the underlying numbers.

## Scoping decision: comparator-country reports NOT extracted

`data/raw/policy-docs/imf-article-iv/` also contains three 2025 Article IV reports for Saudi Arabia,
Korea, and Turkiye. These were **not extracted** for this file. Their `manifest.json` gives no
stated Iran-linkage rationale for their inclusion in the raw folder, and per this project's
Iran-first scoping policy (comparator data is only included when it has a real Iran anchor --
shared border, trade relationship, sanctions-regime comparison, etc., not just "another Middle
Eastern or emerging economy"), pulling three full 2025 Article IV statistical annexes with no
documented Iran connection would be a pure comparator-only expansion out of scope for this task.
This is a deliberate, documented non-extraction, consistent with a similar decision made elsewhere
in this project for a comparator-only EU appliance-statistics dataset. If a future task identifies
a specific Iran-linked reason to mine these three reports (e.g., a Turkiye-Iran trade or
sanctions-evasion angle), they remain available unextracted in the raw folder.

## Schema

`date_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset, citation`

Same schema as this project's other primary-source extraction CSVs. `country_iso3` is always `IRN`.
`subcategory` retains the source table's own line-item hierarchy using `--` separators (e.g.
`"Table 3 Augmented Central Government Operations -- Revenue -- Nontax revenue -- Oil revenue"`)
so the original table structure can be reconstructed by filtering/pivoting on `subcategory` prefix.

## The two source documents and what was extracted

| `source_dataset` | Document | Rows | Tables extracted |
|---|---|---|---|
| `imf-article-iv-iran-2015` | IMF Country Report 15/349, "Islamic Republic of Iran: 2015 Article IV Consultation", Dec 2015 | 975 | Table 1 (Selected Macroeconomic Indicators, 2013/14-2020/21), Table 2 (Balance of Payments), Table 3 (Statement of Government Operations, rials), Table 5 (Monetary Survey), Table 7 (Vulnerability Indicators, 2010/11-2014/15) |
| `imf-article-iv-iran-2018` | IMF Country Report 18/93, "Islamic Republic of Iran: 2018 Article IV Consultation", March 2018 | 972 | Table 2 (Selected Macroeconomic Indicators, 2015/16-2022/23), Table 3 (Augmented Central Government Operations), Table 9 (Balance of Payments), Table 10 (Labor and Population Data), Table 12 (Monetary Survey), plus 3 narrative-text figures from the Press Release |

Both reports bundle multiple sub-documents in one PDF (Staff Report + Informational Annex +
Press Release + Statement by Executive Director); all extracted figures come from the Staff
Report's numbered tables and, for the 2018 file, three additional cited figures from the bundled
Press Release text. The Informational Annexes (Fund Relations, World Bank Relations, Statistical
Issues) contain no economic time-series data and were not mined.

## Tables intentionally NOT extracted (time-boxed scoping, not extraction failure)

Both reports contain additional numbered tables beyond the ones listed above -- these were skipped
as substantially redundant with an already-extracted table, or lower priority given this task's
overall breadth across many source documents:
- **2015 report**: Table 4 (percent-of-GDP restatement of Table 3 -- redundant with Table 1's
  already-included budgetary-operations percent-of-GDP rows), Table 6 (Medium-Term Scenario --
  a summary restatement duplicating figures already in Table 1), and the Appendix I Debt
  Sustainability Analysis (technical debt-dynamics projections, lower priority for this project's
  purposes).
- **2018 report**: Table 1 (Status of Staff Recommendations from the 2016 consultation -- a
  compliance checklist, not economic data), Table 4 (percent-of-GDP restatement of Table 3),
  Table 5 (rials restatement of Table 3/4's central government operations -- Table 3's "Augmented"
  version already captures the fuller rials-denominated picture), Table 6 (Government Oil Revenue
  and Funds) and Table 7 (Targeted Subsidy Organization Accounts, one year only) -- narrower
  sub-topics of the fiscal picture already in Table 3, Table 8 (percent-of-GDP restatement of
  Table 9's Balance of Payments), Table 11 (Central Bank Balance Sheet -- substantially overlaps
  with Table 12's Monetary Survey, which was extracted instead), and Appendices I-III (External
  Sector Assessment narrative, Public DSA, External DSA -- debt-sustainability projections).

If a future task needs any of these specific skipped tables, both raw PDFs are born-digital and
`pdftotext -layout` (for text-layer tables) or `pdftoppm` + visual read (for the handful of
image-embedded tables, confirmed present in the 2015 report's Tables 2/5/7) will extract them
using the same method as this file.

## Notable content

- **2015 report** (written weeks after the JCPOA nuclear deal, Dec 2015): captures Iran's economy
  at the pre-sanctions-relief inflection point -- 2014/15 real GDP growth of just 3%, projected to
  fall to 0-0.5% in 2015/16 before the anticipated sanctions-relief rebound; CPI inflation still at
  15.5% average; a 2012/13 real effective exchange rate collapse of -29.6% visible in Table 7's
  vulnerability indicators; and staff projections built around the expectation of sanctions relief
  (crude oil exports projected to jump from 1.24 to 1.81 million b/d between 2015/16 and 2016/17).
- **2018 report** (last full Article IV as of this project's other holdings, concluded March 2018,
  discussions completed just before Iran-US tensions escalated again): shows the realized post-JCPOA
  rebound -- real GDP growth of 12.5% in 2016/17 (driven by a 61.6% jump in real oil GDP as
  sanctions-era production curbs lifted), crude oil exports rising to 2.1-2.5 million b/d, and a
  detailed Table 10 labor-market breakdown (including gender-disaggregated unemployment: 20.7%
  female vs. 10.5% male in 2016/17, and 29.1% youth unemployment) not available in the 2015 report.
  The Press Release notes an official/market exchange-rate spread that had narrowed to "under 20
  percent" by early 2018 after a February 2018 interest-rate hike -- an early sign of the exchange-
  rate pressure that would intensify later in 2018 after the US withdrew from the JCPOA (outside
  this report's information cutoff).
- Table 3's (2018 report) 2018/19 spike in "Net acquisition of financial assets/liabilities" to
  roughly 4.9-5.3 trillion rials -- two orders of magnitude above neighboring years -- is preserved
  exactly as printed; the source table gives no further breakdown explaining the one-off jump.

## Caveats -- read before charting

- **Every figure from 2015/16 (2015 report) or 2018/19 (2018 report) onward is a Fund staff
  projection, not an outturn** -- check `date_label`'s `"(proj.)"`/`"(est.)"` suffix before treating
  a row as a realized historical value. Because Iran has not completed a full Article IV
  consultation since 2018 (per the existing `imf-article-iv-iran/consultation-history-2002-2025`
  file), none of the 2018 report's projected years (2018/19-2022/23) were ever updated or confirmed
  by a subsequent full consultation -- treat them as the IMF's early-2018 forecast, not as reported
  outturns.
- **The 2015 and 2018 reports use different base years and are not a continuous series** -- the
  2015 report's Table 1 covers 2013/14-2020/21; the 2018 report's Table 2 covers 2015/16-2022/23.
  The overlapping years (2015/16-2017/18) sometimes carry different values between the two reports
  for the same nominal metric (e.g. 2016/17 real GDP growth: the 2015 report had no data for that
  far out, while the 2018 report reports an outturn of 12.5%) because the 2018 report reflects
  updated data/outturns unavailable when the 2015 report was written. Do not silently average or
  splice the two reports' overlapping-year figures together.
- **The Iranian fiscal year ends March 20** — a `date_label` like `"2016/17"` denotes the Iranian
  fiscal year running roughly late March 2016 to late March 2017, not a Gregorian calendar year;
  the `year` column uses the *ending* Gregorian year as its anchor for sortability.
- A handful of Table 10 (2018 report) gender/youth-disaggregated labor rows only have data for
  2015/16-2017/18 -- the source printed literal ellipses (`"..."`) for 2018/19 onward, which were
  left out of this file entirely (not represented as blank rows) rather than guessed.
