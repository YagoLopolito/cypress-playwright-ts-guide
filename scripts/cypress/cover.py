# -*- coding: utf-8 -*-
"""Portada e índice del documento."""

def cover():
    return '''
    <div class="page cover">
      <div class="cover-top">
        <span class="cover-kicker">GUÍA TÉCNICA · QA / AUTOMATION</span>
        <div class="cover-title">Cypress<br/>+ <span class="accent">TypeScript</span></div>
        <div class="cover-sub">Guía completa desde cero: instalación, fundamentos de
        JavaScript/TypeScript, selectores CSS, comandos esenciales, buenas prácticas
        y ejecución en CI/CD.</div>
      </div>
      <div class="cover-mid">
        <div class="cover-pills">
          <span class="cover-pill">Instalación paso a paso</span>
          <span class="cover-pill">Repaso de JS/TS</span>
          <span class="cover-pill">Tutorial de selectores CSS</span>
          <span class="cover-pill">Buenas prácticas</span>
          <span class="cover-pill">Page Object Model</span>
          <span class="cover-pill">CI/CD</span>
        </div>
      </div>
      <div class="cover-bottom">
        <div class="cover-logo">cypress<span class="dot">.</span>ts</div>
        <div>Documento informativo para onboarding de equipo</div>
      </div>
    </div>
    '''


TOC_ITEMS = [
    ("1", "¿Qué es Cypress?", "Arquitectura, comparación con Selenium y Playwright"),
    ("2", "Repaso rápido de JavaScript y TypeScript", "Lo mínimo indispensable antes de empezar"),
    ("3", "Instalación del entorno completo", "Node, npm, Cypress y TypeScript desde cero"),
    ("4", "Primer proyecto Cypress + TypeScript", "Tu primer test corriendo"),
    ("5", "Selectores CSS: la base para encontrar elementos", "Tutorial completo de CSS aplicado a testing"),
    ("6", "Anatomía de un test en Cypress", "describe, it, hooks y el encadenamiento de comandos"),
    ("7", "Comandos esenciales de Cypress", "Tabla de referencia rápida"),
    ("8", "Aserciones (assertions)", "should, expect y retry-ability"),
    ("9", "Fixtures y datos de prueba", "Datos de prueba tipados con TypeScript"),
    ("10", "Comandos personalizados", "Custom commands y su tipado en TS"),
    ("11", "Interceptación de red con cy.intercept", "Mockear y controlar requests HTTP"),
    ("12", "Page Object Model con TypeScript", "Organizar selectores en clases reutilizables"),
    ("13", "Buenas prácticas", "Las reglas que evitan tests frágiles"),
    ("14", "Errores comunes a evitar", "Los tropiezos más frecuentes"),
    ("15", "Ejecutar en CI/CD", "Modo headless, GitHub Actions y reportes"),
    ("16", "Cheat sheet final y recursos", "Referencia compacta para el día a día"),
]


def toc():
    items = ""
    for num, title, desc in TOC_ITEMS:
        items += f'''<li>
          <span class="toc-num">{num}</span>
          <span class="toc-text">{title}</span>
          <span class="toc-desc">{desc}</span>
        </li>'''
    return f'''
    <div class="page toc">
      <div class="toc-title">Índice</div>
      <div class="toc-sub">16 secciones — de cero a producción</div>
      <ul class="toc-list">{items}</ul>
    </div>
    '''
