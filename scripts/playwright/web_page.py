# -*- coding: utf-8 -*-
"""Wrapper de sección para la pista de Playwright (web build)."""
from playwright.cover import PW_TOC_ITEMS, PW_GROUPS


def page_web_pw(eyebrow, num, title, body):
    return f'''<section class="content-section pw-section" id="sec-{num}" data-track="playwright">
      <div class="section-eyebrow">{eyebrow}</div>
      <h1 class="section-title"><span class="num-chip pw-chip">{num.replace("pw-", "")}</span> {title}</h1>
      {body}
    </section>'''


def sidebar_nav_pw():
    by_num = {num: (title, desc) for num, title, desc in PW_TOC_ITEMS}
    out = ['<nav id="sidebar-nav-pw">']
    for label, nums in PW_GROUPS:
        out.append(f'<div class="sidebar-group-label">{label}</div>')
        for n in nums:
            title, _ = by_num[n]
            display_n = n.replace("pw-", "")
            out.append(
                f'<a href="#sec-{n}" data-target="sec-{n}">'
                f'<span class="num">{display_n}</span><span>{title}</span></a>'
            )
    out.append('</nav>')
    return "".join(out)
