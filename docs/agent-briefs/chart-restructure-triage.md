# Task brief: Chart restructure triage

Read `docs/agent-briefs/_shared-context.md` first. Your slice of
`CHART_REGISTRY.csv` rows is given in your launch prompt.

## The doctrine: charts are MEASURES, not reports

A chart on this site is **one economic measure over time**, with Iran as the hero
series and other countries as toggleable comparators. Multiple *unit variants of the
same measure* (current US$ / constant US$ / local currency / % of GDP) belong in ONE
chart as measure-toggles. Different *measures* never share a chart.

The owner's canonical examples:

- **WRONG**: a standalone chart "Iran vs Iraq external debt during the war".
  Foreign debt is the measure → ONE "External debt" chart; Iraq is a comparator
  country the user toggles on; the war years are visible on it. Verdict for such a
  chart: `merge_into` the canonical measure chart (name it), with the useful series
  folded in as comparator-country data.
- **WRONG**: charts named after a report or document (e.g. CIA "Gloomy Prospects"
  1987 tables, one-off OPEC snapshot tables). A report is a *source*, not a chart.
  If its data points extend a real measure (oil exports, current account, debt),
  verdict `merge_into` that measure chart. If it's a grab-bag (`_misc_`), verdict
  `split` or `delete` with the salvageable series named.
- **WRONG**: one chart containing several genuinely different measures (different
  units that are NOT unit-variants of one measure, e.g. production tonnes + price +
  export value jammed together). Verdict `split`, list the resulting measures.
- **WRONG**: a tiny fragment of a bigger metric standing alone (e.g. "Net official
  flows from UN agencies, FAO" as its own chart when sibling rows cover every other
  UN agency). Propose ONE parent chart (e.g. "Net official flows from UN agencies"
  with agency as measure-variant or summed) and `merge_into` it.

## What to check per row

1. Should this chart exist as its own measure? (see doctrine above)
2. Is the EN `title` a clean measure name? Rules:
   - Plain measure phrasing, unit context in parentheses is fine.
   - NO source/report names, NO document years, NO "Iran" prefix (every chart is
     Iran-centric already), NO em dashes (use commas).
3. Is the `category` the natural home for this measure?
4. Cross-slice duplicates: if two rows in YOUR slice are the same measure from
   different sources, propose merging (keep the longer/better-sourced one, other
   becomes `merge_into` + alt source).

You judge mostly from the registry row itself (title, underlying_codes, category,
notes). Open `data/charts/<id>/data.csv` only when the row is ambiguous (e.g. to see
variant_labels/units, or whether a "vs Iraq" chart is really just comparator rows).

## Output shard

`data/processed/quality_audit/restructure_rows_<START>_<END>.csv` with columns:

```
chart_id,verdict,merge_into,proposed_title,proposed_category,reason
```

- `verdict` ∈ `keep | retitle | merge_into | split | delete | needs_review`
- `merge_into`: target chart_id (existing, or a proposed new parent id in the form
  `proposed__<slug>` if the canonical chart doesn't exist yet) — only for
  verdict=merge_into.
- `proposed_title`: only when it differs from current (for retitle/split/merge
  targets). For `split`, put the list of resulting measure titles separated by ` | `.
- `reason`: one terse sentence. Always filled except plain `keep`.

Every row of your slice appears exactly once. Append incrementally. Log progress
per _shared-context.md rule 5.
