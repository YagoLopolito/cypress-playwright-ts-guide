# -*- coding: utf-8 -*-
"""Diagramas SVG para la pista de Playwright."""

# ---------------------------------------------------------------------------
# 1) Arquitectura: proceso Node controlando navegadores en paralelo
# ---------------------------------------------------------------------------
PW_ARCH_DIAGRAM = """
<svg viewBox="0 0 700 290" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="700" height="290" fill="#ffffff"/>
  <rect x="10" y="10" width="250" height="270" rx="10" fill="#0f172a"/>
  <text x="135" y="36" font-size="11" font-weight="700" fill="#a78bfa" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">PROCESO NODE.JS</text>
  <text x="135" y="52" font-size="8.5" fill="#94a3b8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Playwright Test runner</text>
  <rect x="26" y="64" width="218" height="44" rx="5" fill="#1e293b" stroke="#6d28d9"/>
  <text x="135" y="82" font-size="9" fill="#c4b5fd" text-anchor="middle" font-family="DejaVu Sans Mono,monospace">test('nombre', async ({ page })</text>
  <text x="135" y="97" font-size="9" fill="#c4b5fd" text-anchor="middle" font-family="DejaVu Sans Mono,monospace">await page.click(...)</text>
  <rect x="26" y="116" width="218" height="44" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="135" y="134" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Fixtures / test.extend()</text>
  <text x="135" y="149" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page Object Model</text>
  <rect x="26" y="168" width="218" height="44" rx="5" fill="#1e293b" stroke="#334155"/>
  <text x="135" y="186" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Protocolo propio (CDP/WebSocket)</text>
  <text x="135" y="201" font-size="9" fill="#e2e8f0" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">sin WebDriver</text>
  <text x="135" y="258" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">async/await nativo de Node</text>

  <!-- Chromium -->
  <rect x="310" y="14" width="168" height="80" rx="8" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="394" y="36" font-size="10.5" font-weight="700" fill="#0f766e" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Chromium</text>
  <rect x="326" y="46" width="136" height="34" rx="4" fill="#ffffff" stroke="#99f6e4"/>
  <text x="394" y="60" font-size="8.5" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">BrowserContext A</text>
  <text x="394" y="72" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page → test 1</text>

  <!-- Firefox -->
  <rect x="310" y="108" width="168" height="80" rx="8" fill="#fff7ed" stroke="#ea580c" stroke-width="1.5"/>
  <text x="394" y="130" font-size="10.5" font-weight="700" fill="#c2410c" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Firefox</text>
  <rect x="326" y="140" width="136" height="34" rx="4" fill="#ffffff" stroke="#fed7aa"/>
  <text x="394" y="154" font-size="8.5" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">BrowserContext B</text>
  <text x="394" y="166" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page → test 2</text>

  <!-- WebKit -->
  <rect x="310" y="202" width="168" height="80" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>
  <text x="394" y="224" font-size="10.5" font-weight="700" fill="#1d4ed8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">WebKit (Safari)</text>
  <rect x="326" y="234" width="136" height="34" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
  <text x="394" y="248" font-size="8.5" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">BrowserContext C</text>
  <text x="394" y="260" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page → test 3</text>

  <!-- Arrows -->
  <line x1="260" y1="54" x2="310" y2="54" stroke="#a78bfa" stroke-width="2" marker-end="url(#apw1)"/>
  <line x1="260" y1="148" x2="310" y2="148" stroke="#a78bfa" stroke-width="2" marker-end="url(#apw1)"/>
  <line x1="260" y1="242" x2="310" y2="242" stroke="#a78bfa" stroke-width="2" marker-end="url(#apw1)"/>
  <text x="285" y="48" font-size="7" fill="#a78bfa" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">controla</text>
  <text x="285" y="142" font-size="7" fill="#a78bfa" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">controla</text>
  <text x="285" y="236" font-size="7" fill="#a78bfa" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">controla</text>

  <!-- paralelo label -->
  <rect x="494" y="100" width="170" height="90" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="579" y="122" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">En paralelo</text>
  <text x="579" y="140" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Cada worker corre</text>
  <text x="579" y="154" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">su propio Browser</text>
  <text x="579" y="168" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Context aislado</text>
  <line x1="478" y1="54" x2="494" y2="140" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="478" y1="148" x2="494" y2="148" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="478" y1="242" x2="494" y2="158" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>

  <defs>
    <marker id="apw1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#a78bfa"/>
    </marker>
  </defs>
</svg>
"""

