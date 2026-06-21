# -*- coding: utf-8 -*-
"""Contenido del documento — Parte 1: secciones 1 a 4."""
from helpers import code_block, callout, table, figure
import diagrams as dg


def page(eyebrow, num, title, body):
    return f'''<div class="page">
      <div class="section-eyebrow">{eyebrow}</div>
      <h1 class="section-title">{num}. {title}</h1>
      {body}
    </div>'''


# =====================================================================
# SECCIÓN 1 — ¿QUÉ ES CYPRESS?
# =====================================================================
def section_01():
    body = f'''
    <p>Cypress es un <strong>framework de testing end-to-end (E2E)</strong> para aplicaciones web,
    pensado desde cero para JavaScript/TypeScript. A diferencia de herramientas como Selenium,
    Cypress no controla el navegador "desde afuera" mediante un protocolo remoto: se ejecuta
    <strong>dentro del mismo navegador</strong>, en el mismo ciclo de eventos que tu aplicación.
    Esto le da acceso directo al DOM, a la red, al <code class="inline">window</code> y al
    almacenamiento, lo que se traduce en tests más rápidos, más estables y mucho más fáciles
    de depurar.</p>

    {figure(dg.ARCH_DIAGRAM, "Cypress corre en el mismo proceso del navegador que tu aplicacion, no la controla por fuera.")}

    <h2>¿Por qué se volvió tan popular?</h2>
    <div class="kpi-row">
      <div class="kpi"><span class="kpi-num">⏱</span><span class="kpi-label">Auto-espera (auto-wait) sin sleeps manuales</span></div>
      <div class="kpi"><span class="kpi-num">↺</span><span class="kpi-label">Time-travel: ves cada paso del test</span></div>
      <div class="kpi"><span class="kpi-num">TS</span><span class="kpi-label">Soporte nativo de TypeScript</span></div>
      <div class="kpi"><span class="kpi-num">🌐</span><span class="kpi-label">Mock de red real con cy.intercept</span></div>
    </div>

    <ul>
      <li><strong>Auto-waiting / retry-ability:</strong> antes de fallar, Cypress reintenta automáticamente
      comandos y aserciones durante un tiempo configurable (por defecto 4s), así que no necesitás
      <code class="inline">sleep()</code> ni <code class="inline">wait(2000)</code> a mano.</li>
      <li><strong>Time travel:</strong> el Test Runner guarda una "foto" del DOM en cada comando,
      podés pasar el mouse por cada paso y ver exactamente qué pasó.</li>
      <li><strong>Debugging real:</strong> como corre en el navegador, podés abrir las DevTools de
      Chrome igual que con cualquier página y poner <code class="inline">debugger</code>.</li>
      <li><strong>Control de red:</strong> con <code class="inline">cy.intercept()</code> podés espiar,
      modificar o mockear cualquier request sin tocar el backend.</li>
      <li><strong>Todo en un solo paquete:</strong> test runner, librería de aserciones (Chai),
      mocking y documentación, sin tener que combinar mil librerías distintas.</li>
    </ul>

    <h2>Cypress vs. otras herramientas</h2>
    {table(
        ["Característica", "Cypress", "Selenium", "Playwright"],
        [
            ["Arquitectura", "Corre <em>dentro</em> del navegador", "Controla el navegador por fuera (WebDriver)", "Controla el navegador por fuera (protocolo propio)"],
            ["Lenguajes", "JavaScript / TypeScript", "Multi-lenguaje (Java, Python, C#, JS...)", "JS/TS, Python, Java, .NET"],
            ["Auto-espera", "Sí, integrada", "Manual / esperas explícitas", "Sí, integrada"],
            ["Multi-pestaña / dominio", "Limitado (mejoró con cy.origin)", "Sí", "Sí, nativo"],
            ["Curva de aprendizaje", "Baja-media", "Media-alta", "Media"],
            ["Ideal para", "Apps web SPA, equipos JS/TS", "Suites legacy multi-lenguaje", "E2E moderno multi-navegador"],
        ],
        widths=["18%", "27%", "27%", "28%"]
    )}

    {callout("info", "¿Cuándo NO conviene Cypress?",
        '<p>Si necesitás testear múltiples pestañas/ventanas a la vez, navegación entre dominios '
        'totalmente distintos de forma intensiva, o apps nativas/mobile, otras herramientas (como '
        'Playwright) pueden encajar mejor. Para testing E2E de una SPA o sitio web típico, Cypress '
        'es una de las mejores opciones del mercado.</p>')}

    <h2>Tipos de testing que cubre Cypress</h2>
    {table(
        ["Tipo", "Qué prueba", "Ejemplo"],
        [
            ["<strong>E2E Testing</strong>", "El flujo completo de la app, como lo usaría un usuario real", "Login → agregar producto → checkout"],
            ["<strong>Component Testing</strong>", "Un componente de UI aislado (React, Vue, Angular, Svelte)", "Montar un &lt;Button /&gt; y testear sus props"],
            ["<strong>API Testing</strong>", "Llamadas HTTP directas, sin UI", "cy.request('GET', '/api/users')"],
        ]
    )}
    '''
    return page("Fundamentos", 1, "¿Qué es Cypress?", body)


