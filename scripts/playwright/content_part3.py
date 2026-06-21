# -*- coding: utf-8 -*-
"""Contenido Playwright — Parte 3: secciones pw-9 a pw-12."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from helpers import code_block, callout, table, figure
from playwright.content_part1 import page
from playwright import diagrams as dg


# =====================================================================
# SECCIÓN pw-9 — DATOS DE PRUEBA Y FIXTURES
# =====================================================================
def section_pw_09():
    body = f'''
    <p>Playwright tiene dos conceptos separados que se llaman "fixture" y es importante no
    confundirlos:</p>
    <ul>
      <li><strong>Fixtures de datos:</strong> archivos JSON (o cualquier formato) con datos
      de prueba estáticos. Concepto análogo al de Cypress.</li>
      <li><strong>Fixtures de Playwright:</strong> un sistema de inyección de dependencias
      basado en <code class="inline">test.extend()</code> para compartir setup entre tests.
      Este es el concepto poderoso y único de Playwright, sin equivalente en Cypress.</li>
    </ul>

    <h2>1. Fixtures de datos — archivos JSON</h2>
    <p>La forma más simple: archivos de datos que importás directamente en los tests.</p>
    {code_block("""{
  "usuarios": [
    { "email": "ana@mail.com",   "password": "clave123", "rol": "admin" },
    { "email": "beto@mail.com",  "password": "pass456",  "rol": "viewer" }
  ]
}""", "json", "tests/fixtures/usuarios.json")}

    {code_block("""// Tipar los datos con TypeScript
interface Usuario {
  email:    string;
  password: string;
  rol:      'admin' | 'viewer';
}
interface UsuariosFixture {
  usuarios: Usuario[];
}

// Importar y usar en el test
import usuariosData from '../fixtures/usuarios.json';
const data = usuariosData as UsuariosFixture;

test('admin puede acceder al panel', async ({ page }) => {
  const admin = data.usuarios.find(u => u.rol === 'admin')!;
  await page.goto('/login');
  await page.getByLabel('Email').fill(admin.email);
  await page.getByLabel('Contraseña').fill(admin.password);
  await page.getByRole('button', { name: 'Ingresar' }).click();
  await expect(page).toHaveURL(/admin/);
});""", "ts", "tests/login.spec.ts")}

    <h2>2. Fixtures de Playwright — inyección de dependencias</h2>
    <p>Este es el sistema propio de Playwright. Funciona con <code class="inline">test.extend()</code>:
    definís "fixtures" como funciones que reciben otras fixtures y las proporcionan al test.
    El runner se encarga de crear, inyectar y destruir cada fixture en el orden correcto.</p>

    {callout("info", "¿Por qué esto no existe en Cypress?",
        '<p>Cypress resuelve el setup compartido con <code class="inline">beforeEach()</code> y '
        'custom commands. Playwright eligió un modelo más estructurado: las fixtures son '
        'explícitas (aparecen en la firma del test), componibles (una fixture puede usar otras) '
        'y con teardown incorporado (el cleanup vive en la misma función, no en afterEach).</p>')}

    {code_block("""// tests/fixtures/auth.ts
import { test as base, Page } from '@playwright/test';

// Tipo de tus fixtures custom
interface MisFixtures {
  paginaLogueada: Page;
  usuarioAdmin:   { email: string; nombre: string };
}

// Extender el test base con tus fixtures
export const test = base.extend<MisFixtures>({

  // Fixture que autentica al usuario antes de cada test
  paginaLogueada: async ({ page }, use) => {
    // --- SETUP ---
    await page.goto('/login');
    await page.getByLabel('Email').fill('ana@mail.com');
    await page.getByLabel('Contraseña').fill('clave123');
    await page.getByRole('button', { name: 'Ingresar' }).click();
    await page.waitForURL(/dashboard/);

    // "use" hace disponible la fixture al test
    await use(page);

    // --- TEARDOWN (opcional, el BrowserContext se destruye de todas formas) ---
    await page.goto('/logout');
  },

  // Fixture de datos: no necesita teardown
  usuarioAdmin: async ({}, use) => {
    await use({ email: 'ana@mail.com', nombre: 'Ana García' });
  },
});

// Re-exportar expect para que los tests solo importen desde acá
export { expect } from '@playwright/test';""", "ts", "tests/fixtures/auth.ts")}

    {code_block("""// tests/dashboard.spec.ts — importa el test extendido, no el original
import { test, expect } from './fixtures/auth';