# ---------------------------------------------------------------------------
# 2) Browser → Context → Page (jerarquía de aislamiento)
# ---------------------------------------------------------------------------
PW_CONTEXT_DIAGRAM = """
<svg viewBox="0 0 660 240" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="660" height="240" fill="#ffffff"/>

  <!-- Browser -->
  <rect x="20" y="20" width="620" height="200" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="330" y="44" font-size="12" font-weight="700" fill="#0f172a" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Browser (instancia del navegador)</text>

  <!-- Context A -->
  <rect x="40" y="58" width="268" height="144" rx="8" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
  <text x="174" y="78" font-size="10" font-weight="700" fill="#5b21b6" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">BrowserContext A</text>
  <text x="174" y="91" font-size="7.5" fill="#7c3aed" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">cookies / storage / network propios</text>
  <rect x="56" y="100" width="100" height="84" rx="6" fill="#ffffff" stroke="#c4b5fd"/>
  <text x="106" y="120" font-size="9" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page 1</text>
  <text x="106" y="134" font-size="7.5" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">pestaña / tab</text>
  <text x="106" y="166" font-size="7" fill="#94a3b8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">await page.goto(...)</text>
  <rect x="172" y="100" width="100" height="84" rx="6" fill="#ffffff" stroke="#c4b5fd"/>
  <text x="222" y="120" font-size="9" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page 2</text>
  <text x="222" y="134" font-size="7.5" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">otra pestaña</text>
  <text x="222" y="166" font-size="7" fill="#94a3b8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">context.newPage()</text>

  <!-- Context B -->
  <rect x="352" y="58" width="268" height="144" rx="8" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="486" y="78" font-size="10" font-weight="700" fill="#0f766e" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">BrowserContext B</text>
  <text x="486" y="91" font-size="7.5" fill="#0d9488" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">completamente aislado de A</text>
  <rect x="368" y="100" width="220" height="84" rx="6" fill="#ffffff" stroke="#99f6e4"/>
  <text x="478" y="120" font-size="9" fill="#334155" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Page 3</text>
  <text x="478" y="138" font-size="7.5" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">usuario diferente, sesión limpia</text>
  <text x="478" y="158" font-size="7" fill="#94a3b8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">distinto login, distintas cookies</text>

  <!-- Aislamiento note -->
  <text x="330" y="226" font-size="8" fill="#64748b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Cada test recibe un BrowserContext nuevo → aislamiento automático sin configurar nada</text>
</svg>
"""

# ---------------------------------------------------------------------------
# 3) Árbol de carpetas que genera npm init playwright@latest
# ---------------------------------------------------------------------------
def pw_folder_tree():
    lines = [
        (0, "mi-proyecto/",          True),
        (1, "tests/",                True),
        (2, "example.spec.ts",       False),
        (1, "tests-examples/",       True),
        (2, "demo-todo-app.spec.ts", False),
        (1, "playwright.config.ts",  False),
        (1, "package.json",          False),
        (1, "package-lock.json",     False),
        (1, ".gitignore",            False),
        (1, "pages/",                True),
        (2, "LoginPage.ts",          False),
    ]
    h = 26 + len(lines) * 19 + 14
    svg = [f'<svg viewBox="0 0 560 {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect x="0" y="0" width="560" height="{h}" fill="#0f172a" rx="8"/>')
    y = 32
    for depth, name, is_dir in lines:
        x = 24 + depth * 22
        color = "#a78bfa" if is_dir else "#e2e8f0"
        weight = "700" if is_dir else "400"
        icon = "📂 " if is_dir else "📄 "
        svg.append(
            f'<text x="{x}" y="{y}" font-size="10.5" font-family="DejaVu Sans Mono,monospace" '
            f'fill="{color}" font-weight="{weight}">{icon}{name}</text>'
        )
        y += 19
    svg.append("</svg>")
    return "".join(svg)

PW_FOLDER_TREE = pw_folder_tree()

