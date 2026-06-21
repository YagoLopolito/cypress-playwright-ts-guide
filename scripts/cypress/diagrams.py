# -*- coding: utf-8 -*-
"""Diagramas SVG originales para el documento (sin usar logos ni assets de terceros)."""

FONT = "font-family='Liberation Sans, Arial, sans-serif'"

# ---------------------------------------------------------------------------
# 1) Arquitectura: Cypress corre en el mismo run-loop que la app
# ---------------------------------------------------------------------------
ARCH_DIAGRAM = """
<svg viewBox="0 0 680 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="680" height="280" fill="#ffffff"/>
  <rect x="20" y="20" width="640" height="240" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="40" y="46" font-size="12" font-weight="700" fill="#0f172a" font-family="Liberation Sans, Arial, sans-serif">NAVEGADOR (Chrome / Electron / Firefox)</text>

  <rect x="45" y="60" width="270" height="175" rx="8" fill="#0f172a"/>
  <text x="180" y="85" font-size="11.5" font-weight="700" fill="#5eead4" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">PROCESO DE CYPRESS</text>
  <text x="180" y="103" font-size="9" fill="#cbd5e1" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">Test Runner + comandos cy.*</text>
  <rect x="65" y="118" width="230" height="40" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="180" y="135" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">describe / it / before...</text>
  <text x="180" y="150" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">cy.get(), cy.click(), cy.type()...</text>
  <rect x="65" y="168" width="230" height="40" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="180" y="185" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">Acceso directo al DOM,</text>
  <text x="180" y="200" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">window, network, etc.</text>

  <rect x="365" y="60" width="270" height="175" rx="8" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="500" y="85" font-size="11.5" font-weight="700" fill="#0f766e" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">TU APLICACIÓN (AUT)</text>
  <text x="500" y="103" font-size="9" fill="#0f766e" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">Application Under Test</text>
  <rect x="385" y="118" width="230" height="90" rx="5" fill="#ffffff" stroke="#99f6e4"/>
  <text x="500" y="145" font-size="9" fill="#334155" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">React / Angular / Vue / HTML</text>
  <text x="500" y="163" font-size="9" fill="#334155" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">corriendo en un iframe,</text>
  <text x="500" y="181" font-size="9" fill="#334155" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">dentro de la misma pestaña</text>

  <line x1="315" y1="148" x2="365" y2="148" stroke="#0d9488" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="365" y1="178" x2="315" y2="178" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow2)"/>
  <text x="340" y="138" font-size="7.3" fill="#0d9488" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">controla</text>
  <text x="340" y="195" font-size="7.3" fill="#94a3b8" text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif">observa</text>

  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#0d9488"/></marker>
    <marker id="arrow2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker>
  </defs>
</svg>
"""

# ---------------------------------------------------------------------------
# 2) Estructura de carpetas
# ---------------------------------------------------------------------------
def folder_tree():
    lines = [
        (0, "mi-proyecto/", True),
        (1, "cypress/", True),
        (2, "e2e/", True),
        (3, "login.cy.ts", False),
        (3, "checkout.cy.ts", False),
        (2, "fixtures/", True),
        (3, "usuarios.json", False),
        (2, "support/", True),
        (3, "commands.ts", False),
        (3, "e2e.ts", False),
        (2, "pages/", True),
        (3, "LoginPage.ts", False),
        (1, "cypress.config.ts", False),
        (1, "tsconfig.json", False),
        (1, "package.json", False),
    ]
    h = 26 + len(lines) * 19 + 14
    svg = [f'<svg viewBox="0 0 560 {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect x="0" y="0" width="560" height="{h}" fill="#0f172a" rx="8"/>')
    y = 32
    for depth, name, is_dir in lines:
        x = 24 + depth * 22
        color = "#5eead4" if is_dir else "#e2e8f0"
        weight = "700" if is_dir else "400"
        icon = "📁" if False else ("▸" if is_dir else "·")
        prefix = '<tspan fill="#475569">' + ("│  " * 0) + '</tspan>'
        svg.append(f'<text x="{x}" y="{y}" font-size="10.5" font-family="DejaVu Sans Mono, monospace" fill="{color}" font-weight="{weight}">{"📂 " if is_dir else "📄 "}{name}</text>')
        y += 19
    svg.append("</svg>")
    return "".join(svg)

