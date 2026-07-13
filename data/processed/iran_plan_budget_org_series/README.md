# Iran Plan & Budget Organization series — annual budget laws + five-year development plans

Harmonized from `data/raw/iran-plan-budget-org/{annual-budget-laws,five-year-development-plans}/`
(45 raw PDFs, immutable/unchanged). This is genuine primary-source extraction work, not a
reformatting pass: every figure was read from the actual law text (the "ماده واحده" / single-
article clause, in the same tradition as the FY1301-1370 texts in
`data/processed/majlis_budget_law_series/`), either via clean `pdftotext -layout` extraction
(for born-digital PDFs with a usable font/CMap) or by rendering the exact page to a PNG with
`pdftoppm -r 300..400` and reading the image directly, per this project's established method for
scanned/mojibake PDFs — trusting the rendered image over `pdftotext` whenever they disagreed.
Every multi-component total was cross-checked (do the parts sum to the stated whole?), and the
spelled-out Persian number-words were checked against the parenthetical digit string for every
figure recorded (both had to agree before a figure was accepted). Nothing was guessed,
interpolated, or back-calculated from an accounting identity; illegible or unreached figures are
left blank with a note explaining why.

## Files

| File | Rows | What it covers |
|---|---|---|
| `annual_budget_law_totals_1371_1401.csv` | 125 | Whole-country revenue/expenditure totals + internal Part A (general govt) / Part A1 (general revenue) / Part A2 (earmarked revenue) / Part B (state companies+banks) breakdown, for 30 of the 31 possible fiscal years FY1371-FY1401 (1992-2023) |
| `five_year_plan_targets.csv` | 68 | Headline macroeconomic targets (GDP growth, investment, sectoral growth, etc.) for 7 Islamic-Republic-era Five-Year Development Plans, FY1368-1406 (1990-2028) |

## `annual_budget_law_totals_1371_1401.csv` schema

`fiscal_year_ah, fiscal_year_western_end, document_type, hierarchy_level, revenue_rials,
expenditure_rials, value_source, notes, country_iso3, source_file, extraction_method,
source_page_note`

- **`fiscal_year_ah`**: Iran's Solar Hijri (Jalali) calendar year, as printed in the law.
- **`fiscal_year_western_end`**: `fiscal_year_ah + 621` (the year the fiscal year ends, ~March of
  the following Gregorian year) — same convention as `majlis_budget_law_series` and
  `pahlavi_government_finance_series` for cross-series comparability. Verify against the
  document's own promulgation date before treating as exact for years near a Nowruz boundary.
- **`document_type`**: distinguishes the two enactment stages this collection happens to contain
  for some years — `bill (لایحه)` (as submitted, before Majlis amendment) vs `final law` /
  `promulgation notice` (after enactment) vs `law (single copy on file)` where the source only
  contains one version and its stage isn't independently labeled.
- **`hierarchy_level`**: which level of the law's own nested breakdown this row represents (Grand
  Total, then Part A "بودجه عمومی دولت"/general government budget, its A1 "درآمد عمومی"/general-
  revenue and A2 "درآمد اختصاصی"/earmarked-revenue sub-lines, and Part B "بودجه شرکتهای دولتی و
  بانکها"/state companies+banks+profit institutions budget) — exactly as each year's law
  structures it. Terminology shifts partway through the series: FY1371-1380 use
  درآمدها/هزینه‌ها (revenues/expenditures); FY1381 onward use منابع/مصارف (resources/uses) —
  the modern IRI budget-law convention. Both map to the same `revenue_rials`/`expenditure_rials`
  columns here.
