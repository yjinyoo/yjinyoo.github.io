"""Check that the site says what the CV says.

    python scripts/check_cv_match.py

Compares files in the repository against the public CV (assets/pdf/cv.pdf):

  publications  _bibliography/papers.bib: the paper count, each number's title,
                year, volume and pages, equal first authorship, book chapters
  cv page       _pages/cv.md: positions, degrees, fellowships and awards
  research page _pages/research.md "Funded projects": the MIT-era projects

Dated items are paired by their dates and then by name, one to one, in both
directions: an item on the site that the CV lacks fails, and so does a CV item
the site lacks. Wording on the pages is free; dates, names and membership are
not. The only departures accepted are the ones declared in cv_record
(SITE_YEAR, SITE_PROJECTS_FROM).

make_bib.py refuses to write a list that disagrees with the CV, so the list can
only drift when one side is rebuilt without the other. The pages are written by
hand, so they drift whenever either side is edited alone. Exits 1 on any
disagreement and prints each one.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_record  # noqa: E402

BIB = os.path.join(cv_record.SITE, "_bibliography", "papers.bib")
PAGES = os.path.join(cv_record.SITE, "_pages")

# (CV section, page, headings on that page that hold its items)
DATED_PAGES = [
    ("positions", "cv.md", ["Positions"]),
    ("education", "cv.md", ["Education"]),
    ("honors", "cv.md", ["Fellowships", "Awards"]),
    ("projects", "research.md", ["Funded projects"]),
]
MIN_NAME_OVERLAP = 0.6   # share of an item's significant words found in its CV entry
# On the CV the name, institution or title sits just before the date; what follows
# the date (funding, advisor, role) belongs to that item but lands in the next
# item's context. So names are compared against the text just before the date.
CONTEXT_TAIL = 300


def page_items(page, headings):
    """Items under the given '## ' headings: '#### ' blocks or '- **' bullets.
    Name = the first line without markup; dates = the first found in the block."""
    text = open(os.path.join(PAGES, page), encoding="utf-8").read()
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    items = []
    for title, body in zip(parts[1::2], parts[2::2]):
        if title.strip() not in headings:
            continue
        for block in re.split(r"(?m)^(?=#### |- \*\*)", body):
            block = block.strip()
            if not block.startswith(("#### ", "- **")):
                continue
            name = re.sub(r"[#*]", "", block.splitlines()[0]).strip()
            dates = cv_record.dates_in(" ".join(block.split()))
            items.append({"name": name,
                          "start": dates[0][0] if dates else None,
                          "end": dates[0][1] if dates else None})
    return items


def check_dated(bad):
    for section, page, headings in DATED_PAGES:
        cv_items = cv_record.section_items(section)
        if section == "projects":
            cv_items = [c for c in cv_items if c["start"] >= cv_record.SITE_PROJECTS_FROM]
        if section == "education":
            cv_items = [c for c in cv_items if c["start"] >= cv_record.SITE_EDUCATION_FROM]
        site = page_items(page, headings)
        used = set()
        for s in site:
            label = f"{page} [{'/'.join(headings)}] {s['name'][:60]!r}"
            if s["start"] is None:
                bad.append(f"{label}: no date on the site")
                continue
            cands = [(cv_record.overlap(s["name"], c["context"][-CONTEXT_TAIL:]), i)
                     for i, c in enumerate(cv_items)
                     if (c["start"], c["end"]) == (s["start"], s["end"]) and i not in used]
            best = max(cands, default=(0.0, None))
            if best[1] is None or best[0] < MIN_NAME_OVERLAP:
                near = [cv_record.fmt(c["start"], c["end"]) for c in cv_items
                        if cv_record.overlap(s["name"], c["context"][-CONTEXT_TAIL:]) >= MIN_NAME_OVERLAP]
                bad.append(f"{label} {cv_record.fmt(s['start'], s['end'])}: not on the CV"
                           + (f" with these dates (CV has it as {', '.join(near)})" if near else ""))
                continue
            used.add(best[1])
        for i, c in enumerate(cv_items):
            if i not in used:
                bad.append(f"CV {section} {cv_record.fmt(c['start'], c['end'])}: not on {page} "
                           f"(...{c['context'][-90:]})")


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

    try:
        check_dated(bad)
    except ValueError as err:          # a CV heading renamed or missing
        bad.append(f"CV cannot be read for the cv/research pages: {err}")

    if bad:
        print(f"CV and site disagree ({len(bad)}):")
        for b in bad:
            print("  " + b)
        print("The CV is the source. If the CV is right, fix the page (cv.md, research.md) "
              "or rerun scripts/sync_cv.py; if the site is right, fix the CV first.")
        return 1
    counts = ", ".join(f"{len(page_items(p, h))} {s}" for s, p, h in DATED_PAGES)
    print(f"OK: {len(papers)} papers, {len(chapters)} chapter(s), {counts} match the CV "
          f"(declared departures: {len(cv_record.SITE_YEAR)} year, "
          f"projects from {cv_record.SITE_PROJECTS_FROM[0]}-{cv_record.SITE_PROJECTS_FROM[1]:02d}, "
          f"degrees from {cv_record.SITE_EDUCATION_FROM[0]}-{cv_record.SITE_EDUCATION_FROM[1]:02d})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
