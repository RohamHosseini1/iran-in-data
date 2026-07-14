#!/usr/bin/env python3
"""
build_annotation_links.py -- rebuild BOTH annotation layers from the two-score remap.

Replaces the earlier single-"confidence" mapping, which had three fatal defects:
  1. 575 of 1,123 significant laws were silently dropped (no coverage check).
  2. Median coverage was 1 law per chart; Iran's GDP chart had exactly ONE law.
  3. One "confidence" number conflated two different questions, so the White
     Revolution scored 1/5 against GDP -- absurd.

Now every link carries TWO scores:
  relevance   -- should a reader of THIS chart see this at all?   (drives display)
  attribution -- can we say it MOVED this line?                   (drives the causal claim)
The White Revolution on GDP is relevance 5 / attribution 2: you must see it, but we
cannot credit the line's movement to it.

Every free-text field is bilingual (justification/caveats/lag), which is what fixes
English text leaking onto the Persian site.

Outputs:
  data/processed/law_chart_links.csv
  data/processed/policy_chart_correlations_mapped.csv   (events; frontend globs this)
"""
import csv, json, os, sys
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC = os.path.join(ROOT, "data", "processed")
REMAP = os.path.join(PROC, "laws", "remap")
REG = os.path.join(PROC, "CHART_REGISTRY.csv")
csv.field_size_limit(sys.maxsize)

LAW_OUT = os.path.join(PROC, "law_chart_links.csv")
EV_OUT = os.path.join(PROC, "policy_chart_correlations_mapped.csv")

LAW_FIELDS = ["link_id", "chart_id", "law_id", "law_date", "law_title_fa",
              "law_title_en", "law_summary_en", "law_summary_fa",
              "relationship_type", "relevance", "attribution", "direction",
              "lag_en", "lag_fa", "justification_en", "justification_fa",
              "caveats_en", "caveats_fa", "scope", "source_path"]
EV_FIELDS = ["correlation_id", "chart_id", "chart_title", "event_date", "event_title",
             "event_source_file", "relationship_type", "relevance", "attribution",
             "direction", "lag_en", "lag_fa", "justification_en", "justification_fa",
             "caveats_en", "caveats_fa"]



# Agents sometimes wrote a DOMAIN TAG ("oil", "fiscal", "fx") where a chart CATEGORY
# was expected -- they reached for the law-metadata vocabulary. These are real,
# recoverable intentions, not invented nonsense, so map them onto the real categories.
DOMAIN_ALIAS = {
    "oil": ["Energy", "Energy / Oil Production & Trade", "Oil & Energy",
            "Infrastructure (Energy)"],
    "energy": ["Energy", "Infrastructure (Energy)"],
    "fiscal": ["Government Finance", "Macro / National Accounts"],
    "budget_fiscal": ["Government Finance"],
    "macro": ["Macro / National Accounts", "Macro / Expenditure & Trade Aggregates"],
    "trade": ["Trade (Exports)", "Trade (Imports)", "Trade (Goods)", "Trade",
              "Macro / Expenditure & Trade Aggregates"],
    "customs_trade": ["Trade (Exports)", "Trade (Imports)", "Trade (Goods)"],
    "banking": ["Financial Sector (Monetary)", "Financial Sector (Banking Access)",
                "Financial Sector (Private Credit)", "Financial Sector (Interest Rates)",
                "Financial Sector"],
    "banking_money": ["Financial Sector (Monetary)", "Financial Sector (Private Credit)"],
    "fx": ["Exchange Rates", "Exchange Rates (Parallel/Black Market)"],
    "inflation": ["Prices & Inflation"],
    "prices": ["Prices & Inflation"],
    "military": ["Military Expenditure"],
    "conflict": ["Conflict & Violence"],
    "health": ["Health"],
    "migration": ["Migration"],
    "labor": ["Labor & Employment"],
    "housing": ["Housing"],
    "agriculture": ["Agriculture Production", "Agriculture Prices", "Agriculture Trade"],
    "mining": ["Mining & Minerals Production"],
    "industry": ["Industry / Value Added by Sector", "Industry / Light Manufacturing"],
    "taxation": ["Government Finance"],
    "subsidies": ["Government Finance", "Prices & Inflation"],
    "privatization": ["Macro / National Accounts", "Capital Markets"],
    "welfare": ["Social Protection", "Poverty & Inequality"],
}


def load_charts():
    reg = list(csv.DictReader(open(REG, encoding="utf-8")))
    live = [r for r in reg
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]
    title = {r["chart_id"]: r["title"] for r in live}
    by_cat = defaultdict(list)
    for r in live:
        by_cat[r["category"]].append(r["chart_id"])
    return title, by_cat


def targets(link, title, by_cat, bad):
    out = []
    for cid in (link.get("chart_ids") or []):
        if cid in title:
            out.append((cid, "specific"))
        else:
            bad[0] += 1
    for cat in (link.get("categories") or []):
        if cat in by_cat:
            out += [(c, "category") for c in by_cat[cat]]
            continue
        for real in DOMAIN_ALIAS.get(cat.strip().lower(), []):
            if real in by_cat:
                out += [(c, "category") for c in by_cat[real]]
        else:
            if cat.strip().lower() not in DOMAIN_ALIAS:
                bad[1] += 1
    return out


