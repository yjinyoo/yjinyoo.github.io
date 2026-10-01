# CLAUDE.md: Homepage (yjinyoo.github.io)

> Person, environment, session protocol = `~/.claude/CLAUDE.md` (canonical). Do not duplicate here.
> This file = rules that hold only in this repo.

**Project ID: Homepage** · public address <https://yjinyoo.github.io> · repo `yjinyoo/yjinyoo.github.io` (public)
How to edit and where files live: `README.md`. Here, only **what a session must obey**.

**English only, everywhere in this repo** (2026-10-01, user): the repo is public, so CLAUDE.md, NEXT_SESSION_PROMPT.md, `log/`, comments and commit messages are readable on GitHub even though the site build excludes them. `scripts/check_no_hangul.py` refuses Hangul in staged files (pre-commit) and in commit messages (commit-msg); the one allowed exception is the name in `person_schema` alternateName. Replies to the user in chat stay Korean.

## Session start

1. This file 2) `NEXT_SESSION_PROMPT.md` 3) the latest 1 in `log/` 4) `git log --oneline -5`
5. If you touch public-facing wording, **open the CV first** (`~/.claude/projects/.../memory/reference_cv_location_and_ownership.md`)

## CV and site linkage (2026-09-21)

**The CV is canonical, the site follows.** The flow is one-way: edit the CV (OneDrive `Career/CV/` docx) → `python scripts/sync_cv.py`
→ check `git diff` → commit and push. sync does docx→PDF (Word) → public CV → regenerate the publication list → full cross-check,
and records which docx it used in `scripts/cv_source.json`. It does not commit.

| Site | How it comes from the CV | Cross-check |
|---|---|---|
| publications | **Generated**: `cv_record.py` reads number, year, volume, pages, co-first authorship from the public CV PDF | `make_bib.py` does not write unless 1:1 |
| cv page (positions, degrees, fellowships, awards) | Hand-written wording. **Dates, names, and item counts must match the CV** | `check_cv_match.py` |
| research page Funded projects | Hand-written wording. All projects since MIT (`SITE_PROJECTS_FROM`), dates match | `check_cv_match.py` |

- Do not add an item to the site **first**. If it is not in the CV, the cross-check fails (09-21: the MISTI project was only on the site).
- The only intentional differences from the CV are the three in the header of `cv_record.py`: `SITE_YEAR` / `SITE_PROJECTS_FROM` / `SITE_EDUCATION_FROM`. To add more, add them there with a reason.
- **If the cross-check says "in the CV but not on the site", ask the user before adding it to the site.** The omission may be intentional. On 09-21 a morning session added the B.S. to the cv page without asking, to make the check pass, and the user reverted it with "who told you to add that". The public page lists graduate degrees only (`SITE_EDUCATION_FROM`).
- Where the cross-check runs: end of sync, end of `update_publications.py`, end of `build_public_cv.py`, weekly `Site maintenance`.
  **If you edit the CV and do not sync**, the Simulations session-start hook shows "CV changed after the homepage was synced".
- If Word hangs, sync cuts off at 150 s and prints the manual procedure (save PDF from Word → the two scripts).

## Broken features

- **Before fixing, propose removing first.** This site is minimal: on 09-21 the Abs/Bib/PDF in the publication list were wrong, and when a fix for all four was proposed the user cut it down twice, "DOI only" → "title link only". A feature the theme turns on by default is not there because it is needed.

## Never do

- **Do not hand-edit `_bibliography/papers.bib`.** It is a generated file (table above). The exceptions are `ADDITIONS` (not in OpenAlex) / `OVERRIDES` (OpenAlex is stale) in `make_bib.py`. Until 2026-09-21 numbers and years came from OpenAlex, and the site (45) and CV (42) disagreed.
- **Do not upload the CV PDF as-is.** It contains a phone number. `scripts/build_public_cv.py` removes it, rereads the saved file, and if it remains, deletes the output and fails.
- **Do not write `co-advised by Kim and Englund` on public pages.** The CV says so, but in public material Kim comes first and alone, and Englund is scoped (`on the CMOS integrated photonics work`). Basis = memory `user_joint_kim_englund_appointment`.
- **Do not write device structures, numbers, or partners of unpublished projects.** NDA work, manuscripts under submission, and program details are mixed in. The safe line is the level of the already-public GitHub profile.
- **Do not delete `google2cef4b219e13a627.html`.** It looks like a junk file but it is the Google Search Console
  ownership verification file. Deleting it drops verification and stops index status reports. The theme does not render the `google_site_verification`
  config key, so the meta-tag method does not work, and verification is via this file (2026-09-19).
