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

**<span style="white-space:nowrap">Membrane-based</span> integrated photonics.**<br>
**<span style="white-space:nowrap">Multi-physics</span> <span style="white-space:nowrap">simulation-driven</span> <span style="white-space:nowrap">design-to-fab</span>.**

I build active photonic devices on silicon. Silicon does not host the materials that modulate, emit, or store light, so I release those materials as single-crystalline freestanding membranes, transfer them onto CMOS-compatible platforms, and design and fabricate the resulting devices in house or by CMOS foundry tape-out. The most immediate applications are optical interconnects and co-packaged optics for computing, but the same approach reaches resonant-cavity LED microdisplays and quantum photonic integrated circuits.

#### What I work on

- Complex oxides, lithium niobate and barium titanate, for low-voltage electro-optic modulators built on photonic-crystal cavities
- III-V and III-N for on-chip lasers and resonant-cavity LEDs, integrated as coupons at high density
- Heterogeneous integration onto CMOS, photonic ICs, and other platforms through 2D-material-assisted epitaxy and transfer

I work in the [Jeehwan Kim group](https://jeehwanlab.mit.edu/) at MIT, and am co-advised by [Dirk R. Englund](https://qp.mit.edu/) on the CMOS integrated photonics work. [Current projects and funding](/research/).

#### From target to measured device, one loop

Deep research sets the target and the benchmark to beat. Coupled, cross-validated multi-physics simulation derives the device and its fabrication window, inside the CMOS design rules, with inverse design and machine-learning surrogates. Fabrication realizes that window, with DFT-guided interface engineering and membrane transfer. Device and optical measurement, read out with coupled-mode theory, closes the loop and calibrates the model. The loop is scripted end to end and run by coding agents. [Open-source tools](/tools/).

Across the design stage: TCAD for devices, DFT for materials, FEM for electrostatics and mechanics, and FDTD, RCWA, mode solving and ray optics for photonics. Each pass de-risks the next fabrication and sharpens the model.

#### Activity

{% assign sims = site.data.simulation_runs %}
<div style="border:1px solid rgba(128,128,128,.35); border-radius:10px; padding:1.1rem 1.25rem; margin:1.2rem 0 1.6rem;">
  <div style="display:flex; gap:1.5rem; flex-wrap:wrap; font-size:.85rem; line-height:1.55;">
    <div style="flex:1 1 360px; min-width:0;">
      <a href="https://github.com/yjinyoo" target="_blank" rel="noopener" aria-label="GitHub profile">
        <img src="{{ '/assets/img/activity.svg' | relative_url }}"
             alt="GitHub activity per day for the current year"
             style="width:100%; height:auto; display:block; margin-bottom:.8rem;">
      </a>
      <p style="margin:0; opacity:.8;">
        <span aria-hidden="true" style="display:inline-block; width:.7em; height:.7em; border-radius:2px; background:#55a87e; margin-right:.35em;"></span><strong>Project activity.</strong>
        Design, simulation and fabrication scripting, measurement analysis, and the
        shared tooling behind them, across every project. Counted from GitHub
        contributions, mostly to private repositories.
      </p>
    </div>
    <div style="flex:1 1 360px; min-width:0;">
      <img src="{{ '/assets/img/simulations.svg' | relative_url }}"
           alt="Finished simulation runs per day for the current year"
           style="width:100%; height:auto; display:block; margin-bottom:.8rem;">
      <p style="margin:0; opacity:.8;">
        <span aria-hidden="true" style="display:inline-block; width:.7em; height:.7em; border-radius:2px; background:#256abf; margin-right:.35em;"></span><strong>Simulation runs.</strong>
        {{ sims.total_display }} finished jobs on cloud and HPC clusters since
        {{ sims.first_month | append: "-01" | date: "%B %Y" }}, including FDTD, mode
        solving, inverse design and DFT. Runs on local machines and failed jobs are not counted.
      </p>
    </div>
  </div>
</div>

Reach me at <a href="mailto:yjyoo@mit.edu">yjyoo@mit.edu</a> or <a href="mailto:yjyoo0601@gmail.com">yjyoo0601@gmail.com</a>.

{% include person_schema.liquid %}
