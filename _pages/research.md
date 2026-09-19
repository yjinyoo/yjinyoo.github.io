---
layout: page
permalink: /research/
title: research
description: Active photonic devices built from freestanding single-crystalline membranes, and the design-to-fabrication loop behind them.
nav: true
nav_order: 2
---

Silicon photonics is built from a material that neither modulates nor emits light
well. The materials that do, complex oxides and compound semiconductors, do not
grow on silicon. My work is on getting them there anyway, as freestanding
single-crystalline membranes, and on designing the devices that result so they
survive a real process flow.

#### Low-voltage electro-optic modulation from complex-oxide membranes

Lithium niobate and barium titanate have large Pockels coefficients, which is
what a modulator needs, and neither grows on silicon. Grown instead on a
lattice-matched substrate and released as a membrane, the film can be transferred
onto a silicon photonic platform, including the back end of a finished CMOS
wafer, where nothing can be grown at temperature.

Put into a photonic-crystal cavity, the same phase shift is reached over a much
shorter interaction length, which is what brings the drive voltage down toward
the logic supply. The design question is where the field actually falls: the
fraction of the drive voltage that lands across the active film, and the overlap
between the optical mode and that film, decide the answer well before anything is
fabricated.

The ultra-thin-film lithium niobate side of this is joint with the
[Englund group](https://qp.mit.edu/) at MIT RLE.

#### On-chip light sources from III-V and III-N membranes

Silicon does not emit, so a light source has to be brought in. Compound
semiconductor membranes integrated as coupons, many small pieces at high density
rather than whole bonded wafers, give lasers and resonant-cavity LEDs on a
silicon platform without spending III-V area on the parts of the chip that do not
need it.

A low-order cavity built around a thin emitter narrows the emission spectrum and
steers the pattern. That matters as soon as the light has to couple into a
waveguide or a fiber, where a broad Lambertian emitter wastes most of what it
makes.

#### Heterogeneous integration onto CMOS

The transfer step decides whether any of the above survives contact with a
process flow. Remote epitaxy grows the film through an intervening
two-dimensional layer, so the film registers to the substrate lattice yet
releases from it cleanly, and the substrate can be reused.

Whether release is clean is an interface problem, and it is one where
first-principles calculation earns its cost: what sits between the film and the
substrate governs both the epitaxial registry and the separation energy. Our work
on improving remote epitaxy of perovskite complex oxides is in
[ACS Nano](https://doi.org/10.1021/acsnano.4c09445) (2024).

#### How the design work runs

Every device above is decided by more than one kind of physics at once, so the
simulations have to be coupled and cross-validated rather than run in isolation:
TCAD for carrier transport, density functional theory for interfaces, finite
element for electrostatics and mechanics, and FDTD, RCWA, mode solving and ray
optics for the photonics. The output that matters is not a single optimum but a
fabrication window, stated inside the design rules of the process that will build
it, and narrow enough to be worth taping out.

Measurement closes the loop. A resonance read out with coupled-mode theory
calibrates the model, and each pass de-risks the next fabrication.
