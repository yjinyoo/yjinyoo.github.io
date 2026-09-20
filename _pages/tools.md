---
layout: page
permalink: /tools/
title: tools
description: Open-source pieces of the design loop. Each one exists because something got through without it.
nav: true
nav_order: 4
---

{% include site_styles.liquid %}

Screens a design has to pass before it costs anything to simulate, checks a result and a
manuscript have to pass before they go out, and the instrumentation for the agent harness
and the cluster that run them.

<ul style="margin:1.2rem 0 1.8rem; padding-left:1.1rem;">
{%- for tool in site.data.tools %}
  <li style="margin-bottom:.35rem;">
    <a href="#{{ tool.repo }}"><strong>{{ tool.title }}</strong></a>:
    {{ tool.summary }}
  </li>
{%- endfor %}
</ul>

{% for tool in site.data.tools %}
<h4 id="{{ tool.repo }}">{{ tool.title }}</h4>

<p style="font-size:.88rem; opacity:.75; margin:-.4rem 0 .9rem;">
  {{ tool.language }} &nbsp;·&nbsp; updated {{ tool.pushed }} &nbsp;·&nbsp;
  <a href="https://github.com/yjinyoo/{{ tool.repo }}">github.com/yjinyoo/{{ tool.repo }}</a>
</p>

{{ tool.body | markdownify }}
{% endfor %}
