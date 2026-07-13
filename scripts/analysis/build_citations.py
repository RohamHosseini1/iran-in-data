"""Attach real, verifiable citations (source org + URL) to every chart in
CHART_REGISTRY.csv, and propagate them into each materialized data/charts/*/meta.json.
Never fabricates a URL: machine-readable sources get their well-known canonical
citation; archival/hand-curated sources get their exact manifest.json source_url
via direct or fuzzy-matched lookup; anything that can't be confidently resolved is
left blank and flagged for manual follow-up, not guessed.

--- 2026-07-13 citation-accuracy-audit: fuzzy_resolve_archival() false-positive fixes ---
A full manual audit of every one of the 75 rows this function had ever fuzzy-matched
(see logs/downloads/citation-accuracy-audit.log) found 15 confirmed WRONG citations
(country or topic mismatch between the chart and the cited source) caused by two
independent bugs in the matcher, both fixed below:

  Bug A (tier-ordering false positive): the matcher checked the small
  `pahlavi_folders` pool FIRST (min_score=2) and returned the instant it cleared that
  low bar, without ever comparing against a potentially much stronger match sitting in
  the larger `all_manifest_folders` pool (tier 2, min_score=3, previously only checked
  `if not best`). Example: the 4 `iran_census__*` demography charts scored only 3
  tokens against "iranica-fiscal-system-narrative-series-1921-1979" (a pahlavi-pool
  folder about an unrelated topic, fiscal history) and got accepted, while the correct
  folder "iranica-census-demography-narrative-series-1868-1998" (tier-2-only) scored 7
  tokens and was never even evaluated. FIX: both pools are now always scored, and the
  globally-highest-scoring candidate that clears its own pool's threshold wins,
  regardless of which pool it came from.

  Bug B (no country-consistency check): raw token overlap can coincidentally favor a
  wrong-country folder when both share generic tokens (date ranges, "rate", "daily",
  "series", etc.), with nothing to penalize a nonsensical country match. Example:
  both `iran_fx__usd_irr_parallel_rate_daily_2011_2026` and
  `fx__official_vs_parallel_gap_irn` (Iran FX charts) fuzzy-matched to
  "data/raw/argentinadatos/dolares-multi-rate-daily-2011-2026" (an ARGENTINA folder,
  manifest countries=['ARG']) purely because that folder's name shares the tokens
  rate/daily/2011/2026 with the Iran chart's own underlying_codes filename, scoring 4
  vs. the correct Iran folder "usd-irr-parallel-history" (countries=['IRN']) which only
  scored 3 — a purely coincidental generic-token collision beat the right answer by one
  point. FIX: `infer_expected_countries()` guesses the chart's real country from its
  chart_id prefix / category / primary_source (defaulting to Iran, since this is an
  Iran-first database), and `_best_match()` now hard-rejects any candidate whose own
  manifest.json `countries` field is non-empty and shares NO country with the chart's
  expected country — a country mismatch is disqualifying, not just a tie-breaker.

  Bug C (minor, same audit): a `primary_source` value using the documented
  "type:slug" convention (e.g. "ine-portugal:slep2020") silently fell through to the
  noisy fuzzy pools whenever `slug` didn't exactly equal a manifest folder's basename
  (e.g. the real folder was named "long-series-portuguese-economy", not "slep2020") —
  even though `type` ("ine-portugal") unambiguously named a real, single-dataset
  `data/raw/` source directory. FIX: added a direct-match fallback that resolves
  "type:slug" to the sole manifest under `data/raw/<type>/` when there is exactly one
  (still a deterministic direct lookup, not a fuzzy heuristic — if a source directory
  ever has more than one dataset this fallback intentionally declines to guess).

These fixes were verified by hand against all 75 previously-fuzzy-matched rows before
being applied to the matcher (see the audit log for the row-by-row comparison); the 15
confirmed-wrong rows plus 1 completeness improvement were also hand-patched directly
into CHART_REGISTRY.csv (not by re-running this whole script) so the fix could be
verified row-by-row rather than trusting a full-registry regeneration blind.
"""
import csv
import json
import glob
import os
import re
from datetime import datetime

