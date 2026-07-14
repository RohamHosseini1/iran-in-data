"""Apply the 2026-07-14 quality-audit proposals to CHART_REGISTRY.csv and the
materialized charts.

Inputs (never modified): data/processed/quality_audit/{restructure,translation}_rows_*.csv
Targets: data/processed/CHART_REGISTRY.csv (backed up first), data/charts/<id>/
         (new child/parent chart dirs; meta.json title patches; source dirs untouched)

Actions, in order:
  1. Translation retitles: title_fa / category_fa.
  2. Restructure retitles: title / category (category_fa remapped via the
     registry's own category->category_fa majority mapping).
  3. Mechanical splits (FAOSTAT-family: one child chart per variant_code).
     Parent rows become status=merged pointing at the production child.
  4. merge_into existing targets: source hidden (status=merged), data kept on disk.
  5. merge_into proposed__* : three known families get a real parent chart built
     from their fragments (fragments' series become variants); fragments hidden.
     Unknown proposed targets are left visible and reported.
  6. delete: hidden (status=merged, merged_into empty), data kept on disk.
  7. Bespoke (non-mechanical) splits: hidden with an explicit needs-manual-split
     note, data kept on disk.
  8. Em-dash sweep over every remaining title/title_fa (", " / "، ").
  9. meta.json title/category patches for changed, materialized rows.

Everything hidden keeps its data directory: reversible by flipping status back.
A full action report is written to data/processed/quality_audit/APPLY_REPORT.md.
"""
import csv
import glob
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(ROOT, "data/processed/CHART_REGISTRY.csv")
AUDIT_DIR = os.path.join(ROOT, "data/processed/quality_audit")
CHARTS = os.path.join(ROOT, "data/charts")
REPORT = os.path.join(AUDIT_DIR, "APPLY_REPORT.md")
STAMP = "2026-07-14 quality audit"

DRY_RUN = "--dry-run" in sys.argv

# ---------------------------------------------------------------- helpers

def slug_dir(chart_id):
    return chart_id.replace("/", "_")


def slug_label(label):
    s = re.sub(r"[^A-Za-z0-9]+", "_", label.strip().lower()).strip("_")
    return s or "series"


def note_append(row, text):
    row["notes"] = (row["notes"] + " || " if row["notes"] else "") + text


def strip_dashes(text, fa):
    if not text:
        return text
    comma = "، " if fa else ", "
    text = text.replace(" — ", comma).replace("—", comma)
    text = text.replace(" – ", comma).replace("–", comma)
    return re.sub(r"\s{2,}", " ", text).strip()


def read_chart_rows(chart_id):
    path = os.path.join(CHARTS, slug_dir(chart_id), "data.csv")
    if not os.path.exists(path):
        return None, None
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames


def write_chart(dirname, fieldnames, rows, meta):
    d = os.path.join(CHARTS, dirname)
    if DRY_RUN:
        return
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(d, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)


def year_range_of(rows):
    years = [int(r["year"]) for r in rows if str(r.get("year", "")).lstrip("-").isdigit()]
    if not years:
        return None
    return [str(min(years)), str(max(years))]


# ------------------------------------------------------- FAOSTAT split maps

FAO_LABEL_FA = {
    "Production": "تولید",
    "Area harvested": "سطح زیر کشت",
    "Yield": "عملکرد",
    "Stocks": "موجودی دام",
    "Producing Animals/Slaughtered": "دام‌های کشتارشده",
    "Milk Animals": "دام‌های شیری",
    "Yield/Carcass Weight": "وزن لاشه",
    "Laying": "مرغان تخم‌گذار",
    "Prod Popultn": "جمعیت مولد",
}
UNIT_FA = {
    "t": "تن",
    "ha": "هکتار",
    "kg/ha": "کیلوگرم بر هکتار",
    "An": "رأس",
    "1000 An": "هزار رأس",
    "kg/An": "کیلوگرم بر رأس",
    "g/An": "گرم بر رأس",
    "No": "عدد",
    "1000 No": "هزار عدد",
    "No/An": "عدد بر رأس",
    "100 g/An": "صد گرم بر رأس",
    "0.1 g/An": "دهم گرم بر رأس",
}
FA_SPLIT_PREFIX = "تولید، سطح زیر کشت و عملکرد "


def crop_names(row):
    """(crop_en, crop_fa) extracted from the parent's titles."""
    en = row["title"].split(" — ")[0].strip()
    en = re.sub(r",\s*(production|imports and exports|producer price).*$", "", en, flags=re.I).strip()
    fa = row["title_fa"] or ""
    if " — " in fa:
        fa = fa.split(" — ")[0].strip()
    elif fa.startswith(FA_SPLIT_PREFIX):
        fa = fa[len(FA_SPLIT_PREFIX):].strip()
    return en, fa


