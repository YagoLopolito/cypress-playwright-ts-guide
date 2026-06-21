# -*- coding: utf-8 -*-
"""Contenido del documento — Parte 4: secciones 13 a 16."""
from helpers import code_block, callout, table, figure
from content_part1 import page
import diagrams as dg


# =====================================================================
# SECCIÓN 13 — BUENAS PRÁCTICAS
# =====================================================================
def section_13():
    body = f'''
    <p>Esta es probablemente la sección más importante para escribir tests que el equipo pueda
    mantener en el tiempo sin volverse loco. Son las prácticas recomendadas oficialmente por
    Cypress, más las que se aprenden con experiencia real en proyectos grandes.</p>

    <h2>1. Usá atributos <code class="inline">data-cy</code> para seleccionar elementos</h2>
    <p>Es la práctica más importante de todas. No selecciones por clases CSS, IDs pensados para
    estilos, ni por texto que puede cambiar con la traducción del sitio.</p>
    {code_block("""<!-- En tu HTML/JSX -->
<button class="btn btn-primary mt-2" data-cy="submit-button">Enviar</button>""", "css")}
    {code_block("""// MAL: si el equipo de diseño cambia la clase, el test se rompe
cy.get(".btn-primary").click();

// BIEN: el atributo data-cy no tiene ninguna otra funcion mas que testing
cy.get('[data-cy="submit-button"]').click();""", "ts")}
    {callout("best", "¿Por qué data-cy y no data-test o data-testid?",
        '<p>Cualquiera de los tres funciona igual de bien: lo importante es <strong>elegir uno y '
        'usarlo siempre</strong> en todo el proyecto. <code class="inline">data-cy</code> es la '
        'convención que sugiere la documentación oficial de Cypress.</p>')}

    <h2>2. Los tests deben ser independientes entre sí</h2>
    <p>Cada <code class="inline">it()</code> tiene que poder correr solo, en cualquier orden, sin
    depender de que otro test haya corrido antes.</p>
    {code_block("""// MAL: el segundo test depende de que el primero haya creado el usuario
it("crea un usuario", () => { /* ... */ });
it("edita el usuario creado antes", () => { /* ... */ }); // fragil

// BIEN: cada test deja la app lista desde cero (beforeEach, o vía API)
beforeEach(() => {
  cy.request("POST", "/api/test/seed-usuario"); // crea datos por API, no por UI
});
it("edita un usuario", () => { /* ... */ });""", "ts")}

    <h2>3. Nunca uses esperas de tiempo fijo</h2>
    {code_block("""// MAL: tiempo arbitrario, lento si sobra, fragil si falta
cy.wait(3000);
cy.get('[data-cy="resultado"]').should("be.visible");

// BIEN: esperá una condicion real, o un request interceptado
cy.intercept("GET", "/api/resultado").as("getResultado");
cy.wait("@getResultado");
cy.get('[data-cy="resultado"]').should("be.visible"); // ademas, reintenta solo""", "ts")}

    <h2>4. Creá datos de prueba por API, no por UI, cuando sea posible</h2>
    {code_block("""// Lento: pasar por 5 pantallas de formulario solo para tener un usuario de prueba
cy.visit("/registro");
cy.get(...).type(...);
// ...

// Rapido: si solo necesitas que el usuario EXISTA para testear otra cosa
cy.request("POST", "/api/test/usuarios", { email: "ana@mail.com" });
cy.visit("/login");""", "ts")}
    {callout("tip", "Reservá la UI para lo que realmente estás probando",
        '<p>Si tu test trata sobre el checkout, no hace falta registrar el usuario paso a paso por '
        'pantalla: creá el usuario por API y andá directo al checkout. Así el test es más rápido y '
        'más enfocado en lo que importa.</p>')}

    <h2>5. Evitá lógica condicional dentro de los tests</h2>
    {code_block("""// MAL: un test no deberia "decidir" que camino tomar
cy.get("body").then(($body) => {
  if ($body.find('[data-cy="banner"]').length > 0) {
    cy.get('[data-cy="banner"]').click();
  }
});
// Si esto pasa seguido, el test no es deterministico: indica un problema
// en la app (o en como se prepara el estado) que conviene resolver antes.""", "ts")}

    <h2>6. Mantené los tests cortos y enfocados en un solo comportamiento</h2>
    {table(
        ["En vez de...", "Mejor..."],
        [
            ["Un <code class='inline'>it()</code> gigante que prueba login + carrito + checkout", "Tres <code class='inline'>it()</code> separados, cada uno con su propósito claro"],
            ["Nombres genéricos: <code class='inline'>it(\"funciona\")</code>", "Nombres descriptivos: <code class='inline'>it(\"muestra error si el email es invalido\")</code>"],
        ]
    )}

    <h2>Checklist resumen de buenas prácticas</h2>
    <ul class="checklist">
      <li>Selecciono elementos con <code class="inline">[data-cy="..."]</code>, nunca con clases de estilo</li>
      <li>Cada test es independiente y puede correr solo</li>
      <li>No uso <code class="inline">cy.wait(numero)</code> con tiempo fijo</li>
      <li>Creo datos de prueba por API cuando no estoy probando ese flujo de UI específicamente</li>
      <li>Evito <code class="inline">if/else</code> dentro de los tests</li>
      <li>Uso <code class="inline">baseUrl</code> y variables de entorno en vez de URLs hardcodeadas</li>
      <li>Extraigo flujos repetidos a custom commands</li>
      <li>Los nombres de los tests describen el comportamiento esperado, no la implementación</li>
    </ul>
    '''
    return page("Calidad", 13, "Buenas prácticas", body)


