# Majlis historical budget-law texts, FY1301-FY1370 (1922/23-1991/92)

Harmonized 2026-07-13 from `data/raw/majlis-historical-budget-laws/lamtakam-mirror-1301-1363/`
(24 Persian-language HTML files, primary legal texts, immutable/unchanged) via
`scripts/harmonize/harmonize_majlis_budget_laws.py`. **This is genuine primary-source extraction
work, not a reformatting pass**: every HTML file was converted to plain text and the actual law
text was read directly (the "ماده واحده" / single-article clause where Iranian budget laws state
their headline revenue/expenditure figures both in spelled-out Persian words and as a parenthetical
digit string — the digit string was transcribed, the words used only as a cross-check). Every
multi-level total with two or more stated components was independently summed and checked against
the parent total; matches and mismatches are both recorded below, never silently resolved.

## Coverage summary

**21 distinct fiscal years touched across 24 files.** 16 fiscal years yielded a full national
revenue/expenditure total: **FY1341, 1343, 1344, 1346, 1352, 1353, 1354, 1355, 1358, 1360, 1361,
1362, 1363, 1365, 1368, 1370**. Three more yielded only a supplementary (mid-year addition) figure,
not a full-year total: **FY1357, 1369** (main law not located) and **FY1358** (which also has a
separate main-law total, see above). **FY1364** yielded only a foreign-exchange allocation ceiling
(a distinct specialized law), not a general rial budget. **FY1356** yielded no quantitative figure
at all — its one surviving file is a narrow non-monetary pension-rule amendment. **FY1301** predates
consolidated "whole-country" budgeting entirely — 3 separate single-ministry appropriation acts,
denominated in Tomans (not Rials, the currency Iran used until 1932).

**Confirmed real gaps** (not extraction failures — these fiscal years' law texts were not found in
this raw collection at all): FY1302-1340 whole-country laws (ministry-by-ministry budgeting was
still typical for much of this span; a consolidated "kol-e keshvar" format only starts appearing at
FY1341 in this collection), FY1345, FY1347-1351, FY1356 (main law), FY1359, FY1364 (main rial-
denominated law — only the FX-allocation companion law survives), FY1366, FY1367, FY1369 (main law).

## Files

| File | Rows | What it covers |
|---|---|---|
| `national_budget_totals_by_fiscal_year.csv` | 50 | Whole-country revenue/expenditure totals + their internal component breakdowns, for the 16 fiscal years with a legible main budget law |
| `ministry_level_appropriations_1301.csv` | 7 | FY1301's 3 single-ministry appropriation acts (Public Works, Justice, Foreign Affairs), pre-consolidated-budget era, in Tomans |
| `supplementary_budget_additions.csv` | 5 | Mid-year supplementary (متمم) appropriations for FY1357, 1358, 1369 — deltas on top of (or, for 1357/1369, standing in for) the main budget |
| `forex_budget_law_1364.csv` | 1 | FY1364's separate USD 15 billion foreign-exchange allocation ceiling law (war-economy FX rationing) |

### `national_budget_totals_by_fiscal_year.csv` schema

`fiscal_year_ah, fiscal_year_western_end, law_type, hierarchy_level, revenue_rials,
expenditure_rials, value_source, notes, approved_date_ah, gazette_issue_no, country_iso3,
source_file`

- **`fiscal_year_ah`**: Iran's Solar Hijri (Jalali) calendar year, as printed in the law.
- **`fiscal_year_western_end`**: `fiscal_year_ah + 622` — the LATER Western calendar year (the year
  the fiscal year ends, ~March 20). Matches the same convention used in
  `data/processed/pahlavi_government_finance_series/`, for cross-series comparability.
- **`hierarchy_level`**: which level of the law's own nested breakdown this row represents (Grand
  Total, then lettered/numbered parts — General Government Budget, its General-revenue and
  Earmarked-revenue sub-lines, State Companies budget, etc. — exactly as the law itself structures
  it; the hierarchy differs slightly year to year because the laws' own drafting conventions
  evolved).
