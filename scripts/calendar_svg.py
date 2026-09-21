"""Draw calendar-year heatmaps of daily counts, one SVG per measure, for side-by-side display.

    build_activity_svg.py   GitHub activity  -> assets/img/activity.svg     (green)
                            simulation runs  -> assets/img/simulations.svg  (blue)

The two panels sit next to each other on the about page, each taking half the
card. So the WIDTH is fixed and the cell size follows from the number of weeks
drawn (from March in 2026): about 11 px in September, about 7.5 px by December, and the panel always
fills its half instead of leaving the right side empty early in the year. Both
panels get the same week range and so the same cell size, which keeps them the
same height and lets a week on the left be read against the same week on the right.

A panel may end before the other: simulation counts are collected on the
workstation, so days after the last count are left undrawn rather than drawn
empty, which would claim nothing ran.
"""

import datetime as dt
import os

WIDTH = 416                 # half of the 858 px card, less half the 24 px gap
MAX_PITCH = 14              # early in the year, do not blow cells up past this
TOP = 36                    # title line + month row
# Empty days are drawn semi-transparent so the chart reads on a light or a dark
# page without needing to know which one it is sitting on.
EMPTY = ("#8b929c", 0.20)
GREEN = ["#cdead9", "#8fd0ae", "#55a87e", "#2f6f4e"]
# Blue steps sit one notch darker than a plain tint ramp so the lightest blue
# does not merge with the lightest green (OKLab dE 13 against 6 for the tints).
BLUE = ["#9ec5f4", "#5598e7", "#256abf", "#184f95"]
LABEL = "#8b929c"
FONT = '-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def quartile_levels(counts):
    """Levels 1-4 from the quartiles of the non-zero days, the way GitHub shades.
    A fixed scale would not work for runs: a quiet day has one, a sweep has hundreds."""
    vals = sorted(c for c in counts.values() if c > 0)
    if not vals:
        return {d: 0 for d in counts}
    cuts = [vals[min(len(vals) - 1, int(len(vals) * q))] for q in (0.25, 0.5, 0.75)]
    return {d: (0 if c <= 0 else 1 + sum(c > t for t in cuts)) for d, c in counts.items()}


def shared_span(year, panels, full_year=False):
    """First and last day to draw, common to all panels.

    The span opens on the first active month of the FIRST panel (the GitHub record),
    not of whichever panel starts earliest. User decision 2026-09-21: both calendars
    start where the project record starts. The counts printed on each panel still
    cover the whole year, so runs before that month (2,216 in Jan-Feb 2026) are in
    the number but not drawn."""
    today = dt.date.today()
    end = min(dt.date(year, 12, 31), today) if today.year == year else dt.date(year, 12, 31)
    start = dt.date(year, 1, 1)
    active = sorted(d for d, l in panels[0]["levels"].items() if l > 0 and d[:4] == str(year))
    if active and not full_year:
        start = dt.date(year, dt.date.fromisoformat(active[0]).month, 1)
    return start, end


def render_panel(year, p, out_path, start, end, *, title, aria):
    """p: dict with label, unit, counts, levels, scale, and optionally last (a date).
    Returns (year_total, active_days, drawn_total)."""
    last = min(p.get("last") or end, end)
    # Columns are weeks beginning on Sunday, as GitHub lays them out.
    first_col = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    n_cols = ((end - first_col).days // 7) + 1
    pitch = min(MAX_PITCH, (WIDTH - 1) / n_cols)
    cell = round(pitch * 0.82, 2)
    rx = round(min(2.0, cell * 0.2), 2)
    grid_h = 7 * pitch
    sw = min(9, cell)                       # legend swatch
    height = round(TOP + grid_h + 22)

    year_total = sum(c for d, c in p["counts"].items() if d[:4] == str(year))
    active = [d for d, l in p["levels"].items() if l > 0 and d[:4] == str(year)]

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
           f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{aria}">',
           f'<title>{title}</title>',
           f'<style>text{{font-family:{FONT}}}</style>',
           f'<text x="0" y="13" font-size="13" font-weight="600" fill="{LABEL}">{p["label"]}</text>',
           f'<text x="{WIDTH}" y="13" font-size="11" fill="{LABEL}" text-anchor="end">'
           f'{year_total:,} {p["unit"]} in {year}</text>']

    seen = set()
    for col in range(n_cols):
        week = first_col + dt.timedelta(days=7 * col)
        for k in range(7):
            d = week + dt.timedelta(days=k)
            if d.year == year and d.day <= 7 and d.month not in seen and start <= d <= end:
                seen.add(d.month)
                out.append(f'<text x="{col * pitch:.1f}" y="{TOP - 6}" '
                           f'font-size="10" fill="{LABEL}">{MONTHS[d.month - 1]}</text>')
                break

    drawn = 0
    for col in range(n_cols):
        for row in range(7):
            d = first_col + dt.timedelta(days=7 * col + row)
            if d < start or d > last:
                continue
            key = d.isoformat()
            lvl = p["levels"].get(key, 0)
            n = p["counts"].get(key, 0)
            drawn += n
            x, y = col * pitch, TOP + row * pitch
            if lvl == 0:
                fill, extra = EMPTY[0], f' opacity="{EMPTY[1]}"'
            else:
                fill, extra = p["scale"][min(lvl, 4) - 1], ""
            out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell}" height="{cell}" rx="{rx}" '
                       f'fill="{fill}"{extra}><title>{key}: {n:,} {p["unit"]}</title></rect>')

    base = TOP + grid_h + 16
    lx = WIDTH - (5 * (sw + 2) + 62)
    out.append(f'<text x="{lx}" y="{base:.1f}" font-size="10" fill="{LABEL}">Less</text>')
    out.append(f'<rect x="{lx + 26}" y="{base - sw + 1:.1f}" width="{sw}" height="{sw}" rx="{rx}" '
               f'fill="{EMPTY[0]}" opacity="{EMPTY[1]}"/>')
    for k, c in enumerate(p["scale"]):
        out.append(f'<rect x="{lx + 26 + (k + 1) * (sw + 2):.1f}" y="{base - sw + 1:.1f}" '
                   f'width="{sw}" height="{sw}" rx="{rx}" fill="{c}"/>')
    out.append(f'<text x="{lx + 26 + 5 * (sw + 2) + 4:.1f}" y="{base:.1f}" font-size="10" '
               f'fill="{LABEL}">More</text>')
    out.append("</svg>")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return year_total, active, drawn