REGISTRY = "data/processed/CHART_REGISTRY.csv"
CHARTS_DIR = "data/charts"

# ---------- 1. harvest every raw manifest into an index ----------
manifest_index = {}  # folder_slug (basename of the manifest's parent dir) -> citation dict
for mpath in glob.glob("data/raw/**/manifest.json", recursive=True):
    folder = os.path.basename(os.path.dirname(mpath))
    try:
        with open(mpath, encoding="utf-8") as f:
            m = json.load(f)
    except Exception:
        continue
    manifest_index[folder] = {
        "source_org": m.get("source_org", ""),
        "source_url": m.get("source_url") or m.get("download_url") or "",
        "retrieved_at_utc": m.get("retrieved_at_utc", ""),
        "license_terms": m.get("license_terms", ""),
        "countries": m.get("countries") or [],
        "_manifest_path": mpath,
    }

print(f"Harvested {len(manifest_index)} raw manifests into citation index.")

# ---------- 2. canonical citations for the 6 machine-readable sources ----------
TODAY = "2026-07-13"

def wdi_citation(codes):
    code = codes.split("|")[0]
    return [{"source_org": "World Bank, World Development Indicators",
              "source_url": f"https://data.worldbank.org/indicator/{code}",
              "access_date": TODAY, "time_range": ""}]

def weo_citation(codes):
    return [{"source_org": "IMF, World Economic Outlook Database",
              "source_url": "https://www.imf.org/en/Publications/WEO/weo-database/2025/october",
              "access_date": TODAY, "time_range": ""}]

def owid_citation(code):
    return [{"source_org": "Our World in Data",
              "source_url": f"https://ourworldindata.org/grapher/{code.split('__')[0]}",
              "access_date": TODAY, "time_range": ""}]

def wid_citation():
    return [{"source_org": "World Inequality Database (WID.world)",
              "source_url": "https://wid.world/country/iran/",
              "access_date": TODAY, "time_range": ""}]

FAOSTAT_DOMAIN_URL = {
    "qcl": "https://www.fao.org/faostat/en/#data/QCL",
    "fbs": "https://www.fao.org/faostat/en/#data/FBS",
    "fbsh": "https://www.fao.org/faostat/en/#data/FBSH",
    "pp": "https://www.fao.org/faostat/en/#data/PP",
    "pa": "https://www.fao.org/faostat/en/#data/PP",  # archive is the same domain family, pre-1991 vintage
}

def faostat_citation(primary_source):
    doms = re.findall(r"[a-z]+", primary_source.replace("faostat-", ""))
    out = []
    for d in doms:
        if d in FAOSTAT_DOMAIN_URL:
            out.append({"source_org": "FAO, FAOSTAT", "source_url": FAOSTAT_DOMAIN_URL[d],
                        "access_date": TODAY, "time_range": ""})
    return out or [{"source_org": "FAO, FAOSTAT", "source_url": "https://www.fao.org/faostat/en/#data",
                     "access_date": TODAY, "time_range": ""}]

def maddison_citation():
    return [{"source_org": "Maddison Project Database, University of Groningen",
              "source_url": "https://www.rug.nl/ggdc/historicaldevelopment/maddison/",
              "access_date": TODAY, "time_range": ""}]

# ---------- 3. fuzzy match for archival/hand-curated rows ----------
pahlavi_folders = [os.path.basename(p) for p in glob.glob("data/raw/pahlavi-era-primary-extraction/*") if os.path.isdir(p)]
all_manifest_folders = list(manifest_index.keys())

def tokenize(s):
    return set(re.split(r"[_\-./,() ]+", s.lower())) - {"", "csv", "1950", "1960", "1970", "and", "the", "of", "by"}

