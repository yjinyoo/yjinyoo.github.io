"""Refuse Hangul in files tracked by this repository.

The repository is public on GitHub, so everything committed here is readable by anyone,
including files the site build excludes (CLAUDE.md, NEXT_SESSION_PROMPT.md, log/).
Notes, handoffs, logs, comments and commit messages are written in English.

The one allowed exception is the Hangul spelling of the author's name in the structured
data (person_schema alternateName), so that a search in Korean finds the site.

Usage:
    python scripts/check_no_hangul.py            # check staged files (pre-commit)
    python scripts/check_no_hangul.py --all      # check every tracked file
    python scripts/check_no_hangul.py --msg FILE # check a commit message file (commit-msg)
"""

import re
import subprocess
import sys

# Code points, not literal characters, so this file passes its own check.
# Ranges: Hangul Jamo, Compatibility Jamo, Syllables.
HANGUL = re.compile("[%s-%s%s-%s%s-%s]" % tuple(map(chr, (
    0x1100, 0x11FF, 0x3131, 0x318E, 0xAC00, 0xD7A3))))

# path -> substrings that may contain Hangul in that file
AUTHOR_NAME_HANGUL = "".join(map(chr, (0xC720, 0xC601, 0xC9C4)))
ALLOWED = {
    "_includes/person_schema.liquid": [AUTHOR_NAME_HANGUL],
}


def git(*args):
    out = subprocess.run(["git", "-c", "core.quotePath=false", *args],
                         capture_output=True, check=True)
    return out.stdout


def offending_lines(path, text):
    hits = []
    for n, line in enumerate(text.split("\n"), 1):
        stripped = line
        for ok in ALLOWED.get(path, []):
            stripped = stripped.replace(ok, "")
        if HANGUL.search(stripped):
            hits.append((n, line.strip()[:100]))
    return hits


def main():
    args = sys.argv[1:]
    if args[:1] == ["--msg"]:
        text = open(args[1], encoding="utf-8").read()
        text = "\n".join(l for l in text.split("\n") if not l.startswith("#"))
        if HANGUL.search(text):
            print("commit message contains Hangul; this repository is public, write it in English.",
                  file=sys.stderr)
            return 1
        return 0

    if "--all" in args:
        paths = [p for p in git("ls-files", "-z").decode("utf-8").split("\0") if p]
        read = lambda p: open(p, "rb").read()
    else:
        paths = [p for p in git("diff", "--cached", "--name-only", "-z",
                                "--diff-filter=ACMR").decode("utf-8").split("\0") if p]
        read = lambda p: git("show", f":{p}")

    bad = {}
    for p in paths:
        try:
            text = read(p).decode("utf-8")
        except (UnicodeDecodeError, OSError, subprocess.CalledProcessError):
            continue  # binary or unreadable
        hits = offending_lines(p, text)
        if hits:
            bad[p] = hits

    if not bad:
        return 0
    print("Hangul found in files of a PUBLIC repository (anyone can read them on GitHub):",
          file=sys.stderr)
    for p, hits in bad.items():
        print(f"  {p}: {len(hits)} line(s)", file=sys.stderr)
        for n, line in hits[:3]:
            print(f"    {n}: {line}", file=sys.stderr)
    print("Write it in English. Allowed exceptions live in ALLOWED in scripts/check_no_hangul.py.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
