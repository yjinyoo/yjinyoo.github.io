"""Crawl the published site and report internal links that do not resolve.

Run against the live URL after a deploy. External links are only HEAD-checked
when --external is passed, because publisher sites rate-limit aggressively and a
slow reply there is not a broken site.
"""

import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import deque

ROOT = sys.argv[1] if len(sys.argv) > 1 else "https://yjinyoo.github.io/"
CHECK_EXTERNAL = "--external" in sys.argv
UA = {"User-Agent": "Mozilla/5.0 (link check)"}


def get(url, method="GET"):
    req = urllib.request.Request(url, headers=UA, method=method)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, (r.read().decode("utf-8", "ignore") if method == "GET" else "")


seen, queue, broken, external = set(), deque([ROOT]), [], set()

while queue:
    url = queue.popleft()
    if url in seen:
        continue
    seen.add(url)
    try:
        status, body = get(url)
    except urllib.error.HTTPError as e:
        broken.append((url, e.code))
        continue
    except Exception as e:
        broken.append((url, type(e).__name__))
        continue

    for href in re.findall(r'href=["\']([^"\'#]+)', body):
        if href.startswith(("mailto:", "javascript:", "data:", "tel:")):
            continue
        target = urllib.parse.urljoin(url, href)
        if target.startswith(ROOT):
            if target not in seen and not re.search(r"\.(png|jpg|jpeg|svg|webp|pdf|xml|json|js|css|ico)$", target):
                queue.append(target)
        elif target.startswith("http"):
            external.add(target)

print(f"crawled {len(seen)} internal pages")
if broken:
    print(f"\nBROKEN internal links ({len(broken)}):")
    for url, why in broken:
        print(f"  {why}  {url}")
else:
    print("no broken internal links")

print(f"\n{len(external)} distinct external links (not checked; pass --external to check)")
if CHECK_EXTERNAL:
    bad = []
    for url in sorted(external):
        try:
            get(url, "HEAD")
        except urllib.error.HTTPError as e:
            if e.code in (403, 405, 429):
                continue  # publisher bot-blocking, not a dead link
            bad.append((url, e.code))
        except Exception as e:
            bad.append((url, type(e).__name__))
    print(f"external failures: {len(bad)}")
    for url, why in bad:
        print(f"  {why}  {url}")

sys.exit(1 if broken else 0)
