# -*- coding: utf-8 -*-
"""Contenido Playwright — Parte 1: secciones pw-1 a pw-4."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from helpers import code_block, callout, table, figure
from playwright import diagrams as dg


def page(eyebrow, num, title, body):
    return f'''<div class="page">
      <div class="section-eyebrow">{eyebrow}</div>
      <h1 class="section-title">{num}. {title}</h1>
      {body}
    </div>'''


# =====================================================================
# SECCIÓN pw-1 — ¿QUÉ ES PLAYWRIGHT?
# =====================================================================
def section_pw_01():
    body = f'''
    <p>Playwright es un framework de testing E2E de código abierto creado por Microsoft. Permite
    controlar <strong>Chromium, Firefox y WebKit</strong> (el motor de Safari) con una única API,
    usando JavaScript/TypeScript, Python, Java o .NET. A diferencia de Cypress, Playwright
    controla el navegador desde un proceso Node.js externo mediante un protocolo propio
    (basado en WebSocket/CDP), lo que le da soporte nativo a múltiples navegadores, múltiples
    pestañas y múltiples dominios sin restricciones.</p>

    {figure(dg.PW_ARCH_DIAGRAM, "Un proceso Node.js controla Chromium, Firefox y WebKit en paralelo, cada uno con su propio BrowserContext aislado.")}

    <h2>¿Por qué lo creó Microsoft?</h2>
    <p>El equipo que construyó Playwright es en parte el mismo que trabajó en Puppeteer en Google.
    El objetivo era resolver tres limitaciones concretas que tenían con las herramientas existentes:</p>
    <ul>
      <li><strong>Multi-navegador de verdad:</strong> Puppeteer solo controla Chromium. Playwright
      controla los tres motores principales desde la misma API.</li>
      <li><strong>Aislamiento automático:</strong> cada test corre en un BrowserContext nuevo,
      sin necesidad de limpiar cookies ni storage manualmente.</li>
      <li><strong>async/await nativo:</strong> el modelo de comandos es JavaScript puro; no hay
      cola de comandos interna que el programador no vea.</li>
    </ul>

    <h2>Playwright vs. Cypress vs. Selenium — la comparación completa</h2>
    {table(
        ["Característica", "Playwright", "Cypress", "Selenium"],
        [
            ["Arquitectura", "Proceso Node externo, protocolo propio", "Corre <em>dentro</em> del navegador", "WebDriver (protocolo estándar externo)"],
            ["Navegadores", "Chromium, Firefox, <strong>WebKit</strong>", "Chromium-family + Firefox (experimental)", "Todos los navegadores con WebDriver"],
            ["Lenguajes", "JS/TS, Python, Java, .NET", "JavaScript / TypeScript", "Multi-lenguaje (Java, Python, C#, JS...)"],
            ["Asincronía", "<code class='inline'>async/await</code> nativo", "Cola de comandos interna (no uses await)", "Varía por lenguaje"],
            ["Aislamiento entre tests", "BrowserContext nuevo por test (automático)", "Compartido, hay que limpiar manualmente", "Depende del setup"],
            ["Multi-pestaña / dominio", "Sí, nativo", "Limitado (<code class='inline'>cy.origin</code>)", "Sí"],
            ["Debugging", "Trace Viewer, UI Mode, Inspector", "Time-travel en Test Runner", "Varía"],
            ["Ideal para", "E2E multi-navegador, equipos JS/TS", "Apps web SPA, equipos JS/TS", "Suites legacy multi-lenguaje"],
        ],
        widths=["20%", "27%", "26%", "27%"]
    )}

    {callout("info", "¿Cuándo elegir Playwright sobre Cypress?",
        '<p>Si necesitás testear en Safari/WebKit, si tus tests cruzan varios dominios o pestañas, '
        'si querés paralelización nativa sin servicio externo, o si el equipo ya usa '
        '<code class="inline">async/await</code> en todo el codebase, Playwright encaja muy bien. '
        'Si tu stack es 100% JS/TS y valorás la experiencia del Test Runner interactivo para '
        'debuggear visualmente, Cypress sigue siendo una opción excelente.</p>')}

    <h2>Tipos de testing</h2>
    {table(
        ["Tipo", "Qué prueba", "En Playwright"],
        [
            ["<strong>E2E Testing</strong>", "Flujo completo como usuario real", "El caso principal de este documento"],
            ["<strong>Component Testing</strong>", "Componente de UI aislado", "Soporte experimental para React/Vue/Svelte"],
            ["<strong>API Testing</strong>", "Llamadas HTTP directas", "<code class='inline'>request.get('/api/users')</code> vía fixture <code class='inline'>request</code>"],
        ]
    )}
    '''
    return page("Fundamentos", "pw-1", "¿Qué es Playwright?", body)


# =====================================================================
# SECCIÓN pw-2 — DIFERENCIAS CLAVE PARA QUIEN VIENE DE CYPRESS
# =====================================================================
def section_pw_02():
    body = f'''
    <p>Si ya leíste la pista de Cypress (o venís de usarlo), esta sección es la más importante.
    Playwright no es Cypress con el nombre cambiado: tiene un modelo mental distinto en varios
    puntos clave. Ignorar esto genera errores silenciosos difíciles de debuggear.</p>

    <h2>1. Asincronía: el cambio más importante</h2>
    <p>En Cypress los comandos forman una <em>cola interna</em>; Cypress los ejecuta en orden
    y nunca escribís <code class="inline">await</code> en un test normal. En Playwright
    <strong>todo es async/await de verdad</strong>: cada interacción retorna una Promise real.</p>

    {table(
        ["", "Cypress", "Playwright"],
        [
            ["Modelo", "Cola interna de comandos", "Promesas nativas de Node.js"],
            ["¿Usás await?", "Casi nunca (y si lo ponés, puede romper)", "Siempre en cada acción"],
            ["Error silencioso típico", "Usar .then() en el lugar equivocado", "Olvidar el await"],
            ["Por qué importa", "El orden lo maneja Cypress, no vos", "Vos controlás el flujo explícitamente"],
        ],
        widths=["20%", "40%", "40%"]
    )}

    {code_block("""// CYPRESS — sin await, cola interna
