#!/usr/bin/env python3
"""
clean_variant_labels.py -- humanize the measure names shown in each chart's
MEASURE dropdown.

Many variant_labels are raw machine output: snake_case codes, an em dash joining a
label to its own internal code ("General index — cpi_index_1395_100"), or a code
joined to a qualifier ("average_household_size — urban"). The owner banned em
dashes in site copy and flagged these labels as unreadable.

Rules (conservative -- a label is only touched if it looks machine-generated):
  * split on an em/en dash;
  * drop a side that is clearly an internal CODE (snake_case with digits/underscores)
    when the other side is human text;
  * otherwise keep both sides, joined by a comma (never an em dash);
  * snake_case -> spaced sentence case;
  * labels that are already clean English/Persian (no dash, no underscore) are left
    exactly as they are -- e.g. FAOSTAT's "Food supply quantity (kg/capita/yr)".

Pass --apply to write; default is a dry-run preview.
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)

DASH = re.compile(r"\s*[—–]\s*")
CODEY = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)+$")   # snake_case internal code
SNAKE = re.compile(r"^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)+$")


def humanize(tok):
    t = tok.strip()
    if SNAKE.match(t):
        t = t.replace("_", " ").strip()
        t = t[:1].upper() + t[1:]
    return t


def clean(label, code=""):
    """Only a segment that DUPLICATES the row's own variant_code is a redundant
    machine code and gets dropped. Snake_case alone is NOT evidence of a code --
    'total_population' / 'urban_resident' are meaningful qualifiers, and dropping
    them would collapse several distinct measures to the same name."""
    if not label:
        return label
    orig = label
    code = (code or "").strip()
    parts = [p.strip() for p in DASH.split(label) if p.strip()]
    if len(parts) > 1 and code:
        kept = [p for p in parts if p != code and p not in code.split("|")]
        if kept:
            parts = kept
    parts = [humanize(p) for p in parts]
    out = ", ".join(p for p in parts if p)
    out = re.sub(r"\s{2,}", " ", out).strip(" ,")
    out = out.replace("Non resident", "Non-resident")
    if out and out[0].islower():
        out = out[0].upper() + out[1:]
    return out or orig


def main():
    apply = "--apply" in sys.argv
    reg = {r["chart_id"]: r for r in csv.DictReader(open(REG, encoding="utf-8"))}
    live = [c for c, r in reg.items()
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]

    changed_charts = changed_labels = 0
    preview = []
    for cid in sorted(live):
        p = os.path.join(CHARTS, cid.replace("/", "_"), "data.csv")
        if not os.path.exists(p):
            continue
        with open(p, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames
            rows = list(rd)
        if "variant_label" not in (cols or []):
            continue
        # map each (label, code) pair once
        seen = {}
        for r in rows:
            key = (r.get("variant_label") or "", r.get("variant_code") or "")
            if key not in seen:
                seen[key] = clean(key[0], key[1])

        # COLLISION GUARD: two different measures must never end up with the same
        # displayed name. If cleaning collides, keep the originals for that group.
        by_new = {}
        for (old, code), new in seen.items():
            by_new.setdefault(new, set()).add(code)
        for (old, code), new in list(seen.items()):
            if len(by_new.get(new, ())) > 1:
                seen[(old, code)] = old  # revert: ambiguous

        touched = False
        for r in rows:
            key = (r.get("variant_label") or "", r.get("variant_code") or "")
            new = seen[key]
            if new != key[0]:
                r["variant_label"] = new
                touched = True
        seen = {k[0]: v for k, v in seen.items()}
        if touched:
            n = sum(1 for k, v in seen.items() if k != v)
            changed_charts += 1
            changed_labels += n
            for k, v in list(seen.items()):
                if k != v and len(preview) < 18:
                    preview.append((k, v))
            if apply:
                with open(p, "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=cols)
                    w.writeheader()
                    w.writerows(rows)

    print(f"{'APPLIED' if apply else 'DRY RUN'}: {changed_labels} distinct labels cleaned "
          f"across {changed_charts} charts")
    for k, v in preview:
        print(f"   {k[:58]!r}\n     -> {v[:58]!r}")
    if not apply:
        print("\nre-run with --apply to write")


if __name__ == "__main__":
    main()
