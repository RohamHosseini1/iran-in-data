# Progress log: translation_rows_0800_1199

Slice: CHART_REGISTRY.csv data rows [800:1200) (0-indexed, header excluded).
Composition: 212 wdi__* rows (800-1011) + 188 faostat-qcl__*__production rows
(1012-1199). All status=new (0 merged rows in this slice).

- [2026-07-14T00:00Z] rows 800-899 done (100 wdi rows reviewed)
- [2026-07-14T00:00Z] rows 900-999 done (100 wdi rows reviewed)
- [2026-07-14T00:00Z] rows 1000-1011 done (12 wdi rows reviewed; wdi block complete)
- [2026-07-14T00:00Z] rows 1012-1099 done (88 faostat production rows reviewed)
- [2026-07-14T00:00Z] rows 1100-1199 done (100 faostat production rows reviewed; slice complete)

Method: full manual read-through of all 400 title_fa/category_fa pairs (dumped
to a readable side file for review), cross-checked against established
registry-wide conventions via targeted grep/python scans (dash characters,
Arabic ي/ك, tatweel, missing ZWNJ, bare Latin acronyms outside parens,
category-english-to-persian consistency, "per capita" placement precedent).
One batched WebSearch for the single genuinely uncertain term (IDA -> fa.wikipedia
"انجمن توسعه بین‌الملل").

Key finding: the entire faostat-qcl production block (188/188 rows) uses the
dash-suffix pattern "<crop fa> — تولید، سطح زیر کشت و عملکرد", which is exactly
the doctrine's canonical WRONG-example pattern (chart faostat__Butter, Ghee__consumption
elsewhere in the registry literally IS the doc's quoted wrong example). Fixed by
moving the measure phrase to lead and the subject to the end, matching what the
neighboring slice (translation_rows_1200_1522.csv) independently converged on for
the same pattern (verified by inspection: identical "تولید، سطح زیر کشت و عملکرد <subject>"
construction) - good cross-slice consistency signal.

Investigated but decided NOT to change (documented so future agents don't
re-litigate): trailing سرانه after long compound nouns (e.g. "هزینه سلامت عمومی
دولت داخلی سرانه") looks like a rule-1/rule-5 violation at first glance, but is
in fact the established, internally-consistent, Wikipedia-fa-congruent pattern
used identically across sibling GHED/PVTD/CHEX rows elsewhere in the registry
(9 GDP-per-capita rows and 118 "مصرف سرانه" rows registry-wide confirm trailing
سرانه, 0 instances of leading سرانه) - left as keep.

Verdict counts: keep=206, retitle=191, needs_review=3.

Done. No further rows to process in this shard.