it('loguea', () => {
  cy.visit('/login');
  cy.get('[data-cy=email]').type('ana@mail.com');
  cy.get('[data-cy=pass]').type('clave123');
  cy.get('[data-cy=submit]').click();
  cy.url().should('include', '/dashboard');
});

// PLAYWRIGHT — async/await, promesas reales
test('loguea', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('ana@mail.com');
  await page.getByLabel('Contraseña').fill('clave123');
  await page.getByRole('button', { name: 'Ingresar' }).click();
  await expect(page).toHaveURL(/dashboard/);
});""", "ts")}

    {callout("warning", "El error más común: olvidar el await",
        '<p>Si escribís <code class="inline">page.click()</code> sin <code class="inline">await</code>, '
        'el test <strong>no falla inmediatamente</strong>: la Promise queda flotando, el código sigue '
        'ejecutándose, y obtenés comportamientos raros difíciles de entender. La sección 14 cubre '
        'este error en detalle con ejemplos de lo que pasa. Por ahora, la regla simple: '
        '<strong>todo lo que empieza con <code class="inline">page.</code>, '
        '<code class="inline">locator.</code> o <code class="inline">expect()</code> lleva await.</strong></p>')}

    <h2>2. El sistema de test runner propio</h2>
    {code_block("""// Cypress usa Mocha (describe / it)
describe('Suite', () => {
  before(() => { /* ... */ });
  beforeEach(() => { /* ... */ });
  it('caso 1', () => { /* ... */ });
  it('caso 2', () => { /* ... */ });
});

// Playwright tiene su propio runner (test.describe / test)
import {{ test, expect }} from '@playwright/test';

test.describe('Suite', () => {
  test.beforeAll(async () => { /* ... */ });
  test.beforeEach(async ({ page }) => { await page.goto('/'); });
  test('caso 1', async ({ page }) => { /* ... */ });
  test('caso 2', async ({ page }) => { /* ... */ });
});""", "ts")}

    <h2>3. BrowserContext: el aislamiento que Cypress no tiene por defecto</h2>
    {figure(dg.PW_CONTEXT_DIAGRAM, "Cada test recibe su propio BrowserContext: cookies, localStorage y estado de red completamente aislados.")}

    <p>En Cypress, si un test escribe en <code class="inline">localStorage</code>, ese estado puede
    filtrarse al siguiente test (aunque Cypress 12+ mejoró esto). En Playwright, cada test
    recibe un BrowserContext nuevo y destruido al terminar: <strong>aislamiento garantizado sin
    configurar nada</strong>.</p>

    <h2>4. Locators vs. cy.get()</h2>
    <p>Cypress encuentra elementos con selectores CSS via <code class="inline">cy.get()</code>.
    Playwright tiene su propia capa de <strong>Locators</strong>: métodos orientados a cómo el
    usuario percibe la interfaz, no a cómo está construida en HTML.</p>

    {code_block("""// Cypress: selector CSS directo
cy.get('[data-cy="submit"]').click();

// Playwright: locator orientado al usuario (preferido)
await page.getByRole('button', { name: 'Enviar' }).click();

