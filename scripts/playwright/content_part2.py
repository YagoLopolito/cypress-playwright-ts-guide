# -*- coding: utf-8 -*-
"""Contenido Playwright — Parte 2: secciones pw-5 a pw-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from helpers import code_block, callout, table, figure
from playwright.content_part1 import page
from playwright import diagrams as dg


# =====================================================================
# SECCIÓN pw-5 — LOCATORS
# =====================================================================
def section_pw_05():
    body = f'''
    <p>Los <strong>Locators</strong> son la forma de Playwright de encontrar elementos. A diferencia
    de Cypress (que usa selectores CSS vía <code class="inline">cy.get()</code>), Playwright propone
    primero los locators orientados a cómo el usuario percibe la interfaz, y deja CSS/XPath
    como último recurso. Esta jerarquía tiene una razón: los locators semánticos hacen tests
    más robustos y mejoran la accesibilidad del código.</p>

    {figure(dg.PW_LOCATOR_PYRAMID, "Jerarquía de locators: los orientados al usuario son mas robustos que CSS o XPath.")}

    <h2>1. getByRole — el rey de los locators</h2>
    <p>Busca por <strong>rol ARIA</strong> y nombre accesible. Refleja exactamente lo que ve un
    lector de pantalla y lo que espera un usuario.</p>
    {table(
        ["Rol", "Elementos HTML que matchean", "Ejemplo"],
        [
            ["<code class='inline'>button</code>", "<code class='inline'>&lt;button&gt;</code>, <code class='inline'>&lt;input type=submit&gt;</code>", "<code class='inline'>getByRole('button', { name: 'Enviar' })</code>"],
            ["<code class='inline'>link</code>", "<code class='inline'>&lt;a href&gt;</code>", "<code class='inline'>getByRole('link', { name: 'Inicio' })</code>"],
            ["<code class='inline'>heading</code>", "<code class='inline'>&lt;h1&gt;...&lt;h6&gt;</code>", "<code class='inline'>getByRole('heading', { level: 2 })</code>"],
            ["<code class='inline'>textbox</code>", "<code class='inline'>&lt;input type=text&gt;</code>, <code class='inline'>&lt;textarea&gt;</code>", "<code class='inline'>getByRole('textbox', { name: 'Email' })</code>"],
            ["<code class='inline'>checkbox</code>", "<code class='inline'>&lt;input type=checkbox&gt;</code>", "<code class='inline'>getByRole('checkbox', { name: 'Términos' })</code>"],
            ["<code class='inline'>radio</code>", "<code class='inline'>&lt;input type=radio&gt;</code>", "<code class='inline'>getByRole('radio', { name: 'Mensual' })</code>"],
            ["<code class='inline'>combobox</code>", "<code class='inline'>&lt;select&gt;</code>", "<code class='inline'>getByRole('combobox', { name: 'País' })</code>"],
            ["<code class='inline'>listitem</code>", "<code class='inline'>&lt;li&gt;</code>", "<code class='inline'>getByRole('listitem').filter({ hasText: 'Primero' })</code>"],
        ]
    )}

    {code_block("""// Buscar un botón por su texto visible
await page.getByRole('button', { name: 'Agregar al carrito' }).click();

// Ignorar mayúsculas/minúsculas
await page.getByRole('button', { name: /enviar/i }).click();

// Por rol sin nombre (todos los botones)
const botones = page.getByRole('button');
await expect(botones).toHaveCount(3);""", "ts")}

    <h2>2. getByLabel — para inputs y controles de formulario</h2>
    <p>Busca el elemento asociado a un <code class="inline">&lt;label&gt;</code>. Es la forma
    idiomática de encontrar campos de formulario porque vincula visibilidad con semántica.</p>
    {code_block("""// <label for="email">Email</label><input id="email" type="email">
await page.getByLabel('Email').fill('ana@mail.com');

// También funciona con label envolvente:
// <label>Contraseña <input type="password"></label>
await page.getByLabel('Contraseña').fill('clave123');""", "ts")}

    <h2>3. getByText y getByPlaceholder</h2>
    {code_block("""// Busca por texto visible exacto o parcial
await page.getByText('Zapatillas Runner').click();
await page.getByText(/runner/i).click(); // regex: no importa capitalización

// Busca por atributo placeholder del input
await page.getByPlaceholder('tu@email.com').fill('ana@mail.com');""", "ts")}

    <h2>4. getByAltText, getByTitle, getByTestId</h2>
    {code_block("""// Imágenes por atributo alt
await page.getByAltText('Logo de la empresa').click();