# =====================================================================
# SECCIÓN 14 — ERRORES COMUNES
# =====================================================================
def section_14():
    body = f'''
    <p>Estos son los errores que más se repiten en equipos que recién empiezan con Cypress
    (¡y a veces hasta en equipos con experiencia!). Tenerlos identificados ahorra horas de
    frustración.</p>

    {callout("bad", "Encadenar comandos cy.get() muy largos y frágiles",
        '<p>Selectores como <code class="inline">cy.get("div > div:nth-child(3) > span.value")</code> '
        'se rompen con cualquier cambio mínimo de maquetado. Solución: pedí (o agregá vos mismo) '
        'atributos <code class="inline">data-cy</code> en los componentes relevantes.</p>')}

    {callout("bad", "Asumir que .then() es asíncrono como una Promise normal",
        '<p>Es fácil pensar que podés mezclar libremente <code class="inline">async/await</code> con '
        'comandos de Cypress. No funciona así: dentro de un test, dejá que Cypress maneje el orden '
        'con su cola de comandos y <code class="inline">.then()</code>, no mezcles paradigmas.</p>')}

    {callout("bad", "Reusar estado del navegador entre tests sin darte cuenta",
        '<p>Desde Cypress 12+, las cookies, localStorage y sessionStorage se limpian automáticamente '
        'entre tests por defecto. Si tu proyecto usa una versión vieja, o desactivaste ese '
        'comportamiento, un test puede "heredar" sesión de otro y dar falsos positivos.</p>')}

    {callout("bad", "Usar selectores XPath cuando no hace falta",
        '<p>Cypress no trae XPath por defecto (existe un plugin), y en la gran mayoría de los casos '
        'CSS alcanza y sobra. Reservá XPath sólo para casos realmente imposibles de resolver con CSS '
        '(muy poco frecuentes).</p>')}

    {callout("bad", "Tipar todo como any para que TypeScript deje de quejarse",
        '<p>Pierde el sentido de usar TypeScript. Si una fixture o una respuesta de API no tiene tipo '
        'claro, definí la interface correspondiente: te va a ahorrar bugs tontos (typos de propiedades) '
        'todo el tiempo.</p>')}

    {callout("bad", "No limpiar/resetear el estado del backend entre corridas",
        '<p>Si tus tests crean datos (usuarios, pedidos) y no los limpian, las corridas sucesivas '
        'empiezan a fallar por datos duplicados o inconsistentes. Usá tareas de seed/reset vía '
        '<code class="inline">cy.task()</code> o endpoints de test dedicados.</p>')}

    {callout("bad", "Ignorar los videos y screenshots que genera Cypress en CI",
        '<p>Cuando un test falla en CI, Cypress guarda automáticamente una captura de pantalla (y '
        'video, si está habilitado). Es la forma más rápida de entender qué pasó sin tener que '
        'reproducir el fallo localmente.</p>')}
    '''
    return page("Calidad", 14, "Errores comunes a evitar", body)


# =====================================================================
# SECCIÓN 15 — CI/CD
# =====================================================================
def section_15():
    body = f'''
    <p>Los tests E2E muestran su verdadero valor cuando corren automáticamente en cada cambio de
    código, no sólo en la máquina de un desarrollador.</p>

    <h2>Correr Cypress en modo headless</h2>
    {code_block("""npx cypress run                     # corre todos los specs, sin interfaz
npx cypress run --browser chrome    # especifica el navegador
npx cypress run --spec "cypress/e2e/login.cy.ts"   # un solo archivo
npx cypress run --headed            # headless=false, ver el navegador igual""", "bash")}

    <h2>Configurar videos y screenshots</h2>
    {code_block("""// cypress.config.ts
export default defineConfig({
  video: true,              // graba video de cada spec
  screenshotOnRunFailure: true, // captura automatica si un test falla
  e2e: {
    baseUrl: "http://localhost:3000",
  },
});""", "ts", "cypress.config.ts")}

    <h2>Ejemplo de pipeline con GitHub Actions</h2>
    {code_block("""name: e2e-tests

on: [push, pull_request]

jobs:
  cypress-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Instalar dependencias
        run: npm ci

      - name: Levantar la app
        run: npm run start &

      - name: Correr tests de Cypress
        run: npx cypress run

      - name: Subir capturas si falla
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: cypress-screenshots
          path: cypress/screenshots""", "ts", ".github/workflows/e2e.yml")}

    <h2>Código de salida (exit code)</h2>
    <p>Cuando corrés <code class="inline">cypress run</code>, el proceso termina con código
    <code class="inline">0</code> si todos los tests pasaron, o un número mayor a 0 si alguno
    falló. Esto es lo que usa cualquier sistema de CI para marcar el build como exitoso o fallido.</p>

    {table(
        ["Variable / flag", "Para qué sirve"],
        [
            ["<code class='inline'>CYPRESS_BASE_URL</code>", "Sobrescribe baseUrl sin tocar el archivo de config (útil por entorno: staging, prod)"],
            ["<code class='inline'>--env</code>", "Pasa variables custom: <code class='inline'>cypress run --env usuario=qa</code>"],
            ["<code class='inline'>--record</code>", "Sube resultados a un dashboard externo para historial y paralelización"],
            ["<code class='inline'>--parallel</code>", "Corre los specs repartidos entre varias máquinas/jobs"],
        ]
    )}

    {callout("info", "Paralelización y dashboards",
        '<p>Para suites grandes, existen servicios (como Cypress Cloud u otras alternativas) que '
        'permiten correr los specs en paralelo entre varios workers y ver el historial de '
        'ejecuciones. No es necesario para empezar: priorizá primero tener una suite estable y '
        'rápida corriendo en CI de forma secuencial.</p>')}
    '''
    return page("Integración continua", 15, "Ejecutar en CI/CD", body)


