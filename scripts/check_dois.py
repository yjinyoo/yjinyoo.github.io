"""Resolve every DOI on the site against Crossref, so no entry links to nothing.

NOT FOUND is a verdict. UNRESOLVED means the query itself failed (network, rate
limit) and the DOI is simply unchecked, which is not the same as passing.
"""

import io
import json
import os
import re
import time
import urllib.error
import urllib.request

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAILTO = "yjyoo@mit.edu"

targets = [os.path.join(SITE, "_bibliography", "papers.bib")]
news = os.path.join(SITE, "_news")
if os.path.isdir(news):
    targets += [os.path.join(news, f) for f in os.listdir(news) if f.endswith(".md")]

# Only take DOIs from a bib `doi = {...}` field or a doi.org link, never from an
# arbitrary URL: an open-access pdf_url such as .../nanoph-2020-0062/pdf would
# otherwise be read as a DOI with a trailing path and reported as missing.
PATTERNS = [
    re.compile(r"^\s*doi\s*=\s*\{(10\.\d{4,9}/[^}]+)\}", re.M),
    re.compile(r"doi\.org/(10\.\d{4,9}/[^\s{},\)\"'>]+)"),
]

dois = {}
for path in targets:
    text = io.open(path, encoding="utf-8").read()
    for pat in PATTERNS:
        for m in pat.finditer(text):
            dois.setdefault(m.group(1).rstrip(".,"), set()).add(os.path.basename(path))

print(f"checking {len(dois)} DOIs\n")
bad, unresolved = [], []
for doi in sorted(dois):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            msg = json.loads(r.read().decode("utf-8"))["message"]
        title = (msg.get("title") or ["(no title)"])[0]
        print(f"  OK         {doi}  {title[:60]}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            bad.append(doi)
            print(f"  NOT FOUND  {doi}   <- in {', '.join(dois[doi])}")
        else:
            unresolved.append(doi)
            print(f"  UNRESOLVED {doi}  (HTTP {e.code}, not checked)")
    except Exception as e:
        unresolved.append(doi)
        print(f"  UNRESOLVED {doi}  ({type(e).__name__}, not checked)")
    time.sleep(0.05)

print(f"\n{len(dois) - len(bad) - len(unresolved)} resolved, "
      f"{len(bad)} NOT FOUND, {len(unresolved)} unchecked")
if bad:
    raise SystemExit(1)
