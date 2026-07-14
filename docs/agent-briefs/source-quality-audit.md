# Task brief: Source quality audit (NOT YET LAUNCHED — written to survive context loss)

Read `docs/agent-briefs/_shared-context.md` first.

## Goal

For a slice of `CHART_REGISTRY.csv`, verify that each chart's `citations_json` is
real, resolvable, and honest:

1. Every citation has `source_org`, `source_url`, `access_date`.
2. The `source_url` plausibly matches the measure (an indicator page, dataset page,
   or archived document — not a homepage, not a search page).
3. `primary_source` slug matches an entry in `SOURCES.md` and the raw data exists
   under `data/raw/<source-slug>/`.
4. Bias policy: flag any citation to MEK/NCRI-affiliated outlets for removal
   (see _shared-context.md rule 4).
5. Contested numbers (revolution-era, war-era, sanctions-era estimates) should carry
   ranges or multiple sources, not a single unexplained point estimate — flag
   single-sourced contested series as `needs_second_source`.

Spot-check URLs with WebFetch sparingly (max ~1 in 10 rows, prioritizing obscure
sources; WDI/IMF/FAOSTAT URL patterns can be validated by shape).

## Output shard

`data/processed/quality_audit/sources_rows_<START>_<END>.csv`:

```
chart_id,source_verdict,issue,suggested_fix
```

`source_verdict` ∈ `ok | broken_citation | wrong_url | excluded_outlet |
needs_second_source | needs_review`.

Append incrementally; progress log per _shared-context.md rule 5.
