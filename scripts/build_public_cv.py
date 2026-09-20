"""Produce the public copy of the CV by removing the phone numbers.

    python scripts/build_public_cv.py "<source cv>.pdf"

Real redaction, not a black box drawn over the text: apply_redactions strips the
underlying characters, so the numbers cannot be recovered by selecting or by
extracting text. The institutional and personal email addresses and the ORCID
stay, since those are already public on the lab page and in every paper.

Output: assets/pdf/cv.pdf, then verified by re-extracting the text and failing
if any phone digits survive.
"""

import os
import re
import sys

import fitz  # PyMuPDF

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "assets", "pdf", "cv.pdf")
DEFAULT_SRC = r"C:\Users\YJ\OneDrive\Career\CV\Curriculum Vitae_YJYOO_Sep_2026.pdf"

# Lines to remove entirely, matched case-insensitively against the page text.
DROP_PREFIXES = ("phone:",)

# Corrections applied to the source PDF. These exist because the source CV
# itself is wrong; fix the .docx as well, or every rebuild re-applies them.
#   (page index, text to find, replacement, y-range that isolates the right line)
# Text to patch in the exported PDF, as (page, find, replace, y-range). Empty is the
# goal state: a correction here means the source document is still wrong, and the fix
# belongs in the source, not in every export of it.
#
# 2026-09-20: the GIST postdoc end date (Feb 2022 -> Feb 2023) lived here from
# 2026-09-19 until the .docx itself was corrected. Do not re-add it. If a correction
# is ever needed again, check first that the source has not simply been re-exported.
CORRECTIONS = []
# Anything matching these must not survive into the output.
FORBIDDEN = [
    re.compile(r"\+82[\s-]?10[\s-]?\d{3,4}[\s-]?\d{4}"),
    re.compile(r"\+1[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{4}"),
]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.exists(src):
        raise SystemExit(f"source not found: {src}")

    doc = fitz.open(src)

    # Corrections first: redaction carries its own replacement text, so the old
    # string is removed and the new one drawn in its place.
    fixed = 0
    for page_no, old, new, (y0, y1) in CORRECTIONS:
        page = doc[page_no]
        hits = [r for r in page.search_for(old) if y0 <= r.y0 <= y1]
        if len(hits) != 1:
            raise SystemExit(
                f"correction {old!r} -> {new!r} matched {len(hits)} places on page "
                f"{page_no} within y {y0}-{y1}; refusing to guess")
        rect = hits[0]

        # Take the baseline and size from the span being replaced. Letting the
        # redaction annotation carry the text instead makes PyMuPDF shrink it to
        # fit the box, which came out looking like a superscript.
        origin, size = None, 10.0
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if fitz.Rect(span["bbox"]).intersects(rect) and old.split()[-1] in span["text"]:
                        origin, size = span["origin"], span["size"]
        if origin is None:
            raise SystemExit(f"could not locate the span carrying {old!r}")

        page.add_redact_annot(rect)
        page.apply_redactions()
        page.insert_text((rect.x0, origin[1]), new, fontname="tiro", fontsize=size)
        fixed += 1

    marked = 0
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(s["text"] for s in line["spans"])
                if text.strip().lower().startswith(DROP_PREFIXES):
                    rect = fitz.Rect(line["bbox"])
                    page.add_redact_annot(rect)
                    marked += 1
        page.apply_redactions()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc.save(OUT, garbage=4, deflate=True)
    doc.close()

    # Verify against the written file, not against what we think we did.
    check = fitz.open(OUT)
    body = "\n".join(p.get_text() for p in check)
    pages = check.page_count
    check.close()

    leaks = [p.pattern for p in FORBIDDEN if p.search(body)]
    for _, old, new, _ in CORRECTIONS:
        if new not in body:
            raise SystemExit(f"correction did not take: {new!r} absent from the output")
    print(f"source : {src}")
    print(f"output : {OUT}  ({pages} pages, {os.path.getsize(OUT) / 1024:.0f} KB)")
    print(f"lines redacted: {marked}   corrections applied: {fixed}")
    print(f"still present  : mit.edu={'yjyoo@mit.edu' in body}  "
          f"gmail={'yjyoo0601@gmail.com' in body}  ORCID={'0000-0002-6490-2324' in body}")
    if leaks:
        os.remove(OUT)
        raise SystemExit(f"FAILED: phone numbers survived redaction {leaks}; output deleted")
    print("verified: no phone number remains in the extracted text")


if __name__ == "__main__":
    main()
