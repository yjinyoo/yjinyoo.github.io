"""Separate the real Young Jin Yoo (MIT, photonics) record from the OpenAlex merge.

Two filters, applied in order:
  1. co-author network - the photonics record is one connected community; the
     merged-in namesakes share no co-authors with it.
  2. title dedupe - OpenAlex lists journal cover / frontispiece pieces as separate
     works with the same title; keep the most-cited copy.
"""

import json
import re
import os
from collections import Counter

OUT = os.path.dirname(os.path.abspath(__file__))
works = json.load(open(os.path.join(OUT, "works_raw.json"), encoding="utf-8"))

keep_types = {"article", "review", "preprint", "book-chapter", "letter"}
works = [w for w in works if (w.get("type") or "") in keep_types]


def coauthors(w):
    return {a.get("author", {}).get("display_name", "")
            for a in (w.get("authorships") or [])} - {"Young Jin Yoo", ""}


# Seed the community with works in unambiguous photonics venues.
SEED_VENUES = ("Optical Materials Express", "Optics Express", "Nanophotonics",
               "Advanced Optical Materials", "Nature Nanotechnology")
seed = [w for w in works
        if ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
        in SEED_VENUES]

core = set()
for w in seed:
    core |= coauthors(w)

# Grow the community until it stops growing.
for _ in range(6):
    grew = False
    for w in works:
        ca = coauthors(w)
        if ca & core and not ca <= core:
            core |= ca
            grew = True
    if not grew:
        break

def at_mit(w):
    """The MIT postdoc work is a second, disjoint community: match on affiliation."""
    for a in (w.get("authorships") or []):
        if a.get("author", {}).get("display_name") == "Young Jin Yoo":
            names = " ".join(i.get("display_name", "")
                             for i in (a.get("institutions") or []))
            return "Massachusetts Institute of Technology" in names
    return False


def is_mine(w):
    return bool(coauthors(w) & core) or at_mit(w)


mine = [w for w in works if is_mine(w)]
theirs = [w for w in works if not is_mine(w)]

print(f"kept (GIST photonics community + MIT affiliation) : {len(mine)}")
print(f"dropped as namesakes:")
for w in sorted(theirs, key=lambda x: -(x.get("publication_year") or 0)):
    v = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "?"
    print(f"   {w.get('publication_year')}  {v[:38]:<38}  {(w.get('title') or '')[:70]}")


def norm(t):
    t = (t or "").lower()
    t = re.sub(r"\(.*?\)", " ", t)          # drop "(Adv. Sci. 10/2023)" cover suffixes
    # drop "Colorimetric Sensors: ..." cover prefixes. The limit was 30 characters
    # until "Colored Passive Radiative Cooler: " (32) slipped through and the 2018
    # Adv. Opt. Mater. paper was listed twice. make_bib now also refuses two works
    # that match the same CV entry, so a miss here fails loudly instead.
    t = re.sub(r"^[a-z ]{0,60}:\s*", "", t)
    return re.sub(r"[^a-z0-9]", "", t)


best = {}
for w in mine:
    k = norm(w.get("title"))
    prev = best.get(k)
    # prefer the copy with more citations; tie-break on the shorter (non-cover) title
    if (prev is None
            or (w.get("cited_by_count") or 0) > (prev.get("cited_by_count") or 0)
            or ((w.get("cited_by_count") or 0) == (prev.get("cited_by_count") or 0)
                and len(w.get("title") or "") < len(prev.get("title") or ""))):
        best[k] = w

deduped = sorted(best.values(),
                 key=lambda w: (-(w.get("publication_year") or 0),
                                -(w.get("cited_by_count") or 0)))

print(f"\nafter dedupe: {len(deduped)} papers  "
      f"({len(mine) - len(deduped)} cover/preprint duplicates merged)")

# author position tells us which are first-author papers
firsts = []
for w in deduped:
    auths = [a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or [])]
    if auths and auths[0] == "Young Jin Yoo":
        firsts.append(w)
print(f"first-author: {len(firsts)}")

print("\nmost frequent co-authors:")
c = Counter()
for w in deduped:
    c.update(coauthors(w))
for name, n in c.most_common(12):
    print(f"  {n:>3}  {name}")

json.dump(deduped, open(os.path.join(OUT, "works_mine.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
