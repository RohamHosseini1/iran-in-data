"""Build the machine-readable discovery layer for the Iran Economic Database:

  catalog/CHARTS_INDEX.json  -- one JSON array, one object per chart_id in
                                 CHART_REGISTRY.csv, joined with data/charts/<id>/meta.json
                                 wherever that chart has already been materialized.
  catalog/CATEGORIES.json    -- the same chart_ids grouped by category, for a
                                 frontend nav/sidebar or an agent browsing by topic.

This is a pure read-and-join over two things that already exist:
  1. data/processed/CHART_REGISTRY.csv  -- the master flat index (never edited here).
  2. data/charts/<chart_id>/meta.json   -- per-chart metadata, materialized by a
     separate pipeline and still landing incrementally (as of writing, ~215 of
     ~1,790 registry rows have no data/charts/ folder yet -- an archival batch is
     being materialized concurrently). This script queries both FRESH every run and
     degrades gracefully for any registry row that isn't materialized yet: year_range/
     countries/row_count/data_path come back null and "materialized": false, rather
     than erroring or guessing.

Re-runnable: run this any time CHART_REGISTRY.csv grows or more data/charts/
folders land, and CHARTS_INDEX.json / CATEGORIES.json get fully regenerated
(not incrementally patched) from current disk state. Never writes anything
outside catalog/.

Chart-id -> folder-name note: a chart_id containing "/" (e.g. FAOSTAT item names
like "Swine / pigs") cannot be a literal folder name on disk, so the materializer
(scripts/analysis/build_layer3_charts.py) slugifies it via .replace("/", "_") for
the directory only; meta.json's own "chart_id" field, and this script's join, both
still use the original registry chart_id as the canonical identifier.

No fabricated metadata: every field below is either copied verbatim from
CHART_REGISTRY.csv / meta.json, or mechanically derived (see derive_description).
Nothing is guessed.
"""
import csv
import json
import os
import re

REGISTRY = "data/processed/CHART_REGISTRY.csv"
CHARTS_DIR = "data/charts"
OUT_INDEX = "catalog/CHARTS_INDEX.json"
OUT_CATEGORIES = "catalog/CATEGORIES.json"

_SENTENCE_RE = re.compile(r"^(.*?[.!?])(?:\s|$)")


def slugify(chart_id):
    """Mirror scripts/analysis/build_layer3_charts.py's slugify -- the only
    known filesystem-unsafe character actually used in a chart_id is '/'."""
    return chart_id.replace("/", "_")


def derive_description(title, notes):
    """Short, one-sentence description. Never invents content: either the
    first sentence of the registry's own 'notes' field (when that yields a
    reasonably-sized, real sentence), or the chart's title verbatim."""
    notes = (notes or "").strip()
    if not notes:
        return title
    # notes fields sometimes bundle multiple unrelated sub-notes separated by
    # "||" (see docs/bookkeeping.md-adjacent convention in CHART_REGISTRY.csv);
    # only the first sub-note is a candidate for a standalone description.
    segment = notes.split("||")[0].strip()
    match = _SENTENCE_RE.match(segment)
    candidate = match.group(1).strip() if match else segment
    if len(candidate) < 12 or len(candidate) > 320:
        return title
    return candidate


def parse_time_range(time_range_str):
    """CHART_REGISTRY.csv's time_range column is 'YYYY-YYYY' or a single 'YYYY'."""
    s = (time_range_str or "").strip()
    if not s:
        return None
    parts = s.split("-")
    if len(parts) == 2:
        return [parts[0].strip(), parts[1].strip()]
    return [s, s]


def load_registry():
    with open(REGISTRY, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def index_chart_dirs():
    """dir listing of data/charts/, queried fresh every run."""
    if not os.path.isdir(CHARTS_DIR):
        return set()
    return set(os.listdir(CHARTS_DIR))


def resolve_dir(chart_id, dirs):
    if chart_id in dirs:
        return chart_id
    alt = slugify(chart_id)
    if alt in dirs:
        return alt
    return None


def load_meta(dirname):
    path = os.path.join(CHARTS_DIR, dirname, "meta.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def count_csv_rows(path):
    try:
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in csv.reader(f)) - 1  # minus header
    except FileNotFoundError:
        return None


def build_entry(row, dirs):
    chart_id = row["chart_id"]
    title = row["title"]
    category = row["category"] or None
    dirname = resolve_dir(chart_id, dirs)
    meta = load_meta(dirname) if dirname else None

    # citations: registry's citations_json is the canonical copy (present on
    # every row we've seen); fall back to meta.json's "citations" if a row
    # ever lacks it.
    citations = []
    raw_citations = (row.get("citations_json") or "").strip()
    if raw_citations:
        try:
            citations = json.loads(raw_citations)
        except json.JSONDecodeError:
            citations = []
    if not citations and meta and meta.get("citations"):
        citations = meta["citations"]

    if meta:
        year_range = meta.get("year_range")
        countries = meta.get("countries", [])
        data_path = os.path.join(CHARTS_DIR, dirname, "data.csv")
        row_count = meta.get("n_rows")
        if row_count is None:
            row_count = count_csv_rows(data_path)
        primary_source = row["primary_source"] or meta.get("sources") or None
        # registry category is the master taxonomy; only fall back to meta's
        # if the registry row is somehow blank.
        category = category or meta.get("category")
    else:
        year_range = parse_time_range(row.get("time_range"))
        countries = []
        data_path = None
        row_count = None
        primary_source = row["primary_source"] or None

    description = derive_description(title, row.get("notes"))

    return {
        "chart_id": chart_id,
        "title": title,
        "category": category,
        "description": description,
        "year_range": year_range,
        "countries": countries,
        "primary_source": primary_source,
        "citations": citations,
        "data_path": data_path,
        "row_count": row_count,
        "status": row.get("status") or None,
        "materialized": meta is not None,
    }


def main():
    registry_rows = load_registry()
    dirs = index_chart_dirs()

    entries = [build_entry(row, dirs) for row in registry_rows]
    entries.sort(key=lambda e: e["chart_id"])

    os.makedirs("catalog", exist_ok=True)
    with open(OUT_INDEX, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    categories = {}
    for e in entries:
        cat = e["category"] or "Uncategorized"
        categories.setdefault(cat, []).append(e["chart_id"])
    for cat in categories:
        categories[cat].sort()
    categories_out = {cat: categories[cat] for cat in sorted(categories)}
    with open(OUT_CATEGORIES, "w", encoding="utf-8") as f:
        json.dump(categories_out, f, indent=2, ensure_ascii=False)

    materialized_n = sum(1 for e in entries if e["materialized"])
    print(f"CHART_REGISTRY.csv rows: {len(registry_rows)}")
    print(f"materialized (data/charts/ folder found): {materialized_n}")
    print(f"not yet materialized: {len(entries) - materialized_n}")
    print(f"categories: {len(categories_out)}")
    print(f"wrote {OUT_INDEX}")
    print(f"wrote {OUT_CATEGORIES}")


if __name__ == "__main__":
    main()
