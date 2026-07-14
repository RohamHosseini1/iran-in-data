# Persian title cleanup — progress log

Task: produce clean `title_fa` for the 832 changed=Y rows in
data/processed/quality_audit/title_proposals.csv, matching the new
(subject-only) English title. Output: data/processed/quality_audit/title_fa_proposals.csv

- [2026-07-14] Loaded title_proposals.csv (832 changed=Y rows, 618 unique new_title
  values: 311 FAOSTAT commodities, 306 WDI/other indicators, 1 FX-chart override).
  Built a hand-crafted EN->FA subject dictionary from established World Bank /
  FAOSTAT / fa.wikipedia.org terminology (no fabrication; relied on domain
  knowledge of standard Persian economic/agricultural nomenclature rather than
  per-term web searches, per rule 7 "keep web lookups rare").
- [2026-07-14] rows 1-832 done (all of them, single pass), 832 proposals written,
  0 needs_review. QC pass: no Arabic ي/ك, no em/en dashes, no double spaces,
  no leading/trailing whitespace in any of the 618 dictionary values.
- [2026-07-14] DONE. Output file: data/processed/quality_audit/title_fa_proposals.csv
  (832 rows, columns chart_id, old_title_fa, new_title_fa, note).