// paginaLogueada está disponible automáticamente, sin beforeEach
test('dashboard muestra el nombre del usuario', async ({ paginaLogueada, usuarioAdmin }) => {
  await expect(paginaLogueada.getByText(usuarioAdmin.nombre)).toBeVisible();
});

test('puede acceder a configuración', async ({ paginaLogueada }) => {
  await paginaLogueada.getByRole('link', { name: 'Configuración' }).click();
  await expect(paginaLogueada).toHaveURL(/configuracion/);
});""", "ts", "tests/dashboard.spec.ts")}

    {callout("best", "Composición de fixtures: la ventaja real",
        '<p>Una fixture puede recibir otras fixtures. Podés tener <code class="inline">paginaAdmin</code> '
        'que use <code class="inline">paginaLogueada</code>, que use <code class="inline">page</code>. '
        'El runner resuelve el grafo de dependencias automáticamente. El resultado: tests muy '
        'legibles y setup completamente reutilizable sin globals ni beforeEach anidados.</p>')}
    '''
    return page("Organización", "pw-9", "Datos de prueba y fixtures de Playwright", body)


# =====================================================================
# SECCIÓN pw-10 — PAGE OBJECT MODEL Y FIXTURES CUSTOM
# =====================================================================
def section_pw_10():
    body = f'''
    <p>En Cypress, los custom commands (<code class="inline">Cypress.Commands.add()</code>)
    son el mecanismo para reutilizar lógica de UI. En Playwright, ese rol lo cumple el
    <strong>Page Object Model (POM)</strong> combinado con fixtures. No existe el concepto
    de "commands globales": la reutilización es explícita y tipada.</p>

    <h2>¿Por qué POM en vez de custom commands?</h2>
    {table(
        ["Cypress custom commands", "Playwright Page Objects + fixtures"],
        [
            ["<code class='inline'>cy.login('ana', '123')</code>", "<code class='inline'>await loginPage.login('ana', '123')</code>"],
            ["Globales: se agregan al namespace cy", "Clases tipadas, sin polución de globales"],
            ["Definición: <code class='inline'>commands.ts</code> (un archivo)", "Una clase por página/componente (organización natural)"],
            ["Difícil de reutilizar entre tipos de tests", "Fácil de compartir como fixture"],
        ],
        widths=["50%", "50%"]
    )}

    <h2>Un Page Object básico</h2>
    {code_block("""// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  // Locators como propiedades de clase: se definen una vez, se usan en muchos tests
  readonly emailInput:  Locator;
  readonly passInput:   Locator;
  readonly submitBtn:   Locator;
  readonly errorMsg:    Locator;

  constructor(private page: Page) {
    this.emailInput = page.getByLabel('Email');
    this.passInput  = page.getByLabel('Contraseña');
    this.submitBtn  = page.getByRole('button', { name: 'Ingresar' });
    this.errorMsg   = page.getByTestId('login-error');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passInput.fill(password);
    await this.submitBtn.click();
  }

  async loginAndWait(email: string, password: string) {
    await this.login(email, password);
    await this.page.waitForURL(/dashboard/);
  }
}""", "ts", "pages/LoginPage.ts")}

    <h2>Usar el Page Object en un test</h2>
    {code_block("""// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('login exitoso redirige al dashboard', async ({ page }) => {
    await loginPage.loginAndWait('ana@mail.com', 'clave123');
    await expect(page).toHaveURL(/dashboard/);
  });

  test('credenciales incorrectas muestran error', async () => {
    await loginPage.login('ana@mail.com', 'malaclave');
    await expect(loginPage.errorMsg).toBeVisible();
    await expect(loginPage.errorMsg).toContainText('inválidas');
  });
});""", "ts")}

    <h2>Integrar el POM con el sistema de fixtures</h2>
    <p>La combinación más poderosa: envolvé la instanciación del Page Object en una fixture,
    para no repetir el <code class="inline">new LoginPage(page)</code> en cada test.</p>
    {code_block("""// tests/fixtures/pages.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { DashboardPage } from '../../pages/DashboardPage';

interface PageFixtures {
  loginPage:     LoginPage;
  dashboardPage: DashboardPage;
}

export const test = base.extend<PageFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});
export { expect } from '@playwright/test';""", "ts", "tests/fixtures/pages.ts")}

    {code_block("""// tests/login.spec.ts — limpio, sin new, sin beforeEach de setup
import { test, expect } from './fixtures/pages';