// Elementos con atributo title
await page.getByTitle('Cerrar ventana').click();

// Por atributo data-testid (configurable en playwright.config.ts)
// Por defecto busca data-testid="valor"
await page.getByTestId('submit-button').click();""", "ts")}

    {callout("tip", "Configurar el atributo de testId",
        '<p>Por defecto <code class="inline">getByTestId()</code> busca <code class="inline">data-testid</code>. '
        'Podés cambiarlo en <code class="inline">playwright.config.ts</code>: '
        '<code class="inline">use: {{ testIdAttribute: \'data-cy\' }}</code>. '
        'Así usás <code class="inline">getByTestId()</code> con los atributos '
        '<code class="inline">data-cy</code> que ya tenés en tu HTML.</p>')}

    <h2>5. page.locator() — CSS y XPath como fallback</h2>
    {code_block("""// CSS (mismo que cy.get() en Cypress)
await page.locator('[data-testid="submit"]').click();
await page.locator('.btn-primary').click();

// XPath (último recurso)
await page.locator('xpath=//button[@type="submit"]').click();""", "ts")}

    <h2>6. Filtrado, encadenamiento y listas</h2>
    {code_block("""// .filter() — reducir los resultados
const itemsDeCarrito = page.getByRole('listitem');
const productoDeseado = itemsDeCarrito.filter({ hasText: 'Zapatillas' });
await productoDeseado.getByRole('button', { name: 'Quitar' }).click();

// Encadenamiento: buscar dentro de un contenedor
const formulario = page.locator('.checkout-form');
await formulario.getByLabel('Email').fill('ana@mail.com');