FOLDER_TREE = folder_tree()

# ---------------------------------------------------------------------------
# 3) Especificidad CSS
# ---------------------------------------------------------------------------
SPECIFICITY_DIAGRAM = """
<svg viewBox="0 0 660 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="660" height="200" fill="#ffffff"/>
  <text x="20" y="24" font-size="11" font-weight="700" fill="#0f172a" font-family="Liberation Sans, Arial, sans-serif">De menor a mayor especificidad →</text>
  <line x1="20" y1="40" x2="640" y2="40" stroke="#cbd5e1" stroke-width="2"/>
  <polygon points="640,40 632,36 632,44" fill="#cbd5e1"/>

  <g>
    <circle cx="60" cy="100" r="34" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2"/>
    <text x="60" y="98" font-size="10" text-anchor="middle" fill="#334155" font-family="DejaVu Sans Mono, monospace">div</text>
    <text x="60" y="111" font-size="8" text-anchor="middle" fill="#64748b" font-family="Liberation Sans, Arial, sans-serif">elemento</text>
    <text x="60" y="150" font-size="8.3" text-anchor="middle" fill="#64748b" font-family="Liberation Sans, Arial, sans-serif">(0,0,0,1)</text>
  </g>
  <g>
    <circle cx="220" cy="100" r="38" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
    <text x="220" y="97" font-size="9.5" text-anchor="middle" fill="#1e3a8a" font-family="DejaVu Sans Mono, monospace">.card</text>
    <text x="220" y="111" font-size="8" text-anchor="middle" fill="#1e3a8a" font-family="Liberation Sans, Arial, sans-serif">clase</text>
    <text x="220" y="153" font-size="8.3" text-anchor="middle" fill="#64748b" font-family="Liberation Sans, Arial, sans-serif">(0,0,1,0)</text>
  </g>
  <g>
    <circle cx="390" cy="100" r="42" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="390" y="92" font-size="9" text-anchor="middle" fill="#78350f" font-family="DejaVu Sans Mono, monospace">[data-cy=</text>
    <text x="390" y="104" font-size="9" text-anchor="middle" fill="#78350f" font-family="DejaVu Sans Mono, monospace">"submit"]</text>
    <text x="390" y="118" font-size="8" text-anchor="middle" fill="#78350f" font-family="Liberation Sans, Arial, sans-serif">atributo</text>
    <text x="390" y="157" font-size="8.3" text-anchor="middle" fill="#64748b" font-family="Liberation Sans, Arial, sans-serif">(0,0,1,0)</text>
  </g>
  <g>
    <circle cx="560" cy="100" r="46" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="560" y="92" font-size="9" text-anchor="middle" fill="#7f1d1d" font-family="DejaVu Sans Mono, monospace">#main-nav</text>
    <text x="560" y="106" font-size="8" text-anchor="middle" fill="#7f1d1d" font-family="Liberation Sans, Arial, sans-serif">ID</text>
    <text x="560" y="160" font-size="8.3" text-anchor="middle" fill="#64748b" font-family="Liberation Sans, Arial, sans-serif">(0,1,0,0)</text>
  </g>
</svg>
"""