# =====================================================================
# SECCIÓN 2 — REPASO DE JS / TS
# =====================================================================
def section_02():
    body = f'''
    <p>Antes de meternos en Cypress, repasemos lo mínimo de JavaScript y TypeScript que vas a usar
    todo el tiempo al escribir tests. Si ya te sentís cómodo con esto, igual valen unos minutos
    de repaso porque son los bloques con los que se arma <em>cada</em> test.</p>

    <h2>Variables: <code class="inline">const</code> y <code class="inline">let</code></h2>
    <p>En TypeScript moderno casi no se usa <code class="inline">var</code>. Usá
    <code class="inline">const</code> por defecto (no se puede reasignar) y <code class="inline">let</code>
    sólo cuando sepas que el valor va a cambiar.</p>
    {code_block("""const usuario = "ana@mail.com";   // no se puede reasignar
let intentos = 0;                  // si se puede reasignar
intentos = intentos + 1;""", "ts")}

    <h2>Tipos básicos de TypeScript</h2>
    <p>TypeScript agrega <strong>tipos estáticos</strong> sobre JavaScript: el editor te avisa de
    errores antes de correr el código. Esto es oro en testing, porque evita typos en nombres de
    propiedades de objetos grandes (fixtures, respuestas de API, etc.).</p>
    {code_block("""let email: string = "ana@mail.com";
let edad: number = 28;
let activo: boolean = true;
let tags: string[] = ["admin", "qa"];
let coords: [number, number] = [10, 20]; // tupla

// "object shape" con interface
interface Usuario {
  id: number;
  nombre: string;
  email: string;
  esAdmin?: boolean; // el "?" significa opcional
}

const ana: Usuario = { id: 1, nombre: "Ana", email: "ana@mail.com" };""", "ts")}

    {callout("tip", "any vs. tipado real",
        '<p>Vas a sentir la tentación de tipar todo como <code class="inline">any</code> cuando '
        'TypeScript se queje. Resistila: <code class="inline">any</code> apaga el chequeo de tipos '
        'justo donde más lo necesitás. Preferí <code class="inline">unknown</code> si realmente no '
        'sabés el tipo, o definí la interface correspondiente.</p>')}

    <h2>Funciones flecha (arrow functions)</h2>
    <p>Cypress usa funciones flecha (<code class="inline">() =&gt; {{ }}</code>) en casi todos lados:
    en cada <code class="inline">it()</code>, <code class="inline">describe()</code>, callbacks de
    <code class="inline">.then()</code>, etc.</p>
    {code_block("""// funcion tradicional
function sumar(a: number, b: number): number {
  return a + b;
}

// arrow function equivalente
const sumar2 = (a: number, b: number): number => a + b;

// asi se ven en Cypress
describe("Carrito de compras", () => {
  it("agrega un producto", () => {
    // aca va el test
  });
});""", "ts")}

    <h2>Destructuring y template strings</h2>
    {code_block("""const usuario = { nombre: "Ana", email: "ana@mail.com" };
const { nombre, email } = usuario;          // destructuring

const saludo = `Hola, ${nombre}!`;          // template string
console.log(saludo); // "Hola, Ana!" """, "ts")}

    <h2>Promesas y <code class="inline">async/await</code></h2>
    <p>En JavaScript "normal", el código asincrónico (que tarda, como un fetch) se maneja con
    <code class="inline">Promise</code> y <code class="inline">async/await</code>:</p>
    {code_block("""async function traerUsuario() {
  const resp = await fetch("/api/usuario/1");
  const data = await resp.json();
  return data;
}""", "ts")}

    {callout("warning", "Cypress NO usa async/await",
        '<p>Esto es clave y confunde a mucha gente que recién empieza: dentro de un test de Cypress '
        '<strong>casi nunca</strong> vas a escribir <code class="inline">await</code>. Cypress arma '
        'internamente una <em>cola de comandos</em> y los encadena con <code class="inline">.then()</code>. '
        'Vas a ver esto en detalle en la sección 6 (Anatomía de un test), pero quedate con la idea: '
        '<em>se programa distinto a como esperarías con promesas tradicionales.</em></p>')}

    <h2>Resumen de lo que necesitás dominar</h2>
    {table(
        ["Concepto", "Para qué lo usás en Cypress"],
        [
            ["<code class='inline'>const</code> / <code class='inline'>let</code>", "Declarar variables dentro de los tests"],
            ["Arrow functions", "Callbacks de <code class='inline'>it()</code>, <code class='inline'>.then()</code>, hooks"],
            ["Interfaces / types", "Tipar fixtures, respuestas de API, Page Objects"],
            ["Template strings", "Armar selectores o mensajes dinámicos"],
            ["Destructuring", "Extraer datos de objetos de fixtures o respuestas"],
            ["Arrays y métodos (<code class='inline'>map</code>, <code class='inline'>filter</code>)", "Recorrer listas de datos de prueba"],
        ]
    )}
    '''
    return page("Fundamentos", 2, "Repaso rápido de JavaScript y TypeScript", body)


