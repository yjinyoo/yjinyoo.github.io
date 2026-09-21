"""The record as the CV states it, read from the public CV PDF.

The CV is the one source for everything the site states about the record:
which papers count, their numbers, years, volumes, pages and equal first
authorship; and the dated items on the cv and research pages (positions,
degrees, fellowships and awards, funded projects). The publication list is
generated from it (`make_bib.py`); the hand-written pages are checked against it
(`check_cv_match.py`). Bibliographic databases only supply what the CV does not
carry: full author names, DOIs, abstracts and open-access links.

Reading the PDF rather than keeping a copy here is deliberate: a copied list goes
stale silently. On 2026-09-21 the site had 45 papers against the CV's 42, and a
funded project on the research page that the CV did not have.
"""

import os
import re
import unicodedata

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CV_PDF = os.path.join(SITE, "assets", "pdf", "cv.pdf")

# ---- the only places the site departs from the CV on purpose ----
# Sub-1-volt is shown as 2025 at the author's instruction (2026-09-19), knowing
# that Crossref and the CV both say 2026 (volume 15). One line to undo.
SITE_YEAR = {
    "10.1038/s41377-026-02228-2": 2025,
}
# The research page lists the funded projects of the MIT appointment, not the
# GIST-era ones, which stay on the CV only. (year, month) of the first included start.
SITE_PROJECTS_FROM = (2023, 3)
# The cv page lists graduate degrees only; the B.S. stays on the CV. Author's
# instruction 2026-09-21, after an agent added the B.S. to the site unasked to
# make this check pass. (year, month) of the first included start: the M.S.
SITE_EDUCATION_FROM = (2016, 9)

# "43. B. Kim, ... (2026). Co-first author" -> volume, pages, year at the end
LOCATOR = re.compile(r"(\d+),\s*([A-Za-z]?\d+(?:[–—−-]\d+)?)\s*\((\d{4})\)")

MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
_MON = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?"
_DATE = rf"(?:\d{{1,2}}\s+)?{_MON}\s+(\d{{4}})"
# CV: "Mar. 2023 ~ Present", "(Mar. 2021 – Feb. 2024)", "Feb. 2026 - present", "(11 Feb. 2020)"
# site: "Mar 2023 to present", "Feb 2020"
DATED = re.compile(
    rf"{_DATE}\s*(?:~|–|—|-|to)\s*(?:{_DATE}|(present))|\(\s*{_DATE}\s*\)|{_DATE}",
    re.I)

STOP = {"the", "and", "for", "with", "from", "into", "onto", "based", "development",
        "korea", "prof", "award", "awards"}