# ---------------------------------------------------------------------------
# 4) Pirámide de prioridad de locators
# ---------------------------------------------------------------------------
PW_LOCATOR_PYRAMID = """
<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="640" height="300" fill="#ffffff"/>
  <text x="320" y="22" font-size="11" font-weight="700" fill="#0f172a" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">Prioridad de locators en Playwright (mayor arriba)</text>

  <!-- Level 1 - top - best -->
  <polygon points="320,38 210,108 430,108" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="320" y="72" font-size="9" font-weight="700" fill="#0f766e" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">getByRole / getByLabel</text>
  <text x="320" y="86" font-size="7.5" fill="#0d9488" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">refleja cómo lo ve el usuario</text>
  <text x="320" y="98" font-size="7" fill="#0d9488" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">★ preferido</text>

  <!-- Level 2 -->
  <polygon points="210,108 160,168 480,168 430,108" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="320" y="133" font-size="9" font-weight="700" fill="#1e3a8a" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">getByText / getByPlaceholder</text>
  <text x="320" y="147" font-size="7.5" fill="#1d4ed8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">getByAltText / getByTitle</text>
  <text x="320" y="160" font-size="7" fill="#1d4ed8" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">orientados a contenido visible</text>

  <!-- Level 3 -->
  <polygon points="160,168 100,228 540,228 480,168" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
  <text x="320" y="196" font-size="9" font-weight="700" fill="#78350f" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">getByTestId</text>
  <text x="320" y="210" font-size="7.5" fill="#92400e" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">data-testid (o atributo configurado)</text>
  <text x="320" y="224" font-size="7" fill="#92400e" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">cuando no hay locator semántico</text>

  <!-- Level 4 - bottom - worst -->
  <polygon points="100,228 60,278 580,278 540,228" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="320" y="250" font-size="9" font-weight="700" fill="#7f1d1d" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">CSS / XPath → page.locator()</text>
  <text x="320" y="265" font-size="7.5" fill="#991b1b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">frágil si cambia la estructura HTML</text>
  <text x="320" y="279" font-size="7" fill="#991b1b" text-anchor="middle" font-family="Liberation Sans,Arial,sans-serif">último recurso</text>
</svg>
"""

# ---------------------------------------------------------------------------
# 5) Ciclo de vida de un test en Playwright (fixture page entrando/saliendo)
# ---------------------------------------------------------------------------
PW_LIFECYCLE_DIAGRAM = """
<svg viewBox="0 0 680 190" xmlns="http://www.w3.org/2000/svg">
<style>.t{font-family:'DejaVu Sans Mono',monospace;font-size:9.5px;} .d{font-family:'Liberation Sans',Arial,sans-serif;font-size:8px;fill:#64748b;}</style>
  <!-- BrowserContext created -->
  <rect x="10" y="20" width="130" height="50" rx="6" fill="#ede9fe" stroke="#7c3aed"/>
  <text x="75" y="40" class="t" text-anchor="middle" fill="#5b21b6" font-size="8.5">new BrowserContext</text>
  <text x="75" y="54" class="d" text-anchor="middle">aislamiento automático</text>

  <!-- beforeEach -->
  <rect x="170" y="20" width="130" height="50" rx="6" fill="#dbeafe" stroke="#2563eb"/>
  <text x="235" y="40" class="t" text-anchor="middle" fill="#1e3a8a">test.beforeEach</text>
  <text x="235" y="54" class="d" text-anchor="middle">setup por test</text>

  <!-- test body -->
  <rect x="330" y="10" width="180" height="110" rx="6" fill="#ecfdf5" stroke="#0d9488" stroke-width="1.5"/>
  <text x="420" y="32" class="t" text-anchor="middle" fill="#0f766e" font-weight="700">test('nombre',</text>
  <text x="420" y="48" class="t" text-anchor="middle" fill="#0f766e" font-weight="700">async ({ page }) =&gt; {</text>
  <text x="420" y="64" class="d" text-anchor="middle">fixture "page" inyectada</text>
  <text x="420" y="78" class="d" text-anchor="middle">await page.goto(…)</text>
  <text x="420" y="92" class="d" text-anchor="middle">await expect(…).toBe…</text>
  <text x="420" y="106" class="t" text-anchor="middle" fill="#0f766e">})</text>

  <!-- afterEach -->
  <rect x="540" y="20" width="130" height="50" rx="6" fill="#fef3c7" stroke="#d97706"/>
  <text x="605" y="40" class="t" text-anchor="middle" fill="#78350f">test.afterEach</text>
  <text x="605" y="54" class="d" text-anchor="middle">teardown por test</text>

  <!-- Context destroyed -->
  <rect x="330" y="135" width="180" height="40" rx="6" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="420" y="153" class="t" text-anchor="middle" fill="#475569" font-size="8.5">BrowserContext destruido</text>
  <text x="420" y="167" class="d" text-anchor="middle">cookies/storage limpiados</text>

  <!-- Arrows -->
  <line x1="140" y1="45" x2="170" y2="45" stroke="#94a3b8" stroke-width="2" marker-end="url(#apw2)"/>
  <line x1="300" y1="45" x2="330" y2="45" stroke="#94a3b8" stroke-width="2" marker-end="url(#apw2)"/>
  <line x1="510" y1="45" x2="540" y2="45" stroke="#94a3b8" stroke-width="2" marker-end="url(#apw2)"/>
  <line x1="420" y1="120" x2="420" y2="135" stroke="#94a3b8" stroke-width="2" marker-end="url(#apw2)"/>

  <defs><marker id="apw2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker></defs>
</svg>
"""

