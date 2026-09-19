"""Fetch the OpenAlex publication record for Young Jin Yoo (MIT) and emit BibTeX.

Writes:
  works_raw.json  - full OpenAlex payload, kept so we never re-query while editing
  papers.bib      - al-folio style BibTeX
  summary.tsv     - one line per work for human review (year, venue, OA, title)
"""

import json
import urllib.request
import urllib.parse
import re
import os

AUTHOR_ID = "A5009098108"
MAILTO = "yjyoo@mit.edu"
OUT = os.path.dirname(os.path.abspath(__file__))


def fetch_all():
    works, cursor = [], "*"
    while cursor:
        params = urllib.parse.urlencode({
            "filter": f"author.id:{AUTHOR_ID}",
            "per-page": 200,
            "cursor": cursor,
            "mailto": MAILTO,
        })
        url = f"https://api.openalex.org/works?{params}"
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        works.extend(data["results"])
        cursor = data["meta"].get("next_cursor")
        if not data["results"]:
            break
    return works


def invert_abstract(inv):
    """OpenAlex stores abstracts as an inverted index; rebuild the text."""
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def tex_escape(s):
    if not s:
        return ""
    s = s.replace("\\", "")
    for ch in "&%$#_{}":
        s = s.replace(ch, "\\" + ch)
    # keep capitalization of acronyms / chemical formulas that BibTeX would lowercase
    s = re.sub(r"\b([A-Z]{2,}|[A-Z][a-z]?\d+[A-Za-z\d]*)\b", r"{\1}", s)
    return s.strip()


def make_key(work, seen):
    auth = work.get("authorships") or [{}]
    last = (auth[0].get("author", {}) or {}).get("display_name", "anon").split()[-1]
    year = work.get("publication_year") or "n.d."
    title = work.get("title") or ""
    stub = re.sub(r"[^a-z]", "", (title.split() or ["x"])[0].lower())[:10] or "x"
    key = f"{last.lower()}{year}{stub}"
    n = 2
    base = key
    while key in seen:
        key = f"{base}{n}"
        n += 1
    seen.add(key)
    return key


def main():
    works = fetch_all()
    with open(os.path.join(OUT, "works_raw.json"), "w", encoding="utf-8") as f:
        json.dump(works, f, ensure_ascii=False, indent=1)

    # Drop anything that is not a real paper
    keep_types = {"article", "review", "preprint", "book-chapter", "letter"}
    works = [w for w in works if (w.get("type") or "") in keep_types]
    works.sort(key=lambda w: (w.get("publication_year") or 0,
                              w.get("cited_by_count") or 0), reverse=True)

    seen, entries, rows = set(), [], []
    for w in works:
        key = make_key(w, seen)
        authors = [a.get("author", {}).get("display_name", "")
                   for a in (w.get("authorships") or [])]
        authors = [a for a in authors if a]
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        venue = src.get("display_name") or ""
        biblio = w.get("biblio") or {}
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        oa = w.get("best_oa_location") or {}
        oa_url = oa.get("pdf_url") or oa.get("landing_page_url") or ""
        is_preprint = (w.get("type") == "preprint") or ("arxiv" in venue.lower())

        fields = [
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
            fields.append(("pdf", oa_url))
        fields.append(("bibtex_show", "true"))

        body = "\n".join(f"  {k:<12}= {{{v}}}," for k, v in fields if v)
        etype = "misc" if is_preprint else "article"
        entries.append(f"@{etype}{{{key},\n{body}\n}}")

        rows.append("\t".join([
            str(w.get("publication_year") or ""),
            str(w.get("cited_by_count") or 0),
            "OA" if oa_url else "--",
            (venue or "?")[:42],
            (w.get("title") or "")[:88],
        ]))

    with open(os.path.join(OUT, "papers.bib"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries) + "\n")
    with open(os.path.join(OUT, "summary.tsv"), "w", encoding="utf-8") as f:
        f.write("year\tcites\toa\tvenue\ttitle\n")
        f.write("\n".join(rows) + "\n")

    print(f"works kept: {len(works)}")
    venues = {}
    for w in works:
        v = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "?"
        venues[v] = venues.get(v, 0) + 1
    print("\nvenues:")
    for v, n in sorted(venues.items(), key=lambda x: -x[1]):
        print(f"  {n:>3}  {v}")


if __name__ == "__main__":
    main()
