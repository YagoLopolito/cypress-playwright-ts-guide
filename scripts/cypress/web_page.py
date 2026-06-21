# -*- coding: utf-8 -*-
"""Wrapper de sección para la versión web (reemplaza a content_part1.page para el build HTML)."""
from cover import TOC_ITEMS

GROUPS = [
    ("Fundamentos", ["1", "2"]),
    ("Puesta en marcha", ["3", "4"]),
    ("La base: CSS", ["5"]),
    ("El núcleo de Cypress", ["6", "7", "8"]),
    ("Organización", ["9", "10", "11", "12"]),
    ("Calidad y entrega", ["13", "14", "15"]),
    ("Referencia", ["16"]),
]


def page_web(eyebrow, num, title, body):
    return f'''<section class="content-section" id="sec-{num}">
      <div class="section-eyebrow">{eyebrow}</div>
      <h1 class="section-title"><span class="num-chip">{num}</span> {title}</h1>
      {body}
    </section>'''


def sidebar_nav():
    by_num = {num: (title, desc) for num, title, desc in TOC_ITEMS}
    out = ['<nav id="sidebar-nav">']
    for label, nums in GROUPS:
        out.append(f'<div class="sidebar-group-label">{label}</div>')
        for n in nums:
            title, _ = by_num[n]
            out.append(f'<a href="#sec-{n}" data-target="sec-{n}"><span class="num">{n}</span><span>{title}</span></a>')
    out.append('</nav>')
    return "".join(out)