# ------------------------------------------------ proposed__ parent families

def norm_target(t):
    return re.sub(r"[-]", "_", (t or "").strip())


FAMILIES = {
    "proposed__net_official_flows_un_agencies": {
        "title": "Net official flows from UN agencies, by agency (current US$)",
        "title_fa": "جریان‌های رسمی خالص از نهادهای سازمان ملل، به تفکیک نهاد (دلار جاری آمریکا)",
        "category": "Aid & Development Finance",
        "label_re": re.compile(r"Net official flows from UN agencies,\s*(.+?)\s*\(", re.I),
    },
    "proposed__external_debt_net_flows_by_creditor_type": {
        "title": "External debt net flows, by creditor type (current US$)",
        "title_fa": "جریان‌های خالص بدهی خارجی، به تفکیک نوع بستانکار (دلار جاری آمریکا)",
        "category": "External Debt",
        "label_re": re.compile(r"(?:Net flows on external debt,?|NFL[,:]?)\s*(.+?)\s*\(", re.I),
    },
    "proposed__population_by_age_group_sex": {
        "title": "Population by age group and sex (% of group population)",
        "title_fa": "جمعیت به تفکیک گروه سنی و جنس (درصد)",
        "category": "Demographics",
        "label_re": re.compile(r"Population ages\s*(.+?)\s*\(", re.I),
    },
}


# ---------------------------------------------------------------- load all

