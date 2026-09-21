"""The publication record as the CV states it, read from the public CV PDF.

The CV is the one source for what counts as a paper, its number, its year, its
volume and pages, and equal first authorship. The site is generated from it
(`make_bib.py`) and checked against it (`check_cv_match.py`). Bibliographic
databases only supply what the CV does not carry: full author names, DOIs,
abstracts and open-access links.

Reading the PDF rather than keeping a copy of the list here is deliberate: a
copied list goes stale silently, and the two drifted apart once already (the
site had 45 entries against the CV's 42 on 2026-09-21).
"""

import os
import re
import unicodedata

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CV_PDF = os.path.join(SITE, "assets", "pdf", "cv.pdf")

# The only places the site departs from the CV on purpose.
# Sub-1-volt is shown as 2025 at the author's instruction (2026-09-19), knowing
# that Crossref and the CV both say 2026 (volume 15). One line to undo.
SITE_YEAR = {
    "10.1038/s41377-026-02228-2": 2025,
}

# "43. B. Kim, ... (2026). Co-first author" -> volume, pages, year at the end
LOCATOR = re.compile(r"(\d+),\s*([A-Za-z]?\d+(?:[–—−-]\d+)?)\s*\((\d{4})\)")


def compact(s):
    """Title key that survives hyphenation, case, markup and dash variants."""
    s = re.sub(r"<[^>]+>", "", s or "")
    s = unicodedata.normalize("NFKD", s).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def _text():
    import fitz  # PyMuPDF
    doc = fitz.open(CV_PDF)
    return "\n".join(page.get_text() for page in doc)


def _section(text, head, stop):
    up = text.upper()
    i = up.index(head)
    j = up.index(stop, i)
    body = text[text.index("\n", i):j]
    # entries are separated by blank lines; a line broken after a hyphen joins tight
    blocks = re.split(r"\n\s*\n", body)
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


if __name__ == "__main__":
    js = journals()
    print(f"{len(js)} journal entries, {sum(e['co_first'] for e in js)} co-first")
    for e in js:
        print(f"  {e['number']:>3}  {e['year']}  {e['volume']}, {e['pages']}")
    print("chapters:", chapters())