# ---------------------------------------------------------------------------
# 4) Combinadores CSS
# ---------------------------------------------------------------------------
COMBINATORS_DIAGRAM = """
<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg">
<style>.b{font-family:'DejaVu Sans Mono',monospace;font-size:9.5px;} .l{font-family:'Liberation Sans',Arial,sans-serif;font-size:8.3px;fill:#64748b;}</style>
  <!-- descendant -->
  <text x="10" y="20" class="b" fill="#0f172a" font-weight="700">.form .input</text>
  <text x="10" y="34" class="l">descendiente (en cualquier nivel)</text>
  <rect x="10" y="44" width="150" height="60" rx="5" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="20" y="58" class="b" fill="#334155">.form</text>
  <rect x="20" y="64" width="60" height="32" rx="4" fill="#dbeafe" stroke="#2563eb"/>
  <text x="26" y="83" class="b" fill="#1e3a8a" font-size="8">.input</text>

  <!-- child -->
  <text x="220" y="20" class="b" fill="#0f172a" font-weight="700">.list &gt; li</text>
  <text x="220" y="34" class="l">hijo directo</text>
  <rect x="220" y="44" width="150" height="74" rx="5" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="230" y="58" class="b" fill="#334155">.list</text>
  <rect x="230" y="64" width="130" height="22" rx="3" fill="#dbeafe" stroke="#2563eb"/>
  <text x="236" y="79" class="b" fill="#1e3a8a" font-size="8">li (hijo directo)</text>
  <rect x="230" y="90" width="130" height="20" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-dasharray="2,2"/>
  <text x="236" y="103" class="b" fill="#94a3b8" font-size="7.5">li &gt; span (nieto, NO matchea)</text>

  <!-- adjacent sibling -->
  <text x="430" y="20" class="b" fill="#0f172a" font-weight="700">label + input</text>
  <text x="430" y="34" class="l">hermano adyacente</text>
  <rect x="430" y="44" width="70" height="26" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="438" y="61" class="b" fill="#334155" font-size="8">label</text>
  <rect x="510" y="44" width="70" height="26" rx="4" fill="#dbeafe" stroke="#2563eb"/>
  <text x="520" y="61" class="b" fill="#1e3a8a" font-size="8">input</text>
  <text x="498" y="62" font-size="13" fill="#0d9488">→</text>

  <!-- general sibling -->
  <text x="10" y="150" class="b" fill="#0f172a" font-weight="700">h2 ~ p</text>
  <text x="10" y="164" class="l">hermanos generales (todos los p siguientes)</text>
  <rect x="10" y="174" width="60" height="24" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="20" y="190" class="b" fill="#334155" font-size="8">h2</text>
  <rect x="80" y="174" width="60" height="24" rx="4" fill="#dbeafe" stroke="#2563eb"/>
  <text x="90" y="190" class="b" fill="#1e3a8a" font-size="8">p</text>
  <rect x="150" y="174" width="60" height="24" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="158" y="190" class="b" fill="#334155" font-size="8">img</text>
  <rect x="220" y="174" width="60" height="24" rx="4" fill="#dbeafe" stroke="#2563eb"/>
  <text x="230" y="190" class="b" fill="#1e3a8a" font-size="8">p</text>

  <!-- pseudo -->
  <text x="330" y="150" class="b" fill="#0f172a" font-weight="700">li:nth-child(2)</text>
  <text x="330" y="164" class="l">pseudo-clase posicional</text>
  <rect x="330" y="174" width="36" height="24" fill="#f1f5f9" stroke="#94a3b8"/>
  <rect x="368" y="174" width="36" height="24" fill="#fee2e2" stroke="#dc2626"/>
  <rect x="406" y="174" width="36" height="24" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="336" y="190" class="b" fill="#334155" font-size="7.5">li</text>
  <text x="374" y="190" class="b" fill="#7f1d1d" font-size="7.5">li ✓</text>
  <text x="414" y="190" class="b" fill="#334155" font-size="7.5">li</text>
</svg>
"""

