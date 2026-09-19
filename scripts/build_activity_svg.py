"""Render a contribution calendar for one calendar year as a self-contained SVG.

    python scripts/build_activity_svg.py [year]

The third-party chart services only render a rolling twelve months and cannot be
asked for a calendar year, so the data is read straight from the profile and
drawn here. Output: assets/img/activity.svg

Only what the profile shows anonymously is used, which is what a visitor to the
site would see. Private contributions appear only while "Private contributions"
is enabled in the GitHub profile's contribution settings; with it off the year
renders almost empty, and that is a true picture of the public profile, not a
bug in this script.
"""

import datetime as dt
import os
import re
import sys
import urllib.request

USER = "yjinyoo"
YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today().year
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Stable filename: the year is inside the image, so the page never has to be
# edited when the year rolls over.
OUT = os.path.join(SITE, "assets", "img", "activity.svg")

CELL, GAP = 11, 3
PITCH = CELL + GAP
LEFT, TOP = 30, 34          # room for weekday labels and the month row
# Empty days are drawn semi-transparent so the chart reads on a light or a dark
# page without needing to know which one it is sitting on.
EMPTY = ("#8b929c", 0.20)
SCALE = ["#cdead9", "#8fd0ae", "#55a87e", "#2f6f4e"]
LABEL = "#8b929c"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch(year):
    url = (f"https://github.com/users/{USER}/contributions"
           f"?from={year}-01-01&to={year}-12-31")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        html = r.read().decode("utf-8", "ignore")

    days = dict(re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d)"', html))
    if not days:
        raise SystemExit("no contribution cells found; the profile markup changed")

    # Counts live in the tooltips, keyed to each cell by id.
    # data-date precedes id on the cell, so match in that order.
    ids = {cid: date for date, cid in
           re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?id="(contribution-day-component-[\d-]+)"', html)}
    tips = dict(re.findall(r'<tool-tip[^>]*for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)</tool-tip>', html))
    counts = {}
    for cid, date in ids.items():
        m = re.match(r"(\d+) contribution", tips.get(cid, ""))
        counts[date] = int(m.group(1)) if m else 0
    return {d: int(l) for d, l in days.items()}, counts


def build(year):
    levels, counts = fetch(year)
    today = dt.date.today()
    start = dt.date(year, 1, 1)
    end = min(dt.date(year, 12, 31), today) if today.year == year else dt.date(year, 12, 31)

    # Columns are weeks beginning on Sunday, as GitHub lays them out.
    first_col = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    n_cols = ((end - first_col).days // 7) + 1
    width = LEFT + n_cols * PITCH + 8
    height = TOP + 7 * PITCH + 26

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="{USER} contribution activity for {year}">',
           f'<title>Contribution activity, {year}</title>',
           f'<style>text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}</style>']

    # Year, set large enough to be the first thing read.
    out.append(f'<text x="0" y="17" font-size="15" font-weight="700" fill="{LABEL}">{year}</text>')

    # Month labels, placed at the first column whose week contains the 1st.
    seen = set()
    for col in range(n_cols):
        week = first_col + dt.timedelta(days=7 * col)
        for k in range(7):
            d = week + dt.timedelta(days=k)
            if d.year == year and d.day <= 7 and d.month not in seen and start <= d <= end:
                seen.add(d.month)
                out.append(f'<text x="{LEFT + col * PITCH}" y="{TOP - 8}" '
                           f'font-size="10" fill="{LABEL}">{MONTHS[d.month - 1]}</text>')
                break

    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="0" y="{TOP + row * PITCH + CELL - 2}" '
                   f'font-size="9" fill="{LABEL}">{name}</text>')

    total = 0
    for col in range(n_cols):
        for row in range(7):
            d = first_col + dt.timedelta(days=7 * col + row)
            if d < start or d > end:
                continue
            key = d.isoformat()
            lvl = levels.get(key, 0)
            total += counts.get(key, 0)
            x, y = LEFT + col * PITCH, TOP + row * PITCH
            if lvl == 0:
                fill, extra = EMPTY[0], f' opacity="{EMPTY[1]}"'
            else:
                fill, extra = SCALE[min(lvl, 4) - 1], ""
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                       f'fill="{fill}"{extra}><title>{key}: {counts.get(key, 0)}</title></rect>')

    base = TOP + 7 * PITCH + 15
    out.append(f'<text x="0" y="{base}" font-size="10" fill="{LABEL}">'
               f'{total:,} contributions in {year}</text>')

    lx = width - (5 * PITCH + 62)
    out.append(f'<text x="{lx}" y="{base}" font-size="10" fill="{LABEL}">Less</text>')
    out.append(f'<rect x="{lx + 28}" y="{base - 9}" width="{CELL}" height="{CELL}" rx="2" '
               f'fill="{EMPTY[0]}" opacity="{EMPTY[1]}"/>')
    for i, c in enumerate(SCALE):
        out.append(f'<rect x="{lx + 28 + (i + 1) * PITCH}" y="{base - 9}" '
                   f'width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
    out.append(f'<text x="{lx + 28 + 5 * PITCH + 4}" y="{base}" font-size="10" fill="{LABEL}">More</text>')
    out.append("</svg>")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    filled = sum(1 for d, l in levels.items() if l > 0 and start.isoformat() <= d <= end.isoformat())
    print(f"{OUT}\n  {year}: {total:,} contributions, {filled} active days, "
          f"through {end.isoformat()}")
    if total == 0:
        print("  WARNING: zero contributions. Check that 'Private contributions' is "
              "enabled in the GitHub profile contribution settings.")


if __name__ == "__main__":
    build(YEAR)