def main():
    title, by_cat = load_charts()
    bad = [0, 0]

    # ---------- laws ----------
    laws = json.load(open(os.path.join(REMAP, "laws_mapped.json"), encoding="utf-8"))
    meta = {r["law_id"]: r for r in csv.DictReader(
        open(os.path.join(REMAP, "significant_laws.csv"), encoding="utf-8"))}
    tr = {}
    tp = os.path.join(PROC, "laws", "law_translations.csv")
    if os.path.exists(tp):
        tr = {r["law_id"]: r for r in csv.DictReader(open(tp, encoding="utf-8"))}

    # collapse duplicate law texts in the scraped corpus to one canonical id
    import re
    def norm(t):
        return re.sub(r"\s+", " ", (t or "")).strip().replace("ي", "ی").replace("ك", "ک")
    canon, ident = {}, {}
    for lid, m in meta.items():
        k = (norm(m["title_fa"]), m["year"])
        ident.setdefault(k, lid)
        canon[lid] = ident[k]

    rows, seen = [], set()
    for l in laws:
        lid = canon.get(l["law_id"], l["law_id"])
        m = meta.get(lid, {})
        t = tr.get(lid, {})
        for link in (l.get("links") or []):
            for cid, scope in targets(link, title, by_cat, bad):
                key = (cid, lid)
                if key in seen:
                    continue
                seen.add(key)
                rows.append({
                    "link_id": f"law_{len(rows)+1:06d}", "chart_id": cid, "law_id": lid,
                    "law_date": m.get("year", ""),
                    "law_title_fa": m.get("title_fa", ""),
                    "law_title_en": t.get("law_title_en", ""),
                    "law_summary_en": t.get("law_summary_en", ""),
                    "law_summary_fa": t.get("law_summary_fa", ""),
                    "relationship_type": link.get("relationship_type", ""),
                    "relevance": link.get("relevance", ""),
                    "attribution": link.get("attribution", ""),
                    "direction": link.get("direction", ""),
                    "lag_en": link.get("lag_en", ""), "lag_fa": link.get("lag_fa", ""),
                    "justification_en": link.get("justification_en", ""),
                    "justification_fa": link.get("justification_fa", ""),
                    "caveats_en": link.get("caveats_en", ""),
                    "caveats_fa": link.get("caveats_fa", ""),
                    "scope": scope, "source_path": m.get("path", ""),
                })
    with open(LAW_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LAW_FIELDS)
        w.writeheader()
        w.writerows(rows)

    # ---------- events ----------
    events = json.load(open(os.path.join(REMAP, "events_mapped.json"), encoding="utf-8"))
    erows, eseen = [], set()
    for e in events:
        for link in (e.get("links") or []):
            for cid, _ in targets(link, title, by_cat, bad):
                key = (cid, e["event_date"], e["event_title"])
                if key in eseen:
                    continue
                eseen.add(key)
                erows.append({
                    "correlation_id": f"ev_{len(erows)+1:06d}", "chart_id": cid,
                    "chart_title": title.get(cid, ""),
                    "event_date": e["event_date"], "event_title": e["event_title"],
                    "event_source_file": e["event_source_file"],
                    "relationship_type": link.get("relationship_type", ""),
                    "relevance": link.get("relevance", ""),
                    "attribution": link.get("attribution", ""),
                    "direction": link.get("direction", ""),
                    "lag_en": link.get("lag_en", ""), "lag_fa": link.get("lag_fa", ""),
                    "justification_en": link.get("justification_en", ""),
                    "justification_fa": link.get("justification_fa", ""),
                    "caveats_en": link.get("caveats_en", ""),
                    "caveats_fa": link.get("caveats_fa", ""),
                })
    with open(EV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=EV_FIELDS)
        w.writeheader()
        w.writerows(erows)

    # retire the old single-confidence event files: their schema has no relevance/
    # attribution and no Persian, so leaving them in the glob would resurrect the bug
    import glob
    for old in glob.glob(os.path.join(PROC, "policy_chart_correlations_*.csv")):
        if os.path.basename(old) != os.path.basename(EV_OUT):
            os.rename(old, old + ".superseded")

    all_charts = set(title)
    lc = Counter(r["chart_id"] for r in rows)
    ec = Counter(r["chart_id"] for r in erows)
    print(f"law links   : {len(rows):6d} | charts with a law   : {len([c for c in all_charts if lc[c]]):5d} / {len(all_charts)}")
    print(f"event links : {len(erows):6d} | charts with an event: {len([c for c in all_charts if ec[c]]):5d} / {len(all_charts)}")
    print(f"dropped invented refs: {bad[0]} chart_ids, {bad[1]} categories")
    for cid in ("wdi__NY.GDP.MKTP", "wdi__NY.GDP.PCAP", "wdi__FP.CPI.TOTL"):
        print(f"   {title.get(cid,cid):22} laws={lc[cid]:3d} events={ec[cid]:3d}")


if __name__ == "__main__":
    main()