# =====================================================================
# SECCIÓN 16 — CHEAT SHEET FINAL
# =====================================================================
def section_16():
    body = f'''
    <p>Una referencia compacta para tener a mano mientras escribís tests.</p>

    <h2>Comandos más usados</h2>
    {table(
        ["Acción", "Comando"],
        [
            ["Visitar una URL", "<code class='inline'>cy.visit(\"/ruta\")</code>"],
            ["Seleccionar por data-cy", "<code class='inline'>cy.get('[data-cy=\"x\"]')</code>"],
            ["Buscar por texto", "<code class='inline'>cy.contains(\"texto\")</code>"],
            ["Click", "<code class='inline'>.click()</code>"],
            ["Escribir texto", "<code class='inline'>.type(\"texto\")</code>"],
            ["Verificar visibilidad", "<code class='inline'>.should(\"be.visible\")</code>"],
            ["Verificar texto", "<code class='inline'>.should(\"contain.text\", \"x\")</code>"],
            ["Cargar fixture", "<code class='inline'>cy.fixture(\"archivo.json\")</code>"],
            ["Interceptar request", "<code class='inline'>cy.intercept(\"GET\", \"/api/x\", {...})</code>"],
            ["Esperar a un alias", "<code class='inline'>cy.wait(\"@alias\")</code>"],
            ["Custom command", "<code class='inline'>Cypress.Commands.add(\"nombre\", fn)</code>"],
            ["Correr headless", "<code class='inline'>npx cypress run</code>"],
        ],
        widths=["38%", "62%"]
    )}

    <h2>Selectores CSS más usados</h2>
    {table(
        ["Selector", "Ejemplo"],
        [
            ["Clase", "<code class='inline'>.clase</code>"],
            ["ID", "<code class='inline'>#id</code>"],
            ["Atributo exacto", "<code class='inline'>[data-cy=\"x\"]</code>"],
            ["Atributo \"empieza con\"", "<code class='inline'>[data-cy^=\"item-\"]</code>"],
            ["Descendiente", "<code class='inline'>.padre .hijo</code>"],
            ["Hijo directo", "<code class='inline'>.padre &gt; .hijo</code>"],
            ["nth-child", "<code class='inline'>li:nth-child(2)</code>"],
            ["Negación", "<code class='inline'>:not(.clase)</code>"],
        ],
        widths=["38%", "62%"]
    )}

    <h2>Checklist final de buenas prácticas</h2>
    <ul class="checklist">
      <li>Atributos <code class="inline">data-cy</code> en todos los elementos clave</li>
      <li>Tests independientes, sin orden ni estado compartido</li>
      <li>Cero <code class="inline">cy.wait(numeroFijo)</code></li>
      <li>Fixtures tipadas con interfaces de TypeScript</li>
      <li>Custom commands para flujos repetidos (login, etc.)</li>
      <li>cy.intercept() para casos difíciles de reproducir (errores, vacíos)</li>
      <li>CI corriendo la suite en cada push, con screenshots/videos en fallos</li>
    </ul>

    <h2>Recursos para seguir profundizando</h2>
    <div class="badge-row">
      <span class="tag">docs.cypress.io</span>
      <span class="tag">typescriptlang.org/docs</span>
      <span class="tag">developer.mozilla.org (MDN) — CSS Selectors</span>
      <span class="tag">github.com/cypress-io/cypress-example-recipes</span>
    </div>

    <div class="end-box">
      <h3>¡Listo! Ya tenés la base completa</h3>
      <p>Desde la instalación hasta buenas prácticas de equipo. El siguiente paso es práctica: tomá
      una pantalla real de tu aplicación, agregale atributos <code class="inline">data-cy</code> y
      escribí tu primer test de punta a punta.</p>
    </div>
    '''
    return page("Referencia", 16, "Cheat sheet final y recursos", body)
