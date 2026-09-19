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

# Equal first authorship, taken from the CV. No bibliographic database records
# it, so it can only come from there: OpenAlex and Crossref both give author
# order and nothing about contribution.
CO_FIRST = {
    "10.1038/s41928-026-01681-6",   # Nat. Electron. 2026, co-packaged optics
    "10.1002/advs.202304310",       # Adv. Sci. 2023, Fano resonance
    "10.1016/j.nantod.2023.101968", # Nano Today 2023, DeepGT
    "10.1002/adhm.202301104",       # Adv. Healthc. Mater. 2023, outdoor worker
    "10.20517/ss.2023.04",          # Soft Sci. 2023, thermal management
    "10.3390/nano13020319",         # Nanomaterials 2023, trilayered GT
    "10.1016/j.isci.2022.104727",   # iScience 2022, tunable photonics
    "10.3390/s22093455",            # Sensors 2022, light-field camera
    "10.1038/s41467-022-29602-z",   # Nat. Commun. 2022, perovskite microcells
    "10.1515/nanoph-2020-0062",     # Nanophotonics 2020, mechanotunable filters
    "10.1002/adfm.201908592",       # Adv. Funct. Mater. 2020, covert polarization
    "10.1364/ome.9.003342",         # Opt. Mater. Express 2019, sRGB
    "10.1155/2017/2738015",         # J. Nanomater. 2017, porous ZnO/TiO2
    "10.1364/oe.24.0a1033",         # Opt. Express 2016, nanophotonic surfaces
}

# Year as the author lists it, where it differs from the publisher record.
# Crossref gives this paper 2026-02-28 in every date field (created, issued,
# published, published-online) and the CV says 2026, but it is listed as 2025
# elsewhere, so the author's year is used here.
YEAR_OVERRIDE = {
    "10.1038/s41377-026-02228-2": 2025,
}

# On the CV but absent from OpenAlex, which does not index either venue.
ADDITIONS = [
    {
        "authors": ["Joo Ho Yun", "Young Jin Yoo", "Hye Ryun Kim", "Young Min Song"],
        "title": "Recent progress in thermal management for flexible/wearable devices",
        "journal": "Soft Science", "year": 2023, "volume": "3", "number": "12",
        "doi": "10.20517/ss.2023.04", "pages": "", "pdf": "", "abstract": "",
        "type": "article", "cites": 0,
    },
    {
        "authors": ["Young Jin Yoo", "Young Min Song"],
        "title": "Editorial for the Topic on Micromachining for Advanced Biological Imaging",
        "journal": "Micromachines", "year": 2022, "volume": "13", "number": "474",
        "doi": "10.3390/mi13030474", "pages": "", "pdf": "", "abstract": "",
        "type": "article", "cites": 0,
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
        # Journals that number articles rather than paginate report the same
        # value as first and last page; print it once.
        "pages": "--".join(dict.fromkeys(
            p for p in [biblio.get("first_page"), biblio.get("last_page")] if p)),
        "doi": doi,
        "pdf": oa.get("pdf_url") or oa.get("landing_page_url") or "",
        "abstract": invert_abstract(w.get("abstract_inverted_index")),
        "type": w.get("type") or "article",
        "cites": w.get("cited_by_count") or 0,
    }
    f.update(OVERRIDES.get(doi, {}))
    if f["doi"] in YEAR_OVERRIDE:
        f["year"] = YEAR_OVERRIDE[f["doi"]]
    return f


works = json.load(open(os.path.join(OUT, "works_mine.json"), encoding="utf-8"))
flat = [fields_for(w) for w in works] + ADDITIONS
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

    # The layout renders "<journal>, <year>" and nothing for volume, number or
    # pages. additional_info is the only slot in between, but it is run through
    # markdownify, which eats the leading space and leaves a trailing newline
    # ("Nature Electronics9, 853-867 , 2026"). So the locator is carried in the
    # journal string, and the separate fields are dropped rather than repeated,
    # which would make a reference manager print the volume twice.
    journal = f["journal"] if "\\&" in f["journal"] else tex_escape(f["journal"])
    vol, num = f["volume"], f["number"]
    pages = f["pages"].replace("--", "–")
    if vol and pages:
        journal = f"{journal} {vol}, {pages}"
    elif vol and num:
        journal = f"{journal} {vol}, {num}"   # article number, not a page range
    elif vol:
        journal = f"{journal} {vol}"

    rows = [
        ("abbr", str(number)),
        ("author", " and ".join(authors)),
        ("title", tex_escape(f["title"])),
        ("journal", journal),
        ("year", str(f["year"] or "")),
        ("doi", f["doi"]),
        ("url", f"https://doi.org/{f['doi']}" if f["doi"] else ""),
        ("abstract", tex_escape(f["abstract"])),
    ]
    if f["doi"] in CO_FIRST:
        # `note` gets its own line in the theme's entry layout; `additional_info`
        # is appended to the journal name and reads as part of the venue.
        rows.append(("note", "Equal first-author contribution"))
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