# ---------------------------------------------------------------------------
# 5) Ciclo de vida / hooks
# ---------------------------------------------------------------------------
LIFECYCLE_DIAGRAM = """
<svg viewBox="0 0 660 170" xmlns="http://www.w3.org/2000/svg">
<style>.t{font-family:'DejaVu Sans Mono',monospace;font-size:9.5px;} .d{font-family:'Liberation Sans',Arial,sans-serif;font-size:8px;fill:#64748b;}</style>
  <rect x="10" y="20" width="100" height="46" rx="6" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="60" y="40" class="t" text-anchor="middle" fill="#334155">before()</text>
  <text x="60" y="55" class="d" text-anchor="middle">1 vez, antes de todo</text>

  <rect x="140" y="20" width="120" height="46" rx="6" fill="#dbeafe" stroke="#2563eb"/>
  <text x="200" y="40" class="t" text-anchor="middle" fill="#1e3a8a">beforeEach()</text>
  <text x="200" y="55" class="d" text-anchor="middle">antes de cada it()</text>

  <rect x="290" y="10" width="160" height="100" rx="6" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="370" y="28" class="t" text-anchor="middle" fill="#0f766e" font-weight="700">it('caso 1')</text>
  <text x="370" y="48" class="t" text-anchor="middle" fill="#0f766e" font-weight="700">it('caso 2')</text>
  <text x="370" y="68" class="t" text-anchor="middle" fill="#0f766e" font-weight="700">it('caso 3')</text>
  <text x="370" y="92" class="d" text-anchor="middle">tus casos de prueba</text>

  <rect x="480" y="20" width="120" height="46" rx="6" fill="#fef3c7" stroke="#d97706"/>
  <text x="540" y="40" class="t" text-anchor="middle" fill="#78350f">afterEach()</text>
  <text x="540" y="55" class="d" text-anchor="middle">después de cada it()</text>

  <rect x="630" y="-1000" width="0" height="0"/>
  <line x1="110" y1="43" x2="140" y2="43" stroke="#94a3b8" stroke-width="2" marker-end="url(#a3)"/>
  <line x1="260" y1="43" x2="290" y2="43" stroke="#94a3b8" stroke-width="2" marker-end="url(#a3)"/>
  <line x1="450" y1="43" x2="480" y2="43" stroke="#94a3b8" stroke-width="2" marker-end="url(#a3)"/>

  <text x="370" y="135" class="d" text-anchor="middle" font-size="8.6" fill="#475569">El ciclo beforeEach → it → afterEach se repite para CADA test del bloque describe()</text>
  <rect x="180" y="145" width="380" height="1" fill="none"/>
  <defs><marker id="a3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
</svg>
"""

# ---------------------------------------------------------------------------
# 6) Page Object Model
# ---------------------------------------------------------------------------
POM_DIAGRAM = """
<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg">
<style>.t{font-family:'DejaVu Sans Mono',monospace;} .d{font-family:'Liberation Sans',Arial,sans-serif;fill:#475569;}</style>
  <rect x="20" y="20" width="190" height="170" rx="7" fill="#0f172a"/>
  <text x="115" y="44" font-size="10.5" font-weight="700" fill="#5eead4" text-anchor="middle" class="d">login.cy.ts</text>
  <rect x="36" y="56" width="158" height="118" rx="5" fill="#1e293b"/>
  <text x="46" y="74" font-size="8" fill="#e2e8f0" class="t">it('loguea ok', () =&gt; {</text>
  <text x="52" y="90" font-size="8" fill="#93c5fd" class="t">loginPage</text>
  <text x="58" y="104" font-size="8" fill="#e2e8f0" class="t">.visit()</text>
  <text x="58" y="118" font-size="8" fill="#e2e8f0" class="t">.typeEmail(x)</text>
  <text x="58" y="132" font-size="8" fill="#e2e8f0" class="t">.typePass(y)</text>
  <text x="58" y="146" font-size="8" fill="#e2e8f0" class="t">.submit();</text>
  <text x="46" y="162" font-size="8" fill="#e2e8f0" class="t">});</text>

  <line x1="210" y1="105" x2="260" y2="105" stroke="#0d9488" stroke-width="2.5" marker-end="url(#a4)"/>
  <text x="235" y="97" font-size="7.5" fill="#0d9488" text-anchor="middle" class="d">usa</text>

  <rect x="260" y="20" width="190" height="170" rx="7" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="355" y="44" font-size="10.5" font-weight="700" fill="#0f766e" text-anchor="middle" class="d">LoginPage.ts</text>
  <rect x="276" y="56" width="158" height="118" rx="5" fill="#ffffff" stroke="#99f6e4"/>
  <text x="286" y="74" font-size="8" fill="#334155" class="t">class LoginPage {</text>
  <text x="294" y="90" font-size="8" fill="#0f766e" class="t">visit() {...}</text>
  <text x="294" y="104" font-size="8" fill="#0f766e" class="t">typeEmail(v) {...}</text>
  <text x="294" y="118" font-size="8" fill="#0f766e" class="t">typePass(v) {...}</text>
  <text x="294" y="132" font-size="8" fill="#0f766e" class="t">submit() {...}</text>
  <text x="286" y="160" font-size="8" fill="#334155" class="t">}</text>

  <line x1="450" y1="105" x2="500" y2="105" stroke="#0d9488" stroke-width="2.5" marker-end="url(#a4)"/>
  <text x="475" y="97" font-size="7.5" fill="#0d9488" text-anchor="middle" class="d">encapsula</text>

  <rect x="500" y="40" width="120" height="130" rx="7" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="560" y="60" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle" class="d">Selectores</text>
  <text x="560" y="76" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle" class="d">CSS reales</text>
  <text x="512" y="100" font-size="7.3" fill="#475569" class="t">[data-cy=email]</text>
  <text x="512" y="116" font-size="7.3" fill="#475569" class="t">[data-cy=pass]</text>
  <text x="512" y="132" font-size="7.3" fill="#475569" class="t">[data-cy=submit]</text>
  <text x="560" y="155" font-size="7.2" fill="#94a3b8" text-anchor="middle" class="d">(viven en un solo lugar)</text>

  <defs><marker id="a4" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#0d9488"/></marker></defs>
</svg>
"""