- **Do not shorten official project titles.** On 2026-09-19 the MISTI title was shortened and, of all things, `advanced quantum photonic integrated circuits` was cut. **The canonical source is the award notification** (`OneDrive/MIT/Proposal/MIT-Imperial seed fund/Accepted/MIT_Global_Seed_Fund_Notification.pdf`), not the final report we wrote. The report dropped the tail `for etch-free integration process`, and the CV and site that followed it were writing the MISTI title identical to the NSF project title (user 09-22).

## Deploy and verify

On push, the `Deploy site` workflow builds and pushes to the `gh-pages` branch. The Pages source is that branch (not `main`).

```bash
SHA=$(git rev-parse HEAD)
until [ "$(gh run list --workflow='Deploy site' --limit 8 --json headSha,status \
  --jq "[.[] | select(.headSha==\"$SHA\")][0].status")" = "completed" ]; do sleep 15; done
gh run list --workflow='Deploy site' --limit 8 --json headSha,conclusion \
  --jq "[.[] | select(.headSha==\"$SHA\")][0]"
```

- **Select by commit hash when waiting.** `--limit 1` returns the previous run right after a push, so you mistake someone else's build for yours.
- **Do not trust the exit code of `gh run watch`.** It returns 0 even for a failed run. Read `conclusion`.
- After deploy, `python scripts/check_links.py` (all internal links), and if you touched publications, `python scripts/check_dois.py`.
- If the page looks unchanged, it is cache. Fetch with `?cb=$(date +%s)` appended and judge from that.

## Beating the theme CSS

The theme lives inside the gem and cannot be edited. `_includes/site_styles.liquid` overrides it on each page.
For templates, a local copy at the same path wins: `_layouts/bib.liquid` (single paper, 09-21 title link and buttons removed). If you upgrade the theme gem, diff against the new upstream.
**`!important` alone does not win.** The theme also uses `!important` in places, and then specificity decides.
That is why the number badge stayed white twice (the theme's `.publications ol.bibliography li .abbr abbr`
hardcodes the text color to the card background color). Read the actual rule first and match the selector:

```bash
curl -s https://yjinyoo.github.io/assets/css/main.css | grep -oE "<selector fragment>[^{]*\{[^}]*\}"
```

## Four generated outputs

| What | Script | When |
|---|---|---|
| Publication list + public CV | `scripts/sync_cv.py` (inside: `build_public_cv.py` → `update_publications.py`) | Always, whenever the CV was edited |
| Activity graphs (left: Project activity, right: Simulation runs) | `scripts/build_activity_svg.py` → `assets/img/activity.svg` + `simulations.svg` (drawing is `scripts/calendar_svg.py`) | Daily automatic (`refresh-activity.yml`) + **session wrap-up step 9** |
| tools page data | `scripts/update_tools.py` | Weekly automatic (`site-maintenance.yml`), manual when a new tool is published |
| Link card | `scripts/build_og_image.py` | When the intro wording changes |

