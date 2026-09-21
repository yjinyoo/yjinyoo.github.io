"""Check that the publication list on the site says what the CV says.

    python scripts/check_cv_match.py

Compares the two files in the repository, assets/pdf/cv.pdf and
_bibliography/papers.bib: the paper count, each number's title, year, volume and
pages, equal first authorship, and the book chapters. The only departures it
accepts are the ones declared in cv_record.SITE_YEAR.

make_bib.py refuses to write a list that disagrees with the CV, so the two can only
drift when one side is rebuilt without the other: a new CV PDF without rerunning
update_publications.py, or the reverse. That is what this catches. It exits 1 on
any disagreement and prints each one.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_record  # noqa: E402

BIB = os.path.join(cv_record.SITE, "_bibliography", "papers.bib")


def bib_entries():
    text = open(BIB, encoding="utf-8").read()
    out = []
    for kind, key, body in re.findall(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        fields = dict(re.findall(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", body, re.M))
        out.append({"kind": kind, "key": key, **fields})
    return out


def main():
    try:
        cv = cv_record.journals()
        cv_chapters = cv_record.chapters()
    except ValueError as err:          # e.g. an entry with no year, numbering gaps
        print(f"CV cannot be read as a publication list: {err}")
        return 1
    entries = bib_entries()
    papers = [e for e in entries if e["kind"] == "article"]
    chapters = [e for e in entries if e["kind"] == "incollection"]
    others = [e for e in entries if e["kind"] not in ("article", "incollection")]
    bad = []

    if len(papers) != len(cv):
        bad.append(f"count: site lists {len(papers)} papers, CV lists {len(cv)}")
    numbers = sorted(int(e.get("abbr", 0)) for e in papers)
    if numbers != list(range(1, len(papers) + 1)):
        bad.append(f"site numbers are not 1..{len(papers)}: {numbers}")
    for e in others:
        bad.append(f"entry of type @{e['kind']} is neither a paper nor a chapter: {e['key']}")

    by_number = {e["number"]: e for e in cv}
    for e in papers:
        n = int(e.get("abbr", 0))
        c = by_number.get(n)
        if c is None:
            bad.append(f"#{n} {e['key']}: no such number on the CV")
            continue
        label = f"#{n} {e['key']}"
        if cv_record.compact(e.get("title", "")) not in cv_record.compact(c["text"]):
            bad.append(f"{label}: title not in CV #{n} ({e.get('title', '')[:60]!r})")
        want_year = cv_record.SITE_YEAR.get(e.get("doi", ""), c["year"])
        if str(want_year) != e.get("year", ""):
            bad.append(f"{label}: year {e.get('year')} on the site, {c['year']} on the CV")
        locator = f"{c['volume']}, {c['pages']}" if c["volume"] else ""
        if locator and not e.get("journal", "").endswith(locator):
            bad.append(f"{label}: '{e.get('journal')}' does not end with the CV's '{locator}'")
        if bool(e.get("note")) != c["co_first"]:
            bad.append(f"{label}: equal first authorship is "
                       f"{'marked' if e.get('note') else 'unmarked'} on the site, "
                       f"{'marked' if c['co_first'] else 'unmarked'} on the CV")

    if len(chapters) != len(cv_chapters):
        bad.append(f"chapters: site lists {len(chapters)}, CV lists {len(cv_chapters)}")
    for e in chapters:
        if not any(cv_record.compact(e.get("title", "")) in cv_record.compact(c)
                   for c in cv_chapters):
            bad.append(f"chapter {e['key']}: not under Book Chapters on the CV")

    if bad:
        print(f"CV and site disagree ({len(bad)}):")
        for b in bad:
            print("  " + b)
        print("Rebuild whichever side is stale: scripts/build_public_cv.py for the CV, "
              "scripts/update_publications.py for the list.")
        return 1
    print(f"OK: {len(papers)} papers and {len(chapters)} chapter(s) match the CV "
          f"(declared departures: {len(cv_record.SITE_YEAR)} year)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
