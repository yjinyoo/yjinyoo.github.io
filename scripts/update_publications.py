"""Refresh the publication list end to end.

    python scripts/update_publications.py

Re-queries OpenAlex, re-separates the record from the namesakes, rewrites
_bibliography/papers.bib, reapplies the manual corrections, and checks that
every DOI still resolves. Safe to re-run; it overwrites papers.bib.
"""

import runpy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

for step in ["fetch_pubs.py", "curate.py", "make_bib.py", "check_dois.py"]:
    print(f"\n=== {step} ===")
    runpy.run_path(os.path.join(HERE, step), run_name="__main__")
