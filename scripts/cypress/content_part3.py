# -*- coding: utf-8 -*-
"""Contenido del documento — Parte 3: secciones 9 a 12."""
from helpers import code_block, callout, table, figure
from content_part1 import page
import diagrams as dg


# =====================================================================
# SECCIÓN 9 — FIXTURES
# =====================================================================
def section_09():
    body = f'''
    <p>Las <strong>fixtures</strong> son archivos (normalmente JSON) con datos de prueba fijos:
    usuarios, productos, respuestas de API simuladas, etc. Vivem en
    <code class="inline">cypress/fixtures/</code> y se cargan con <code class="inline">cy.fixture()</code>.</p>

    <h2>Crear una fixture</h2>
    {code_block("""{
  "email": "ana@mail.com",
  "password": "Secreta123!",
  "nombre": "Ana Gomez"
}""", "json", "cypress/fixtures/usuario-valido.json")}

    <h2>Usarla en un test</h2>
    {code_block("""describe("Login con datos de fixture", () => {
  it("inicia sesion con un usuario valido", () => {
    cy.fixture("usuario-valido.json").then((usuario) => {
      cy.visit("/login");
      cy.get('[data-cy="email"]').type(usuario.email);
      cy.get('[data-cy="password"]').type(usuario.password);
      cy.get('[data-cy="submit"]').click();
    });
  });
});""", "ts")}

    {callout("tip", "Tipá tus fixtures", '<p>Definí una interface para que TypeScript te avise si '
        'falta un campo o lo escribiste mal:</p>'
        + code_block("""interface UsuarioFixture {
  email: string;
  password: string;
  nombre: string;
}

cy.fixture<UsuarioFixture>("usuario-valido.json").then((usuario) => {
  cy.get('[data-cy="email"]').type(usuario.email); // autocompletado + chequeo de tipos
});""", "ts"))}

    <h2>Fixtures + <code class="inline">cy.intercept()</code>: el combo más usado</h2>
    <p>La combinación más poderosa: usar una fixture como respuesta simulada de una API, para no
    depender de un backend real corriendo durante el test (lo vas a ver en detalle en la sección 11):</p>
    {code_block("""cy.intercept("GET", "/api/productos", { fixture: "productos.json" }).as("getProductos");
cy.visit("/catalogo");
cy.wait("@getProductos");""", "ts")}

    {table(
        ["Buena práctica", "Por qué"],
        [
            ["Una fixture por escenario (válido, inválido, vacío, error)", "Tests claros y fáciles de mantener"],
            ["Nombres descriptivos: <code class='inline'>usuario-admin.json</code>, no <code class='inline'>data1.json</code>", "Cualquiera del equipo entiende qué representa"],
            ["Tipar las fixtures con interfaces de TS", "Evita errores de tipeo silenciosos"],
            ["No poner credenciales reales en fixtures versionadas", "Seguridad: usá variables de entorno para secretos reales"],
        ]
    )}
    '''
    return page("Organización de datos", 9, "Fixtures y datos de prueba", body)


