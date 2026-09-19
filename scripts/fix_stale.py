"""Replace entries where OpenAlex still carries the preprint after the paper ran.

OpenAlex had the Gires-Tournois monopixel paper only as the Research Square
preprint, with the author order scrambled. The journal version is open access
(CC-BY), so the record is taken from the publisher instead.
"""

import io
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(os.path.dirname(OUT), "_bibliography", "papers.bib")

PUBLISHED = """@article{ko2026subvolt,
  abbr        = {Light Sci. Appl.},
  author      = {Joo Hwan Ko and Hyo Eun Jeong and Serim Kim and Doeun Kim and Se Yeon Kim and Young Jin Yoo and Hyeon-Ho Jeong and Young Min Song},
  title       = {Sub-1-volt, reconfigurable Gires-Tournois resonators for full-coloured monopixel array},
  journal     = {Light: Science \\& Applications},
  year        = {2026},
  volume      = {15},
  number      = {134},
  doi         = {10.1038/s41377-026-02228-2},
  url         = {https://doi.org/10.1038/s41377-026-02228-2},
  pdf         = {https://pmc.ncbi.nlm.nih.gov/articles/PMC12949994/},
  abstract    = {An electrically reconfigurable Gires-Tournois resonator integrated with polyaniline produces colour shifts beyond complementary hue ranges at sub-1-volt drive and 90 uW/cm2, scaling from ~16,900 PPI pixel densities to centimetre-scale arrays, with memory-in-pixel operation.},
  bibtex_show = {true},
  selected    = {true},
}"""

with io.open(BIB, encoding="utf-8") as f:
    bib = f.read()

pattern = re.compile(r"@misc\{song2025subvolt,.*?\n\}", re.S)
if not pattern.search(bib):
    raise SystemExit("stale preprint entry not found - already fixed?")
bib = pattern.sub(PUBLISHED, bib)

with io.open(BIB, "w", encoding="utf-8") as f:
    f.write(bib)

n = bib.count("@article{") + bib.count("@misc{")
print(f"replaced the preprint with the Light: Science & Applications record")
print(f"total entries: {n}, selected: {bib.count('selected    = {true}')}")
