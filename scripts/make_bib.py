"""Turn the curated OpenAlex record into the BibTeX file al-folio renders from."""

import json
import os
import re

from fetch_pubs import tex_escape, invert_abstract, make_key

OUT = os.path.dirname(os.path.abspath(__file__))
works = json.load(open(os.path.join(OUT, "works_mine.json"), encoding="utf-8"))

ME = "Young Jin Yoo"

# Badge text shown in the left margin of each entry.
ABBR = {
    "Nature Electronics": "Nat. Electron.",
    "Nature Nanotechnology": "Nat. Nanotech.",
    "Nature Communications": "Nat. Commun.",
    "Advanced Materials": "Adv. Mater.",
    "Advanced Optical Materials": "Adv. Opt. Mater.",
    "Advanced Functional Materials": "Adv. Funct. Mater.",
    "Advanced Science": "Adv. Sci.",
    "Advanced Healthcare Materials": "Adv. Healthc. Mater.",
    "ACS Nano": "ACS Nano",
    "ACS Applied Materials & Interfaces": "ACS AMI",
    "ACS Applied Nano Materials": "ACS ANM",
    "ACS Energy Letters": "ACS Energy Lett.",
    "Optics Express": "Opt. Express",
    "Optical Materials Express": "Opt. Mater. Express",
    "Optical and Quantum Electronics": "Opt. Quantum Electron.",
    "Nanophotonics": "Nanophotonics",
    "Nanoscale": "Nanoscale",
    "Nano Today": "Nano Today",
    "Nano Research": "Nano Res.",
    "Scientific Reports": "Sci. Rep.",
    "Biosensors and Bioelectronics": "Biosens. Bioelectron.",
    "iScience": "iScience",
    "Sensors": "Sensors",
    "Nanomaterials": "Nanomaterials",
    "Coatings": "Coatings",
    "Journal of Nanomaterials": "J. Nanomater.",
    "Journal of Visualized Experiments": "JoVE",
    "Applied Spectroscopy Reviews": "Appl. Spectrosc. Rev.",
    "Research Square": "preprint",
    "SSRN Electronic Journal": "preprint",
}

entries, seen = [], set()
n_selected = 0

for w in works:
    key = make_key(w, seen)
    authors = [a.get("author", {}).get("display_name", "")
               for a in (w.get("authorships") or [])]
    authors = [a for a in authors if a]
    first_author = bool(authors) and authors[0] == ME

    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    venue = src.get("display_name") or ""
    biblio = w.get("biblio") or {}
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    oa = w.get("best_oa_location") or {}
    oa_url = oa.get("pdf_url") or oa.get("landing_page_url") or ""
    cites = w.get("cited_by_count") or 0
    is_preprint = (w.get("type") == "preprint") or venue in ("Research Square",
                                                             "SSRN Electronic Journal")

    # Front-page highlights: own first-author papers that landed, plus the
    # high-visibility group papers.
    selected = (first_author and cites >= 20) or cites >= 100 or venue.startswith("Nature")
    if selected:
        n_selected += 1

    fields = [
        ("abbr", ABBR.get(venue, "")),
        ("author", " and ".join(authors)),
        ("title", tex_escape(w.get("title"))),
        ("journal", tex_escape(venue)),
        ("year", str(w.get("publication_year") or "")),
        ("volume", biblio.get("volume") or ""),
        ("number", biblio.get("issue") or ""),
        ("pages", "--".join(p for p in [biblio.get("first_page"),
                                        biblio.get("last_page")] if p)),
        ("doi", doi),
        ("url", f"https://doi.org/{doi}" if doi else (loc.get("landing_page_url") or "")),
        ("abstract", tex_escape(invert_abstract(w.get("abstract_inverted_index")))),
    ]
    if oa_url:
        fields.append(("pdf", oa_url))          # free-to-read copy, not the publisher PDF
    fields.append(("bibtex_show", "true"))
    if selected:
        fields.append(("selected", "true"))

    body = "\n".join(f"  {k:<12}= {{{v}}}," for k, v in fields if v)
    entries.append(f"@{'misc' if is_preprint else 'article'}{{{key},\n{body}\n}}")

header = (
    "---\n"
    "# Publication record for Young Jin Yoo (ORCID 0000-0002-6490-2324).\n"
    "# Generated from OpenAlex; regenerate with scripts/make_bib.py.\n"
    "# 'selected' marks the papers shown on the front page.\n"
    "---\n\n"
)
BIB = os.path.join(os.path.dirname(OUT), "_bibliography", "papers.bib")
with open(BIB, "w", encoding="utf-8") as f:
    f.write(header.replace("---\n", "").replace("# ", "% ") + "\n\n".join(entries) + "\n")

print(f"wrote {len(entries)} entries, {n_selected} marked selected")

# Which papers can legally be self-hosted right now, per OpenAlex OA status
oa_yes = [w for w in works if (w.get("best_oa_location") or {})]
print(f"already open access (free copy exists) : {len(oa_yes)} / {len(works)}")
print(f"closed access (link to DOI only)       : {len(works) - len(oa_yes)}")