test('login exitoso', async ({ loginPage }) => {
  await loginPage.goto();
  await loginPage.loginAndWait('ana@mail.com', 'clave123');
});""", "ts")}

    {callout("best", "Regla: un Page Object por pantalla o componente importante",
        '<p>Creá una clase por página o componente complejo (<code class="inline">LoginPage</code>, '
        '<code class="inline">CheckoutPage</code>, <code class="inline">Header</code>). '
        'No pongas toda la app en un solo archivo ni hagas Page Objects para páginas triviales.</p>')}
    '''
    return page("Organización", "pw-10", "Page Object Model y fixtures custom", body)


# =====================================================================
# SECCIÓN pw-11 — INTERCEPTACIÓN Y MOCK DE RED
# =====================================================================
def section_pw_11():
    body = f'''
    <p>Playwright intercepta y modifica requests de red con <code class="inline">page.route()</code>,
    el equivalente de <code class="inline">cy.intercept()</code> en Cypress. La API es async/await,
    y tiene soporte para modificar headers, cuerpo, status code, o directamente abortar la request.</p>

    {figure(dg.PW_ROUTE_DIAGRAM, "page.route() intercepta la request antes de que salga al servidor y puede responder con un mock.")}

    <h2>Mockear una respuesta completa</h2>
    {code_block("""test('muestra la lista mockeada de usuarios', async ({ page }) => {
  // Registrar el handler ANTES de navegar
  await page.route('/api/usuarios', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, nombre: 'Ana García',  email: 'ana@mail.com' },
        { id: 2, nombre: 'Beto López',  email: 'beto@mail.com' },
      ]),
    });
  });

  await page.goto('/usuarios');
  await expect(page.getByRole('listitem')).toHaveCount(2);
  await expect(page.getByText('Ana García')).toBeVisible();
});""", "ts")}

    <h2>Modificar (no reemplazar) la respuesta real</h2>
    {code_block("""test('inyecta un campo extra en la respuesta real', async ({ page }) => {
  await page.route('/api/perfil', async route => {
    // Obtener la respuesta real del servidor
    const response = await route.fetch();
    const json = await response.json();

    // Modificar y reenviar
    json.badge = 'beta-tester';
    await route.fulfill({ json });
  });

  await page.goto('/perfil');
  await expect(page.getByTestId('badge')).toHaveText('beta-tester');
});""", "ts")}

    <h2>Simular errores de red</h2>
    {code_block("""// Abortar la request (simula corte de red)
await page.route('/api/usuarios', route => route.abort());

// Responder con un error HTTP
await page.route('/api/usuarios', route =>
  route.fulfill({ status: 500, body: 'Error interno' })
);

// Pasar la request al servidor sin modificar (útil para desactivar parcialmente)
await page.route('/api/usuarios', route => route.continue());""", "ts")}

    <h2>Esperar una request o respuesta</h2>
    {code_block("""// Patrón: lanzar la acción y esperar la response en paralelo
const [response] = await Promise.all([
  page.waitForResponse(resp => resp.url().includes('/api/usuarios') && resp.status() === 200),
  page.getByRole('button', { name: 'Recargar' }).click(),
]);
const data = await response.json();
expect(data.length).toBeGreaterThan(0);

// Forma simple: solo esperar la URL
await Promise.all([
  page.waitForResponse('/api/usuarios'),
  page.reload(),
]);""", "ts")}

    <h2>Comparación rápida con cy.intercept()</h2>
    {table(
        ["Cypress", "Playwright"],
        [
            ["<code class='inline'>cy.intercept('GET', '/api/u', { fixture: 'u.json' })</code>", "<code class='inline'>await page.route('/api/u', r => r.fulfill({ json: data }))</code>"],
            ["<code class='inline'>cy.intercept(...).as('alias')</code>", "No hay alias: guardás la Promise directamente"],
            ["<code class='inline'>cy.wait('@alias')</code>", "<code class='inline'>await page.waitForResponse('/api/u')</code>"],
            ["<code class='inline'>cy.intercept(url, req => { req.reply(resp => {...}) })</code>", "<code class='inline'>route.fetch() luego route.fulfill(modified)</code>"],
        ]
    )}

    {callout("tip", "Usá page.route() en el setup si el mock aplica a muchos tests",
        '<p>Si necesitás el mismo mock en varios tests, registrá el handler en '
        '<code class="inline">test.beforeEach</code> o creá una fixture que lo inyecte. '
        'Así no repetís el <code class="inline">await page.route(...)</code> en cada test.</p>')}
    '''
    return page("Organización", "pw-11", "Interceptación y mock de red", body)


# =====================================================================
# SECCIÓN pw-12 — MULTI-NAVEGADOR Y MULTI-CONTEXTO
# =====================================================================
def section_pw_12():
    body = f'''
    <p>Dos de las capacidades más distintivas de Playwright: correr los mismos tests en
    múltiples navegadores con un solo config, y simular múltiples usuarios en el mismo test
    con <code class="inline">BrowserContext</code>s independientes.</p>

    <h2>Multi-navegador: projects en playwright.config.ts</h2>
    {code_block("""// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    // Desktop browsers
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } },

    // Mobile
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 14'] } },

    // Con viewport y base URL específicos
    {
      name: 'tablet',
      use: {
        ...devices['iPad Pro'],
        baseURL: 'https://staging.miapp.com',
      },
    },
  ],
});""", "ts", "playwright.config.ts")}

    {code_block("""# Correr todos los projects
