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

`_bibliography/papers.bib` is generated, not hand-written. To refresh it after a
new paper appears:

```
python scripts/update_publications.py
```

That does five things:

1. `fetch_pubs.py` pulls every work OpenAlex attributes to ORCID
   0000-0002-6490-2324.
2. `curate.py` separates the real record from the other researchers named Young
   Jin Yoo that OpenAlex has merged into the same author ID. It keeps a work if
   it shares a co-author with the GIST photonics community or if the MIT
   affiliation is on the authorship. **Check its printed drop list** whenever a
   new co-author group appears, because a genuinely new collaboration has no
   shared co-author yet and will be dropped until the affiliation catches it.
3. `make_bib.py` writes the BibTeX. `selected={true}` controls which papers show
   on the front page. The rule is first-author with 20+ citations, or a leading
   slot (top six) at a Nature-family venue, or 200+ citations. Citation count on
   its own is deliberately not enough: it would promote large group papers where
   the contribution was one author slot out of twenty.
4. `fix_stale.py` applies manual corrections where OpenAlex is behind the
   publisher. There is one right now: the Gires-Tournois monopixel paper, which
   OpenAlex still lists only as a Research Square preprint with the author order
   scrambled.
5. `check_dois.py` resolves every DOI against Crossref. `NOT FOUND` means the
   link is dead. `UNRESOLVED` means the check itself failed and the DOI is
   simply unchecked, which is not the same as passing.

## Hosting a PDF of a paper

The `pdf` field on an entry points at a free copy where one exists, which is why
21 of the 43 entries have one. Do not add a publisher PDF for a paywalled paper:
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
