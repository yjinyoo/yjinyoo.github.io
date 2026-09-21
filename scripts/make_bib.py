"""Turn the curated OpenAlex record into the BibTeX file al-folio renders from.

The CV decides what is listed and how: each paper's number, year, volume and
pages, and equal first authorship come from the public CV PDF through
`cv_record.py`. OpenAlex supplies the rest (full author names, DOI, abstract,
open-access link). Every record must match exactly one CV entry and every CV
entry exactly one record, or nothing is written: the site and the CV once drifted
to 45 entries against 42 without anyone noticing.

The `abbr` field drives the badge in the left margin. It carries the CV's
publication number, not a journal abbreviation: the journal name is already
spelled out in the citation itself, so a venue badge was duplicate ink. The CV
numbers from the oldest paper, so a paper keeps its number when a new one is
published and the number at the top of the page is the total count.
"""

import json
import os

import cv_record
from fetch_pubs import tex_escape, invert_abstract, make_key

OUT = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(os.path.dirname(OUT), "_bibliography", "papers.bib")
ME = "Young Jin Yoo"

# On the CV but absent from OpenAlex, which does not index either venue.
# Year, volume and pages come from the CV like every other entry.
ADDITIONS = [
    {
        "authors": ["Joo Ho Yun", "Young Jin Yoo", "Hye Ryun Kim", "Young Min Song"],
        "title": "Recent progress in thermal management for flexible/wearable devices",
        "journal": "Soft Science", "doi": "10.20517/ss.2023.04",
        "pdf": "", "abstract": "", "type": "article", "cites": 0,
    },
    {
        "authors": ["Young Jin Yoo", "Young Min Song"],
        "title": "Editorial for the Topic on Micromachining for Advanced Biological Imaging",
        "journal": "Micromachines", "doi": "10.3390/mi13030474",
        "pdf": "", "abstract": "", "type": "article", "cites": 0,
    },
]

# Records where OpenAlex is behind the publisher. Keyed by the DOI OpenAlex has;
# the values replace the rendered fields outright.
OVERRIDES = {
    "10.21203/rs.3.rs-5801345/v1": {
        "authors": ["Joo Hwan Ko", "Hyo Eun Jeong", "Serim Kim", "Doeun Kim",
                    "Se Yeon Kim", "Young Jin Yoo", "Hyeon-Ho Jeong", "Young Min Song"],
        "title": "Sub-1-volt, reconfigurable Gires-Tournois resonators for full-coloured monopixel array",
        "journal": "Light: Science \\& Applications",
        "doi": "10.1038/s41377-026-02228-2",
        "pdf": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12949994/",
        "abstract": ("An electrically reconfigurable Gires-Tournois resonator integrated with "
                     "polyaniline produces colour shifts beyond complementary hue ranges at "
                     "sub-1-volt drive and 90 uW/cm2, scaling from ~16,900 PPI pixel densities "
                     "to centimetre-scale arrays, with memory-in-pixel operation."),
        "type": "article",
    },
    # OpenAlex has no source for the chapter; the CV lists it under Book Chapters.
    "10.4324/9781315153551-17": {
        "booktitle": "Silicon Nanomaterials Sourcebook",
        "publisher": "CRC Press",
        "pages": "373--396",
    },
}


def fields_for(w):
    """Flatten one OpenAlex work into the fields we render, overrides applied."""
    src = (w.get("primary_location") or {}).get("source") or {}
    oa = w.get("best_oa_location") or {}
    doi = (w.get("doi") or "").replace("https://doi.org/", "")

    f = {
        "authors": [a.get("author", {}).get("display_name", "")
                    for a in (w.get("authorships") or []) if a.get("author")],
        "title": w.get("title") or "",
        "journal": src.get("display_name") or "",
        "year": w.get("publication_year"),
        "doi": doi,
        "pdf": oa.get("pdf_url") or oa.get("landing_page_url") or "",
        "abstract": invert_abstract(w.get("abstract_inverted_index")),
        "type": w.get("type") or "article",
        "cites": w.get("cited_by_count") or 0,
    }
    f.update(OVERRIDES.get(doi, {}))
    return f


works = json.load(open(os.path.join(OUT, "works_mine.json"), encoding="utf-8"))
flat = [fields_for(w) for w in works] + [dict(a) for a in ADDITIONS]
papers = [f for f in flat if f["type"] != "book-chapter"]
chapters = [f for f in flat if f["type"] == "book-chapter"]