// Playwright: si necesitás CSS igual (válido, pero no es el primer recurso)
await page.locator('[data-testid="submit"]').click();""", "ts")}

    {callout("tip", "¿Por qué locators orientados al usuario?",
        '<p>Un test que busca por <em>rol</em> y <em>nombre accesible</em> falla si el botón '
        'desaparece o cambia su texto visible — que es exactamente lo que querés detectar. '
        'Un test que busca por clase CSS puede pasar aunque el botón sea completamente inaccesible '
        'para un lector de pantalla. Los locators de Playwright te hacen testear y mejorar '
        'la accesibilidad al mismo tiempo.</p>')}
    '''
    return page("Fundamentos", "pw-2", "Diferencias clave para quien viene de Cypress", body)


# =====================================================================
# SECCIÓN pw-3 — INSTALACIÓN
# =====================================================================
def section_pw_03():
    body = f'''
    <p>Playwright trae todo en un solo paquete: el test runner, los binarios de los navegadores,
    las definiciones de TypeScript y el reporter HTML. No necesitás combinar varias librerías.</p>

    <ol class="steps">
      <li>
        <div class="step-title">Crear el proyecto e inicializar Playwright</div>
        <p>Desde una carpeta vacía (o un proyecto Node.js existente):</p>
        {code_block("""mkdir mi-proyecto-playwright
cd mi-proyecto-playwright
npm init playwright@latest""", "bash")}
        <p>El asistente te pregunta:</p>
        <ul>
          <li><strong>TypeScript o JavaScript</strong> — elegí TypeScript.</li>
          <li><strong>Carpeta de tests</strong> — por defecto <code class="inline">tests/</code> (podés dejarlo).</li>
          <li><strong>Agregar flujo de GitHub Actions</strong> — elegí Sí si vas a usar CI.</li>
          <li><strong>Instalar browsers</strong> — Sí. Esto descarga Chromium, Firefox y WebKit.</li>
        </ul>
      </li>

      <li>
        <div class="step-title">Estructura generada</div>
        {figure(dg.PW_FOLDER_TREE, "Estructura tipica generada por npm init playwright@latest")}
        <p>A diferencia de Cypress, no hay una carpeta <code class="inline">cypress/</code> separada:
        los tests conviven con el resto del proyecto desde la raíz, y la config vive en
        <code class="inline">playwright.config.ts</code>.</p>
      </li>

      <li>
        <div class="step-title">playwright.config.ts — entender la configuración</div>
        {code_block("""import {{ defineConfig, devices }} from '@playwright/test';

export default defineConfig({{
  // Carpeta con los tests
  testDir: './tests',

  // Reintenta tests fallidos en CI (0 en local para desarrollo ágil)
  retries: process.env.CI ? 2 : 0,

  // Workers en paralelo (undefined = número de cores del SO)
  workers: process.env.CI ? 1 : undefined,

  // Reporter: 'html' genera un reporte visual completo
  reporter: 'html',

  // Configuración compartida por todos los projects
  use: {{
    baseURL: 'http://localhost:3000',
    // Captura trace en el primer reintento de un test fallido
    trace: 'on-first-retry',
  }},

  // "Projects" = combinaciones de navegador/dispositivo
  projects: [
    {{ name: 'chromium', use: {{ ...devices['Desktop Chrome'] }} }},
    {{ name: 'firefox',  use: {{ ...devices['Desktop Firefox'] }} }},
    {{ name: 'webkit',   use: {{ ...devices['Desktop Safari'] }} }},
    // Mobile:
    {{ name: 'mobile-chrome', use: {{ ...devices['Pixel 5'] }} }},
  ],
}});""", "ts", "playwright.config.ts")}

        {callout("tip", "La clave de playwright.config.ts: projects",
            '<p><code class="inline">projects</code> es lo que hace a Playwright único: con una sola '
            'entrada de config corrés los mismos tests en Chromium, Firefox y WebKit. Podés agregar '
            'perfiles de dispositivos móviles, diferentes <code class="inline">baseURL</code> para '
            'staging vs. producción, o diferentes timeouts sin duplicar ningún test.</p>')}
      </li>

      <li>
        <div class="step-title">Instalar (o reinstalar) navegadores</div>
        {code_block("""# Instala todos los navegadores configurados
npx playwright install