# Keyword -> ISO3 hints for guessing which country a chart is actually about, used only
# to REJECT an obviously-wrong-country fuzzy candidate (Bug B fix, see module docstring).
# This project is Iran-first, so the default/fallback is IRN whenever no other country
# keyword is present in the chart_id/category/primary_source.
COUNTRY_HINTS = [
    ("portugal", "PRT"), ("spain", "ESP"), ("venezuela", "VEN"), ("saudi", "SAU"),
    ("turkey", "TUR"), ("turk", "TUR"), ("korea", "KOR"), ("russia", "RUS"),
    ("soviet", "RUS"), ("ussr", "RUS"), ("argentina", "ARG"), ("usa_comparator", "USA"),
    ("greece", "GRC"), ("germany", "DEU"), ("france", "FRA"), ("britain", "GBR"),
    ("united_kingdom", "GBR"), ("italy", "ITA"), ("netherlands", "NLD"), ("sweden", "SWE"),
]

def infer_expected_countries(chart_id, category, primary_source):
    haystack = f"{chart_id} {category} {primary_source}".lower()
    hits = {iso3 for kw, iso3 in COUNTRY_HINTS if kw in haystack}
    return hits or {"IRN"}

def _best_match(target_tokens, pool, min_score, expected_countries):
    best, best_score = None, 0
    for folder in pool:
        score = len(target_tokens & tokenize(folder))
        if score < min_score or score <= best_score:
            continue
        c = manifest_index.get(folder)
        if c is not None:
            folder_countries = set(c.get("countries") or [])
            # Hard-reject a candidate whose own manifest names countries that share NONE
            # with the chart's expected country -- a token-overlap coincidence is not
            # allowed to override a real country mismatch (this is exactly what let an
            # Argentina FX folder outscore the correct Iran one by one generic token).
            if folder_countries and not (folder_countries & expected_countries):
                continue
        best, best_score = folder, score
    return (best, best_score) if best else (None, 0)

def _single_manifest_under(type_dir):
    """If data/raw/<type_dir>/ contains exactly one dataset with a manifest.json,
    return its folder basename; otherwise None. Deterministic direct lookup (Bug C
    fix), not a fuzzy heuristic -- declines to guess if there's more than one dataset."""
    candidates = [os.path.basename(os.path.dirname(p))
                  for p in glob.glob(f"data/raw/{type_dir}/*/manifest.json")]
    return candidates[0] if len(candidates) == 1 else None

def fuzzy_resolve_archival(chart_id, underlying_codes, primary_source, category=""):
    # direct: primary_source has "type:slug" pattern and slug is a real manifest folder
    if ":" in primary_source:
        ptype, slug = primary_source.split(":", 1)
        if slug in manifest_index:
            c = manifest_index[slug]
            return [{"source_org": c["source_org"], "source_url": c["source_url"],
                      "access_date": c["retrieved_at_utc"][:10] if c["retrieved_at_utc"] else TODAY, "time_range": ""}]
        # slug didn't match a folder name exactly, but the type prefix may unambiguously
        # name a single-dataset source directory (Bug C fix)
        sole = _single_manifest_under(ptype)
        if sole:
            c = manifest_index[sole]
            return [{"source_org": c["source_org"], "source_url": c["source_url"],
                      "access_date": c["retrieved_at_utc"][:10] if c["retrieved_at_utc"] else TODAY, "time_range": ""}]
    # direct: primary_source itself (no colon) is exactly a manifest folder name
    if primary_source in manifest_index:
        c = manifest_index[primary_source]
        return [{"source_org": c["source_org"], "source_url": c["source_url"],
                  "access_date": c["retrieved_at_utc"][:10] if c["retrieved_at_utc"] else TODAY, "time_range": ""}]
    target_tokens = tokenize(chart_id) | tokenize(underlying_codes)
    expected_countries = infer_expected_countries(chart_id, category, primary_source)
    # Score BOTH pools (tight threshold for the common pahlavi-extraction pool, higher
    # threshold for the larger/noisier full-manifest pool) and let the globally
    # highest-scoring, country-consistent candidate win -- previously tier 1 returned
    # immediately upon clearing its own threshold even when tier 2 had a much better
    # match (Bug A fix, see module docstring).
    best1, score1 = _best_match(target_tokens, pahlavi_folders, 2, expected_countries)
    best2, score2 = _best_match(target_tokens, all_manifest_folders, 3, expected_countries)
    if best1 and best2:
        best, best_score = (best1, score1) if score1 >= score2 else (best2, score2)
    else:
        best, best_score = (best1, score1) if best1 else (best2, score2)
    if best and best in manifest_index:
        c = manifest_index[best]
        return [{"source_org": c["source_org"], "source_url": c["source_url"],
                  "access_date": c["retrieved_at_utc"][:10] if c["retrieved_at_utc"] else TODAY,
                  "time_range": "", "match_confidence": f"fuzzy:{best_score}tok:{best}"}]
    return []