# ---- match every record to the CV, and the CV to every record ----
cv = cv_record.journals()
cv_chapters = cv_record.chapters()
problems, claimed = [], {}
for f in papers:
    hits = cv_record.find(cv, f["title"])
    if len(hits) != 1:
        problems.append(f"record matches {len(hits)} CV entries: {f['title'][:70]} ({f['doi']})")
        continue
    n = hits[0]["number"]
    if n in claimed:
        problems.append(f"CV #{n} matched by two records: {claimed[n]} and {f['doi']}")
    claimed[n] = f["doi"]
    f["cv"] = hits[0]
for e in cv:
    if e["number"] not in claimed:
        problems.append(f"CV #{e['number']} has no record (OpenAlex lacks it? add to ADDITIONS): "
                        f"{e['text'][:80]}")
for f in chapters:
    if not any(cv_record.compact(f["title"]) in cv_record.compact(c) for c in cv_chapters):
        problems.append(f"book chapter not on the CV: {f['title']} ({f['doi']})")
if len(chapters) != len(cv_chapters):
    problems.append(f"{len(chapters)} chapter records against {len(cv_chapters)} on the CV")
if problems:
    raise SystemExit("The publication record and the CV disagree; nothing written.\n  "
                     + "\n  ".join(problems))

for f in papers:
    e = f["cv"]
    f["year"] = cv_record.SITE_YEAR.get(f["doi"], e["year"])
    f["volume"], f["pages"], f["co_first"] = e["volume"], e["pages"], e["co_first"]
papers.sort(key=lambda f: f["cv"]["number"], reverse=True)

seen, entries, n_selected = set(), [], 0

for f in papers + chapters:
    is_paper = "cv" in f
    authors = f["authors"]
    first_author = bool(authors) and authors[0] == ME
    position = next((k + 1 for k, a in enumerate(authors) if a == ME), len(authors))
    top_venue = f["journal"].startswith(("Nature", "Light"))
    selected = is_paper and ((first_author and f["cites"] >= 20)
                             or (top_venue and position <= 6)
                             or f["cites"] >= 200)
    n_selected += bool(selected)

    key = make_key({"authorships": [{"author": {"display_name": a}} for a in authors],
                    "publication_year": f["year"], "title": f["title"]}, seen)

    rows = []
    if is_paper:
        # The layout renders "<journal>, <year>" and nothing for volume, number or
        # pages. additional_info is the only slot in between, but it is run through
        # markdownify, which eats the leading space and leaves a trailing newline
        # ("Nature Electronics9, 853-867 , 2026"). So the locator is carried in the
        # journal string, and the separate fields are dropped rather than repeated,
        # which would make a reference manager print the volume twice.
        journal = f["journal"] if "\\&" in f["journal"] else tex_escape(f["journal"])
        if f["volume"]:                       # none yet while online ahead of print
            journal = f"{journal} {f['volume']}, {f['pages']}"
        rows += [("abbr", str(f["cv"]["number"])),
                 ("author", " and ".join(authors)),
                 ("title", tex_escape(f["title"])),
                 ("journal", journal)]
    else:
        rows += [("author", " and ".join(authors)),
                 ("title", tex_escape(f["title"])),
                 ("booktitle", f["booktitle"]),
                 ("publisher", f["publisher"]),
                 ("pages", f["pages"])]
    rows += [
        ("year", str(f["year"] or "")),
        ("doi", f["doi"]),
        ("url", f"https://doi.org/{f['doi']}" if f["doi"] else ""),
        ("abstract", tex_escape(f["abstract"])),
    ]
    if is_paper and f["co_first"]:
        # `note` gets its own line in the theme's entry layout; `additional_info`
        # is appended to the journal name and reads as part of the venue.
        rows.append(("note", "Equal first-author contribution"))
    if f["pdf"]:
        rows.append(("pdf", f["pdf"]))          # a free copy, never the publisher PDF
    rows.append(("bibtex_show", "true"))
    if selected:
        rows.append(("selected", "true"))

    body = "\n".join(f"  {k:<12}= {{{v}}}," for k, v in rows if v)
    kind = "article" if is_paper else "incollection"
    entries.append(f"@{kind}{{{key},\n{body}\n}}")

header = ("% Publication record for Young Jin Yoo (ORCID 0000-0002-6490-2324).\n"
          "% Numbers, years, volumes and pages from the CV (assets/pdf/cv.pdf);\n"
          "% authors, DOIs and abstracts from OpenAlex. Regenerate with\n"
          "% scripts/update_publications.py, never by hand.\n\n")
with open(BIB, "w", encoding="utf-8") as fh:
    fh.write(header + "\n\n".join(entries) + "\n")

print(f"wrote {len(papers)} papers numbered {len(papers)} down to 1 as on the CV, "
      f"{len(chapters)} book chapter(s), {n_selected} marked selected")
print(f"equal first author: {sum(f['co_first'] for f in papers)}   "
      f"open access copies linked: {sum(1 for f in papers + chapters if f['pdf'])}")