# Solo uno específico:
npx playwright install chromium""", "bash")}
        <p>Los binarios se guardan en un directorio local de caché. No son los Chrome/Firefox del
        sistema: son builds específicos de Playwright, garantizando reproducibilidad entre máquinas.</p>
      </li>
    </ol>

    {callout("best", "Scripts útiles en package.json",
        '<p>Estos son los atajos más usados:</p>' +
        code_block("""{
  "scripts": {
    "test": "playwright test",
    "test:ui": "playwright test --ui",
    "test:debug": "playwright test --debug",
    "test:report": "playwright show-report"
  }
}""", "json", "package.json"))}
    '''
    return page("Puesta en marcha", "pw-3", "Instalación del entorno completo", body)


# =====================================================================
# SECCIÓN pw-4 — PRIMER PROYECTO
# =====================================================================
def section_pw_04():
    body = f'''
    <p>Con todo instalado, vamos a escribir y correr tu primer test. Los archivos de test en
    Playwright terminan en <code class="inline">.spec.ts</code> y viven dentro de la carpeta
    configurada en <code class="inline">testDir</code> (por defecto <code class="inline">tests/</code>).</p>

    <h2>Tu primer archivo de test</h2>
    {code_block("""// tests/home.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Página de inicio', () => {
  test('muestra el título principal', async ({ page }) => {
    await page.goto('/');
    const titulo = page.getByRole('heading', { level: 1 });
    await expect(titulo).toBeVisible();
    await expect(titulo).toContainText('Bienvenido');
  });

  test('el link de contacto navega correctamente', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: 'Contacto' }).click();
    await expect(page).toHaveURL(/contacto/);
  });
});""", "ts", "tests/home.spec.ts")}

    <h2>Tres formas de correr los tests</h2>
    {table(
        ["Comando", "Modo", "Cuándo usarlo"],
        [
            ["<code class='inline'>npx playwright test</code>", "Headless, todos los proyectos", "CI/CD o para correr todo rápido"],
            ["<code class='inline'>npx playwright test --ui</code>", "<strong>UI Mode</strong>: interfaz gráfica interactiva", "Mientras escribís y debuggeás tests"],
            ["<code class='inline'>npx playwright test --debug</code>", "Playwright Inspector paso a paso", "Para entender qué hace un test fallido"],
        ]
    )}

    <h2>UI Mode: el equivalente (mejorado) del Cypress Test Runner</h2>
    <p>El UI Mode (<code class="inline">--ui</code>) es el entorno interactivo de Playwright. A diferencia
    del Test Runner de Cypress, el UI Mode corre en el mismo proceso Node.js que tus tests y muestra:</p>
    <ul>
      <li>Lista de todos los tests con filtros por archivo, proyecto y estado.</li>
      <li>Ejecución en tiempo real con log de acciones.</li>
      <li><strong>Trace Viewer integrado</strong>: podés ver el estado del DOM en cada paso,
      capturas de pantalla automáticas, y un timeline de la ejecución.</li>
      <li>Selector picker: hacé click en cualquier elemento de la app y Playwright te sugiere
      el locator más apropiado.</li>
    </ul>

    <h2>Ver el reporte HTML</h2>
    {code_block("""npx playwright show-report""", "bash")}
    <p>Después de cada <code class="inline">npx playwright test</code>, Playwright genera un reporte
    HTML en <code class="inline">playwright-report/</code>. Con <code class="inline">show-report</code>
    lo abrís en el navegador: incluye capturas de pantalla, videos y traces de los tests fallidos.</p>

    <h2>Codegen: grabá acciones y generá tests automáticamente</h2>
    {code_block("""npx playwright codegen http://localhost:3000""", "bash")}
    <p><code class="inline">codegen</code> abre un navegador donde interactuás normalmente con la
    app, y Playwright genera el código de test correspondiente en tiempo real. Es la forma más
    rápida de arrancar con un test nuevo.</p>

    {callout("best", "Usá codegen para arrancar, después revisá los locators",
        '<p><code class="inline">codegen</code> a veces usa CSS o XPath cuando podría usar un '
        'locator semántico. Tomá el código generado como punto de partida y reemplazá los '
        '<code class="inline">page.locator(\'div.btn\')</code> por '
        '<code class="inline">page.getByRole(\'button\', { name: \'...\' })</code> cuando sea posible.</p>')}

    <h2>Checklist antes de seguir</h2>
    <ul class="checklist">
      <li>npm init playwright@latest corrido y navegadores instalados</li>
      <li><code class="inline">playwright.config.ts</code> con <code class="inline">baseURL</code> configurada</li>
      <li>Un primer test corriendo con <code class="inline">npx playwright test</code></li>
      <li>UI Mode abierto y explorado (<code class="inline">npx playwright test --ui</code>)</li>
      <li>Reporte HTML generado y visto (<code class="inline">npx playwright show-report</code>)</li>
    </ul>
    '''
    return page("Puesta en marcha", "pw-4", "Primer proyecto Playwright + TypeScript", body)