def compact(s):
    """Title key that survives hyphenation, case, markup and dash variants."""
    s = re.sub(r"<[^>]+>", "", s or "")
    s = unicodedata.normalize("NFKD", s).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def words(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    return {w for w in re.findall(r"[a-z0-9]+", s) if len(w) >= 3 and w not in STOP}


def overlap(name, context):
    """Share of the significant words of `name` that appear in `context`."""
    w = words(name)
    return len(w & words(context)) / len(w) if w else 0.0


def _text():
    import fitz  # PyMuPDF
    doc = fitz.open(CV_PDF)
    return "\n".join(page.get_text() for page in doc)


def _section_body(text, head, stop):
    """Text between two CV headings ('ARCHIVAL JOURNALS ____', 'BOOK CHAPTERS____')."""
    def at(h, start=0):
        # headings may carry a qualifier: "PROCEEDINGS AND PRESENTATIONS (INTERNATIONAL)___"
        m = re.compile(rf"^\s*{h}[^_\n]*_{{3,}}", re.M).search(text.upper(), start)
        if not m:
            raise ValueError(f"CV heading not found: {h}")
        return m
    i = at(head)
    j = at(stop, i.end())
    return text[i.end():j.start()]


def _section(text, head, stop):
    # entries are separated by blank lines; a line broken after a hyphen joins tight
    blocks = re.split(r"\n\s*\n", _section_body(text, head, stop))
    out = []
    for b in blocks:
        lines = [ln.strip() for ln in b.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        joined = lines[0]
        for ln in lines[1:]:
            joined += ln if joined.endswith("-") else " " + ln
        out.append(joined)
    return out


def journals():
    """Archival journal entries, oldest first, as dicts."""
    entries = []
    for block in _section(_text(), "ARCHIVAL JOURNALS", "RESEARCH PROJECTS"):
        m = re.match(r"(\d{1,3})\.\s+(.*)", block)
        if not m:
            raise ValueError(f"unnumbered block in ARCHIVAL JOURNALS: {block[:80]!r}")
        text = m.group(2)
        loc = LOCATOR.findall(text)
        if loc:
            volume, pages, year = loc[-1]
        else:
            # online ahead of print: "Nat. Electron. (2026)", no volume or pages yet
            years = re.findall(r"\((\d{4})\)", text)
            if not years:
                raise ValueError(f"CV #{m.group(1)} has no year: {text[-80:]!r}")
            volume, pages, year = "", "", years[-1]
        entries.append({
            "number": int(m.group(1)),
            "text": text,
            "volume": volume,
            "pages": re.sub(r"[—−-]", "–", pages),
            "year": int(year),
            "co_first": "Co-first author" in text,
        })
    entries.sort(key=lambda e: e["number"])
    numbers = [e["number"] for e in entries]
    if numbers != list(range(1, len(entries) + 1)):
        raise ValueError(f"CV numbering is not 1..N: {numbers}")
    return entries


def chapters():
    """Book chapter entries as plain text (the CV lists the book, then chapters)."""
    blocks = _section(_text(), "BOOK CHAPTERS", "ACADEMIC SERVICES")
    return [b for b in blocks if b.lower().startswith("chapter")]


def find(entries, title):
    """The CV entries whose text contains this title."""
    key = compact(title)
    return [e for e in entries if key and key in compact(e["text"])]


# ---- dated items: positions, degrees, fellowships and awards, projects ----

def _ym(mon, year):
    return (int(year), MONTHS[mon.lower()[:3]])


def dates_in(text):
    """Every date or date range in `text`, in order: (start, end, match).
    `end` is None for 'present', equal to `start` for a single date."""
    out = []
    for m in DATED.finditer(text):
        g = m.groups()
        if g[0]:                                    # range
            start = _ym(g[0], g[1])
            end = None if g[4] else _ym(g[2], g[3])
        elif g[5]:                                  # "(11 Feb. 2020)"
            start = end = _ym(g[5], g[6])
        else:                                       # bare "Feb 2020"
            start = end = _ym(g[7], g[8])
        out.append((start, end, m))
    return out


def dated_items(head, stop):
    """Items of one CV section, split at their dates. Each item's context is the
    text since the previous date, which holds its name, institution or title."""
    body = " ".join(_section_body(_text(), head, stop).split())
    items, prev = [], 0
    for start, end, m in dates_in(body):
        items.append({"start": start, "end": end, "context": body[prev:m.end()]})
        prev = m.end()
    return items


SECTIONS = {
    # key: (CV heading, next CV heading)
    "positions": ("WORK EXPERIENCE", "EDUCATION"),
    "education": ("EDUCATION", "AWARDS AND FELLOWSHIPS"),
    "honors": ("AWARDS AND FELLOWSHIPS", "ARCHIVAL JOURNALS"),
    "projects": ("RESEARCH PROJECTS", "PROCEEDINGS AND PRESENTATIONS"),
}


def section_items(key):
    return dated_items(*SECTIONS[key])


def fmt(start, end):
    s = f"{start[0]}-{start[1]:02d}"
    if end == start:
        return s
    return f"{s} to " + ("present" if end is None else f"{end[0]}-{end[1]:02d}")


if __name__ == "__main__":
    js = journals()
    print(f"{len(js)} journal entries, {sum(e['co_first'] for e in js)} co-first")
    print("chapters:", len(chapters()))
    for key in SECTIONS:
        items = section_items(key)
        print(f"{key}: {len(items)}")
        for it in items:
            print(f"   {fmt(it['start'], it['end']):<22} {it['context'][:70]}")