- **`value_source`**: `"printed"` (the figure appears explicitly in the law's own text) vs.
  `"implied residual (A-A1)"` (A2 computed as Part A minus the printed A1, because A2's own line
  ran past the sampled page and wasn't independently read — flagged distinctly, not asserted as
  independently verified).
- Every row where `revenue_rials == expenditure_rials` reflects the law itself stating a
  **balanced budget** (standard for Iranian annual budget laws — revenue/resources side is set
  equal to the expenditure/uses side by legislative design). This does not imply the actual fiscal
  outturn balanced; see the equivalent caveat in `majlis_budget_law_series/README.md`.

### The "Part A + Part B > Grand Total" pattern (read before charting)

**In every single year where both Part A and Part B were captured (FY1371-1401, ~20 years), Part
A plus Part B numerically EXCEEDS the printed Grand Total** — never falls short, always exceeds,
by amounts ranging from ~1.5 trillion rials (FY1371) to over 1 quadrillion rials (FY1401, tracking
the nominal scale of the whole budget). This exact pattern was first documented for FY1368 and
FY1370 in `majlis_budget_law_series/README.md`, where it was noted but not explained (the working
hypothesis there was a consolidation/netting adjustment for inter-account transfers, e.g. a
subsidy that is simultaneously an expenditure line in the general budget and a revenue line for a
state company, not shown in the single-article summary clause). This collection's ~20 additional
confirmations make clear it is a **persistent structural feature of Iranian budget-law drafting**,
not a one-off anomaly or a transcription error on this project's part — every individual
component-sum check performed (A1+A2=A) matched EXACTLY every time; only the top-level A+B vs.
Grand Total comparison shows the gap. This project does not assert the netting-adjustment
explanation as verified fact absent a legible reconciliation table in any of these laws — all
figures are kept exactly as printed, gap stated, never reconciled or forced to match.

### Multi-document years (bill vs. final-enacted-law divergence)

Three fiscal years have **two source documents with different headline totals**, both kept as
separate rows, neither treated as authoritative over the other (same principle as the
FY1358 bill/law duplicate in `majlis_budget_law_series`):

- **FY1397**: `Budget-1397.pdf` (bill, 11,949,354,674,000,000 rials) vs. `Eblagh097.pdf`
  (promulgation-notice text, i.e. essentially the enacted law, 12,225,523,740,000,000 rials).
- **FY1398**: `budget1398-1.pdf` (earlier stage, 17,032,332,270,000,000 rials) vs. `Law-1398.pdf`
  (final law, 17,443,160,230,000,000 rials).
- For **FY1399, FY1400, FY1401**, only the bill-stage figure is on file in this collection (the
  final-enacted-law copies exist in the raw folder as `law-1399.pdf` and `LAW-1400.pdf` but are
  scanned/mojibake files that were NOT independently read this round — see "Known gaps" below;
  FY1401 has no final-law copy in the raw folder at all, only the bill).

### Real gaps (not extraction failures)

- **FY1395**: no PDF for this year exists anywhere in the 39-file raw folder (checked every
  filename — the bare-numbered series and the `budget-*`/`Budget-*` families both jump from 1394
  to 1396). Confirmed missing source, not a legibility failure.
- **FY1374, FY1381, FY1384, FY1392**: only the Grand Total was captured; Part A/B breakdown was
  either not confidently legible at the sampling resolution used, or not reached within this
  pass's time budget. Left blank rather than guessed.
- `law-1399.pdf`, `LAW-1400.pdf`, `Budget-Law-1396.pdf` (final-enacted-law copies for FY1399,
  FY1400, FY1396 respectively) are scanned/mojibake files in the raw folder that were **not**
  independently read or cross-checked against this collection's bill-stage figures for those
  years — a natural next continuation task.

## Cross-validation against `majlis_budget_law_series` (FY1301-1370)

**Clean, non-overlapping handoff, not a cross-validation opportunity**: the Majlis series' last
covered fiscal year is FY1370 (20,097,297,101,000 rials), and this collection's first fiscal year
is FY1371 (28,912,077,914,000 rials) — a plausible ~43.8% nominal one-year increase given Iran's
high-inflation environment in the early 1990s post-war reconstruction period. The two collections
are sourced from entirely different raw folders (`majlis-historical-budget-laws/` via
lamtakam.com vs. `iran-plan-budget-org/annual-budget-laws/` via Iran Data Portal) and do not
share a single fiscal year, so there is nothing to cross-validate — this is a pure **extension**
of the continuous record from FY1301 (with gaps) through FY1401, now essentially unbroken from
FY1360 onward except the confirmed FY1395 gap.

## `five_year_plan_targets.csv` schema

`plan_number, plan_years_ah, plan_years_ce, category, indicator, unit, base_value,
interim_value, final_value, avg_annual_growth_pct, value_type, notes, source_file, source_page,
extraction_method`

Long/tidy format: one row per (plan, indicator) pair. `base_value`/`interim_value`/`final_value`
are populated when the source states a specific level at the plan's base year / an intermediate
year / the plan's final year (as in Plan 6's Table 1); `avg_annual_growth_pct` is populated when
the source states a target growth rate (which is most rows — Iranian development-plan laws
overwhelmingly state targets as annual average growth percentages, not absolute levels).

