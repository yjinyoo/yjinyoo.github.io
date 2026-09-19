---
layout: page
permalink: /research/
title: research
description: What I build at MIT, and the funded projects it runs under.
nav: true
nav_order: 2
---

{% include site_styles.liquid %}

Silicon does not host the materials that modulate, emit, or store light. Those
materials are released as single-crystalline freestanding membranes, transferred
onto CMOS-compatible platforms, and the resulting devices are designed and
fabricated in house or by CMOS foundry tape-out.

## Research projects

What is actually being built.

#### Electro-optic modulators on complex-oxide membranes

Lithium niobate and barium titanate have the Pockels coefficients a modulator
needs, and neither grows on silicon. Grown on a lattice-matched substrate and
released as a membrane, the film can be placed on a silicon photonic platform,
including the back end of a finished CMOS wafer where nothing can be grown at
temperature. Built into photonic-crystal cavities, nanobeams and microrings, the
same phase shift is reached over a far shorter interaction length, which is what
brings the drive voltage toward the logic supply. The work covers PLD growth,
crystallographic orientation and interface engineering, and DFT-guided defect
and oxygen-vacancy control.

#### On-chip light sources from III-V and III-N membranes

Silicon does not emit. Compound semiconductor membranes integrated as coupons,
many small pieces at high density rather than whole bonded wafers, give lasers
and resonant-cavity LEDs on a silicon platform without spending III-V area where
it is not needed. A low-order cavity around a thin emitter narrows the spectrum
and steers the pattern, which decides how much of the light survives coupling
into a waveguide or a fiber.

#### Heterogeneous integration onto CMOS and photonic ICs

The transfer step decides whether any of the above survives a process flow.
Remote and 2D-material-assisted epitaxy grows the film through an intervening
layer so it registers to the substrate lattice yet releases cleanly, and the
substrate can be reused. Whether release is clean is an interface problem, which
is where first-principles calculation earns its cost.

#### The design-to-fab loop

Scope the target and the benchmark to beat. Design the device and its
fabrication window by coupled, cross-validated multi-physics simulation inside
the CMOS design rules, with inverse design and machine-learning surrogates.
Build it with DFT-guided interface engineering and membrane transfer. Prove it
by device and optical measurement read out with coupled-mode theory. Each pass
calibrates the model and de-risks the next fabrication run. Across the design
stage: TCAD for devices, DFT for materials, FEM for electrostatics and
mechanics, and FDTD, RCWA, mode solving and ray optics for photonics.

These feed optical interconnects and co-packaged optics for computing,
resonant-cavity LED microdisplays, and quantum photonic integrated circuits. Our
review of co-packaged optics for high-performance computing and AI is in
[Nature Electronics](https://doi.org/10.1038/s41928-026-01681-6) (2026).

## Funded projects

The grants the work runs under.

#### TOPCHIP: photonic integrated circuit testing and heterogeneous device integration for quantum information science

*Feb 2026 to present. Quantum Information Sciences Branch, Air Force Research
Laboratory Information Directorate (AFRL/RITQ), US Air Force. Principal
investigator: Prof. Dirk R. Englund.*

Photonic integrated circuit testing and heterogeneous device integration, with
the design and fabrication of membrane-based active photonic devices carried out
jointly between the Kim and Englund groups.

#### Pre-patterned freestanding single-crystalline lithium niobate photonic components for advanced quantum photonic integrated circuits

*Sep 2024 to present. Electronics, Photonics and Magnetic Devices (EPMD),
National Science Foundation. Principal investigator: Prof. Jeehwan Kim.*

Proposal preparation and day-to-day charge of the project, developing
pre-patterned lithium niobate photonic components.

#### Pre-patterned freestanding single-crystalline lithium niobate photonic components for advanced quantum photonic integrated circuits

*May 2024 to Jan 2026. MIT-Imperial College London Seed Fund, MIT Global Seed
Funds (MISTI). Principal investigator: Prof. Jeehwan Kim. International
collaborator: Prof. Myungshik Kim, Imperial College London.*

The seed-fund collaboration behind the project above, assessing the feasibility
of an etch-free route to freestanding lithium niobate components for quantum
photonic circuits: MIT on materials growth and membrane fabrication, Imperial on
the modeling. Proposal preparation and reporting.

#### Entire-life implantable nanomesh brain-machine integration interface for neurological disorders

*Jul 2024 to present. STEAM Research Business, Korea Global Cooperative
Convergence Research Program, National Research Foundation of Korea, funded by
the Ministry of Science and ICT. Principal investigator: Prof. Jeehwan Kim.*

Proposal preparation and day-to-day charge of the project, developing a
neuronal-resolution micro-LED array.