# =====================================================================
# SECCIÓN 10 — CUSTOM COMMANDS
# =====================================================================
def section_10():
    body = f'''
    <p>Cuando un mismo flujo se repite en muchos tests (el típico ejemplo: el login), conviene
    extraerlo a un <strong>comando personalizado</strong>. Se definen en
    <code class="inline">cypress/support/commands.ts</code> y quedan disponibles como
    <code class="inline">cy.miComando()</code> en cualquier test.</p>

    <h2>Definir el comando</h2>
    {code_block("""// cypress/support/commands.ts

Cypress.Commands.add("login", (email: string, password: string) => {
  cy.visit("/login");
  cy.get('[data-cy="email"]').type(email);
  cy.get('[data-cy="password"]').type(password);
  cy.get('[data-cy="submit"]').click();
  cy.url().should("include", "/dashboard");
});""", "ts", "cypress/support/commands.ts")}

    <h2>Tiparlo para TypeScript (paso clave, no opcional)</h2>
    <p>Si no hacés esto, TypeScript va a marcar error en <code class="inline">cy.login(...)</code>
    porque no sabe que ese comando existe. Hay que extender la interface global
    <code class="inline">Cypress.Chainable</code>:</p>
    {code_block("""// cypress/support/index.d.ts  (o al final de commands.ts)

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Inicia sesion con email y password, y espera a llegar al dashboard.
       * @example cy.login("ana@mail.com", "Secreta123!")
       */
      login(email: string, password: string): Chainable<void>;
    }
  }
}

export {};""", "ts", "cypress/support/index.d.ts")}

    <h2>Usarlo en cualquier test</h2>
    {code_block("""describe("Dashboard", () => {
  beforeEach(() => {
    cy.login("ana@mail.com", "Secreta123!"); // una linea en vez de 5
  });

  it("muestra el nombre del usuario", () => {
    cy.get('[data-cy="bienvenida"]').should("contain.text", "Ana");
  });
});""", "ts")}

    <h2>Asegurate de importar el archivo de comandos</h2>
    {code_block("""// cypress/support/e2e.ts
import "./commands";""", "ts", "cypress/support/e2e.ts")}

    {callout("best", "¿Cuándo crear un custom command?",
        '<p>Regla práctica: si copiás y pegás el mismo bloque de 3 o más líneas en 3 o más tests, '
        'es candidato a comando personalizado. Cosas típicas: login, agregar producto al carrito, '
        'crear un recurso vía API antes del test (más rápido que hacerlo por UI), seleccionar un '
        'elemento por <code class="inline">data-cy</code> con sintaxis más corta, etc.</p>')}

    <h2>Otro ejemplo útil: selector corto por data-cy</h2>
    {code_block("""Cypress.Commands.add("getByCy", (valor: string) => {
  return cy.get(`[data-cy="${valor}"]`);
});

// uso:
cy.getByCy("submit-button").click(); // mas corto que cy.get('[data-cy="submit-button"]')""", "ts")}
    '''
    return page("Reutilización", 10, "Comandos personalizados (custom commands)", body)


# =====================================================================
# SECCIÓN 11 — CY.INTERCEPT
# =====================================================================
def section_11():
    body = f'''
    <p><code class="inline">cy.intercept()</code> te permite observar, modificar o reemplazar
    cualquier request de red que haga tu aplicación, sin tocar el backend. Es una de las
    funcionalidades que más distingue a Cypress de otras herramientas.</p>

    {figure(dg.INTERCEPT_DIAGRAM, "cy.intercept() se para entre tu app y la red real, y puede responder con datos simulados.")}

    <h2>Sintaxis básica</h2>
    {code_block("""cy.intercept(metodo, url, respuesta?)""", "ts")}

    <h2>Caso 1: sólo espiar (sin modificar nada)</h2>
    {code_block("""cy.intercept("POST", "/api/login").as("loginRequest");
cy.get('[data-cy="submit"]').click();
cy.wait("@loginRequest").its("response.statusCode").should("eq", 200);""", "ts")}

    <h2>Caso 2: mockear la respuesta completa</h2>
    {code_block("""cy.intercept("GET", "/api/productos", {
  statusCode: 200,
  body: [
    { id: 1, nombre: "Zapatillas", precio: 15000 },
    { id: 2, nombre: "Remera", precio: 5000 },
  ],
}).as("getProductos");

cy.visit("/catalogo");
cy.wait("@getProductos");
cy.get('[data-cy="producto"]').should("have.length", 2);""", "ts")}

    <h2>Caso 3: mockear con una fixture (más prolijo)</h2>
    {code_block("""cy.intercept("GET", "/api/productos", { fixture: "productos.json" }).as("getProductos");""", "ts")}

    <h2>Caso 4: simular un error del servidor</h2>
    {code_block("""cy.intercept("GET", "/api/productos", {
  statusCode: 500,
  body: { error: "Error interno del servidor" },
}).as("getProductosError");

cy.visit("/catalogo");
cy.wait("@getProductosError");
cy.get('[data-cy="mensaje-error"]').should("be.visible");""", "ts")}

    <h2>Caso 5: usar un wildcard / patrón de URL</h2>
    {code_block("""cy.intercept("GET", "/api/productos/*", { fixture: "producto-detalle.json" });
cy.intercept("**/api/usuarios/**").as("cualquierLlamadaAUsuarios");""", "ts")}

    {table(
        ["¿Por qué usar intercept en vez de pegarle a una API real?", "Beneficio"],
        [
            ["No depende de que el backend esté levantado y con datos", "Tests más rápidos y confiables (deterministas)"],
            ["Podés simular casos difíciles de reproducir (errores 500, respuestas lentas, listas vacías)", "Cobertura de casos límite sin esfuerzo"],
            ["<code class='inline'>cy.wait(\"@alias\")</code> espera al request real, no a un tiempo fijo", "Elimina <code class='inline'>cy.wait(3000)</code> y el \"flakiness\""],
        ]
    )}

    {callout("warning", "No abuses del mock", '<p>Mockear TODO hace que tus tests E2E dejen de '
        'probar la integración real con el backend. Una estrategia sana: usar datos reales en los '
        'flujos críticos (ej. compra completa) y mockear en tests que prueban casos de UI específicos '
        '(errores, estados vacíos, listas grandes).</p>')}
    '''
    return page("Red y mocking", 11, "Interceptación de red con cy.intercept", body)


