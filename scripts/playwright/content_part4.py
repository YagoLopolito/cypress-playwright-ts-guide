# -*- coding: utf-8 -*-
"""Contenido Playwright — Parte 4: secciones pw-13 a pw-16."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from helpers import code_block, callout, table, figure
from playwright.content_part1 import page
from playwright import diagrams as dg


# =====================================================================
# SECCIÓN pw-13 — BUENAS PRÁCTICAS
# =====================================================================
def section_pw_13():
    body = f'''
    <p>Las buenas prácticas de Playwright comparten el espíritu de las de Cypress
    (independencia entre tests, sin sleeps manuales, datos de prueba robustos), pero
    las herramientas concretas son distintas.</p>

    <h2>1. Usá locators semánticos antes que CSS o XPath</h2>
    {code_block("""// MAL: CSS frágil — si el equipo de diseño cambia la clase, el test se rompe
await page.locator('.btn-primary.submit').click();

// MAL: XPath — imposible de leer y mantener
await page.locator('xpath=//div[@class="form"]//button[2]').click();

// BIEN: rol y nombre accesible
await page.getByRole('button', { name: 'Enviar formulario' }).click();

// BIEN si no hay locator semántico: data-testid explícito
await page.getByTestId('submit-button').click();""", "ts")}

    <h2>2. Usá aserciones web-first, no aserciones sobre valores obtenidos</h2>
    {code_block("""// MAL: sin auto-retry — puede fallar por timing aunque el elemento esté a punto de aparecer
const text = await page.getByTestId('resultado').textContent();
expect(text).toBe('Completado');

// BIEN: auto-retry — espera hasta que se cumpla o venza el timeout
await expect(page.getByTestId('resultado')).toHaveText('Completado');""", "ts")}

    <h2>3. Nunca uses waitForTimeout</h2>
    {code_block("""// MAL: espera ciega, lenta y frágil
await page.waitForTimeout(3000);
await expect(page.getByTestId('resultado')).toBeVisible();

// BIEN: esperá la condición real
await expect(page.getByTestId('resultado')).toBeVisible(); // auto-retry incluido

// BIEN si esperás una request:
await Promise.all([
  page.waitForResponse('/api/calcular'),
  page.getByRole('button', { name: 'Calcular' }).click(),
]);
await expect(page.getByTestId('resultado')).toBeVisible();""", "ts")}

    <h2>4. Usá test.step para tests largos</h2>
    {code_block("""// Sin steps: difícil de diagnosticar qué falló
test('flujo completo de compra', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Productos' }).click();
  // ... 30 líneas más sin estructura visible

  // CON steps: el reporte HTML y el Trace Viewer los muestran separados
  await test.step('Agregar al carrito', async () => {
    await page.getByRole('button', { name: 'Agregar' }).first().click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');
  });
  await test.step('Checkout', async () => {
    await page.getByRole('link', { name: 'Carrito' }).click();
    await page.getByRole('button', { name: 'Pagar' }).click();
  });
});""", "ts")}

    <h2>5. Aprovechá el aislamiento automático de BrowserContext</h2>
    {code_block("""// En Cypress había que limpiar estado entre tests:
// beforeEach(() => { cy.clearCookies(); cy.clearLocalStorage(); });

// En Playwright NO hace falta: cada test recibe un contexto nuevo
test('test A', async ({ page }) => {
  // Este test escribe en localStorage
  await page.evaluate(() => localStorage.setItem('tema', 'oscuro'));
});

test('test B', async ({ page }) => {
  // localStorage está limpio: el contexto es nuevo
  const tema = await page.evaluate(() => localStorage.getItem('tema'));
  expect(tema).toBeNull(); // pasa siempre
});""", "ts")}

    <h2>6. Usá data-testid cuando no hay locator semántico</h2>
    {code_block("""<!-- En el HTML: cuando no hay rol ni label natural -->
<div data-testid="cart-count" aria-label="Ítems en el carrito">3</div>""", "css")}
    {code_block("""// En el test:
await expect(page.getByTestId('cart-count')).toHaveText('3');

