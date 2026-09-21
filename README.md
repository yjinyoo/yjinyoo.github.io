# yjinyoo.github.io

Personal academic site for Young Jin Yoo, built on the
[al-folio](https://github.com/alshedivat/al-folio) Jekyll theme and served by
GitHub Pages at <https://yjinyoo.github.io>.

## Editing

| What you want to change | File |
| --- | --- |
| Bio on the front page | `_pages/about.md` |
| Name, site title, description, URL | `_config.yml` |
| Email, ORCID, Scholar, GitHub, LinkedIn | `_data/socials.yml` |
| Profile photo | `assets/img/prof_pic.jpg` |
| News items on the front page | `_news/announcement_*.md` |
| Publication list | `_bibliography/papers.bib` |
| Co-author links, venue badge colors | `_data/coauthors.yml`, `_data/venues.yml` |

Push to `main` and the `Deploy site` GitHub Action rebuilds and publishes. There
is no local build step; nothing needs Ruby on your machine.

## Publication list

`_bibliography/papers.bib` is generated, not hand-written, and the CV is its
source. What counts as a paper, its number, year, volume and pages, and equal
first authorship are read from `assets/pdf/cv.pdf` by `scripts/cv_record.py`.
OpenAlex only fills in what the CV does not carry (full author names, DOI,
abstract, open-access link). The one deliberate departure from the CV is declared
in `cv_record.SITE_YEAR`.

When a new paper appears:

1. Add it to the CV (the Word original), export the PDF.
2. `python scripts/build_public_cv.py` writes `assets/pdf/cv.pdf` without the
   phone number, then reports that the publication list no longer matches.
3. `python scripts/update_publications.py` regenerates the list.

`update_publications.py` does five things:

1. `fetch_pubs.py` pulls every work OpenAlex attributes to ORCID
   0000-0002-6490-2324.
2. `curate.py` separates the real record from the other researchers named Young
   Jin Yoo that OpenAlex has merged into the same author ID. It keeps a work if
   it shares a co-author with the GIST photonics community or if the MIT
   affiliation is on the authorship. **Check its printed drop list** whenever a
   new co-author group appears, because a genuinely new collaboration has no
   shared co-author yet and will be dropped until the affiliation catches it.
   It also merges journal cover and frontispiece records into the paper they
   illustrate.
3. `make_bib.py` matches every record to exactly one CV entry and writes the
   BibTeX; if any record or CV entry is left unmatched, it writes nothing and
   lists them. Records OpenAlex lacks go in `ADDITIONS`, records where it is
   behind the publisher in `OVERRIDES`. `selected={true}` controls which papers
   show on the front page. The rule is first-author with 20+ citations, or a
   leading slot (top six) at a Nature-family venue, or 200+ citations. Citation
   count on its own is deliberately not enough: it would promote large group
   papers where the contribution was one author slot out of twenty. Book chapters
   are written as `@incollection` and listed after the papers, unnumbered.
4. `check_dois.py` resolves every DOI against Crossref. `NOT FOUND` means the
   link is dead. `UNRESOLVED` means the check itself failed and the DOI is
   simply unchecked, which is not the same as passing.
5. `check_cv_match.py` compares the written list with the CV once more: count,
   and each number's title, year, volume, pages and equal first authorship. The
   weekly `Site maintenance` run repeats it, since the two files can drift when
   only one of them is rebuilt.

## Hosting a PDF of a paper

The `pdf` field on an entry points at a free copy where one exists, which is why
only some entries have one. Do not add a publisher PDF for a paywalled paper:
Wiley, Elsevier, ACS and Springer Nature all forbid redistributing the typeset
version. The accepted manuscript is usually allowed after an embargo. Check the
journal at <https://openpolicyfinder.jisc.ac.uk/> before adding a file to
`assets/pdf/`.

## Adding a CV

The CV page is switched off (`al_folio.features.cv.enabled: false` in
`_config.yml`) because it needs dates that are not in the publication record.
Two ways to turn it back on:

- Drop a PDF at `assets/pdf/cv.pdf` and uncomment `cv_pdf` in
  `_data/socials.yml`. A CV icon then appears under the profile photo.
- Or set the feature back to `true`, restore `_pages/cv.md` and `_data/cv.yml`
  from the al-folio template, and fill in the entries.
