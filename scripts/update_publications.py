"""Refresh the publication list end to end.

    python scripts/update_publications.py

Re-queries OpenAlex, re-separates the record from the namesakes, rewrites
_bibliography/papers.bib from the CV (assets/pdf/cv.pdf: numbers, years, volumes,
pages, equal first authorship), checks that every DOI still resolves, and checks
the result against the CV once more. Safe to re-run; it overwrites papers.bib.

Order when a paper comes out: add it to the CV, run build_public_cv.py (which
will say the list is now stale), then run this.
"""

import runpy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# check_cv_match exits through sys.exit even on success, so it has to stay last
for step in ["fetch_pubs.py", "curate.py", "make_bib.py", "check_dois.py", "check_cv_match.py"]:
    print(f"\n=== {step} ===")
    runpy.run_path(os.path.join(HERE, step), run_name="__main__")
