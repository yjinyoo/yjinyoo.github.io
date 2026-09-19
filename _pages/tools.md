---
layout: page
permalink: /tools/
title: tools
description: Open-source pieces of the design loop. Each one exists because something got through without it.
nav: true
nav_order: 4
---

{% include site_styles.liquid %}

Most of what runs the loop is project code and stays private. These survive
without the project: two screens a design has to pass before it costs anything to
simulate, a check a manuscript has to pass before it is submitted, and the
instrumentation for the agent harness that runs all of them.

A theme runs through them. Each one separates a check that passed from a check
that never ran, because the second reads like the first and is the one that gets
through.

#### Electro-optic prescreen

Three closed-form checks to run before the electrostatic sweep and before any
full-wave simulation of a membrane electro-optic modulator. What fraction of the
drive voltage lands on the active film, what field survives at the mode center for
a slanted electrode pair, and what confinement factor and index shift follow from a
mode solve. Nothing here needs a mesh, and each returns in well under a second.

A back-end-of-line stack puts a thick low-permittivity cladding in series with a
thin high-permittivity film, and capacitors in series divide the voltage by
thickness over permittivity: 800 nm of oxide above a 100 nm film leaves 57 mV of a
3.3 V drive on the film, 1.7 percent, while every plot downstream still looks
reasonable. Slanted electrodes fail less visibly than that. A mirror-symmetric pair
driven push-pull holds the potential identically zero along the mode axis, so the
field there is exactly zero by symmetry rather than by geometry, which no mesh
refinement will reveal: the sweep completes, every point returns a valid field, and
the modulation is zero.

[github.com/yjinyoo/beol-eo-prescreen](https://github.com/yjinyoo/beol-eo-prescreen)

#### Fab-grain check

Looks a design value up against what the process can actually give, before the
value is locked, and reads a cached file of process constraints to do it. It is
advisory rather than blocking, because a constraint file is always incomplete
and a screen that refuses to run is a screen that gets switched off.

The verdict that matters is not the one that fails. A material has an entry, so
the lookup succeeds; that entry happens to carry an orientation policy and no
thickness rule, so nothing numeric is evaluated; and a naive tool prints a pass.
The caller reads "within cached constraints" and locks the number. So there are
four verdicts here, and `NO CONSTRAINT`, meaning the entry exists but this
property was never cached, is reported as distinct from `OK`. One more case is
worth its own rule: a process offers a few sidewall angles rather than a
continuum, so a sweep that optimizes to 22 degrees has optimized to an angle
nobody can etch. A range cannot catch that. A set can.

[github.com/yjinyoo/fab-check](https://github.com/yjinyoo/fab-check)

#### Reference audit

Checks a numbered reference list against CrossRef, OpenAlex and Semantic Scholar,
and separates three outcomes that a single index cannot tell apart: an entry found
but printed with the wrong volume, page or year; an entry held by no index at all;
and an entry that could not be scored, which is not a pass. Input is a proof PDF,
in which the reference list is located automatically, or a plain text list.

One index is not enough because a real paper missing from CrossRef, which happens
for preprints, conference papers and older society journals, looks exactly like a
reference nobody ever wrote. Both land in the same bucket, and at proof stage the
reference numbers are often the last thing still correctable. Entries printed
without titles, as in the Science style, are matched on journal, volume and first
page instead, which is an exact key even with the title missing.

[github.com/yjinyoo/refcheck](https://github.com/yjinyoo/refcheck)

#### Harness budget

Four checks for a coding-agent harness that loads files into context automatically:
which of those files are over their size budget, whether a file-based memory store
is internally consistent, whether every path the documents name still exists, and
recall@K for retrieving the right memory from a question.

A harness accumulates, and nothing in the loop reports what it costs. These numbers
used to be typed into the rules file by hand, and they were wrong for weeks: a byte
count read as a character count put one file at 86 percent over budget when it was
12 percent over. Counting is in characters, never bytes, because one Korean
character is three bytes in UTF-8 and `wc -c` reports three times what the context
window actually sees.

[github.com/yjinyoo/harness-budget](https://github.com/yjinyoo/harness-budget)
