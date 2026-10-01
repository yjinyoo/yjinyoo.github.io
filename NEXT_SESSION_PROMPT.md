# NEXT SESSION: Homepage

The site is public and working: <https://yjinyoo.github.io>
**Read `CLAUDE.md` first.** What not to do and how to verify a deploy are there.

## Status (2026-09-21)

| Page | Status |
|---|---|
| about | Intro, 3 lines on what I do, design loop, activity (left Project activity · right Simulation runs, captions 4 lines each), contact. Link to tools at the end of the loop paragraph. Right calendar and number → `/simulation-runs/` run list (09-21) |
| research | 3 device projects, funded projects (since MIT, cross-checked with the CV) |
| publications | Journal papers + book chapters section. **Number, year, volume, pages, co-first authorship are read from the CV** (since 09-21). No descriptive text. **Title is the DOI link, no buttons** (user 09-21, local copy `_layouts/bib.liquid`) |
| tools | 7 public repos. Rendered from `_data/tools.yml` |
| cv | Positions, degrees (graduate only, B.S. only in the CV: user 09-21), **Fellowships / Awards separated**, PDF. Dates and items cross-checked with the CV |

No broken internal links. Paper and DOI counts are not written here: `check_cv_match.py` and `check_dois.py` measure them.

## What runs on its own (no need to touch)

| When | What | File |
|---|---|---|
| Daily | Refresh activity graph, redeploy if changed | `.github/workflows/refresh-activity.yml` |
| Daily 23:30 + every session wrap-up | Recount the simulation side of the activity graph + **run-list CSV** + push (workstation scheduled task `SimulationRunsPublish`, not Actions). Cluster job kinds are split by job name: `fem_` = FEM, the rest = DFT (10-01). If you run a new kind on the cluster, add it to the counter's `cluster_kind()` | `Simulations/tools/publish_simulation_runs.py` |
| Weekly Mon | Refresh tools data from GitHub, commit + redeploy if changed | `.github/workflows/site-maintenance.yml` |
| Weekly Mon | Internal links + DOI + publication list vs CV. **Reports as a failure because it needs a person to fix** | same file |
| Always | Visit analytics (country, page, referrer) | Cloudflare Web Analytics, turned on 09-20 |

If the weekly check is red, that is this project's next task. First see which job failed:
the `tools` job is built to heal itself, so a failure there is a GitHub API or permission problem; if the `checks` job
failed, a link or DOI is actually broken, or only one of the CV and the publication list was regenerated.

## When a new tool is published

1. Add one block to `_data/tools.yml` (`repo` / `title` / `summary` / `body`)
2. `python scripts/update_tools.py`: the script fills the fields GitHub knows. **Do not write them by hand**
3. Push and verify the deploy

`summary` is the clause shown as one line in the list. `body` is two paragraphs: what it does, and **which failure
it catches.** The second is the value of this page.

## If the CV was edited (new paper, project, award, position, even one typo)

**The CV first, the site follows.** Full rules in `CLAUDE.md` "CV and site linkage".

1. Edit the CV original (OneDrive `Career/CV/` docx). For a paper, including the `Co-first author` mark
2. `python scripts/sync_cv.py`: PDF export → public CV → regenerate publication list → full site cross-check
3. If the cross-check fails, that line is the task. If a new project, award, or position appeared, write wording on the cv/research page
   (dates and names exactly as in the CV). Then `python scripts/check_cv_match.py` again
4. Look at `git diff`, commit and push, verify the deploy

For an online-first paper without volume and pages, writing just `(2026)` in the CV is fine. When volume and pages come out, edit only the CV and sync.
If you edit the CV and forget to sync, the Simulations session-start hook notifies.

## When writing (2026-09-19, three user corrections)

1. **Do not hardcode a specific language into public material.** Not just wording, code too. The tokenizer had the Hangul syllable range
   hardcoded, and **characters outside it produce no tokens at all, so they do not even show up as "none" in the results.**
   Keep only the structure and let the writer supply the language.
2. **Do not write sentences that guide the reader.** The kind like "this line is worth reading twice", "this deserves a line
   of its own". They preempt what the next sentence should do on its own. Also do not mention that private code exists.
3. **No unexplained jargon.** `recall@K` was written as is and the user asked what it meant.
   The fact that they asked is the answer. **09-21, second time:** `Commits` was recommended as the activity calendar name and got the same question.
   Before offering candidate public wording, first filter on "would a visitor from outside the field know this word without explanation".

## Open items

1. **The CV original and the public version now match (resolved 09-20).** The GIST postdoc end date in the docx was fixed,
   and Word COM succeeded at conversion this time and produced a new `Curriculum Vitae_YJYOO_Sep_2026.pdf`.
   `DEFAULT_SRC` in `build_public_cv.py` points to that file and `CORRECTIONS` is **empty.**
   Do not fill it again: if a correction is needed, the original is wrong and the place to fix is the original.
   ⚠ If items removed from the site cv page remain in the original, they diverge again. When editing public wording,
   check the original as well.
2. **Things only the user can do by hand so far:** GitHub profile Website field, Google Scholar Homepage field,
   LinkedIn Contact info. The lab member page (`jeehwanlab.mit.edu`) link is on an MIT domain so it has the
   largest effect, but it has to be requested from the administrator.
   **These three come before visit analytics.** Even with analytics on, there is nothing to look at without traffic,
   and these three must be linked for referrers to separate out in Cloudflare.
3. **Search visibility.** Ownership verification and sitemap submission are done. Check indexing with `site:yjinyoo.github.io`
   first and judge from that.
4. **10 patents, 15 international conference talks.** In the CV, not on the site. Recommended adding patents only; no answer yet.
5. **cv page MIT entries duplicate research.** The user knows and decided to leave it. Do not bring it up first.

## Public repos

Currently seven: `beol-eo-prescreen`, `refcheck`, `harness-budget`, `fab-check`, `device-assert`,
`resonance-extract`, `mpi-env-check`.

**Do not pick candidates from a list; scan the folder.** On 09-20 `resonance-extract` was missing, because
only the two candidate lists in the handoff were looked at and taken as everything. Scanning `tools/` directly turned up two more.
The remaining candidate is `gds_lint` (3 BLOCKs are shallow: one line mentioning a foundry NDA, one line with an internal path).

**What we decided not to publish.** Seven figure tools (user instruction, including the `house_check` family);
the bonding photo → GDS item was held back because **even with all dimensions removed from the code, the workflow itself remains, and that is
the method of an unpublished project.** A generalized version exists only locally at `~/bondmap/bondmap.py`.

**The Origin MCP is not ours.** It is a clone of `youngminsw/Origin-Pro-MCP` (MIT, 39 stars, on PyPI),
and 124 of 141 commits are the original author's. **Our 17 commits are not upstream**
(batch tool, house style, 13 fixes from a full review). The answer is not a new repo but an **upstream PR**,
and whether to submit it as one chunk or split it is a matter to sit down with separately. It is also stronger to cite on the homepage.

## 5 internal-version migrations (in a Simulations session)

Canonical = the 2026-09-19 section of `Simulations/harness/known_issues.md` + earlier records.

- **Unconditional, right away:** the bug where layer thickness comes out short by one sample spacing (`tools/device_assert.py`),
  two false positives in the leak checker (`tools/leak_check.py`)
- **Conditional:** the three reference tools. The handoff says "run the public version on a real proof first", but the
  **intent** of that condition is "do not break the path verified on the Science format". A single proof is one format anyway,
  so it only half satisfies the intent. **Making about ten reference lists in formats that print titles and formats that do not,
  and running them on both versions** is cheaper and covers more.
