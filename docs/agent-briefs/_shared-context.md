# Shared context for all data-quality agents (READ FIRST)

You are one agent in a fleet working on the **Iran Economic Database** at
`/Users/rohamhosseini/Iran Economic database`. The database feeds a bilingual
(English/Persian) public website, "Iran in Data" (ایران در داده‌ها). The owner has
judged the current chart catalog **not publishable**: wrong charts, bad titles,
report-fragments masquerading as charts. Your job is to fix that, one slice at a time.

## File map

- `data/processed/CHART_REGISTRY.csv` — THE canonical chart list (1,846 rows).
  Columns: `chart_id, title, title_fa, category, category_fa, primary_source,
  alt_sources, n_unit_variants_merged, underlying_codes, status, extends_chart_id,
  merged_into, time_range, notes, citations_json`.
  Rows with `status=merged` are already dead — skip them.
- `data/charts/<chart_id>/data.csv` — materialized data. Columns include
  `year, value, unit, variant_code, variant_label, country_iso3, original_period_label`.
  Open these ONLY for spot checks when the registry row alone can't answer a question.
- `data/charts/<chart_id>/meta.json` — materialized metadata (regenerated from the
  registry by a pipeline; you never edit these).
- `catalog/CHARTS_INDEX.json` — build artifact, never edit.
- `docs/bookkeeping.md` — repo bookkeeping conventions.

## Hard rules

1. **Never edit `CHART_REGISTRY.csv` directly.** You write PROPOSALS to your own
   output shard (defined in your task brief). A separate controlled step applies them.
2. **Never spawn sub-agents.** Do all work yourself, in your own context.
3. **No fabricated data.** If you can't verify something, say `needs_review` with a
   reason; never invent a fact, translation source, or citation.
4. **Bias policy**: sources from MEK/NCRI-affiliated outlets are excluded from this
   project. This is a specific-outlet exclusion, not a political filter. Contested
   estimates are recorded as ranges, not adjudicated.
5. **Incremental bookkeeping (mandatory).** Append to your progress log
   `logs/agents/<your-shard-name>.progress.md` after EVERY ~20 charts processed:
   one line, `- [timestamp] rows X–Y done, N proposals`. Write your output shard
   incrementally too (append rows as you go, not one big dump at the end). If you
   die mid-task, the next agent must be able to resume from your files alone.
6. Work ONLY your assigned row slice. Do not "helpfully" fix things outside it.
7. Keep web lookups rare and purposeful (translation terminology checks only).

## Output shard conventions

- Directory: `data/processed/quality_audit/` (create if missing).
- CSV, UTF-8, header row, RFC-4180 quoting (quote any field containing commas,
  quotes, or newlines). One row per chart you reviewed, including `keep` verdicts,
  so coverage is provable.

## How to get your row slice

```python
import csv
with open('data/processed/CHART_REGISTRY.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
# rows is 0-indexed over data rows (header excluded).
# Your brief gives you a slice like rows[0:400].
```