// Posición en lista
await page.getByRole('listitem').first().click();
await page.getByRole('listitem').last().click();
await page.getByRole('listitem').nth(1).click(); // 0-based""", "ts")}

    {callout("best", "Regla de oro: sé específico, no selecciones de más",
        '<p>Si <code class="inline">page.getByRole(\'button\')</code> matchea tres botones, '
        'añadí <code class="inline">{{ name: \'Enviar\' }}</code>. Un locator que matchea '
        'exactamente un elemento hace tests más legibles y fallos más claros.</p>')}
    '''
    return page("La base: Locators", "pw-5", "Locators: la forma Playwright de encontrar elementos", body)


# =====================================================================
# SECCIÓN pw-6 — ANATOMÍA DE UN TEST
# =====================================================================
def section_pw_06():
    body = f'''
    <p>Un test de Playwright es una función <code class="inline">async</code> que recibe
    <strong>fixtures inyectadas</strong> (como <code class="inline">page</code>,
    <code class="inline">context</code>, <code class="inline">request</code>) y usa
    <code class="inline">await</code> para cada interacción. El runner de Playwright crea y
    destruye automáticamente el BrowserContext de cada test.</p>

    <h2>Estructura básica</h2>
    {code_block("""import { test, expect } from '@playwright/test';

// test.describe agrupa tests relacionados (equivalente a describe() en Cypress/Mocha)
test.describe('Carrito de compras', () => {

  // beforeAll: corre una sola vez antes de todos los tests del bloque
  test.beforeAll(async ({ browser }) => {
    // ej: crear datos en una BD de test
  });

  // beforeEach: corre antes de CADA test (fixture page es nueva por test)
  test.beforeEach(async ({ page }) => {
    await page.goto('/productos');
  });

  // El test en sí: función async que recibe fixtures entre {}
  test('agrega un producto al carrito', async ({ page }) => {
    await page.getByRole('button', { name: 'Agregar' }).first().click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');
  });

  test('muestra precio total actualizado', async ({ page }) => {
    await page.getByRole('button', { name: 'Agregar' }).first().click();
    await expect(page.getByTestId('cart-total')).toContainText('$');
  });

  test.afterEach(async ({ page }) => {
    // Playwright destruye el BrowserContext aqui de todas formas,
    // pero podés hacer cleanup adicional si querés
  });
});""", "ts")}

    {figure(dg.PW_LIFECYCLE_DIAGRAM, "Ciclo de vida: BrowserContext nuevo → beforeEach → test → afterEach → BrowserContext destruido.")}

    <h2>La fixture page — qué es y de dónde viene</h2>
    <p>En Playwright, <code class="inline">page</code> no es un global: es una
    <strong>fixture inyectada por el runner</strong>. Cada test recibe su propia instancia de
    <code class="inline">Page</code>, creada en un BrowserContext nuevo y destruida al terminar.
    Nunca necesitás importar ni inicializar <code class="inline">page</code>: simplemente la
    declarás entre los parámetros de la función de test.</p>

    {code_block("""// page, context, browser, request — fixtures built-in disponibles en cualquier test
test('ejemplo con múltiples fixtures', async ({ page, context, request }) => {
  // page: la Page activa (tab del navegador)
  await page.goto('/login');

  // context: el BrowserContext (útil para crear pages adicionales)
  const otraPage = await context.newPage();
  await otraPage.goto('/admin');

  // request: para llamadas HTTP puras sin navegador
  const resp = await request.get('/api/health');
  expect(resp.ok()).toBeTruthy();
});""", "ts")}

    <h2>test.only, test.skip y test.fixme</h2>
    {code_block("""// Correr solo este test (útil mientras debuggeás)
test.only('este es el único que corre', async ({ page }) => { /* ... */ });

// Saltar este test
test.skip('pendiente de implementar', async ({ page }) => { /* ... */ });

// Marcar como roto (corre y se espera que falle)
test.fixme('este test falla conocido', async ({ page }) => { /* ... */ });""", "ts")}

    <h2>test.step — para legibilidad en tests largos</h2>
    {code_block("""test('checkout completo', async ({ page }) => {
  await test.step('Agregar producto al carrito', async () => {
    await page.goto('/productos');
    await page.getByRole('button', { name: 'Agregar' }).first().click();
  });

  await test.step('Ir al checkout', async () => {
    await page.getByRole('link', { name: 'Ver carrito' }).click();
    await page.getByRole('button', { name: 'Pagar ahora' }).click();
  });

  await test.step('Verificar confirmación', async () => {
    await expect(page.getByRole('heading', { name: 'Pedido confirmado' })).toBeVisible();
  });
});""", "ts")}

    {callout("tip", "test.step aparece en el trace y el reporte",
        '<p>Los pasos nombrados con <code class="inline">test.step</code> aparecen como secciones '
        'diferenciadas en el Trace Viewer y el reporte HTML. Es la forma más directa de hacer '
        'un test largo legible tanto para quien lo escribe como para quien lo lee en el reporte.</p>')}
    '''
    return page("El núcleo de PW", "pw-6", "Anatomía de un test", body)


# =====================================================================
# SECCIÓN pw-7 — COMANDOS ESENCIALES
# =====================================================================
def section_pw_07():
    body = f'''
    <p>Esta es la referencia de las acciones más usadas sobre una <code class="inline">Page</code>
    y sus <code class="inline">Locator</code>s. Todas son <code class="inline">async</code>:
    recordá el <code class="inline">await</code>.</p>

    <h2>Navegación</h2>
    {table(
        ["Comando", "Equivalente Cypress", "Descripción"],
        [
            ["<code class='inline'>await page.goto('/ruta')</code>", "<code class='inline'>cy.visit('/')</code>", "Navega a la URL (relativa a baseURL)"],
            ["<code class='inline'>await page.reload()</code>", "<code class='inline'>cy.reload()</code>", "Recarga la página"],
            ["<code class='inline'>await page.goBack()</code>", "<code class='inline'>cy.go('back')</code>", "Navega hacia atrás"],
            ["<code class='inline'>await page.waitForURL(/dashboard/)</code>", "<code class='inline'>cy.url().should('include', ...)</code>", "Espera hasta que la URL cambie"],
        ]
    )}

    <h2>Interacciones con elementos</h2>
    {table(
        ["Comando", "Equivalente Cypress", "Notas"],
        [
            ["<code class='inline'>await locator.click()</code>", "<code class='inline'>.click()</code>", "Click izquierdo estándar"],
            ["<code class='inline'>await locator.dblclick()</code>", "<code class='inline'>.dblclick()</code>", "Doble click"],
            ["<code class='inline'>await locator.fill('texto')</code>", "<code class='inline'>.type('texto')</code>", "<strong>Preferido</strong>: limpia el campo y escribe de una vez"],
            ["<code class='inline'>await locator.type('letra')</code>", "—", "Simula tecla a tecla (útil para autocompletar)"],
            ["<code class='inline'>await locator.clear()</code>", "<code class='inline'>.clear()</code>", "Limpia el contenido del campo"],
            ["<code class='inline'>await locator.press('Enter')</code>", "<code class='inline'>.type('{enter}')</code>", "Presiona una tecla"],
            ["<code class='inline'>await locator.check()</code>", "<code class='inline'>.check()</code>", "Marca un checkbox/radio"],
            ["<code class='inline'>await locator.uncheck()</code>", "<code class='inline'>.uncheck()</code>", "Desmarca un checkbox"],
            ["<code class='inline'>await locator.selectOption('valor')</code>", "<code class='inline'>.select('valor')</code>", "Selecciona en un &lt;select&gt;"],
            ["<code class='inline'>await locator.hover()</code>", "<code class='inline'>.trigger('mouseover')</code>", "Hover sobre el elemento"],
            ["<code class='inline'>await locator.focus()</code>", "<code class='inline'>.focus()</code>", "Da foco al elemento"],
            ["<code class='inline'>await locator.setInputFiles('foto.jpg')</code>", "<code class='inline'>cy.get(input).attachFile(...)</code>", "Sube un archivo"],
        ]
    )}

    <h2>fill vs. type — ¿cuál usar?</h2>
    {code_block("""// fill: limpia el campo y lo rellena de una vez → preferido para la mayoría de casos
await page.getByLabel('Email').fill('ana@mail.com');

// type: simula tecla a tecla, respeta keydown/keypress → útil para autocompletar
await page.getByLabel('Buscar').type('zapatill');
await page.getByRole('option', { name: 'Zapatillas Runner' }).click();""", "ts")}

    <h2>Capturas y estado de la página</h2>
    {table(
        ["Comando", "Descripción"],
        [
            ["<code class='inline'>await page.screenshot({ path: 'img.png' })</code>", "Captura de pantalla completa"],
            ["<code class='inline'>await locator.screenshot({ path: 'elem.png' })</code>", "Captura solo del elemento"],
            ["<code class='inline'>await page.title()</code>", "Devuelve el título de la página (string)"],
            ["<code class='inline'>await page.url()</code>", "URL actual (string)"],
            ["<code class='inline'>await locator.textContent()</code>", "Texto del elemento (string)"],
            ["<code class='inline'>await locator.inputValue()</code>", "Valor actual de un input (string)"],
            ["<code class='inline'>await locator.isVisible()</code>", "¿Es visible? (boolean)"],
            ["<code class='inline'>await locator.isEnabled()</code>", "¿Está habilitado? (boolean)"],
        ]
    )}

    {callout("warning", "Evitá usar el valor retornado para aserciones",
        '<p>Si hacés <code class="inline">const text = await locator.textContent(); expect(text).toBe(\'Hola\');</code>, '
        'perdés el <strong>auto-retry</strong> de Playwright. Usá siempre las aserciones web-first: '
        '<code class="inline">await expect(locator).toHaveText(\'Hola\')</code>. '
        'Esas sí reintentan hasta que se cumplan o venza el timeout.</p>')}

    <h2>Esperar eventos de red</h2>
    {code_block("""// Esperá una respuesta específica
const [response] = await Promise.all([
  page.waitForResponse('/api/usuarios'),
  page.getByRole('button', { name: 'Cargar' }).click(),
]);
expect(response.ok()).toBeTruthy();

// Alternativamente: waitForURL después de una navegación
await page.getByRole('link', { name: 'Perfil' }).click();
await page.waitForURL(/perfil/);""", "ts")}
    '''
    return page("El núcleo de PW", "pw-7", "Comandos esenciales", body)


# =====================================================================
# SECCIÓN pw-8 — ASERCIONES WEB-FIRST
# =====================================================================
def section_pw_08():
    body = f'''
    <p>Las aserciones de Playwright se llaman <strong>web-first assertions</strong> porque
    <em>reintentan automáticamente</em> hasta que la condición se cumple o vence el timeout
    configurado. Es el equivalente al <code class="inline">.should()</code> de Cypress, pero
    con sintaxis estándar de Jest/expect y soporte de <code class="inline">async/await</code>.</p>

    {callout("warning", "Siempre expect(locator), nunca expect(await locator.textContent())",
        '<p>La clave del auto-retry está en pasar el <em>Locator</em> al expect, no el valor ya '
        'resuelto. <code class="inline">expect(locator).toHaveText(\'X\')</code> reintenta. '
        '<code class="inline">expect(await locator.textContent()).toBe(\'X\')</code> '
        '<strong>no reintenta</strong>: si el texto no está listo, falla de inmediato.</p>')}

    <h2>Aserciones de visibilidad y estado</h2>
    {table(
        ["Aserción", "Qué verifica", "Opuesto"],
        [
            ["<code class='inline'>toBeVisible()</code>", "El elemento es visible en la página", "<code class='inline'>toBeHidden()</code>"],
            ["<code class='inline'>toBeEnabled()</code>", "El elemento está habilitado (no disabled)", "<code class='inline'>toBeDisabled()</code>"],
            ["<code class='inline'>toBeChecked()</code>", "Un checkbox/radio está marcado", "<code class='inline'>not.toBeChecked()</code>"],
            ["<code class='inline'>toBeEditable()</code>", "El input es editable", "<code class='inline'>not.toBeEditable()</code>"],
            ["<code class='inline'>toBeEmpty()</code>", "El elemento no tiene contenido", "—"],
            ["<code class='inline'>toBeFocused()</code>", "El elemento tiene el foco", "—"],
            ["<code class='inline'>toBeAttached()</code>", "El elemento está en el DOM (aunque no visible)", "—"],
        ]
    )}

    <h2>Aserciones de contenido</h2>
    {table(
        ["Aserción", "Descripción"],
        [
            ["<code class='inline'>toHaveText('texto')</code>", "El texto <em>exacto</em> del elemento (trimmed)"],
            ["<code class='inline'>toContainText('parcial')</code>", "El elemento <em>contiene</em> ese texto"],
            ["<code class='inline'>toHaveText(/regex/)</code>", "El texto matchea la expresión regular"],
            ["<code class='inline'>toHaveValue('valor')</code>", "El valor actual de un input/select"],
            ["<code class='inline'>toHaveAttribute('attr', 'valor')</code>", "El elemento tiene ese atributo con ese valor"],
            ["<code class='inline'>toHaveClass('clase')</code>", "El elemento tiene esa clase CSS"],
            ["<code class='inline'>toHaveCount(n)</code>", "El locator matchea exactamente n elementos"],
        ]
    )}

    {code_block("""// Ejemplos de uso
await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
await expect(page.getByRole('button', { name: 'Enviar' })).toBeEnabled();
await expect(page.getByTestId('cart-count')).toHaveText('3');
await expect(page.getByLabel('Email')).toHaveValue('ana@mail.com');
await expect(page.getByRole('listitem')).toHaveCount(5);
await expect(page.getByTestId('banner')).toHaveAttribute('aria-live', 'polite');

// Negación
await expect(page.getByRole('button', { name: 'Sin stock' })).toBeDisabled();
await expect(page.getByTestId('modal')).not.toBeVisible();""", "ts")}

    <h2>Aserciones de página (no de elemento)</h2>
    {code_block("""// URL actual
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveURL(/dashboard/);

// Título de la página
await expect(page).toHaveTitle('Mi App — Dashboard');
await expect(page).toHaveTitle(/Dashboard/);""", "ts")}

    <h2>Soft assertions — no detienen el test al fallar</h2>
    {code_block("""// Las soft assertions acumulan fallos sin lanzar excepción inmediata
test('verificar múltiples campos del perfil', async ({ page }) => {
  await page.goto('/perfil');

  // Estas tres aserciones se verifican TODAS, aunque alguna falle
  await expect.soft(page.getByLabel('Nombre')).toHaveValue('Ana');
  await expect.soft(page.getByLabel('Email')).toHaveValue('ana@mail.com');
  await expect.soft(page.getByLabel('Rol')).toHaveValue('Admin');

  // Al final del test, si alguna soft assertion falló, el test falla
  // y el reporte muestra TODOS los fallos, no solo el primero
});""", "ts")}

    {callout("tip", "¿Cuándo usar soft assertions?",
        '<p>Son útiles cuando querés verificar un estado de UI que tiene múltiples campos '
        '(un formulario, un perfil, un detalle de pedido) y querés ver todos los fallos de una vez '
        'en lugar de tener que correr el test N veces para encontrarlos de a uno.</p>')}

    <h2>Comparación rápida con Cypress</h2>
    {table(
        ["Cypress (.should)", "Playwright (expect web-first)"],
        [
            ["<code class='inline'>.should('be.visible')</code>", "<code class='inline'>await expect(loc).toBeVisible()</code>"],
            ["<code class='inline'>.should('have.text', 'x')</code>", "<code class='inline'>await expect(loc).toHaveText('x')</code>"],
            ["<code class='inline'>.should('have.value', 'x')</code>", "<code class='inline'>await expect(loc).toHaveValue('x')</code>"],
            ["<code class='inline'>.should('be.disabled')</code>", "<code class='inline'>await expect(loc).toBeDisabled()</code>"],
            ["<code class='inline'>.should('have.length', n)</code>", "<code class='inline'>await expect(loc).toHaveCount(n)</code>"],
        ]
    )}
    '''
    return page("El núcleo de PW", "pw-8", "Aserciones web-first", body)
