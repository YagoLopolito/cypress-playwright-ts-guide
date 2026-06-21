# -*- coding: utf-8 -*-
"""
Orquestador principal.
Genera dist/index.html con ambas pistas (Cypress + Playwright) en un solo HTML,
con un switcher de pista en el sidebar.
"""
import re
import sys
import os

# ---------------------------------------------------------------------------
# Path setup
# Order matters: shared first (helpers.py), then scripts root (for package imports),
# then cypress (so its local diagrams.py / helpers.py resolve correctly).
# Playwright is imported as a package via scripts root, NOT added to sys.path directly.
# ---------------------------------------------------------------------------
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED_DIR  = os.path.join(SCRIPTS_DIR, "shared")
CYPRESS_DIR = os.path.join(SCRIPTS_DIR, "cypress")

# Build sys.path: shared → scripts root → cypress
for p in [CYPRESS_DIR, SCRIPTS_DIR, SHARED_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ---------------------------------------------------------------------------
# Importar pista Cypress
# (content files live in cypress/ and import helpers/diagrams from same dir)
# ---------------------------------------------------------------------------
import content_part1 as cy_p1
import content_part2 as cy_p2
import content_part3 as cy_p3
import content_part4 as cy_p4
import web_page as cy_web_page
from web_page import sidebar_nav as cypress_sidebar_nav
from playground import playground_html as cypress_playground_html

# ---------------------------------------------------------------------------
# Importar pista Playwright
# (imported as package; helpers resolved via SHARED_DIR in sys.path)
# ---------------------------------------------------------------------------
import playwright.content_part1 as pw_p1
import playwright.content_part2 as pw_p2
import playwright.content_part3 as pw_p3
import playwright.content_part4 as pw_p4
import playwright.web_page as pw_web_page
from playwright.web_page import sidebar_nav_pw as playwright_sidebar_nav
from playwright.playground import pw_playground_html

# ---------------------------------------------------------------------------
# Importar shared: CSS, JS
# ---------------------------------------------------------------------------
from web_styles import CSS
from web_js import JS

# ---------------------------------------------------------------------------
# Monkeypatch Cypress sections → page_web wrapper con data-track="cypress"
# ---------------------------------------------------------------------------
def cy_page_web(eyebrow, num, title, body):
    return f'''<section class="content-section" id="sec-{num}" data-track="cypress">
      <div class="section-eyebrow">{eyebrow}</div>
      <h1 class="section-title"><span class="num-chip">{num}</span> {title}</h1>
      {body}
    </section>'''

cy_p1.page = cy_page_web
cy_p2.page = cy_page_web
cy_p3.page = cy_page_web
cy_p4.page = cy_page_web

# Playwright sections ya tienen data-track="playwright" desde su page_web_pw()
pw_p1.page = pw_web_page.page_web_pw
pw_p2.page = pw_web_page.page_web_pw
pw_p3.page = pw_web_page.page_web_pw
pw_p4.page = pw_web_page.page_web_pw

# ---------------------------------------------------------------------------
# Renderizar secciones Cypress
# ---------------------------------------------------------------------------
cy_sections_fns = [
    cy_p1.section_01, cy_p1.section_02, cy_p1.section_03, cy_p1.section_04,
    cy_p2.section_05, cy_p2.section_06, cy_p2.section_07, cy_p2.section_08,
    cy_p3.section_09, cy_p3.section_10, cy_p3.section_11, cy_p3.section_12,
    cy_p4.section_13, cy_p4.section_14, cy_p4.section_15, cy_p4.section_16,
]
cy_sections_html = [s() for s in cy_sections_fns]

# Inject CSS playground into section 5 (index 4)
cy_sections_html[4] = cy_sections_html[4].replace(
    "</section>", cypress_playground_html() + "</section>", 1
)

# ---------------------------------------------------------------------------
# Renderizar secciones Playwright
# ---------------------------------------------------------------------------
pw_sections_fns = [
    pw_p1.section_pw_01, pw_p1.section_pw_02, pw_p1.section_pw_03, pw_p1.section_pw_04,
    pw_p2.section_pw_05, pw_p2.section_pw_06, pw_p2.section_pw_07, pw_p2.section_pw_08,
    pw_p3.section_pw_09, pw_p3.section_pw_10, pw_p3.section_pw_11, pw_p3.section_pw_12,
    pw_p4.section_pw_13, pw_p4.section_pw_14, pw_p4.section_pw_15, pw_p4.section_pw_16,
]
pw_sections_html = [s() for s in pw_sections_fns]

# Inject Playwright playground into section 5 (index 4)
pw_sections_html[4] = pw_sections_html[4].replace(
    "</section>", pw_playground_html() + "</section>", 1
)

# ---------------------------------------------------------------------------
# Combinar todas las secciones
# ---------------------------------------------------------------------------
all_sections_html = "\n".join(cy_sections_html) + "\n" + "\n".join(pw_sections_html)

# ---------------------------------------------------------------------------
# Post-process: checklists interactivas + tablas scrollables
# ---------------------------------------------------------------------------
_counter = [0]


def _li_to_checkbox(m):
    inner = m.group(1).strip()
    _counter[0] += 1
    key = f"item-{_counter[0]}"
    return (
        '<li><label class="check-item">'
        f'<input type="checkbox" data-key="{key}">'
        '<span class="check-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>'
        f'<span class="check-text">{inner}</span>'
        '</label></li>'
    )


def make_checklists_interactive(html: str) -> str:
    li_pattern = re.compile(r"<li>(.*?)</li>", re.DOTALL)

    def repl_ul(m):
        ul_inner = m.group(1)
        count = len(li_pattern.findall(ul_inner))
        new_inner = li_pattern.sub(_li_to_checkbox, ul_inner)
        progress_div = f'<div class="checklist-progress">0 / {count} completados</div>'
        return progress_div + f'<ul class="checklist">{new_inner}</ul>'

    return re.sub(r'<ul class="checklist">(.*?)</ul>', repl_ul, html, flags=re.DOTALL)


def wrap_tables_scrollable(html: str) -> str:
    return re.sub(
        r'(<table class="ref-table">.*?</table>)',
        r'<div class="table-scroll">\1</div>',
        html,
        flags=re.DOTALL,
    )


all_sections_html = make_checklists_interactive(all_sections_html)
all_sections_html = wrap_tables_scrollable(all_sections_html)

# ---------------------------------------------------------------------------
# SVG / Icon constants
# ---------------------------------------------------------------------------
ICON_HAMBURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>'
ICON_SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'
ICON_MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>'
ICON_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>'

# ---------------------------------------------------------------------------
# Sidebar con switcher + ambos navs
# ---------------------------------------------------------------------------
sidebar_html = f'''
<div class="track-switcher">
  <button class="track-btn active" data-track="cypress" type="button">
    <span class="track-label-badge" data-track="cypress">C</span>
    Cypress
  </button>
  <button class="track-btn" data-track="playwright" type="button">
    <span class="track-label-badge" data-track="playwright">PW</span>
    Playwright
  </button>
</div>
{cypress_sidebar_nav()}
{playwright_sidebar_nav()}
'''

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
header_html = f'''
<div id="progress-bar"></div>
<header class="topbar">
  <button class="menu-toggle" id="menu-toggle" type="button" aria-label="Abrir menú">{ICON_HAMBURGER}</button>
  <div class="topbar-logo"><span class="topbar-logo-badge">E2E</span><span class="full">testing<span class="dot">.</span>ts</span></div>
  <div class="search-wrap">
    <span class="search-icon">{ICON_SEARCH}</span>
    <input type="text" id="searchInput" placeholder="Buscar en la guía... ( / )" autocomplete="off">
    <div class="search-nav" id="searchNav">
      <button id="searchPrev" type="button" aria-label="Resultado anterior">‹</button>
      <span id="searchCount">0/0</span>
      <button id="searchNext" type="button" aria-label="Resultado siguiente">›</button>
    </div>
  </div>
  <div class="topbar-actions">
    <button class="icon-btn" id="theme-toggle" type="button" aria-label="Cambiar tema claro/oscuro">{ICON_SUN}{ICON_MOON}</button>
  </div>
</header>
<div class="overlay-backdrop" id="overlay-backdrop"></div>
'''

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
hero_html = '''
<div class="hero">
  <span class="hero-kicker">Guía interactiva · QA / Automation</span>
  <h1>Cypress <span class="accent">+</span> Playwright <span class="accent">+ TypeScript</span></h1>
  <p class="lead">Guía completa con dos pistas independientes: aprendé Cypress o Playwright desde cero,
  con playgrounds interactivos, checklists de progreso, búsqueda en toda la guía y tema claro/oscuro.
  Usá los botones del sidebar para cambiar de pista.</p>
  <div class="hero-pills">
    <span class="hero-pill">🧪 Playgrounds interactivos</span>
    <span class="hero-pill">☑️ Checklists con progreso guardado</span>
    <span class="hero-pill">🔎 Búsqueda en toda la página</span>
    <span class="hero-pill">🌓 Tema claro / oscuro</span>
    <span class="hero-pill">📋 Copiar código con un click</span>
    <span class="hero-pill">🔀 Switcher Cypress / Playwright</span>
  </div>
</div>
'''

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
footer_html = '''
<div class="content-section" style="padding-top:14px;">
  <div class="end-box">
    <h3>¡Listo! Ya tenés la base completa</h3>
    <p>Desde la instalación hasta buenas prácticas de equipo. Cambiá de pista cuando quieras
    comparar Cypress y Playwright, tildá la checklist a medida que avanzás, y usá el playground
    para practicar en vivo. Tu progreso queda guardado en el navegador.</p>
  </div>
</div>
'''

# ---------------------------------------------------------------------------
# Ensamblar HTML final
# ---------------------------------------------------------------------------
html = f'''<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cypress + Playwright + TypeScript — Guía interactiva</title>
<style>{CSS}</style>
</head>
<body>
{header_html}
<div class="layout">
  <aside class="sidebar">{sidebar_html}</aside>
  <main class="content">
    {hero_html}
    {all_sections_html}
    {footer_html}
  </main>
</div>
<button id="back-to-top" type="button" aria-label="Volver arriba">{ICON_UP}</button>
<script>{JS}</script>
</body>
</html>'''

# ---------------------------------------------------------------------------
# Escribir output
# ---------------------------------------------------------------------------
out_dir = os.path.join(SCRIPTS_DIR, "..", "dist")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "index.html")

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML generado: {os.path.abspath(out_path)} ({len(html):,} caracteres)")
