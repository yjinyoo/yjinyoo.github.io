"""Turn the curated OpenAlex record into the BibTeX file al-folio renders from.

The `abbr` field drives the badge in the left margin. It carries a publication
number, not a journal abbreviation: the journal name is already spelled out in
the citation itself, so a venue badge was duplicate ink. Numbering runs from the
oldest paper, so a paper keeps its number when a new one is published and the
number at the top of the page is the total count.
"""

import json
import os

from fetch_pubs import tex_escape, invert_abstract, make_key

OUT = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(os.path.dirname(OUT), "_bibliography", "papers.bib")
ME = "Young Jin Yoo"

# Records where OpenAlex is behind the publisher. Keyed by the DOI OpenAlex has.
# Values replace the rendered fields outright.
OVERRIDES = {
    "10.21203/rs.3.rs-5801345/v1": {
        "authors": ["Joo Hwan Ko", "Hyo Eun Jeong", "Serim Kim", "Doeun Kim",
                    "Se Yeon Kim", "Young Jin Yoo", "Hyeon-Ho Jeong", "Young Min Song"],
        "title": "Sub-1-volt, reconfigurable Gires-Tournois resonators for full-coloured monopixel array",
        "journal": "Light: Science \\& Applications",
        "year": 2026,
        "volume": "15",
        "number": "134",
        "doi": "10.1038/s41377-026-02228-2",
        "pdf": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12949994/",
        "abstract": ("An electrically reconfigurable Gires-Tournois resonator integrated with "
                     "polyaniline produces colour shifts beyond complementary hue ranges at "
                     "sub-1-volt drive and 90 uW/cm2, scaling from ~16,900 PPI pixel densities "
                     "to centimetre-scale arrays, with memory-in-pixel operation."),
        "type": "article",
    },
}


def fields_for(w):
    """Flatten one OpenAlex work into the fields we render, overrides applied."""
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    biblio = w.get("biblio") or {}
    oa = w.get("best_oa_location") or {}
    doi = (w.get("doi") or "").replace("https://doi.org/", "")

    f = {
        "authors": [a.get("author", {}).get("display_name", "")
                    for a in (w.get("authorships") or []) if a.get("author")],
        "title": w.get("title") or "",
        "journal": src.get("display_name") or "",
        "year": w.get("publication_year"),
        "volume": biblio.get("volume") or "",
        "number": biblio.get("issue") or "",
        "pages": "--".join(p for p in [biblio.get("first_page"), biblio.get("last_page")] if p),
        "doi": doi,
        "pdf": oa.get("pdf_url") or oa.get("landing_page_url") or "",
        "abstract": invert_abstract(w.get("abstract_inverted_index")),
        "type": w.get("type") or "article",
        "cites": w.get("cited_by_count") or 0,
    }
    f.update(OVERRIDES.get(doi, {}))
    return f


works = json.load(open(os.path.join(OUT, "works_mine.json"), encoding="utf-8"))
flat = [fields_for(w) for w in works]
flat.sort(key=lambda f: (f["year"] or 0, f["cites"]), reverse=True)

total = len(flat)
seen, entries, n_selected = set(), [], 0

for i, f in enumerate(flat):
    number = total - i                       # oldest paper is 1
    authors = f["authors"]
    first_author = bool(authors) and authors[0] == ME
    position = next((k + 1 for k, a in enumerate(authors) if a == ME), len(authors))
    top_venue = f["journal"].startswith(("Nature", "Light"))
    selected = ((first_author and f["cites"] >= 20)
                or (top_venue and position <= 6)
                or f["cites"] >= 200)
    n_selected += bool(selected)

    key = make_key({"authorships": [{"author": {"display_name": a}} for a in authors],
                    "publication_year": f["year"], "title": f["title"]}, seen)

    rows = [
        ("abbr", str(number)),
        ("author", " and ".join(authors)),
        ("title", tex_escape(f["title"])),
        ("journal", f["journal"] if "\\&" in f["journal"] else tex_escape(f["journal"])),
        ("year", str(f["year"] or "")),
        ("volume", f["volume"]),
        ("number", f["number"]),
        ("pages", f["pages"]),
        ("doi", f["doi"]),
        ("url", f"https://doi.org/{f['doi']}" if f["doi"] else ""),
        ("abstract", tex_escape(f["abstract"])),
    ]
    if f["pdf"]:
        rows.append(("pdf", f["pdf"]))          # a free copy, never the publisher PDF
    rows.append(("bibtex_show", "true"))
    if selected:
        rows.append(("selected", "true"))

    body = "\n".join(f"  {k:<12}= {{{v}}}," for k, v in rows if v)
    kind = "misc" if f["type"] == "preprint" else "article"
    entries.append(f"@{kind}{{{key},\n{body}\n}}")

header = ("% Publication record for Young Jin Yoo (ORCID 0000-0002-6490-2324).\n"
          "% Generated from OpenAlex; regenerate with scripts/update_publications.py.\n"
          "% 'abbr' is the publication number, counted from the oldest paper.\n\n")
with open(BIB, "w", encoding="utf-8") as f:
    f.write(header + "\n\n".join(entries) + "\n")

print(f"wrote {total} entries, numbered {total} down to 1, {n_selected} marked selected")
print(f"open access copies linked: {sum(1 for f in flat if f['pdf'])} / {total}")