# =====================================================================
# SECCIÓN 12 — PAGE OBJECT MODEL
# =====================================================================
def section_12():
    body = f'''
    <p>El <strong>Page Object Model (POM)</strong> es un patrón de diseño: en vez de escribir
    selectores CSS sueltos en cada test, los encapsulás dentro de una clase que representa una
    página (o un componente). El test queda leyendo como una descripción del flujo de negocio,
    no como una lista de selectores.</p>

    {figure(dg.POM_DIAGRAM, "El test usa metodos de alto nivel; la clase Page Object es la unica que conoce los selectores CSS reales.")}

    <h2>Sin Page Object Model (selectores sueltos)</h2>
    {code_block("""it("inicia sesion", () => {
  cy.visit("/login");
  cy.get('[data-cy="email"]').type("ana@mail.com");
  cy.get('[data-cy="password"]').type("Secreta123!");
  cy.get('[data-cy="submit"]').click();
});""", "ts")}

    <h2>Con Page Object Model</h2>
    {code_block("""// cypress/pages/LoginPage.ts

class LoginPage {
  visit() {
    cy.visit("/login");
    return this;
  }

  typeEmail(email: string) {
    cy.get('[data-cy="email"]').type(email);
    return this;
  }

  typePassword(password: string) {
    cy.get('[data-cy="password"]').type(password);
    return this;
  }

  submit() {
    cy.get('[data-cy="submit"]').click();
    return this;
  }

  login(email: string, password: string) {
    this.visit();
    this.typeEmail(email);
    this.typePassword(password);
    this.submit();
  }
}

export default new LoginPage();""", "ts", "cypress/pages/LoginPage.ts")}

    {code_block("""// cypress/e2e/login.cy.ts
import loginPage from "../pages/LoginPage";

it("inicia sesion", () => {
  loginPage.login("ana@mail.com", "Secreta123!");
  cy.url().should("include", "/dashboard");
});""", "ts", "cypress/e2e/login.cy.ts")}

    <h2>Ventajas y costos</h2>
    <div class="two-col">
      <div>
        {callout("best", "A favor", '<ul style="margin:0;padding-left:4mm;">'
            '<li>Si cambia un selector, lo arreglás en un solo lugar</li>'
            '<li>Tests más legibles, casi lenguaje natural</li>'
            '<li>Reutilización entre muchos archivos de test</li></ul>')}
      </div>
      <div>
        {callout("warning", "A tener en cuenta", '<ul style="margin:0;padding-left:4mm;">'
            '<li>Capa extra de abstracción: más código para mantener</li>'
            '<li>En proyectos chicos puede ser sobre-ingeniería</li>'
            '<li>Cypress recomienda priorizar funciones reutilizables simples antes que POM completo</li></ul>')}
      </div>
    </div>

    {callout("info", "Alternativa más liviana: funciones en vez de clases",
        '<p>El equipo de Cypress sugiere, para casos simples, usar funciones sueltas (o custom '
        'commands de la sección 10) en vez de clases con estado. El POM con clases brilla más en '
        'proyectos grandes con muchas páginas y flujos compartidos entre equipos.</p>')}
    '''
    return page("Organización del código", 12, "Page Object Model con TypeScript", body)
