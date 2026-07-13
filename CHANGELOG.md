# Changelog

Tracks changes that matter to anyone re-using or citing this data — new categories, methodology
changes, and data-quality fixes. Not a running commit log (see git history for that); see
`docs/bookkeeping.md` § "Versioning & changelog" for what belongs here.

## 2026-07-13

- **Policy-timeline correlation coverage expanded** (task #14): added 46 new correlation rows
  across 27 chart_ids in `data/processed/policy_chart_correlations_social_industry_energy.csv`,
  covering Health, Education, Demographics, Labor, Industry, Energy, and Media themes previously
  underrepresented (the two existing files were oil/trade/agriculture and macro/fiscal/FX themed).
  Every event cited was verified to exist in the underlying `timeline/*.csv` file; none invented.
- **Real-USD coverage extended to the last 25 WDI currency charts** (task #18): these are
  government-finance/fiscal aggregates (e.g. `GC.REV.XGRT` "Revenue, excluding grants") where WDI
  publishes only a current-LCU variant with no native current-USD counterpart at all — the existing
  `build_currency_variants.py` only knew how to compute a *real*-USD variant starting from a
  WDI-native nominal-USD row. Added `process_wdi_lcu_only()` to compute BOTH nominal and real
  (2015-base) USD variants directly from the LCU value via each country's own FX/CPI lookup,
  reusing the same conversion helpers already used for Iran's rial-denominated archival series.
  All 17 project countries covered. Every currency chart in the registry now has a real-USD variant.
- **Every chart now has a real citation** (task #17): resolved all 98 archival rows that had a
  genuinely empty `citations_json` (the true count — the original task estimate of "9" was stale).
  Each was hand-traced via its `data/processed/*_series/README.md` provenance note to the specific
  `data/raw/**/manifest.json` it actually came from — none were guessed or left to a blind
  re-run of the fuzzy matcher. `CHART_REGISTRY.csv` now has a non-empty, real citation on all
  1,846 rows.
- **Iran 2004-2010 parallel-FX data now primary-sourced and corrected** (task #15): found CBI's own
  daily "Exchange Rates Statistics" page via 40 Wayback Machine snapshots (Dec 2005-Oct 2010) plus 6
  IMF Article IV/Statistical Appendix reports, replacing the prior one-hop-removed Wikipedia
  transcription. Confirmed 2005/2006/2009/2010 as originally recorded; corrected 2004 (8,885→8,615),
  2007 (9,408→9,280), and 2008 (9,143→9,421) — the 2008 error had been producing a nonsensical
  negative black-market premium in the flagship `fx__official_vs_parallel_gap_irn` chart. Also fixed
  `build_fx_gap_chart.py` to read title/category/sources/citations from `CHART_REGISTRY.csv` instead
  of hardcoding them (the hardcoded copy had already gone stale once, dropping a citation and an
  old chart title). See `data/raw/iran-cbi-imf-fx-verification-2004-2010/manifest.json`.
- **Fixed 14 Git LFS files stuck as unresolved pointers** in the local working tree (`macro_wdi.csv`
  and 13 others) — `git lfs migrate import --everything` (used earlier to fix the GitHub 100MB-limit
  push failure) rewrites history but doesn't automatically re-smudge the working copy; `git lfs pull`
  restores the real content. Found when a script reading `macro_wdi.csv` failed with a `KeyError`
  because the file was still just an LFS pointer stub.
- **Category taxonomy: fixed a real mislabeling bug** (task #13, scoped): 11 WDI social-protection
  charts (`per_sa_allsa.*`, `per_allsp.*` — social safety net coverage/benefit-incidence indicators)
  were mis-bucketed into a broken placeholder category `"Other (per)"` due to a case-sensitivity bug
  in `build_chart_registry.py`'s topic-prefix lookup (`WDI_PREFIX_CATEGORY` keys are uppercase, but
  these indicator codes' prefix is lowercase `per`, so a correct `'PER': 'Social Protection'` mapping
  that already existed in the code was never reached). Fixed at the root and re-categorized the 11
  rows into the pre-existing `"Social Protection"` category (97→96 total categories). The deeper
  question of redesigning the ~96-category taxonomy into a small, clean set for site navigation is
  intentionally left for the frontend/IA session (per the project owner's own framing — see
  `frontend-notes-for-future-chat` notes) rather than decided here; this pass only fixed a genuine
  mechanical bug, not a design choice.
- **Registry-wide dedup/QA sweep** (task #12): confirmed clean overall (no duplicate `chart_id`s, no
  duplicate title+category pairs, no malformed `citations_json`, all "duplicate" `underlying_codes`
  are legitimate same-commodity/different-metric FAOSTAT variants). Found and properly resolved one
  real issue: `faostat__Cereals, Other__{trade,consumption}` and the lowercase-cased
  `faostat__Cereals, other__{trade,consumption}` are two separate `CHART_REGISTRY.csv` rows that
  collide to the *same* `data/charts/` directory on this machine's case-insensitive filesystem
  (confirmed via matching inode numbers) — editing one's `meta.json` silently edits the other's too.
  Added a `merged_into` column; the lowercase-cased rows are now marked `status: merged` with
  `merged_into` pointing at the canonical capital-cased row, and `build_catalog_index.py` passes
  `merged_into` through to the public catalog. The canonical rows' `meta.json` were restored to their
  correct un-merged state after an in-progress edit briefly (locally, uncommitted) wrote the wrong
  status into the shared file. No other case-insensitive `chart_id` collisions exist in the registry.
- **Persian (Farsi) translation added** (task #16): every chart title (`title_fa`) and every category
  (`category_fa`, all 96) now has a professional Persian translation, propagated to
  `data/charts/*/meta.json` and `catalog/CHARTS_INDEX.json`/`CATEGORIES.json`. Western numerals used
  throughout Persian text per standard technical/financial writing convention; organization acronyms
  (FAO, IMF, OECD, etc.) kept as-is; real Persian historical/institutional terminology used for
  Iran-specific archival charts (سپاه دانش, انقلاب سفید, بانک مرکزی, etc.).
  - Along the way, found and fixed a real English-title bug the translation work surfaced: 14 WDI
    charts (school enrollment, mortality, tobacco-use indicators) were titled as if male-only
    ("...male (% gross)") by `build_chart_registry.py`'s `shortest_label()` heuristic, when their
    underlying data actually bundles BOTH male and female series (500+500 rows each). Retitled to
    "...by sex (% gross)" and re-translated those 14 rows.
  - Also found and fixed a genuine duplicate `build_citations.py`/dedup-sweep missed:
    `faostat__Beverages, Alcoholic__{trade,consumption}` is a strict data subset (0 unique rows) of
    `faostat__Alcoholic Beverages__{trade,consumption}` — same pattern as the earlier
    `Cereals, Other`/`Cereals, other` case, just a word-order variant instead of a casing variant.
    Marked `status: merged` / `merged_into` the same way.
  - One terminology fix: an early translation batch rendered "deflator" as بادکننده (literally
    "inflator/something that puffs up") instead of the correct تعدیل‌کننده — caught by spot-check,
    fixed across all 5 affected WDI deflator-series charts.
- **Chart title/description cleanup pass** (task #11): 51 of the 262 archival/hand-curated chart
  titles shortened and clarified for public display (max length dropped from 200 to 88 characters);
  any detail trimmed from a title that wasn't already in `notes` was preserved there. Machine-source
  (WDI/FAOSTAT/WEO/OWID/WID) titles were left as-is (official taxonomy labels, already consistent).
- **Layer-3 archival rebuild script fixed to be genuinely idempotent** (`build_layer3_archival_charts.py`):
  it previously only materialized chart_ids missing a `data/charts/` folder, silently skipping
  metadata (title/category/sources/citations) sync for already-built charts on every re-run despite
  its own docstring claiming otherwise. Added a dedicated sync pass so future registry edits
  propagate correctly.
- **Citation regression found and fixed**: 8 of the 16 rows the citation-accuracy audit (below) had
  hand-fixed had silently reverted to worse/wrong fuzzy-matched citations sometime after that audit
  completed, most likely when a later staging-merge re-ran `build_citations.py` from a pre-audit
  registry snapshot. Restored all 8 from the audit log's documented fixes + the cited source
  manifests. Root-cause-fixed `build_citations.py` so a hand-curated archival citation is never
  silently overwritten by a future re-run again (deterministic machine-source citations still always
  recompute fresh, since that's safe/idempotent). See `logs/downloads/citation-accuracy-audit.log`
  for the full incident detail.
- **Project named and licensed.** Public name: "Iran in Data" (iranindata.org), compiled by Roham
  Hosseini. Dual-licensed: code under MIT, data compilation under CC BY 4.0.
- **Chart deduplication registry established** (`CHART_REGISTRY.csv`). Raw indicator counts across
  the machine-readable sources (WDI, FAOSTAT, IMF WEO, OWID, Maddison, WID) were heavily inflated by
  unit/currency variants and cross-source duplication; deduplicated to real distinct chart concepts.
- **Currency & inflation-adjustment methodology established**, then corrected twice:
  1. Base methodology: deflate in local currency to a 2015 base year using each country's own CPI,
     then convert to USD at the 2015 exchange rate (mirrors WDI's own "constant US$" convention).
  2. **Correction**: for Iran's Islamic Republic era (1979–present), official multi-tier exchange
     rates are not representative of what the public or private sector actually transacted at — the
     parallel/black-market rate is used instead, except 2003–2010 (a genuinely unified rate era) and
     the still-open pre-1999 stretch.
  3. Extended to all 17 project countries; Venezuela and Argentina also get a parallel-rate
     correction for their own documented divergence eras, following the same evidence-based logic
     as Iran rather than a blanket rule.
- **Citation-accuracy audit.** All fuzzy-matched archival citations were manually verified; found and
  fixed 15 wrong citations (country/topic mismatches) caused by two bugs in the matching script,
  which were fixed at the root rather than just patched per-row.
- **Timeline broadened** beyond deliberate policy decisions to include wars, revolutions, disasters,
  and global shocks (e.g. the 1941 Anglo-Soviet occupation, the 1917–18 famine and flu pandemic, the
  1990 Manjil-Rudbar earthquake) that can plausibly correlate with economic chart movements.
- **Public-good packaging added**: machine-readable catalog (`catalog/CHARTS_INDEX.json`), category
  index, `llms.txt` for AI-agent discoverability, and bulk-download zip packaging.
- Project moved into version control for the first time.
