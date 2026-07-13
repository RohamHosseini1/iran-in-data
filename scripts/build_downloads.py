"""Package data/charts/ for bulk download: one zip of everything, plus one zip
per category (so a researcher who only wants "Energy" or "Health" doesn't have
to pull the whole 200+MB archive). Individual charts need no packaging of their
own -- each data/charts/<chart_id>/ folder (a data.csv + meta.json, a few KB to
a few hundred KB) is already trivially downloadable as-is; see README.md.

Reads catalog/CHARTS_INDEX.json and catalog/CATEGORIES.json (run
scripts/build_catalog_index.py first if they're stale) and writes:

  downloads/iran-economic-database-all-charts.zip   -- the whole data/charts/ tree
  downloads/by-category/<category-slug>.zip          -- one per category
  downloads/MANIFEST.json                            -- filename, chart count,
                                                         byte size of each zip

Only materialized charts (those with an actual data/charts/<id>/ folder) can be
zipped; any registry row still pending materialization is silently skipped here
(it's already flagged via "materialized": false in CHARTS_INDEX.json).

Re-runnable: overwrites downloads/ contents from current disk state every run.
"""
import json
import os
import re
import zipfile

CHARTS_INDEX = "catalog/CHARTS_INDEX.json"
CATEGORIES = "catalog/CATEGORIES.json"
CHARTS_DIR = "data/charts"
OUT_DIR = "downloads"
BY_CATEGORY_DIR = os.path.join(OUT_DIR, "by-category")


def slugify_category(name):
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def zip_chart_folder(zf, chart_dir_abs, arc_prefix):
    for fname in ("data.csv", "meta.json"):
        fpath = os.path.join(chart_dir_abs, fname)
        if os.path.isfile(fpath):
            zf.write(fpath, arcname=os.path.join(arc_prefix, fname))


def main():
    with open(CHARTS_INDEX, encoding="utf-8") as f:
        entries = json.load(f)
    with open(CATEGORIES, encoding="utf-8") as f:
        categories = json.load(f)

    by_id = {e["chart_id"]: e for e in entries}

    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(BY_CATEGORY_DIR, exist_ok=True)
    manifest = []

    # (a) one zip of the entire data/charts/ directory
    all_zip_path = os.path.join(OUT_DIR, "iran-economic-database-all-charts.zip")
    n_charts_all = 0
    with zipfile.ZipFile(all_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for e in entries:
            if not e["materialized"]:
                continue
            dirname = os.path.basename(os.path.dirname(e["data_path"]))
            chart_dir_abs = os.path.join(CHARTS_DIR, dirname)
            zip_chart_folder(zf, chart_dir_abs, os.path.join("data/charts", dirname))
            n_charts_all += 1
    all_zip_bytes = os.path.getsize(all_zip_path)
    manifest.append({
        "file": os.path.relpath(all_zip_path, OUT_DIR),
        "scope": "all charts",
        "chart_count": n_charts_all,
        "bytes": all_zip_bytes,
    })
    print(f"{all_zip_path}: {n_charts_all} charts, {all_zip_bytes / 1e6:.1f} MB")

    # (b) one zip per category
    total_category_bytes = 0
    for category, chart_ids in sorted(categories.items()):
        materialized_ids = [cid for cid in chart_ids if by_id.get(cid, {}).get("materialized")]
        if not materialized_ids:
            print(f"  skip category '{category}': 0 materialized charts")
            continue
        slug = slugify_category(category)
        zip_path = os.path.join(BY_CATEGORY_DIR, f"{slug}.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for cid in materialized_ids:
                e = by_id[cid]
                dirname = os.path.basename(os.path.dirname(e["data_path"]))
                chart_dir_abs = os.path.join(CHARTS_DIR, dirname)
                zip_chart_folder(zf, chart_dir_abs, os.path.join("data/charts", dirname))
        zip_bytes = os.path.getsize(zip_path)
        total_category_bytes += zip_bytes
        manifest.append({
            "file": os.path.relpath(zip_path, OUT_DIR),
            "scope": category,
            "chart_count": len(materialized_ids),
            "bytes": zip_bytes,
        })

    with open(os.path.join(OUT_DIR, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    n_category_zips = len(manifest) - 1
    print(f"wrote {n_category_zips} category zips under {BY_CATEGORY_DIR}/ "
          f"({total_category_bytes / 1e6:.1f} MB total)")
    print(f"wrote {os.path.join(OUT_DIR, 'MANIFEST.json')}")
    grand_total = all_zip_bytes + total_category_bytes
    print(f"grand total (all-charts zip + all category zips): {grand_total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