- **`value_source`**: `"printed"` (the figure appears explicitly, digit-string, in the law's
  single-article clause) vs. `"implied residual (...)"` (computed as Grand Total minus the
  explicitly printed parts, because the source's own summary clause did not itemize that
  particular component — arithmetic on printed numbers, not a fabricated figure, but flagged
  distinctly).
- **`notes`**: every arithmetic cross-check performed, and every discrepancy found, in full.

## A mislabeling found in the raw files (important — read before using FY1301 data)

**Two of the three FY1301 raw HTML files have their filenames swapped relative to their actual
body-text content.** This was discovered by reading each file's full law text, not just its
manifest title metadata:

- `budget-law-1301-foreign-ministry.html` — filename says "foreign ministry," but its actual law
  text (verified: opening line "قانون بودجه سال ایت ئیل 1301 وزارت فوائد عامه", Article 1 states
  53,640 tomans admin + 3,000 tomans pension) is the **Public Works Ministry** (وزارت فوائد عامه)
  budget.
- `budget-law-1301-public-works-ministry.html` — filename says "public works," but its actual law
  text (verified: opening line "قانون بودجه سال ایت ئیل 1301 وزارت امور خارجه", Article 1 states
  640,000 tomans, itemized 609,000 ministry + 31,000 League of Nations dues) is the **Foreign
  Affairs Ministry** (وزارت امور خارجه) budget.
- `budget-law-1301-justice-ministry.html` — this one is CORRECTLY labeled (verified: its text is
  genuinely the Justice Ministry/وزارت عدلیه budget).

This is most likely a scraping/caching artifact at the source (lamtakam.com), not an error
introduced by this project's earlier download round — but it was NOT caught before this
harmonization pass, since the earlier round's manifest recorded the site's own page titles, which
in turn may have been mismatched to the numeric law/parliament/NNNNN URL IDs at the source. Per
`docs/bookkeeping.md` ("raw data is immutable"), **the raw HTML filenames were NOT renamed** — this
processed CSV instead uses the CORRECT ministry attribution based on the verified text content,
while `ministry_level_appropriations_1301.csv`'s `raw_file` column cites the (mislabeled) actual raw
filename for full traceability, with an explicit "(MISLABELED — see README)" flag on every affected
row. Anyone consulting the raw HTML directly by filename should be aware of this swap.

## Discrepancies found and preserved (never resolved to one number)

- **FY1358 main law**: the round headline total (2,463,000,000,000 rials, stated with no finer
  digits in the clause's opening sentence) does not equal the sum of its own two lettered
  components (2,358,042,371,000 + 82,098,000,000 = 2,440,140,371,000) — a gap of 22,859,629,000
  rials. Both kept as printed.
- **FY1368 and FY1370**: unlike most other years, both laws print their "general government" and
  "state companies/banks" components in FULL (not requiring a residual computation) — but in both
  years the two parts SUM TO MORE than the printed grand total (FY1368: 451,138,478,000 rials over;
  FY1370: 1,244,946,502,000 rials over). Plausibly a consolidation/netting adjustment for
  inter-account transfers not shown in the single-article summary clause (normal practice in
  government accounting, to avoid double-counting a subsidy that is simultaneously an expenditure
  line in the general budget and a revenue line for a state company) — but this project does not
  assert that explanation as verified fact absent a legible reconciliation table, so all three
  figures are kept exactly as printed with the gap stated, not resolved.
- **FY1344**: the overall deficit (176,662,000,000 − 175,046,000,000 = 1,616,000,000) does not
  exactly equal the deficit within its own general+earmarked-revenue subset (59,695,681,000 −
  58,301,631,000 = 1,394,050,000) — unlike FY1343 and FY1355, where the equivalent check matched
  exactly. Not reconciled.
- **FY1365**: the source's spelled-out Persian words for one expenditure figure are grammatically
  malformed in a way that reads as an OCR/transcription defect in the ORIGINAL lamtakam.com HTML
  (not introduced by this project) — the unambiguous parenthetical digit string was used instead
  and is what appears in this CSV.
- **FY1358 "bill" vs "main law"**: `budget-bill-1358-whole-country.html` (Gazette 10066) states
  figures IDENTICAL, word-for-word, to `budget-law-1358-whole-country.html` (Gazette 52866) —
  almost certainly the same enactment registered/gazetted twice rather than a genuinely distinct
  second budget. Both rows are kept (for traceability of the two Gazette numbers) but are NOT summed
  as two separate FY1358 data points in any total.

## Caveats — read before charting

- **Units**: FY1301 figures are in **Tomans** (Iran's currency until the 1932 conversion to Rials,
  1 Toman = 10 Rials at that conversion, though this project makes no attempt to retroactively
  convert — the FY1301 figures are transcribed in their original Toman denomination and are NOT
  directly comparable in magnitude to the Rial-denominated whole-country figures from FY1341
  onward). All other files are in **Rials**.
  Note this project's separate `pahlavi_government_finance_series/` folder (World Bank-sourced
  1955-1973 fiscal tables) uses **million or billion rials** depending on table — always check units
  before combining series.