**The activity graph is two images, with different sources and update paths.** The left (green) reads the contribution count of the public GitHub profile via daily Actions.
The right (blue) is drawn from `_data/simulation_runs.json`, and this file is produced only on the workstation
(`Simulations/tools/simulation_run_counter.py`; needs the cloud solver account, the local archive drive, and cluster access).
At session wrap-up `Simulations/tools/publish_simulation_runs.py` recounts and pushes **only two data files (JSON and the run-list CSV) and the two SVGs**.
- The two images use **the same week range**, width fixed at half a card (416 px), and the cell size shrinks with the number of weeks (September ≈ 11 px, December ≈ 7.5 px). So redrawing only one misaligns left and right. Commit both together.
- The range starts **from the month the GitHub record starts** (March for 2026). Even though simulations started earlier, do not align to that (user 09-21). Each image's number is the whole year, so the 2,216 runs in January-February are only in the number, not in the graph. The original GitHub calendar was also "graph from the first active month, number for the whole year".
- The simulation side is drawn only up to the counted date. Drawing blanks after that becomes a claim of "did not run".
- The simulation count includes **only finished runs** (cloud `success`, cluster COMPLETED with at least 60 s, excluding `_` names).
- Do not use the solver dashboard number (13,733 on 09-21): it includes drafts that were only quoted and never run. Where records of runs deleted for server capacity survive: the counter's header comment.
- **Names and wording (user 09-21 finalized):** the left name is `Project activity`, with `GitHub contributions` next to the number to state the source. About 45 % of this year's commits are in the harness repo, which is why the caption includes `the shared tooling behind them`. Remove it and "Project" becomes an inflated word. `Code` (too narrow, since measurement and growth records are in there too) and `Commits` (the user asked what it meant) were rejected. On public pages, no solver product names, cluster names, or direct phrases like "cloud FDTD". Write the kinds **as examples ("including ...") and do not pin them to a count** (user 09-21: pinning it at three makes it look not diverse). But the examples must be only what was actually counted: FDTD, FEM (cluster FEniCSx, counted separately from DFT since 2026-10-01), mode analysis, inverse design (adjoint FDTD runs), DFT. State that local runs are excluded. Captions are **2-3 sentences, with left and right line counts matched by rendering with the actual site CSS** (user 09-21. Our own mockup had a different font and was off by one line). The link to the per-date count file was removed: it gives visitors no new information and takes them to an internal document in a public repo.
**Instead, the run-list page `/simulation-runs/` (user 09-21 evening):** the right calendar and the caption number link here. Each line is date, kind, short ID (first 8 characters of the cloud task ID, cluster job ID), so the number can be spot-checked. Job names are private (`D:/Tidy3D_archive/finished_runs.csv`), they contain NDA and unpublished design values. The data is `assets/data/simulation_runs.csv`, written by the counter, which does not write if the line count differs from the total. Do not show per-kind totals on the page (see "do not pin them to three" above). Do not write that the source of the simulation number is "GitHub records": the source is the job records, and GitHub only receives the per-date count file.

In `_data/tools.yml`, **do not hand-edit the fields GitHub knows (`description`/`language`/`pushed`).**
The script overwrites them. Only `title`/`summary`/`body` are hand-written.

The weekly check (`site-maintenance.yml`) is two jobs of different nature. `tools` heals itself (update →
commit → redeploy), `checks` (internal links + DOI + site vs CV) needs a person to fix, so **it reports as a failure.**

The left activity graph reads only **public** contributions of the GitHub profile. If `Private contributions` in the profile settings is turned off,
an almost empty graph comes out, and that is not a bug but a fact of the public profile.

## Page roles (2026-09-19 user finalized)

- **about** = impact on the first screen. Do not defer content to research. Most readers read only this far.
- **research** = the same topics in more depth. It differs from about **by depth, not length** (e.g., Landau-Devonshire is only in research).
- **publications** = journal papers + a book chapters section below. Numbering is **the CV numbering as is** (oldest is 1). Do not write the count here (`check_cv_match.py` measures it).
- **cv** = record + PDF. The user knows the MIT entries overlap with research and decided to leave it.

## Known pitfalls

- **Word COM sometimes hangs.** On 09-19 it was unresponsive twice, 09-20 and 09-21 succeeded. The method that worked on 09-21: copy the docx outside OneDrive (scratch), open it read-only with `Documents.Open(src, False, True, False)`, `ExportAsFixedFormat(out, 17)`, and wrap the whole thing in `Start-Job` + `Wait-Job -Timeout 150` to cut it off if it hangs. It worked even while the user had another document open in Word.
- **Put journal volume and pages in the `journal` string.** The layout does not render the volume/pages fields, and `additional_info` in between goes through markdownify, which strips the leading space and appends a line break.
- **Do not link coauthors.** The theme paints them in the accent color, so in my own publication list the corresponding author becomes the most prominent.
- **OpenAlex has merged 7 people with the same name into one author record.** Separate them by coauthor network + MIT affiliation. When a new collaboration appears, coauthors do not overlap so it may be dropped; check the rejection list in `curate.py`.
