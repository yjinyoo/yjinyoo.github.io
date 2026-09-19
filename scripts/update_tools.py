"""Fill the generated fields in `_data/tools.yml` from the GitHub API.

Hand-written fields (title, summary, body) say why a tool exists, which GitHub cannot know.
Everything GitHub does know is written by this script so the page cannot drift from the
repositories: description, primary language, and the date of the last push.

    python scripts/update_tools.py            # update in place
    python scripts/update_tools.py --check    # exit 1 if anything is stale, change nothing

`--check` is for the deploy workflow: it makes a page that has fallen behind loud instead of
quietly wrong.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "_data" / "tools.yml"
OWNER = "yjinyoo"
API = "https://api.github.com/repos/{owner}/{repo}"
UA = {"User-Agent": "tools-page-update", "Accept": "application/vnd.github+json"}

# Each generated field: the yaml key, and how to read it out of the API payload.
GENERATED = {
    "description": lambda d: (d.get("description") or "").strip(),
    "language": lambda d: d.get("language") or "",
    "pushed": lambda d: (d.get("pushed_at") or "")[:10],
}


def fetch(repo):
    req = urllib.request.Request(API.format(owner=OWNER, repo=repo), headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def repos_in(text):
    """[(repo, start_of_block, end_of_block), ...] in file order.

    The file is edited as text rather than round-tripped through a yaml library, because a
    round trip reflows every block scalar in the file and the diff then hides the one line
    that actually changed.
    """
    starts = [m.start() for m in re.finditer(r"^- repo:", text, re.M)]
    out = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(text)
        repo = re.match(r"- repo:\s*(\S+)", text[s:e]).group(1)
        out.append((repo, s, e))
    return out


def set_field(block, key, value):
    """Set `key` in one yaml block, inserting it after `repo:` if it is not there yet."""
    value = str(value).replace('"', "'")
    line = f"  {key}: \"{value}\"\n"
    pat = re.compile(rf"^  {key}:.*\n", re.M)
    if pat.search(block):
        return pat.sub(line, block, count=1)
    m = re.search(r"^- repo:.*\n", block, re.M)
    return block[:m.end()] + line + block[m.end():]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="report staleness and exit 1; write nothing")
    args = ap.parse_args()

    text = DATA.read_text(encoding="utf-8")
    blocks = repos_in(text)
    if not blocks:
        print(f"no tool entries in {DATA}")
        return 1

    stale, out, cursor = [], [], 0
    for repo, s, e in blocks:
        out.append(text[cursor:s])
        block = text[s:e]
        try:
            data = fetch(repo)
        except urllib.error.HTTPError as err:
            # A repo that has been renamed or made private is a page pointing at a 404. Say so
            # and keep the old values rather than silently blanking the entry.
            print(f"  {repo}: HTTP {err.code} -- left unchanged")
            out.append(block)
            cursor = e
            stale.append(f"{repo}: unreachable (HTTP {err.code})")
            continue
        for key, read in GENERATED.items():
            new = read(data)
            old = re.search(rf"^  {key}: \"(.*)\"$", block, re.M)
            if old is None or old.group(1) != new:
                stale.append(f"{repo}.{key}: {old.group(1) if old else '(missing)'} -> {new}")
            block = set_field(block, key, new)
        print(f"  {repo}: {read_summary(data)}")
        out.append(block)
        cursor = e
    out.append(text[cursor:])

    if args.check:
        if stale:
            print(f"\nSTALE: {len(stale)} field(s) differ from GitHub")
            for s_ in stale:
                print(f"  {s_}")
            return 1
        print("\nup to date")
        return 0

    DATA.write_text("".join(out), encoding="utf-8")
    print(f"\nwrote {DATA.name}: {len(blocks)} tools, {len(stale)} field(s) changed")
    return 0


def read_summary(d):
    return (f"{d.get('language') or 'n/a':<10} pushed {(d.get('pushed_at') or '')[:10]}  "
            f"{d.get('stargazers_count', 0)} star(s)")


if __name__ == "__main__":
    raise SystemExit(main())
