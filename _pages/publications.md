---
layout: page
permalink: /publications/
title: publications
nav: true
nav_order: 3
---

{% include site_styles.liquid %}

{% include bib_search.liquid %}

<div class="publications">

{% bibliography --query @article %}

<h2 class="bibliography">book chapter</h2>

{% bibliography --query @incollection --group_by none %}

</div>