# =====================================================================
# SECCIÓN 3 — INSTALACIÓN DEL ENTORNO COMPLETO
# =====================================================================
def section_03():
    pkg_scripts = code_block("""{
  "scripts": {
    "cy:open": "cypress open",
    "cy:run": "cypress run"
  }
}""", "json", "package.json")

    body = f'''
    <p>Vamos a instalar todo desde cero: Node.js, un proyecto nuevo, Cypress, y la configuración
    de TypeScript. Seguí los pasos en orden.</p>

    <ol class="steps">
      <li>
        <div class="step-title">Instalar Node.js</div>
        <p>Cypress necesita Node.js (incluye npm). Descargalo desde
        <code class="inline">nodejs.org</code> (versión LTS) o instalalo con un gestor de versiones
        como <code class="inline">nvm</code>. Verificá la instalación:</p>
        {code_block("""node --version   # ej: v20.11.0
npm --version    # ej: 10.2.4""", "bash")}
      </li>

      <li>
        <div class="step-title">Crear la carpeta del proyecto</div>
        {code_block("""mkdir mi-proyecto-cypress
cd mi-proyecto-cypress
npm init -y""", "bash")}
        <p><code class="inline">npm init -y</code> crea un <code class="inline">package.json</code>
        con valores por defecto, donde se van a guardar las dependencias del proyecto.</p>
      </li>

      <li>
        <div class="step-title">Instalar Cypress y TypeScript</div>
        {code_block("""npm install --save-dev cypress typescript""", "bash")}
        <p>Cypress trae soporte de TypeScript integrado: no hace falta ningún transpilador
        adicional, sólo un <code class="inline">tsconfig.json</code> bien configurado (paso 6).</p>
      </li>

      <li>
        <div class="step-title">Abrir Cypress por primera vez</div>
        {code_block("""npx cypress open""", "bash")}
        <p>Esto abre el Test Runner gráfico. Te va a preguntar qué tipo de testing querés
        configurar:</p>
        <ul>
          <li><strong>E2E Testing</strong> — para probar la app completa como un usuario real (es el foco de esta guía).</li>
          <li><strong>Component Testing</strong> — para montar y probar componentes de UI de forma aislada.</li>
        </ul>
        <p>Elegí <strong>E2E Testing</strong> y seguí el asistente: Cypress detecta el navegador
        instalado y crea automáticamente la estructura de carpetas.</p>
      </li>

      <li>
        <div class="step-title">Estructura de carpetas generada</div>
        <p>Después del asistente, vas a tener algo así (vamos a sumar la carpeta
        <code class="inline">pages/</code> más adelante para el Page Object Model):</p>
        {figure(dg.FOLDER_TREE, "Estructura tipica de un proyecto Cypress + TypeScript")}
      </li>

      <li>
        <div class="step-title">Configurar TypeScript dentro de Cypress</div>
        <p>Cypress genera <code class="inline">cypress.config.ts</code> automáticamente. Necesitás
        además un <code class="inline">tsconfig.json</code> <strong>dentro de la carpeta
        <code class="inline">cypress/</code></strong> (separado del tsconfig de tu app, si lo tenés):</p>
        {code_block("""{
  "compilerOptions": {
    "target": "es5",
    "lib": ["es5", "dom"],
    "types": ["cypress", "node"],
    "module": "commonjs",
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true
  },
  "include": ["**/*.ts"]
}""", "json", "cypress/tsconfig.json")}
        {callout("tip", "¿Por qué un tsconfig separado?",
            '<p>Si tu proyecto principal (la app) ya tiene su propio <code class="inline">tsconfig.json</code>, '
            'lo mejor es que Cypress tenga el suyo dentro de <code class="inline">cypress/</code>. Así evitás '
            'que la configuración de build de tu app interfiera con la de los tests (y viceversa).</p>')}
      </li>

      <li>
        <div class="step-title"><code class="inline">cypress.config.ts</code></div>
        <p>Acá vive la configuración general: URL base, patrones de archivos de test, timeouts,
        variables de entorno, etc.</p>
        {code_block("""import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:3000",
    specPattern: "cypress/e2e/**/*.cy.ts",
    supportFile: "cypress/support/e2e.ts",
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 6000,
    setupNodeEvents(on, config) {
      // aca se registran plugins / tareas de Node
      return config;
    },
  },
});""", "ts", "cypress.config.ts")}
      </li>

      <li>
        <div class="step-title">Extensión recomendada para el editor</div>
        <p>Si usás VS Code, instalá la extensión oficial <strong>Cypress</strong> (de Cypress.io) para
        autocompletado de comandos, y asegurate de tener la extensión de <strong>ESLint</strong> activa.
        No es obligatorio, pero ahorra muchísimo tiempo.</p>
      </li>
    </ol>

    {callout("best", "Scripts útiles en package.json",
        '<p>Agregá estos atajos para no escribir <code class="inline">npx cypress ...</code> siempre:</p>'
        + pkg_scripts)}
    '''
    return page("Puesta en marcha", 3, "Instalación del entorno completo", body)