def _is_hand_curated(raw_citations_json):
    """True only for archival rows whose EXISTING citation was hand-verified (by the
    2026-07-13 citation-accuracy-audit or a later manual restoration) rather than
    produced by fuzzy_resolve_archival() -- i.e. every entry either lacks a
    match_confidence key or has one that doesn't start with "fuzzy:". Only ever
    consulted for the archival/fuzzy-matched branch below -- the deterministic
    wdi/faostat/weo/owid/wid/maddison branches always recompute fresh (safe: same
    input codes always produce the same canonical citation, so re-running is a
    no-op unless the citation function itself improves, in which case regenerating
    IS the correct behavior).
    Re-running main() must never silently clobber a hand-curated archival citation:
    that exact bug happened once already (a later staging-merge re-ran this script
    from a pre-audit snapshot and wiped 8 of the 16 audit-fixed rows back to
    worse/wrong fuzzy matches -- see logs/downloads/citation-accuracy-audit.log's
    2026-07-13 restoration entry). Rows entirely produced by fuzzy_resolve_archival()
    (every entry tagged "fuzzy:...") are NOT hand-curated and remain safe/intended to
    regenerate, since that's how matcher improvements propagate."""
    if not raw_citations_json:
        return False
    try:
        cites = json.loads(raw_citations_json)
    except json.JSONDecodeError:
        return False
    if not cites:
        return False
    return not all(str(c.get("match_confidence", "")).startswith("fuzzy:") for c in cites)


def main():
    with open(REGISTRY, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    if "citations_json" not in fieldnames:
        fieldnames.append("citations_json")

    resolved, unresolved, preserved = 0, [], 0
    for r in rows:
        cid, ps, uc = r["chart_id"], r["primary_source"], r["underlying_codes"]

        cites = []
        if cid.startswith("wdi__"):
            cites = wdi_citation(uc)
        elif cid.startswith("faostat__"):
            cites = faostat_citation(ps)
        elif cid.startswith("weo__"):
            cites = weo_citation(uc)
        elif cid.startswith("owid__"):
            cites = owid_citation(uc)
        elif cid.startswith("wid__"):
            cites = wid_citation()
        elif ps == "maddison" or "maddison" in cid.lower():
            cites = maddison_citation()
        elif _is_hand_curated(r.get("citations_json", "")):
            preserved += 1
            resolved += 1
            continue
        else:
            cites = fuzzy_resolve_archival(cid, uc, ps, r.get("category", ""))

        r["citations_json"] = json.dumps(cites, ensure_ascii=False)
        if cites:
            resolved += 1
        else:
            unresolved.append(cid)

    print(f"Hand-curated archival citations preserved untouched: {preserved}")

    with open(REGISTRY, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"Chart rows with a resolved citation: {resolved}/{len(rows)}")
    print(f"Unresolved (flagged, left blank, NOT fabricated): {len(unresolved)}")
    for cid in unresolved[:40]:
        print("  ", cid)

    # propagate into materialized data/charts/*/meta.json
    cite_by_id = {r["chart_id"]: json.loads(r["citations_json"]) for r in rows}
    updated_meta = 0
    for folder in os.listdir(CHARTS_DIR):
        meta_path = os.path.join(CHARTS_DIR, folder, "meta.json")
        if not os.path.exists(meta_path):
            continue
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        cid = meta.get("chart_id", folder)
        if cid in cite_by_id and cite_by_id[cid]:
            meta["citations"] = cite_by_id[cid]
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            updated_meta += 1
    print(f"Updated citations in {updated_meta} data/charts/*/meta.json files.")


if __name__ == "__main__":
    main()