def main():
    with open(REGISTRY, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    registry = {r["chart_id"]: r for r in rows}
    order = [r["chart_id"] for r in rows]

    restr, trans = {}, {}
    for path in sorted(glob.glob(os.path.join(AUDIT_DIR, "restructure_rows_*.csv"))):
        for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
            restr[r["chart_id"]] = r
    for path in sorted(glob.glob(os.path.join(AUDIT_DIR, "translation_rows_*.csv"))):
        for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
            trans[r["chart_id"]] = r

    log = defaultdict(list)
    missing = [cid for cid in set(restr) | set(trans) if cid not in registry]
    if missing:
        log["warn"] += [f"shard chart_id not in registry: {m}" for m in missing]

    # category -> category_fa majority map from the registry itself
    cat_fa = {}
    counts = defaultdict(Counter)
    for r in rows:
        if r["category"] and r["category_fa"]:
            counts[r["category"]][r["category_fa"]] += 1
    for cat, c in counts.items():
        cat_fa[cat] = c.most_common(1)[0][0]

    # -- 1. translation retitles ------------------------------------------
    for cid, t in trans.items():
        row = registry.get(cid)
        if not row or t.get("fa_verdict") != "retitle":
            continue
        if (t.get("proposed_title_fa") or "").strip():
            row["title_fa"] = t["proposed_title_fa"].strip()
            log["fa_retitle"].append(cid)
        if (t.get("proposed_category_fa") or "").strip():
            row["category_fa"] = t["proposed_category_fa"].strip()

    # -- 2. restructure retitles ------------------------------------------
    for cid, a in restr.items():
        row = registry.get(cid)
        if not row or a.get("verdict") != "retitle":
            continue
        if (a.get("proposed_title") or "").strip():
            row["title"] = a["proposed_title"].strip()
            log["en_retitle"].append(cid)
            # fa follow-up: a chart retitled to production-only must not keep
            # the three-measure Persian phrase.
            if re.search(r",\s*production \(tonnes\)", row["title"], re.I) and \
               (row["title_fa"] or "").startswith(FA_SPLIT_PREFIX):
                crop = row["title_fa"][len(FA_SPLIT_PREFIX):].strip()
                row["title_fa"] = f"تولید {crop} (تن)"
                log["fa_followup"].append(cid)
        if (a.get("proposed_category") or "").strip():
            newcat = a["proposed_category"].strip()
            row["category"] = newcat
            if newcat in cat_fa:
                row["category_fa"] = cat_fa[newcat]
            else:
                log["category_fa_missing"].append(f"{cid}: {newcat}")
            log["recategorized"].append(cid)

    new_rows = []  # (after_chart_id, row) appended to registry order

    # -- 3. mechanical FAOSTAT splits --------------------------------------
    for cid, a in restr.items():
        row = registry.get(cid)
        if not row or a.get("verdict") != "split":
            continue
        data, fieldnames = (read_chart_rows(cid) if cid.startswith("faostat__") else (None, None))
        by_variant = defaultdict(list)
        if data:
            for r in data:
                by_variant[(r["variant_code"], r["variant_label"], r["unit"])].append(r)
        if not data or len(by_variant) < 2:
            # bespoke split: hide, keep data, flag for manual restructure
            row["status"] = "merged"
            row["merged_into"] = ""
            note_append(row, f"{STAMP}: flagged split ({a.get('reason','')[:160]}); hidden pending manual restructure, data preserved")
            log["hidden_bespoke_split"].append(cid)
            continue

        crop_en, crop_fa = crop_names(row)
        meta_parent = {}
        meta_path = os.path.join(CHARTS, slug_dir(cid), "meta.json")
        if os.path.exists(meta_path):
            meta_parent = json.load(open(meta_path, encoding="utf-8"))

        child_ids = []
        for (vcode, vlabel, unit), vrows in sorted(by_variant.items()):
            child_id = f"{cid}__{slug_label(vlabel)}"
            if child_id in registry:
                log["warn"].append(f"split child exists already: {child_id}")
                continue
            unit_fa = UNIT_FA.get(unit, unit)
            label_fa = FAO_LABEL_FA.get(vlabel)
            title_en = f"{crop_en}, {vlabel.lower()} ({unit})"
            if label_fa and crop_fa:
                title_fa = f"{label_fa} {crop_fa} ({unit_fa})"
            else:
                title_fa = f"{crop_fa}، {vlabel}" if crop_fa else ""
                log["fa_label_gap"].append(f"{child_id}: {vlabel}")
            yr = year_range_of(vrows)
            child_row = dict(row)
            child_row.update({
                "chart_id": child_id,
                "title": title_en,
                "title_fa": title_fa,
                "n_unit_variants_merged": "1",
                "underlying_codes": vcode,
                "status": "new",
                "extends_chart_id": "",
                "merged_into": "",
                "time_range": f"{yr[0]}-{yr[1]}" if yr else "",
                "notes": f"Split from {cid} by {STAMP}",
            })
            meta_child = dict(meta_parent) if meta_parent else {}
            meta_child.update({
                "chart_id": child_id,
                "title": title_en,
                "title_fa": title_fa,
                "n_rows": len(vrows),
                "year_range": yr,
                "countries": sorted({r["country_iso3"] for r in vrows}),
            })
            write_chart(slug_dir(child_id), fieldnames, vrows, meta_child)
            new_rows.append((cid, child_row))
            child_ids.append(child_id)
            log["split_children"].append(child_id)

        prod_child = next((c for c in child_ids if c.endswith("__production")), child_ids[0] if child_ids else "")
        row["status"] = "merged"
        row["merged_into"] = prod_child
        note_append(row, f"{STAMP}: split into {len(child_ids)} measure charts ({', '.join(child_ids)})")
        log["split_parents"].append(cid)

    # -- 4/5. merges --------------------------------------------------------
    family_frags = defaultdict(list)
    for cid, a in restr.items():
        row = registry.get(cid)
        if not row or a.get("verdict") != "merge_into":
            continue
        target = norm_target(a.get("merge_into"))
        if not target:
            log["warn"].append(f"merge_into without target: {cid}")
            continue
        if target.startswith("proposed__"):
            family_frags[target].append(cid)
            continue
        if target not in registry:
            log["warn"].append(f"merge target missing, left visible: {cid} -> {target}")
            continue
        row["status"] = "merged"
        row["merged_into"] = target
        note_append(row, f"{STAMP}: folded into {target} ({a.get('reason','')[:160]}); data preserved on disk")
        log["merged_existing"].append(f"{cid} -> {target}")

    for target, frags in family_frags.items():
        fam = FAMILIES.get(target)
        if not fam:
            log["family_unknown"].append(f"{target}: {len(frags)} fragments left visible")
            continue
        all_rows, fieldnames, countries = [], None, set()
        used = []
        for cid in sorted(frags):
            data, fn = read_chart_rows(cid)
            if not data:
                log["warn"].append(f"family fragment not materialized, skipped: {cid}")
                continue
            fieldnames = fieldnames or fn
            frow = registry[cid]
            m = fam["label_re"].search(frow["title"])
            label = m.group(1).strip() if m else frow["title"]
            vcode = frow["underlying_codes"] or slug_label(label)
            for r in data:
                r = dict(r)
                r["variant_code"] = vcode
                r["variant_label"] = label
                all_rows.append(r)
                countries.add(r["country_iso3"])
            used.append(cid)
        if not all_rows:
            log["warn"].append(f"family {target}: nothing to build")
            continue
        yr = year_range_of(all_rows)
        citations = registry[used[0]].get("citations_json", "")
        parent_row = dict(registry[used[0]])
        parent_row.update({
            "chart_id": target,
            "title": fam["title"],
            "title_fa": fam["title_fa"],
            "category": fam["category"],
            "category_fa": cat_fa.get(fam["category"], registry[used[0]]["category_fa"]),
            "primary_source": registry[used[0]]["primary_source"],
            "n_unit_variants_merged": str(len(used)),
            "underlying_codes": ";".join(registry[c]["underlying_codes"] for c in used),
            "status": "new",
            "extends_chart_id": "",
            "merged_into": "",
            "time_range": f"{yr[0]}-{yr[1]}" if yr else "",
            "notes": f"Built by {STAMP} from {len(used)} fragment charts",
            "citations_json": citations,
        })
        meta = {
            "chart_id": target,
            "title": fam["title"],
            "title_fa": fam["title_fa"],
            "category": fam["category"],
            "category_fa": parent_row["category_fa"],
            "sources": registry[used[0]]["primary_source"],
            "n_rows": len(all_rows),
            "year_range": yr,
            "countries": sorted(countries),
            "citations": json.loads(citations) if citations else [],
        }
        write_chart(slug_dir(target), fieldnames, all_rows, meta)
        new_rows.append((used[-1], parent_row))
        for cid in used:
            registry[cid]["status"] = "merged"
            registry[cid]["merged_into"] = target
            note_append(registry[cid], f"{STAMP}: folded into {target} as variant")
        log["family_built"].append(f"{target} ({len(used)} fragments)")

    # -- 6. deletes ---------------------------------------------------------
    for cid, a in restr.items():
        row = registry.get(cid)
        if not row or a.get("verdict") != "delete":
            continue
        row["status"] = "merged"
        row["merged_into"] = ""
        note_append(row, f"{STAMP}: removed from catalog ({a.get('reason','')[:160]}); data preserved on disk")
        log["deleted"].append(cid)

    # needs_review: note only
    for cid, a in restr.items():
        row = registry.get(cid)
        if row and a.get("verdict") == "needs_review":
            note_append(row, f"{STAMP}: needs_review ({a.get('reason','')[:160]})")
            log["needs_review"].append(cid)

    # -- 8. em-dash sweep ---------------------------------------------------
    for r in list(registry.values()) + [nr for _, nr in new_rows]:
        t0, f0 = r["title"], r["title_fa"]
        r["title"] = strip_dashes(r["title"], fa=False)
        r["title_fa"] = strip_dashes(r["title_fa"], fa=True)
        if (t0, f0) != (r["title"], r["title_fa"]):
            log["dash_swept"].append(r["chart_id"])

    # -- write registry -----------------------------------------------------
    out_rows = []
    inserted_after = defaultdict(list)
    for after, nr in new_rows:
        inserted_after[after].append(nr)
    for cid in order:
        out_rows.append(registry[cid])
        out_rows.extend(inserted_after.get(cid, []))

    if not DRY_RUN:
        shutil.copy2(REGISTRY, REGISTRY + ".bak-quality-apply")
        with open(REGISTRY, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(out_rows)

    # -- 9. patch meta.json titles for changed materialized rows ------------
    patched = 0
    if not DRY_RUN:
        for r in out_rows:
            mp = os.path.join(CHARTS, slug_dir(r["chart_id"]), "meta.json")
            if not os.path.exists(mp):
                continue
            try:
                meta = json.load(open(mp, encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            changed = False
            for src, dst in [("title", "title"), ("title_fa", "title_fa"),
                             ("category", "category"), ("category_fa", "category_fa")]:
                if r[src] and meta.get(dst) != r[src]:
                    meta[dst] = r[src]
                    changed = True
            if changed:
                json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                patched += 1

    # -- report --------------------------------------------------------------
    lines = [f"# Quality-audit apply report ({STAMP})", ""]
    lines.append(f"Registry rows before: {len(order)}, after: {len(out_rows)} (dry_run={DRY_RUN})")
    lines.append(f"meta.json files patched: {patched}")
    for key in sorted(log):
        lines.append(f"\n## {key} ({len(log[key])})")
        for item in log[key][:400]:
            lines.append(f"- {item}")
    report_text = "\n".join(lines)
    if not DRY_RUN:
        with open(REPORT, "w", encoding="utf-8") as f:
            f.write(report_text + "\n")

    print(f"rows: {len(order)} -> {len(out_rows)} | " +
          " | ".join(f"{k}:{len(v)}" for k, v in sorted(log.items())))


if __name__ == "__main__":
    main()