# ---------------------------------------------------------------------------
# 7) cy.intercept network flow
# ---------------------------------------------------------------------------
INTERCEPT_DIAGRAM = """
<svg viewBox="0 0 640 190" xmlns="http://www.w3.org/2000/svg">
<style>.t{font-family:'DejaVu Sans Mono',monospace;font-size:9px;} .d{font-family:'Liberation Sans',Arial,sans-serif;font-size:8.2px;fill:#64748b;}</style>
  <rect x="20" y="50" width="130" height="60" rx="6" fill="#ecfdf5" stroke="#0d9488"/>
  <text x="85" y="75" class="t" text-anchor="middle" fill="#0f766e" font-weight="700">Tu App</text>
  <text x="85" y="92" class="d" text-anchor="middle">hace fetch('/api/users')</text>

  <rect x="245" y="20" width="150" height="120" rx="6" fill="#0f172a"/>
  <text x="320" y="42" class="t" text-anchor="middle" fill="#5eead4" font-weight="700">cy.intercept()</text>
  <text x="320" y="60" class="d" text-anchor="middle" fill="#94a3b8">intercepta la</text>
  <text x="320" y="72" class="d" text-anchor="middle" fill="#94a3b8">request antes</text>
  <text x="320" y="84" class="d" text-anchor="middle" fill="#94a3b8">de que salga</text>
  <rect x="260" y="94" width="120" height="34" rx="4" fill="#1e293b"/>
  <text x="320" y="108" class="t" text-anchor="middle" fill="#fcd34d" font-size="7.6">GET /api/users</text>
  <text x="320" y="121" class="t" text-anchor="middle" fill="#86efac" font-size="7.6">→ fixture.json</text>

  <rect x="490" y="50" width="130" height="60" rx="6" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="555" y="73" class="t" text-anchor="middle" fill="#334155" font-weight="700">Servidor real</text>
  <text x="555" y="90" class="d" text-anchor="middle">(no se llega a tocar)</text>

  <line x1="150" y1="80" x2="245" y2="80" stroke="#0d9488" stroke-width="2.5" marker-end="url(#a5)"/>
  <line x1="395" y1="80" x2="490" y2="80" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="442" y="72" class="d" text-anchor="middle" fill="#94a3b8">bloqueada ✕</text>

  <line x1="320" y1="140" x2="320" y2="165" stroke="#0d9488" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#a5)"/>
  <rect x="200" y="165" width="240" height="22" rx="4" fill="#fffbeb" stroke="#d97706"/>
  <text x="320" y="180" class="t" text-anchor="middle" fill="#78350f" font-size="7.8">cy.wait('@getUsers') → test determinístico</text>

  <defs><marker id="a5" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#0d9488"/></marker></defs>
</svg>
"""
