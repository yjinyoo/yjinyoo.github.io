"""Render the activity calendar: code (GitHub contributions) and simulation runs.

    python scripts/build_activity_svg.py [year]

Output: assets/img/activity.svg (GitHub) and assets/img/simulations.svg, two panels
drawn over the same weeks so they sit side by side (see calendar_svg.py).

CODE ROW. The third-party chart services only render a rolling twelve months and
cannot be asked for a calendar year, so the data is read straight from the
profile. Only what the profile shows anonymously is used, which is what a visitor
to the site would see. Private contributions appear only while "Private
contributions" is enabled in the GitHub profile's contribution settings; with it
off the year renders almost empty, and that is a true picture of the public
profile, not a bug in this script.

SIMULATION ROW. Read from _data/simulation_runs.json, which is NOT made here and
cannot be made on GitHub Actions: `Simulations/tools/simulation_run_counter.py`
counts it on the workstation (it needs the cloud solver account, the local
archive of runs deleted from the cloud, and the cluster login) and
`publish_simulation_runs.py` pushes it at every session wrap-up. The daily
refresh here redraws that row from the committed file, ending it on the day the
counts were collected. With no data file the chart is the code row alone.
"""

import datetime as dt
import json
import os
import re
import sys
import urllib.request

from calendar_svg import BLUE, GREEN, quartile_levels, render_panel, shared_span

USER = "yjinyoo"
ARGS = [a for a in sys.argv[1:] if not a.startswith("-")]
YEAR = int(ARGS[0]) if ARGS else dt.date.today().year
# By default the empty run before the first active day is cut, so the chart opens
# on the month the work actually started rather than on a bank of blank weeks.
# The totals beside each row still count the whole year.
FULL_YEAR = "--full" in sys.argv[1:]
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Stable filename: the year is inside the image, so the page never has to be
# edited when the year rolls over.
OUT = os.path.join(SITE, "assets", "img", "activity.svg")
OUT_SIMS = os.path.join(SITE, "assets", "img", "simulations.svg")
SIMS = os.path.join(SITE, "_data", "simulation_runs.json")


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


def simulation_panel(year):
    if not os.path.exists(SIMS):
        return None
    with open(SIMS, encoding="utf-8") as f:
        doc = json.load(f)
    collected = dt.date.fromisoformat(doc["collected_on"])
    counts = {d: sum(v) for d, v in doc["by_day"].items()}
    in_year = {d: c for d, c in counts.items() if d[:4] == str(year)}
    return dict(label="Simulation runs", unit="runs", counts=counts,
                levels=quartile_levels(in_year), scale=BLUE,
                last=collected if collected.year == year else None)


def build(year):
    levels, counts = fetch(year)
    gh = dict(label="Project activity", unit="GitHub contributions", counts=counts,
              levels=levels, scale=GREEN)
    sims = simulation_panel(year)
    panels = [gh] + ([sims] if sims else [])
    start, end = shared_span(year, panels, FULL_YEAR)
    print(f"chart spans {start.isoformat()} to {end.isoformat()}")

    jobs = [(gh, OUT, f"Project activity, {year}",
             f"{USER} GitHub contributions per day in {year}")]
    if sims:
        jobs.append((sims, OUT_SIMS, f"Simulation runs, {year}",
                     f"Finished simulation runs per day in {year}"))
    for p, path, title, aria in jobs:
        year_total, active, drawn = render_panel(year, p, path, start, end, title=title, aria=aria)
        print(f"{path}\n  {year_total:,} {p['unit']} on {len(active)} days in {year}"
              + (f", drawn through {p['last']}" if p.get("last") and p["last"] < end else ""))
        if drawn != year_total:
            print(f"  NOTE: {year_total - drawn:,} fall outside the drawn range")
    if not sum(counts.values()):
        print("  WARNING: zero contributions. Check that 'Private contributions' is "
              "enabled in the GitHub profile contribution settings.")


if __name__ == "__main__":
    build(YEAR)
