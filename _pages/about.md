---
layout: about
title: about
permalink: /
subtitle: Postdoctoral researcher, <a href="https://www.rle.mit.edu/">Research Laboratory of Electronics</a>, MIT. <a href="https://jeehwanlab.mit.edu/">Jeehwan Kim Group</a>.

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false
  more_info: >
    <p>Room 38-276</p>
    <p>Massachusetts Institute of Technology</p>
    <p>50 Vassar Street</p>
    <p>Cambridge, MA 02139</p>

selected_papers: false
social: true

announcements:
  enabled: false

latest_posts:
  enabled: false
---

{% include site_styles.liquid %}

**Membrane-based integrated photonics. Multi-physics simulation-driven design-to-fab.**

I build active photonic devices on silicon. Silicon does not host the materials that modulate, emit, or store light, so I release those materials as single-crystalline freestanding membranes, transfer them onto CMOS-compatible platforms, and design and fabricate the resulting devices in house or by CMOS foundry tape-out. The most immediate applications are optical interconnects and co-packaged optics for computing, but the same approach reaches resonant-cavity LED microdisplays and quantum photonic integrated circuits.

#### What I work on

- Complex oxides, lithium niobate and barium titanate, for low-voltage electro-optic modulators built on photonic-crystal cavities
- III-V and III-N for on-chip lasers and resonant-cavity LEDs, integrated as coupons at high density
- Heterogeneous integration onto CMOS, photonic ICs, and other platforms through 2D-material-assisted epitaxy and transfer

I work in the [Jeehwan Kim group](https://jeehwanlab.mit.edu/) at MIT, and am co-advised by [Dirk R. Englund](https://qp.mit.edu/) on the CMOS integrated photonics work. [Current projects and funding](/research/).

#### From target to measured device, one loop

Deep research sets the target and the benchmark to beat. Coupled, cross-validated multi-physics simulation derives the device and its fabrication window, inside the CMOS design rules, with inverse design and machine-learning surrogates. Fabrication realizes that window, with DFT-guided interface engineering and membrane transfer. Device and optical measurement, read out with coupled-mode theory, closes the loop and calibrates the model.

Across the design stage: TCAD for devices, DFT for materials, FEM for electrostatics and mechanics, and FDTD, RCWA, mode solving and ray optics for photonics. Each pass de-risks the next fabrication and sharpens the model.

#### Activity

<div style="border:1px solid rgba(128,128,128,.35); border-radius:10px; padding:1.1rem 1.25rem; margin:1.2rem 0 1.6rem;">
  <div style="display:flex; align-items:baseline; justify-content:space-between; flex-wrap:wrap; gap:.5rem; margin-bottom:.9rem;">
    <strong style="font-size:1.02rem;">Contribution activity</strong>
    <a href="https://github.com/yjinyoo" target="_blank" rel="noopener" style="font-size:.85rem;">github.com/yjinyoo</a>
  </div>
  <a href="https://github.com/yjinyoo" target="_blank" rel="noopener" aria-label="GitHub profile">
    <img src="{{ '/assets/img/activity.svg' | relative_url }}"
         alt="Contribution activity for the current year"
         style="width:100%; max-width:540px; display:block;">
  </a>
  <p style="font-size:.95rem; line-height:1.65; margin:1rem 0 0; opacity:.85;">
    Each square is one day, darkening with the number of commits: simulations, mask
    layouts, process flows, and the analysis behind the work above. Almost every
    repository is private, so the days fill in without naming what is in them, and the
    count covers what reaches version control, not time in the cleanroom.
  </p>
</div>

Reach me at <a href="mailto:yjyoo@mit.edu">yjyoo@mit.edu</a>.