- **"Balanced" budgets before the mid-1350s (1976-77) largely reflect that revenue and expenditure
  are simply set to the identical stated figure by law**, not that Iran ran literally zero deficits
  in practice — actual/audited outturns can and do differ from the enacted law (see the separate
  World-Bank-sourced Pahlavi actuals-vs-budgeted comparison in
  `data/processed/pahlavi_government_finance_series/budgeted_vs_actual_expenditures_1955_60.csv`
  for a directly comparable example of budgeted vs. actual divergence in the same era).
  From FY1355 onward several years show an explicit, law-stated deficit.
  Do not treat "revenue = expenditure" pre-1355 as evidence of fiscal balance in outturn.
- **Approval dates often lag the fiscal year significantly**, especially for FY1341 (approved
  retroactively ~2 years after the fiscal year ended) — a reminder that "the FY1341 budget law" is
  a legal/accounting artifact finalized well after the year it covers, not necessarily reflecting
  in-year fiscal decisions made contemporaneously.
- **`ministry_level_appropriations_1301.csv`**: the Justice Ministry's second appropriation
  (191,213 tomans, 5 qeran) uses "qeran" (1 toman = 10 qeran at the time), recorded here as a
  decimal (191213.5) with the unit column spelling out the qeran conversion for clarity — do not
  read the ".5" as "half a toman" without checking the `unit` column.
- **Supplementary-law rows are NOT annual totals** — they are mid-year top-up appropriations only,
  and for FY1357/FY1369 they are the ONLY primary-source figure available at all for that year (the
  main law was not found), so a chart must not present them as if they were the full-year budget.
- **This folder does not yet reconcile against `data/processed/pahlavi_government_finance_series/`**
  (which covers overlapping FY1962/63-1973 government revenue/expenditure from World Bank sources)
  or against `data/raw/iran-plan-budget-org/annual-budget-laws/` (a separately-sourced collection
  starting FY1371, one year after this collection's FY1370 endpoint) — see the
  `chart_registry_staging/government_finance_banking.csv` entry for how this maps to the existing
  chart registry; the actual splice/cross-check against those series is left to a future pass since
  the fiscal-year definitions, "general government" vs. "whole country" scope, and units differ
  across all three collections and deserve dedicated reconciliation, not an assumed match.

## Sources

Majlis Shoraye Melli (National Consultative Assembly, Pahlavi era) / Revolutionary Council (Shoraye
Enghelab, 1979-1980) / Majlis Shoraye Eslami (Islamic Consultative Assembly) — original legislature
of enactment for each law. Texts mirrored via Lam ta Kam (lamtakam.com), a private Iranian legal-
reference aggregator republishing the Majlis Research Center's own law database; the primary/
official source (rc.majlis.ir) was unreachable this project (geo-blocked, consistent with this
project's broader finding that Iran-domestic sites are blocked from this session's IP — see
`docs/bookkeeping.md`). Full per-file citation chain (exact lamtakam.com URLs, SHA256, Gazette
issue numbers where stated): `data/raw/majlis-historical-budget-laws/lamtakam-mirror-1301-1363/
manifest.json`.