// Configurar un atributo alternativo en playwright.config.ts:
// use: { testIdAttribute: 'data-cy' }  → getByTestId() busca data-cy=""", "ts")}

    {callout("best", "Jerarquía de decisión para elegir un locator",
        '<p>1° <code class="inline">getByRole</code> + nombre accesible — '
        '2° <code class="inline">getByLabel</code> (formularios) — '
        '3° <code class="inline">getByText</code> / <code class="inline">getByPlaceholder</code> — '
        '4° <code class="inline">getByTestId</code> — '
        '5° <code class="inline">page.locator(css)</code> — '
        'Último recurso: XPath.</p>')}
    '''
    return page("Calidad y entrega", "pw-13", "Buenas prácticas", body)


# =====================================================================
# SECCIÓN pw-14 — ERRORES COMUNES
# =====================================================================
def section_pw_14():
    body = f'''
    <h2>1. Olvidar el await — el error más común</h2>
    <p>Este es, con diferencia, el error más frecuente para quien empieza con Playwright,
    especialmente si viene de Cypress donde nunca se usa <code class="inline">await</code>.</p>
    {code_block("""// MAL: la Promise queda flotando — el click no se espera
test('click sin await', async ({ page }) => {
  await page.goto('/');
  page.getByRole('button', { name: 'Enviar' }).click(); // ← falta await
  // El test puede pasar o fallar de forma no determinística
  await expect(page).toHaveURL(/confirmacion/);
});

// BIEN:
test('click con await', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Enviar' }).click(); // ← await
  await expect(page).toHaveURL(/confirmacion/);
});""", "ts")}

    {callout("tip", "Activá la regla ESLint para detectarlo automáticamente",
        '<p>El plugin <code class="inline">eslint-plugin-playwright</code> tiene la regla '
        '<code class="inline">playwright/no-floating-promises</code> que detecta estos casos. '
        'También <code class="inline">@typescript-eslint/no-floating-promises</code> de la '
        'config base de TypeScript funciona. Configurá el linter desde el inicio.</p>')}

    <h2>2. No usar el Trace Viewer ni el UI Mode para debuggear</h2>
    {code_block("""# En vez de agregar console.log y re-correr:

# Opción 1: UI Mode — interfaz visual con step-by-step
npx playwright test --ui

# Opción 2: Debug mode — abre el Inspector de Playwright
npx playwright test --debug

# Opción 3: Ver el trace después de un fallo (trace: 'on-first-retry' en config)
npx playwright show-report

# Opción 4: Forzar generación de trace
npx playwright test --trace on""", "bash")}

    <h2>3. Usar waitForTimeout en vez de esperar la condición real</h2>
    {code_block("""// MAL: si la animación tarda más de 500ms en otro entorno, el test falla
await page.waitForTimeout(500);
await expect(page.getByTestId('spinner')).not.toBeVisible();

// BIEN: la aserción web-first reintenta sola hasta que se cumpla
await expect(page.getByTestId('spinner')).not.toBeVisible();
// Playwright espera (por defecto hasta 5s) y reintenta automáticamente""", "ts")}

    <h2>4. No usar codegen para arrancar</h2>
    {code_block("""# Grabá acciones en vez de escribir todo a mano desde cero
npx playwright codegen http://localhost:3000

# También podés grabar en un archivo directamente
npx playwright codegen --output tests/nuevo-flujo.spec.ts http://localhost:3000""", "bash")}

    <h2>5. Buscar con CSS cuando existe un locator semántico</h2>
    {code_block("""// MAL: depende de la estructura del HTML
await page.locator('form.login-form > div:nth-child(2) > input').fill('ana@mail.com');

// BIEN: independiente de la estructura HTML
await page.getByLabel('Email').fill('ana@mail.com');""", "ts")}

    <h2>6. No usar storageState para reutilizar autenticación</h2>
    {code_block("""// MAL: hacer login en CADA test cuando ya se probó que funciona
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('ana@mail.com');
  await page.getByLabel('Contraseña').fill('clave123');
  await page.getByRole('button', { name: 'Ingresar' }).click();
});

// BIEN: login una sola vez, guardar estado, reutilizarlo
// (ver sección 12 para el patrón completo con auth.setup.ts)""", "ts")}

    <h2>7. Confundir fixtures de datos con fixtures de Playwright</h2>
    {callout("info", "Son dos conceptos distintos",
        '<p>"Fixture" en Playwright puede significar: (a) un archivo de datos JSON con datos '
        'de prueba, o (b) el sistema de inyección de dependencias de <code class="inline">test.extend()</code>. '
        'El primero es análogo a <code class="inline">cy.fixture()</code> de Cypress. '
        'El segundo no tiene equivalente en Cypress: es más poderoso y sirve para setup/teardown '
        'reutilizable. Ver sección 9 para la distinción completa con ejemplos.</p>')}
    '''
    return page("Calidad y entrega", "pw-14", "Errores comunes a evitar", body)


# =====================================================================
# SECCIÓN pw-15 — CI/CD
# =====================================================================
def section_pw_15():
    body = f'''
    <p>Playwright fue diseñado para correr en CI desde el día uno: los tests corren headless
    por defecto, la paralelización es nativa (sin necesitar un servicio externo), y el reporter
    HTML incluye traces, videos y capturas de pantalla de los fallos.</p>

    <h2>GitHub Actions</h2>
    {code_block("""# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:   { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with: { node-version: lts/* }

      - name: Install dependencies
        run: npm ci

      # La action oficial instala los browsers cacheados
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      # Subir el reporte HTML aunque fallen los tests
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30""", "bash", ".github/workflows/playwright.yml")}

    <h2>Configuración para CI en playwright.config.ts</h2>
    {code_block("""export default defineConfig({
  // Reintentar tests fallidos en CI (evita falsos negativos por flakiness)
  retries: process.env.CI ? 2 : 0,

  // En CI: 1 worker (estable); en local: todos los cores
  workers: process.env.CI ? 1 : undefined,

  use: {
    // Guardar trace en el primer reintento — disponible en el reporte HTML
    trace: 'on-first-retry',

    // Video solo cuando falla
    video: 'retain-on-failure',

    // Screenshot solo cuando falla
    screenshot: 'only-on-failure',
  },
});""", "ts")}

    <h2>Paralelización nativa — diferencia clave con Cypress</h2>
    {table(
        ["", "Playwright", "Cypress"],
        [
            ["Paralelización", "Nativa, sin configuración extra", "Requiere Cypress Cloud (servicio de pago) o configuración avanzada"],
            ["Workers", "Configurable en <code class='inline'>playwright.config.ts</code>", "Un runner por máquina por defecto"],
            ["Aislamiento por worker", "BrowserContext independiente por test", "Compartido si no se configura"],
        ]
    )}
    {code_block("""# Controlar workers desde la línea de comando
npx playwright test --workers=4

# Un worker por project (estable para CI con recursos limitados)
npx playwright test --workers=1""", "bash")}

    <h2>Ver el reporte HTML del CI</h2>
    {code_block("""# Descargar el artifact de GitHub Actions y abrirlo localmente
npx playwright show-report path/to/playwright-report/""", "bash")}

    <h2>Checklist de CI/CD</h2>
    <ul class="checklist">
      <li>Browsers instalados con <code class="inline">npx playwright install --with-deps</code></li>
      <li><code class="inline">retries: 2</code> en CI para tolerar flakiness puntual</li>
      <li><code class="inline">trace: 'on-first-retry'</code> para diagnosticar fallos</li>
      <li>Artifact del reporte HTML subido con <code class="inline">upload-artifact</code></li>
      <li>Auth guardada con <code class="inline">storageState</code> para no repetir login</li>
      <li>Tests independientes entre sí (el orden puede cambiar con paralelización)</li>
    </ul>
    '''
    return page("Calidad y entrega", "pw-15", "Ejecutar en CI/CD", body)


# =====================================================================
# SECCIÓN pw-16 — CHEAT SHEET FINAL
# =====================================================================
def section_pw_16():
    body = f'''
    <h2>Locators — referencia rápida</h2>
    {table(
        ["Locator", "Cuándo usarlo"],
        [
            ["<code class='inline'>getByRole('button', {{ name: '...' }})</code>", "Botones, links, headings — primer recurso"],
            ["<code class='inline'>getByLabel('Campo')</code>", "Inputs de formulario con label asociado"],
            ["<code class='inline'>getByText('texto')</code>", "Elementos con texto visible específico"],
            ["<code class='inline'>getByPlaceholder('texto')</code>", "Inputs por su placeholder"],
            ["<code class='inline'>getByAltText('descripción')</code>", "Imágenes"],
            ["<code class='inline'>getByTitle('tooltip')</code>", "Elementos con atributo title"],
            ["<code class='inline'>getByTestId('id')</code>", "Cuando no hay locator semántico — usa data-testid"],
            ["<code class='inline'>page.locator('.css')</code>", "Último recurso — CSS o XPath"],
        ]
    )}

    <h2>Acciones — referencia rápida</h2>
    {table(
        ["Acción", "Código"],
        [
            ["Navegar", "<code class='inline'>await page.goto('/ruta')</code>"],
            ["Rellenar input", "<code class='inline'>await locator.fill('texto')</code>"],
            ["Click", "<code class='inline'>await locator.click()</code>"],
            ["Presionar tecla", "<code class='inline'>await locator.press('Enter')</code>"],
            ["Marcar checkbox", "<code class='inline'>await locator.check()</code>"],
            ["Seleccionar option", "<code class='inline'>await locator.selectOption('valor')</code>"],
            ["Subir archivo", "<code class='inline'>await locator.setInputFiles('foto.jpg')</code>"],
            ["Screenshot", "<code class='inline'>await page.screenshot({{ path: 'img.png' }})</code>"],
        ]
    )}

    <h2>Aserciones — referencia rápida</h2>
    {table(
        ["Aserción", "Código"],
        [
            ["Es visible", "<code class='inline'>await expect(loc).toBeVisible()</code>"],
            ["No es visible", "<code class='inline'>await expect(loc).toBeHidden()</code>"],
            ["Tiene texto exacto", "<code class='inline'>await expect(loc).toHaveText('...')</code>"],
            ["Contiene texto", "<code class='inline'>await expect(loc).toContainText('...')</code>"],
            ["Tiene valor (input)", "<code class='inline'>await expect(loc).toHaveValue('...')</code>"],
            ["Cantidad de items", "<code class='inline'>await expect(loc).toHaveCount(n)</code>"],
            ["Está deshabilitado", "<code class='inline'>await expect(loc).toBeDisabled()</code>"],
            ["URL de la página", "<code class='inline'>await expect(page).toHaveURL(/patron/)</code>"],
        ]
    )}

    <h2>Debugging — comandos de consola</h2>
    {table(
        ["Objetivo", "Comando"],
        [
            ["UI Mode (interactivo)", "<code class='inline'>npx playwright test --ui</code>"],
            ["Inspector paso a paso", "<code class='inline'>npx playwright test --debug</code>"],
            ["Grabar un test nuevo", "<code class='inline'>npx playwright codegen URL</code>"],
            ["Ver reporte HTML", "<code class='inline'>npx playwright show-report</code>"],
            ["Ver un trace", "<code class='inline'>npx playwright show-trace trace.zip</code>"],
            ["Forzar trace en todos", "<code class='inline'>npx playwright test --trace on</code>"],
            ["Correr un solo test", "<code class='inline'>npx playwright test -g 'nombre del test'</code>"],
            ["Solo un project", "<code class='inline'>npx playwright test --project=firefox</code>"],
        ]
    )}

    <h2>Checklist de buenas prácticas</h2>
    <ul class="checklist">
      <li>Siempre <code class="inline">await</code> en cada acción e interacción</li>
      <li>Locators orientados al usuario (<code class="inline">getByRole</code>, <code class="inline">getByLabel</code>) antes que CSS</li>
      <li>Aserciones web-first (<code class="inline">expect(locator).toBeVisible()</code>) nunca valores directos</li>
      <li>Sin <code class="inline">waitForTimeout</code>: esperá la condición o la request real</li>
      <li>Cada test es independiente (BrowserContext nuevo automático)</li>
      <li>Usar <code class="inline">storageState</code> para no repetir login en cada test</li>
      <li>Usar <code class="inline">test.step</code> para structurar tests largos</li>
      <li>Linter con <code class="inline">eslint-plugin-playwright</code> activado</li>
      <li>CI con <code class="inline">trace: 'on-first-retry'</code> y artifact del reporte HTML</li>
    </ul>

    <h2>Recursos</h2>
    {table(
        ["Recurso", "URL"],
        [
            ["Documentación oficial", "<code class='inline'>playwright.dev</code>"],
            ["Best Practices guide", "<code class='inline'>playwright.dev/docs/best-practices</code>"],
            ["API Reference", "<code class='inline'>playwright.dev/docs/api/class-page</code>"],
            ["Locators guide", "<code class='inline'>playwright.dev/docs/locators</code>"],
            ["Fixtures guide", "<code class='inline'>playwright.dev/docs/test-fixtures</code>"],
        ]
    )}
    '''
    return page("Referencia", "pw-16", "Cheat sheet final y recursos", body)