npx playwright test

# Solo un project específico
npx playwright test --project=firefox

# Un test file en un project
npx playwright test tests/login.spec.ts --project=webkit""", "bash")}

    {callout("info", "Diferencia clave con Cypress",
        '<p>En Cypress, correr en Firefox requiere configuración adicional y sigue siendo experimental '
        'para algunas funcionalidades. WebKit (Safari) no está disponible en Cypress. En Playwright, '
        'los tres motores son ciudadanos de primera clase: misma API, mismo nivel de soporte.</p>')}

    <h2>Multi-contexto en un solo test: simular dos usuarios</h2>
    <p>Un caso común en aplicaciones colaborativas: verificar que la acción de un usuario
    se refleja para otro usuario en tiempo real.</p>
    {code_block("""test('dos usuarios ven el mismo documento compartido', async ({ browser }) => {
  // Crear dos contextos completamente aislados
  const ctxUsuario1 = await browser.newContext();
  const ctxUsuario2 = await browser.newContext();

  const pageUsuario1 = await ctxUsuario1.newPage();
  const pageUsuario2 = await ctxUsuario2.newPage();

  // Usuario 1 se loguea y crea un documento
  await pageUsuario1.goto('/login');
  await pageUsuario1.getByLabel('Email').fill('ana@mail.com');
  await pageUsuario1.getByLabel('Contraseña').fill('clave123');
  await pageUsuario1.getByRole('button', { name: 'Ingresar' }).click();
  await pageUsuario1.getByRole('button', { name: 'Nuevo documento' }).click();

  // Obtener el link para compartir
  const shareUrl = await pageUsuario1.getByTestId('share-url').inputValue();

  // Usuario 2 accede al documento con el link
  await pageUsuario2.goto(shareUrl);
  await expect(pageUsuario2.getByRole('heading', { name: 'Documento sin título' })).toBeVisible();

  // Usuario 1 edita, usuario 2 ve el cambio
  await pageUsuario1.getByRole('textbox', { name: 'Título' }).fill('Mi documento');
  await expect(pageUsuario2.getByRole('heading', { name: 'Mi documento' })).toBeVisible();

  // Cleanup
  await ctxUsuario1.close();
  await ctxUsuario2.close();
});""", "ts")}

    <h2>Almacenar y reutilizar estado de autenticación</h2>
    <p>Para no hacer login en cada test, Playwright permite guardar el estado del BrowserContext
    (cookies + localStorage) en un archivo y reutilizarlo.</p>
    {code_block("""// tests/auth.setup.ts — corre una sola vez antes de los tests
import { test as setup, expect } from '@playwright/test';

setup('autenticar y guardar estado', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('ana@mail.com');
  await page.getByLabel('Contraseña').fill('clave123');
  await page.getByRole('button', { name: 'Ingresar' }).click();
  await page.waitForURL(/dashboard/);

  // Guarda cookies + localStorage en un archivo
  await page.context().storageState({ path: 'playwright/.auth/ana.json' });
});""", "ts", "tests/auth.setup.ts")}

    {code_block("""// playwright.config.ts — configurar el storageState por project
export default defineConfig({
  projects: [
    // Proyecto de setup: corre primero
    { name: 'setup', testMatch: /.*\\.setup\\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Cada test arranca ya autenticado
        storageState: 'playwright/.auth/ana.json',
      },
      dependsOn: ['setup'],
    },
  ],
});""", "ts")}
    '''
    return page("Organización", "pw-12", "Multi-navegador y multi-contexto", body)
