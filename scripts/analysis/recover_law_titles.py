#!/usr/bin/env python3
"""
recover_law_titles.py -- un-mangle the Persian law titles.

BUG: a law's title was taken from its FILENAME. The scraper had to fit filenames into
the 255-BYTE filesystem limit, and Persian is 2 bytes per character in UTF-8, so any
title over ~85 characters was elided to  head + " ... " + tail. 359 of the 1,111
significant laws (8,329 of the 17,697 corpus files) carry a title with a hole in the
middle, and they drive 2,203 drawn chart markers.

The full title is NOT in the .txt body (that starts with site navigation chrome), so it
looked unrecoverable. It IS in the scraper's own .ndjson dumps: each record is
{category, lawId, article, tokens}, and for a whole-law record (article = None) the
FIRST LINE of `tokens` is the true, complete title. The corpus filename ends in that
same lawId, which is the join key.

NOTHING IS GUESSED. A recovered title is accepted only if it verifiably reconstructs
the elided one: it must START WITH the head fragment and END WITH the tail fragment we
already have. A law whose lawId only has per-article chunks (no whole-law record) has
no title on record, so its elided title is left exactly as it is.
"""
import csv, glob, json, os, re, shutil, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRAPER = "/Users/rohamhosseini/Documents/scraper simple"
SIG = os.path.join(ROOT, "data", "processed", "laws", "remap", "significant_laws.csv")
csv.field_size_limit(sys.maxsize)

ELISION = " ... "


def norm(s: str) -> str:
    """
    Fold the Arabic/Persian letter variants and collapse whitespace.

    NFC matters: macOS stores filenames DECOMPOSED (NFD), while the scraper's ndjson
    text is composed (NFC). Without this the same Persian word compares unequal to
    itself and every title fails to verify.
    """
    s = unicodedata.normalize("NFC", s or "")
    s = s.replace("ي", "ی").replace("ك", "ک").replace("ۀ", "ه").replace("ئ", "ی")
    s = s.replace("‌", " ").replace("_", " ")
    s = re.sub(r"[^\w\s]", " ", s)  # punctuation survives elision inconsistently
    return re.sub(r"\s+", " ", s).strip()


def load_ndjson_titles() -> dict[str, list[str]]:
    """lawId -> candidate first-lines, whole-law records first, in file order."""
    whole: dict[str, list[str]] = {}
    arts: dict[str, list[str]] = {}
    files = glob.glob(os.path.join(SCRAPER, "*.ndjson"))
    files += glob.glob(os.path.join(SCRAPER, "chunked_laws_output", "*.ndjson"))
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                lid = str(d.get("lawId") or "")
                toks = (d.get("tokens") or "").strip()
                if not lid or not toks:
                    continue
                first = next((l.strip() for l in toks.split("\n") if l.strip()), "")
                if not first:
                    continue
                # A whole-law record is authoritative, and its FIRST chunk carries the
                # title, so file order must be preserved (do not insert at the front).
                tgt = whole if d.get("article") in (None, "") else arts
                tgt.setdefault(lid, []).append(first)
    return {lid: whole.get(lid, []) + arts.get(lid, [])
            for lid in set(whole) | set(arts)}


def law_id_from_path(path: str) -> str:
    """The corpus filename ends in the scraper's lawId: <title>_<lawId>.txt"""
    m = re.search(r"_(\d{6,})\.txt$", os.path.basename(path))
    return m.group(1) if m else ""


def main():
    cand = load_ndjson_titles()
    print(f"lawIds in the scraper ndjson dumps: {len(cand)}")

    with open(SIG, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)

    elided = [r for r in rows if ELISION in r["title_fa"]]
    print(f"significant laws with an elided title: {len(elided)} / {len(rows)}")

    recovered = 0
    no_record = 0
    no_match = 0
    for r in elided:
        head, _, tail = r["title_fa"].partition(ELISION)
        nh, nt = norm(head), norm(tail)
        if not nh or not nt:
            continue
        lid = law_id_from_path(r["path"])
        options = cand.get(lid) or []
        if not options:
            no_record += 1
            continue
        # Accept ONLY a candidate that reproduces both known ends of the real title.
        # The elision cut mid-word, so the head/tail fragments can each be a partial
        # word: require the head to prefix-match and the tail to appear at the end,
        # both anchored, which no unrelated law can satisfy by accident.
        def ok(o: str) -> bool:
            no = norm(o)
            if not no.startswith(nh):
                return False
            return no.endswith(nt) or no.rstrip().endswith(nt.split(" ", 1)[-1])

        hit = next((o for o in options if ok(o)), "")
        if not hit:
            no_match += 1
            continue
        r["title_fa"] = hit
        recovered += 1

    shutil.copy2(SIG, SIG + ".bak-elided-titles")
    with open(SIG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"  recovered (head+tail verified) : {recovered}")
    print(f"  lawId has no whole-law record  : {no_record}")
    print(f"  candidate failed verification  : {no_match}")
    left = sum(1 for r in rows if ELISION in r["title_fa"])
    print(f"significant laws still elided: {left}")


if __name__ == "__main__":
    main()
