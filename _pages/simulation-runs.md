---
layout: page
permalink: /simulation-runs/
title: simulation runs
description: Every run counted in the activity calendar on the front page.
nav: false
---

{% include site_styles.liquid %}
{% assign sims = site.data.simulation_runs %}

{{ sims.total_display }} finished runs since {{ sims.first_month | append: "-01" | date: "%B %Y" }},
one row each. A run is counted once it finished: a cloud job that returned its result, or a cluster
job that completed and ran for more than a minute. Drafts, failed jobs and runs on local machines are
not listed.

The id is the first eight hex digits of the cloud task id, or the cluster job id, so any row can be
matched against the provider's records on request. Task names are withheld because they carry design
parameters of unpublished work. Rows dated by month only come from the first archive, in 2025, which
kept the month and not the day.

<a href="{{ '/assets/data/simulation_runs.csv' | relative_url }}" download>Download the list (CSV)</a>

<div class="runs-list">
  <input id="runs-filter" type="search" placeholder="Filter by date, kind or id (e.g. 2026-08, dft)"
         aria-label="Filter the list">
  <p id="runs-status">Loading the list.</p>
  <table>
    <thead><tr><th>date</th><th>kind</th><th>id</th></tr></thead>
    <tbody id="runs-body"></tbody>
  </table>
</div>

<style>
  .runs-list input {
    width: 100%;
    max-width: 26rem;
    padding: .45rem .7rem;
    border: 1px solid rgba(128, 128, 128, .5);
    border-radius: 6px;
    background: transparent;
    color: inherit;
    margin: 1rem 0 .4rem;
  }
  .runs-list #runs-status {
    font-size: .88rem;
    opacity: .75;
    margin-bottom: .6rem;
  }
  .runs-list table {
    border-collapse: collapse;
    font-size: .9rem;
  }
  .runs-list th,
  .runs-list td {
    /* The theme drew the kind column in the accent colour, which reads as a link. */
    color: var(--global-text-color) !important;
    text-align: left;
    padding: .18rem 1.6rem .18rem 0;
    border-bottom: 1px solid rgba(128, 128, 128, .18);
  }
  .runs-list td:last-child {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }
</style>

<script>
  (() => {
    // Rows come straight from the CSV a visitor can download, so the page and the file cannot differ.
    const LABEL = { fdtd: "FDTD", mode_solver: "mode solving", dft: "DFT" };
    const SHOWN = 1000; // enough to browse; the CSV has every row
    const body = document.getElementById("runs-body");
    const status = document.getElementById("runs-status");
    const filter = document.getElementById("runs-filter");
    let rows = [];
    let summary = "";

    const render = () => {
      const q = filter.value.trim().toLowerCase();
      const hits = q ? rows.filter((r) => r.text.includes(q)) : rows;
      const frag = document.createDocumentFragment();
      hits.slice(0, SHOWN).forEach((r) => {
        const tr = document.createElement("tr");
        [r.date, LABEL[r.kind] || r.kind, r.id].forEach((v) => {
          const td = document.createElement("td");
          td.textContent = v;
          tr.appendChild(td);
        });
        frag.appendChild(tr);
      });
      body.replaceChildren(frag);
      const n = hits.length.toLocaleString("en-US");
      const more = hits.length > SHOWN ? `, newest ${SHOWN.toLocaleString("en-US")} shown` : "";
      status.textContent = q ? `${n} matching rows${more}.` : `${summary}${more}.`;
    };

    fetch("{{ '/assets/data/simulation_runs.csv' | relative_url }}")
      .then((r) => {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      })
      .then((text) => {
        rows = text
          .trim()
          .split("\n")
          .slice(1)
          .map((line) => {
            const [date, kind, id] = line.split(",");
            return { date, kind, id, text: `${date} ${kind} ${LABEL[kind] || ""} ${id}`.toLowerCase() };
          })
          .reverse();
        // Total only: a per-kind breakdown would read as "three kinds of simulation" (CLAUDE.md).
        summary = `${rows.length.toLocaleString("en-US")} rows`;
        render();
        filter.addEventListener("input", render);
      })
      .catch(() => {
        status.textContent = "The list could not be loaded; the CSV link above has it.";
      });
  })();
</script>
