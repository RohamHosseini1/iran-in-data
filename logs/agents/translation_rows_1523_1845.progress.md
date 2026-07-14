# Progress log: translation_rows_1523_1845

Slice: CHART_REGISTRY.csv data rows [1523:1846) (0-indexed, header excluded, through
end of file). 323 rows. Mixed sources: faostat price series (39 rows), weo/owid/wid,
pahlavi-era historical series, comparator-country blocks (maritime/mining/portugal/
spain/saudi/venezuela/argentina FX), iran_census/iran_disasters/iran_institutions/
iran_fx/iran_migration/iran_trade, banking history, dams, mining/industry production,
insurance, provincial, energy, PMI/business-cycle, census1996, UNCTAD/OPEC/GIEWS,
USSR/Russia (CIA + Narkhoz + Imperial), FX gap, aviation, telecom/media, White
Revolution corps, poverty, specialty goods, FRUS citation-bundles, CIA econ reports,
NIS-33, USAID. All 323 rows have status=new (0 merged in this slice, verified
programmatically) — no skip_merged rows needed.

Method: dumped the full slice to a scratch TSV and read it end-to-end (two passes),
cross-checked with regex scans for: em/en dash characters, ASCII " - " separators,
Arabic ي/ك chars, verb-based ZWNJ patterns (می‌/نمی‌ + verb roots), leftover Latin
text, and category_fa cross-slice consistency (checked against the *entire* registry,
not just this slice — 0 inconsistencies found for any category_fa used in this slice).

- [2026-07-14T00:00Z] rows 1523-1845 done, 89 proposals (full slice reviewed in one
  pass). Output shard written in one batch to
  data/processed/quality_audit/translation_rows_1523_1845.csv (323 rows, order-matched
  to source slice, verified programmatically).

Key finding 1 (39 rows, 1523-1561): the entire faostat producer-price block in this
slice uses the dash-suffix pattern "<crop fa> — قیمت تولیدکننده" — exactly the
doctrine's canonical WRONG-example shape. Fixed to "قیمت تولیدکننده <crop fa>".
Cross-checked against the neighboring already-completed shard
translation_rows_1200_1522.csv, which independently converged on the identical
"قیمت تولیدکننده <subject>" construction and the identical reason string for the
same faostat__*__price pattern one row earlier in the registry (rows 1433-1522) —
strong cross-slice consistency signal, reused verbatim.

Key finding 2 (7 rows, 1577-1583): pahlavi-era production series use
"<crop fa> — تولید، YYYY-YYYY". Fixed to "تولید <crop fa>، YYYY-YYYY" (same
measure-leads-subject rule, applied to a production/production-value verb noun
instead of a price noun).

Key finding 3 (new pattern, first occurrence in the registry — 43 rows): every
"*_comparator__*" chart (maritime, mining/USGS, Portugal INE/BdP, Spain
Carreras&Tafunell, Saudi GASTAT, Venezuela, Argentina BCRA/FX) uses a
"<Country fa> — <description>" dash-prefix pattern in title_fa (mirroring the
English "Country — Description" convention, which is NOT in scope — only title_fa/
category_fa are). No earlier slice had "_comparator__" rows to set precedent, so
this fix pattern is being established here: move the country to an izafe modifier
after the measure noun, e.g. "آرژانتین — تولید مواد معدنی..." →
"تولید مواد معدنی آرژانتین..."; "پرتغال — جمعیت، اشتغال..." →
"جمعیت، اشتغال... پرتغال...". One exception (fx_comparator__argentina_badlar_interest_rate_daily,
row 1663) uses "در آرژانتین" (preposition) instead of a bare izafe chain because the
subject already ends in an embedded acronym (BADLAR) and a second izafe would read
awkwardly in Persian.

Key finding 4 (remaining ~13 scattered dash-suffix rows): one-off historical/
narrative chart titles (dams, Sar Cheshmeh copper, D'Arcy concession, USSR GNP/
livestock, White Revolution corps, Iran vs. parallel-FX gap, state railways) each
retitled individually with the same measure-leads-subject rule; recorded as
individual "dash suffix" reasons rather than a shared template since each required
custom word-order judgement.

Terminology checks (targeted WebSearch, batched, 2 queries): (1) "بزرگا" vs "بزرگی"
for earthquake magnitude (row 1643, iran_disasters__significant_earthquakes) —
fa.wikipedia's "مقیاس بزرگی ریشتر" uses بزرگی, but بزرگا is the standard technical
term used by Iran's official seismological bulletins (IIEES/IRSC); kept as-is, not
an error, no doctrine term list conflict. (2) "برتری شهری" (urban primacy) for row
1627 (Tehran population/primacy) — no canonical fa.wikipedia article found for
"urban primacy"; left as-is (not clearly wrong, no better established alternative
found). Neither triggered a retitle.

No Arabic ي/ك instances found. No verb-based ZWNJ issues found (this slice is
entirely noun-phrase titles, no می‌شود-type constructs). No English country names
left untranslated (all Latin-script leftovers are institutional acronyms — USGS,
GASTAT, INE/BdP, BCRA, BADLAR, GFDD, IMIDRO, IDRO, CIA, FRUS, OECD, IBRD, UNCTAD,
WTO/GATT, IMF, CITES, PMI, MIMT, CIP, COICOP, SH-prefixed fiscal-year tags, NIGC,
THC — or a report-author surname (Motheral) — consistent with how acronyms are kept
elsewhere in the registry, e.g. GFDD/WDI). category_fa: 0 inconsistencies, checked
against the full registry (not just this slice).

Verdict counts: keep=234, retitle=89, needs_review=0.

Done. No further rows to process in this shard.
