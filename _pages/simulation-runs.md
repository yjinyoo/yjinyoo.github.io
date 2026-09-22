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
  <button id="runs-more" type="button" hidden></button>
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
    text-align: left;
    padding: .18rem 1.6rem .18rem 0;
    border-bottom: 1px solid rgba(128, 128, 128, .18);
  }
  .runs-list td:last-child {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }
  .runs-list #runs-more {
    margin: 1rem 0;
    padding: .4rem 1rem;
    border: 1px solid rgba(128, 128, 128, .5);
    border-radius: 6px;
    background: transparent;
    color: inherit;
    font-size: .88rem;
    cursor: pointer;
  }
  .runs-list #runs-more:hover {
    border-color: var(--global-theme-color);
    color: var(--global-theme-color);
  }
</style>

<script>
  (() => {
    // Rows come straight from the CSV a visitor can download, so the page and the file cannot differ.
    const LABEL = { fdtd: "FDTD", mode_solver: "mode solving", dft: "DFT" };
    const PAGE = 1000; // rows per "show more"; the first screen stays light
    const body = document.getElementById("runs-body");
    const status = document.getElementById("runs-status");
    const filter = document.getElementById("runs-filter");
    const moreButton = document.getElementById("runs-more");
    const fmt = (n) => n.toLocaleString("en-US");
    let rows = [];
    let summary = "";
    let limit = PAGE;

    const render = () => {
      const q = filter.value.trim().toLowerCase();
      const hits = q ? rows.filter((r) => r.text.includes(q)) : rows;
      const shown = Math.min(limit, hits.length);
      const frag = document.createDocumentFragment();
      hits.slice(0, shown).forEach((r) => {
        const tr = document.createElement("tr");
        [r.date, LABEL[r.kind] || r.kind, r.id].forEach((v) => {
          const td = document.createElement("td");
          td.textContent = v;
          tr.appendChild(td);
        });
        frag.appendChild(tr);
      });
      body.replaceChildren(frag);
      const left = hits.length - shown;
      const part = left > 0 ? `, newest ${fmt(shown)} shown` : "";
      status.textContent = q ? `${fmt(hits.length)} matching rows${part}.` : `${summary}${part}.`;
      moreButton.hidden = left <= 0;
      moreButton.textContent = `Show ${fmt(Math.min(PAGE, left))} more (${fmt(left)} not shown)`;
    };

    fetch("{{ '/assets/data/simulation_runs.csv' | relative_url }}")
      .then((r) => {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      })
      .then((text) => {
        rows = text
          .trim()
          .split(/\r?\n/)
          .slice(1)
          .map((line) => {
            const [date, kind, id] = line.split(",");
            return { date, kind, id, text: `${date} ${kind} ${LABEL[kind] || ""} ${id}`.toLowerCase() };
          })
          .reverse();
        // Total only: a per-kind breakdown would read as "three kinds of simulation" (CLAUDE.md).
        summary = `${rows.length.toLocaleString("en-US")} rows`;
        render();
        filter.addEventListener("input", () => {
          limit = PAGE; // a new filter starts from the newest rows again
          render();
        });
        moreButton.addEventListener("click", () => {
          limit += PAGE;
          render();
        });
      })
      .catch(() => {
        status.textContent = "The list could not be loaded; the CSV link above has it.";
      });
  })();
</script>