# ---------------------------------------------------------------------------
# 6) page.route() interceptando una request
# ---------------------------------------------------------------------------
PW_ROUTE_DIAGRAM = """
<svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg">
<style>.t{font-family:'DejaVu Sans Mono',monospace;font-size:9px;} .d{font-family:'Liberation Sans',Arial,sans-serif;font-size:8.2px;fill:#64748b;}</style>
  <rect x="20" y="50" width="130" height="60" rx="6" fill="#ede9fe" stroke="#7c3aed"/>
  <text x="85" y="75" class="t" text-anchor="middle" fill="#5b21b6" font-weight="700">Tu App</text>
  <text x="85" y="92" class="d" text-anchor="middle">fetch('/api/users')</text>

  <rect x="245" y="20" width="150" height="130" rx="6" fill="#0f172a"/>
  <text x="320" y="42" class="t" text-anchor="middle" fill="#a78bfa" font-weight="700">page.route()</text>
  <text x="320" y="60" class="d" text-anchor="middle" fill="#94a3b8">intercepta antes</text>
  <text x="320" y="72" class="d" text-anchor="middle" fill="#94a3b8">de salir a la red</text>
  <rect x="260" y="84" width="120" height="52" rx="4" fill="#1e293b"/>
  <text x="320" y="100" class="t" text-anchor="middle" fill="#fcd34d" font-size="7.6">GET /api/users</text>
  <text x="320" y="116" class="t" text-anchor="middle" fill="#86efac" font-size="7.6">route.fulfill(&#123;</text>
  <text x="320" y="128" class="t" text-anchor="middle" fill="#86efac" font-size="7.6">  body: mock &#125;)</text>

  <rect x="490" y="50" width="130" height="60" rx="6" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="555" y="73" class="t" text-anchor="middle" fill="#334155" font-weight="700">Servidor real</text>
  <text x="555" y="90" class="d" text-anchor="middle">(no se llega a tocar)</text>

  <line x1="150" y1="80" x2="245" y2="80" stroke="#a78bfa" stroke-width="2.5" marker-end="url(#apw3)"/>
  <line x1="395" y1="80" x2="490" y2="80" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="442" y="72" class="d" text-anchor="middle" fill="#94a3b8">bloqueada ✕</text>

  <line x1="320" y1="150" x2="320" y2="170" stroke="#a78bfa" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#apw3)"/>
  <rect x="186" y="170" width="268" height="22" rx="4" fill="#fffbeb" stroke="#d97706"/>
  <text x="320" y="185" class="t" text-anchor="middle" fill="#78350f" font-size="7.8">await page.waitForResponse('/api/users') → determinístico</text>

  <defs><marker id="apw3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#a78bfa"/></marker></defs>
</svg>
"""