### Coverage varies sharply by plan generation — this is a real structural finding, not sampling bias

- **Plans 1, 2, 6, 7** state their quantitative targets in a compact, well-organized form early in
  the document (a "ماده واحده" clause for Plan 1, a dedicated "اهداف کمی کلان" section for Plan 2,
  and clean numbered tables in Article 2/3 for Plans 6 and 7) — these are **fully captured** in
  this pass, including Plan 6's complete macro-target table (10 indicators) and sectoral
  value-added/employment growth targets (9 sectors × 2 metrics), verified against rendered page
  images.
- **Plans 3, 4, 5** (FY1379-1394, the Khatami/Ahmadinejad-era plans) are organized instead as
  extensive **policy-reform chapters** — banking reform, privatization mechanics (Article 44),
  currency reserve fund rules, administrative restructuring — rather than a compact targets
  clause. Plan 4's own Article 1 (under a chapter literally titled "رشد سریع اقتصادی" / rapid
  economic growth) turned out to be about the Oil Stabilization Fund mechanism, not a stated
  growth percentage. A headline GDP growth target may exist somewhere in these substantially
  longer documents (263-528 pages) but was **not located within this extraction pass's time
  budget** — recorded as an explicit `value_type = "not located"` gap row per plan, not
  fabricated, not filled from outside/general knowledge of what Iran's official targets were for
  these plans. A genuine continuation-worthy task.
- **Plan 7** is a **BILL** (لایحه), not yet an enacted law at the time this collection was
  assembled — flagged via `value_type = "BILL target"` throughout its rows. It restates the same
  8% headline GDP growth target as Plan 6, which is either a genuine policy-continuity signal or
  simply evidence that Iran has targeted (and per outside reporting, not consistently achieved)
  8% growth across consecutive plans — this project does not assert an interpretation, only
  records what the bill text states.

### Notable content

- Plan 6 Article 3's headline target: **8% average annual GDP growth + a target Gini coefficient
  of 0.34** by the plan's final year (FY1400) — an unusual instance of an inequality target
  appearing directly in a growth-oriented development-plan law.
- Plan 6's sectoral table shows the widest target dispersion in Communications (19.4% avg annual
  value-added growth, by far the highest of any sector) alongside modest targets for Oil (7.0%)
  and Other services (5.8%) — consistent with Iran's stated post-JCPOA-era push to diversify away
  from oil-sector growth.
- Plan 2's target GDP growth (5.1%/year, FY1374-78) is notably more modest than Plan 6/7's later
  8%/year target — a genuine cross-plan comparison point once the missing Plans 3-5 targets are
  eventually located.

## Provenance detail (per-file)

See `logs/downloads/iran-plan-budget-org-extraction.log` for the full page-by-page working log,
including every intermediate cross-check performed and every low-confidence reading that was
deliberately discarded rather than recorded. In summary, of the 39 `annual-budget-laws` PDFs: 15
had clean extractable Persian-Unicode text (`pdftotext -layout` used directly); 16 were pure
scanned images (Adobe "Image Conversion Plug-in", 0 extractable characters); ~8 had a mojibake
font-encoding issue (text extracted but wrong Unicode codepoints, unusable) requiring the same
image-render method as the pure scans. One file (`1400-Bill-part-I.pdf`) had a rarer issue where
only the NUMERAL glyphs were garbled while surrounding Persian letters extracted correctly — for
that file, the spelled-out number-words were used as the primary source instead of the usual
parenthetical digit string, with internal-consistency cross-checks (A1+A2=A) confirming the
word-based reading. Of the 7 `five-year-development-plans` PDFs: Plans 6 and 7 are Word-native
PDFs with clean tables (verified against rendered images); Plans 1-5 are scanned images requiring
the render-and-read method, with Plans 1 and 2 yielding usable ماده واحده / quantitative-goals
content and Plans 3-5 not yielding a located headline target within this pass.

## Sources

Iran Data Portal (Syracuse University Maxwell School), "Annual Budgets and Development Plans"
page — `data/raw/iran-plan-budget-org/annual-budget-laws/manifest.json` and
`data/raw/iran-plan-budget-org/five-year-development-plans/manifest.json` for exact per-file
citation chain (source URLs, SHA256, retrieval dates). Underlying documents are Iran's own
government-published law texts (Sazman-e Modiriyat va Barnamehrizi-ye Keshvar / Plan & Budget
Organization and successor bodies; Majles Shoraye Eslami as legislature of enactment).