# =====================================================================
# SECCIÓN 4 — PRIMER PROYECTO
# =====================================================================
def section_04():
    body = f'''
    <p>Con todo instalado, vamos a escribir y correr tu primer test. La convención de Cypress es
    que los archivos de test terminen en <code class="inline">.cy.ts</code> y vivan dentro de
    <code class="inline">cypress/e2e/</code>.</p>

    <h2>Tu primer archivo de test</h2>
    {code_block("""// cypress/e2e/home.cy.ts

describe("Pagina de inicio", () => {
  it("muestra el titulo principal", () => {
    cy.visit("/");
    cy.get("h1").should("be.visible");
    cy.get("h1").should("contain.text", "Bienvenido");
  });
});""", "ts", "cypress/e2e/home.cy.ts")}

    <h2>Dos formas de correr los tests</h2>
    {table(
        ["Comando", "Modo", "Cuándo usarlo"],
        [
            ["<code class='inline'>npx cypress open</code>", "Interactivo, con interfaz gráfica", "Mientras escribís y debuggeás tests"],
            ["<code class='inline'>npx cypress run</code>", "Headless, por consola", "En CI/CD o para correr todo rápido"],
        ]
    )}

    <h2>Qué vas a ver en el Test Runner</h2>
    <ul>
      <li>A la izquierda, la lista de comandos ejecutados (<code class="inline">visit</code>,
      <code class="inline">get</code>, <code class="inline">should</code>...), en orden.</li>
      <li>A la derecha, tu aplicación corriendo de verdad, dentro de un iframe.</li>
      <li>Si pasás el mouse sobre cualquier comando de la izquierda, el panel de la derecha
      "viaja en el tiempo" y te muestra cómo estaba el DOM en ese momento exacto
      (esto es el famoso <strong>time-travel</strong>).</li>
      <li>Si un comando falla, Cypress reintenta automáticamente hasta el timeout configurado
      antes de marcar el test como fallido, y te muestra el error con una captura de pantalla.</li>
    </ul>

    {callout("note", "baseUrl: tu mejor amigo",
        '<p>Notá que en el ejemplo usamos <code class="inline">cy.visit(\'/\')</code> en vez de la URL '
        'completa. Eso es porque definimos <code class="inline">baseUrl</code> en '
        '<code class="inline">cypress.config.ts</code>. Siempre que tu app corra en una URL fija '
        '(local o de staging), configurá <code class="inline">baseUrl</code>: así los tests son '
        'portables entre entornos sin tocar el código.</p>')}

    <h2>Checklist antes de seguir</h2>
    <ul class="checklist">
      <li>Node.js y npm instalados y verificados</li>
      <li>Cypress y TypeScript instalados como devDependencies</li>
      <li><code class="inline">cypress.config.ts</code> con <code class="inline">baseUrl</code> apuntando a tu app</li>
      <li><code class="inline">cypress/tsconfig.json</code> creado</li>
      <li>Un primer test corriendo en modo interactivo (<code class="inline">cypress open</code>)</li>
    </ul>
    '''
    return page("Puesta en marcha", 4, "Primer proyecto Cypress + TypeScript", body)
