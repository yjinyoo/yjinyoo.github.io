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
DEFAULT_SRC = r"C:\Users\YJ\OneDrive\Career\CV\Curriculum Vitae_YJYOO_Aug_2026.pdf"

# Lines to remove entirely, matched case-insensitively against the page text.
DROP_PREFIXES = ("phone:",)
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
    print(f"source : {src}")
    print(f"output : {OUT}  ({pages} pages, {os.path.getsize(OUT) / 1024:.0f} KB)")
    print(f"lines redacted: {marked}")
    print(f"still present  : mit.edu={'yjyoo@mit.edu' in body}  "
          f"gmail={'yjyoo0601@gmail.com' in body}  ORCID={'0000-0002-6490-2324' in body}")
    if leaks:
        os.remove(OUT)
        raise SystemExit(f"FAILED: phone numbers survived redaction {leaks}; output deleted")
    print("verified: no phone number remains in the extracted text")


if __name__ == "__main__":
    main()
