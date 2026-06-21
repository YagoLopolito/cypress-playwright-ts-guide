# -*- coding: utf-8 -*-
"""Contenido del documento — Parte 2: secciones 5 a 8."""
from helpers import code_block, callout, table, figure, practice_reveal
from content_part1 import page
import diagrams as dg


# =====================================================================
# SECCIÓN 5 — TUTORIAL DE SELECTORES CSS
# =====================================================================
def section_05():
    body = f'''
    <p>Cypress encuentra elementos en la página usando <strong>selectores CSS</strong>
    (los mismos que usás para aplicar estilos). Si dominás CSS, ya sabés encontrar
    cualquier elemento con <code class="inline">cy.get()</code>. Repasemos los selectores
    de la forma en que más se usan en testing.</p>

    {callout("info", "El selector va siempre dentro de cy.get()",
        '<p>Todo lo que veas en esta sección se usa así: <code class="inline">cy.get("SELECTOR")</code>. '
        'Por ejemplo, <code class="inline">cy.get(".btn-primary")</code> selecciona todos los elementos '
        'con clase <code class="inline">btn-primary</code>, igual que en una hoja de estilos.</p>')}

    <h2>1. Selectores básicos</h2>
    {table(
        ["Selector", "Qué selecciona", "Ejemplo CSS", "Ejemplo en Cypress"],
        [
            ["Tipo / etiqueta", "Todos los elementos de esa etiqueta", "<code class='inline'>button</code>", "<code class='inline'>cy.get('button')</code>"],
            ["Clase", "Elementos con esa clase", "<code class='inline'>.btn-primary</code>", "<code class='inline'>cy.get('.btn-primary')</code>"],
            ["ID", "El único elemento con ese id", "<code class='inline'>#email</code>", "<code class='inline'>cy.get('#email')</code>"],
            ["Universal", "Todos los elementos", "<code class='inline'>*</code>", "<code class='inline'>cy.get('*')</code> (rara vez se usa)"],
            ["Agrupado", "Varios selectores a la vez", "<code class='inline'>h1, h2, h3</code>", "<code class='inline'>cy.get('h1, h2, h3')</code>"],
        ]
    )}

    <h2>2. Selectores de atributo</h2>
    <p>Son los <strong>más importantes para testing</strong>: permiten seleccionar por cualquier
    atributo HTML, incluyendo atributos personalizados como <code class="inline">data-cy</code>
    (vas a ver por qué esto es clave en la sección de buenas prácticas).</p>
    {table(
        ["Selector", "Significa", "Ejemplo"],
        [
            ["<code class='inline'>[attr]</code>", "Tiene el atributo (cualquier valor)", "<code class='inline'>[disabled]</code>"],
            ["<code class='inline'>[attr=\"valor\"]</code>", "El atributo es exactamente ese valor", "<code class='inline'>[type=\"submit\"]</code>"],
            ["<code class='inline'>[attr^=\"valor\"]</code>", "Empieza con ese valor", "<code class='inline'>[data-cy^=\"item-\"]</code>"],
            ["<code class='inline'>[attr$=\"valor\"]</code>", "Termina con ese valor", "<code class='inline'>[src$=\".png\"]</code>"],
            ["<code class='inline'>[attr*=\"valor\"]</code>", "Contiene ese valor en cualquier parte", "<code class='inline'>[class*=\"error\"]</code>"],
        ]
    )}
    {code_block("""// El selector estrella en testing con Cypress:
cy.get('[data-cy="submit-button"]').click();
cy.get('[data-cy=email-input]').type("ana@mail.com");""", "ts")}

    <h2>3. Combinadores: relaciones entre elementos</h2>
    {figure(dg.COMBINATORS_DIAGRAM, "Los 4 combinadores CSS mas usados: descendiente, hijo directo, hermano adyacente y hermano general.")}
    {table(
        ["Combinador", "Sintaxis", "Significa"],
        [
            ["Descendiente", "<code class='inline'>A B</code>", "B en cualquier nivel dentro de A"],
            ["Hijo directo", "<code class='inline'>A &gt; B</code>", "B hijo inmediato de A (no nietos)"],
            ["Hermano adyacente", "<code class='inline'>A + B</code>", "B justo después de A, mismo padre"],
            ["Hermano general", "<code class='inline'>A ~ B</code>", "Cualquier B después de A, mismo padre"],
        ]
    )}
    {code_block("""cy.get(".form .input");        // cualquier .input dentro de .form
cy.get(".list > li");          // solo los <li> hijos directos de .list
cy.get("label + input");       // el input justo despues de un label
cy.get("h2 ~ p");              // todos los <p> que vienen despues de un h2""", "css")}

    <h2>4. Pseudo-clases más útiles</h2>
    {table(
        ["Pseudo-clase", "Selecciona"],
        [
            ["<code class='inline'>:first-child</code>", "El primer hijo de su contenedor"],
            ["<code class='inline'>:last-child</code>", "El último hijo de su contenedor"],
            ["<code class='inline'>:nth-child(n)</code>", "El hijo en la posición <em>n</em> (1-based)"],
            ["<code class='inline'>:not(selector)</code>", "Todo lo que NO matchea el selector"],
            ["<code class='inline'>:checked</code>", "Checkboxes / radios marcados"],
            ["<code class='inline'>:disabled</code>", "Elementos deshabilitados"],
            ["<code class='inline'>:visible</code> *", "Extensión propia de Cypress (no es CSS estándar)"],
        ]
    )}
    {code_block("""cy.get("li:nth-child(2)");          // el segundo <li>
cy.get("input:not([disabled])");    // inputs habilitados
cy.get(".checkbox:checked");        // checkboxes tildados""", "css")}

    <h2>5. Especificidad: quién gana cuando hay conflicto</h2>
    <p>La especificidad determina qué regla CSS "gana" si varias aplican al mismo elemento. Se
    calcula como una tupla <code class="inline">(inline, IDs, clases/atributos/pseudo-clases, elementos)</code>.
    Para testing rara vez vas a tener "conflictos" como en CSS de diseño, pero entender esto te
    ayuda a elegir el selector más <strong>específico y estable</strong> posible.</p>
    {figure(dg.SPECIFICITY_DIAGRAM, "A mayor especificidad, mas preciso (y mas fragil ante cambios de estructura) es el selector.")}

    {callout("best", "Selectores estables vs. selectores frágiles",
        '<p>Un selector como <code class="inline">div &gt; div:nth-child(3) &gt; span</code> es muy '
        'específico, pero se rompe apenas alguien cambia el HTML. Un atributo dedicado como '
        '<code class="inline">[data-cy="precio-total"]</code> es mucho más resistente a cambios '
        'de diseño o de estructura. Volvemos sobre esto en la sección 13.</p>')}

    <h2>Practicá: ¿qué selecciona cada línea?</h2>
    <p>Pensá la respuesta y tocá cada selector para revelarla.</p>
    {practice_reveal([
        ("<code class='inline'>nav ul li a</code>", "Cualquier &lt;a&gt; dentro de un &lt;li&gt;, dentro de un &lt;ul&gt;, dentro de &lt;nav&gt; (en cualquier nivel)"),
        ("<code class='inline'>.card:first-child</code>", "El primer elemento con clase <code class='inline'>.card</code>, si además es el primer hijo de su padre"),
        ("<code class='inline'>[data-cy=\"row\"] &gt; td:nth-child(2)</code>", "La segunda celda &lt;td&gt; hija directa de cada fila con <code class='inline'>data-cy=\"row\"</code>"),
        ("<code class='inline'>button:not(.disabled)</code>", "Todos los botones que no tengan la clase <code class='inline'>disabled</code>"),
    ])}
    '''
    return page("La base: CSS", 5, "Selectores CSS: la base para encontrar elementos", body)


# =====================================================================
# SECCIÓN 6 — ANATOMÍA DE UN TEST
# =====================================================================
def section_06():
    body = f'''
    <p>Todo test de Cypress se arma con bloques de <strong>Mocha</strong> (el framework de test
    sobre el que corre Cypress) más <strong>Chai</strong> (la librería de aserciones). Vamos a
    desarmar un test completo, pieza por pieza.</p>

    <h2>Los bloques estructurales</h2>
    {table(
        ["Bloque", "Para qué sirve"],
        [
            ["<code class='inline'>describe()</code>", "Agrupa tests relacionados (una \"suite\")"],
            ["<code class='inline'>context()</code>", "Alias de <code class='inline'>describe()</code>, útil para sub-agrupar"],
            ["<code class='inline'>it()</code>", "Un caso de prueba individual"],
            ["<code class='inline'>before()</code>", "Corre 1 sola vez, antes de todos los tests del bloque"],
            ["<code class='inline'>beforeEach()</code>", "Corre antes de CADA test del bloque"],
            ["<code class='inline'>after()</code>", "Corre 1 sola vez, al final de todos los tests"],
            ["<code class='inline'>afterEach()</code>", "Corre después de CADA test"],
        ]
    )}
    {figure(dg.LIFECYCLE_DIAGRAM, "Orden de ejecucion de los hooks alrededor de cada it().")}

    <h2>Test completo y comentado</h2>
    {code_block("""describe("Login", () => {
  beforeEach(() => {
    // se ejecuta antes de cada test: dejamos la app en un estado conocido
    cy.visit("/login");
  });

  it("permite iniciar sesion con credenciales validas", () => {
    cy.get('[data-cy="email"]').type("ana@mail.com");
    cy.get('[data-cy="password"]').type("Secreta123!");
    cy.get('[data-cy="submit"]').click();

    cy.url().should("include", "/dashboard");
    cy.get('[data-cy="bienvenida"]').should("contain.text", "Hola, Ana");
  });

  it("muestra un error con credenciales invalidas", () => {
    cy.get('[data-cy="email"]').type("ana@mail.com");
    cy.get('[data-cy="password"]').type("incorrecta");
    cy.get('[data-cy="submit"]').click();

    cy.get('[data-cy="mensaje-error"]')
      .should("be.visible")
      .and("contain.text", "Credenciales invalidas");
  });
});""", "ts", "cypress/e2e/login.cy.ts")}

    <h2>El "encadenamiento" (chaining): la idea más importante de Cypress</h2>
    <p>Cuando escribís <code class="inline">cy.get(...).click()</code>, NO estás llamando a dos
    funciones que se ejecutan inmediatamente una tras otra como en JS normal. Cypress encola
    comandos y los va resolviendo en orden, esperando automáticamente a que cada uno esté listo.</p>
    {code_block("""// Esto NO ejecuta get() y luego click() al instante.
// Cypress arma una "cola": primero resuelve get(), reintentando
// hasta encontrar el elemento, y RECIEN AHI ejecuta click().
cy.get('[data-cy="boton"]').click();

// Por eso esto NO funciona como esperarias en JS normal:
const boton = cy.get('[data-cy="boton"]'); // esto NO es el elemento todavia
// boton.click()  -> error conceptual, cy.get() devuelve una "Chainable", no el DOM""", "ts")}

    {callout("warning", "No guardes resultados de cy.get() en variables comunes",
        '<p>Como en el ejemplo de arriba: <code class="inline">cy.get()</code> no devuelve el '
        'elemento del DOM directamente, devuelve un objeto especial (<code class="inline">Chainable</code>) '
        'que Cypress resuelve más tarde. Si necesitás "guardar" algo para usarlo después, la forma '
        'correcta es con <code class="inline">.then()</code> o con alias (<code class="inline">.as()</code>), '
        'que vas a ver en la sección 7.</p>')}

    <h2>Usando <code class="inline">.then()</code> para trabajar con el valor real</h2>
    {code_block("""cy.get('[data-cy="precio"]').then(($el) => {
  const texto = $el.text();              // aca SI tenes el elemento real (jQuery)
  const precio = parseFloat(texto.replace("$", ""));
  expect(precio).to.be.greaterThan(0);
});""", "ts")}
    '''
    return page("El núcleo de Cypress", 6, "Anatomía de un test en Cypress", body)


# =====================================================================
# SECCIÓN 7 — COMANDOS ESENCIALES (REFERENCIA)
# =====================================================================
def section_07():
    body = f'''
    <p>Esta es la caja de herramientas que vas a usar en el 90% de tus tests. No hace falta
    memorizarla: volvé a esta tabla cada vez que la necesites.</p>

    <h2>Navegación y selección</h2>
    {table(
        ["Comando", "Qué hace", "Ejemplo"],
        [
            ["<code class='inline'>cy.visit(url)</code>", "Navega a una URL", "<code class='inline'>cy.visit(\"/login\")</code>"],
            ["<code class='inline'>cy.get(selector)</code>", "Busca elementos por selector CSS", "<code class='inline'>cy.get(\".btn\")</code>"],
            ["<code class='inline'>cy.contains(texto)</code>", "Busca un elemento que contenga ese texto", "<code class='inline'>cy.contains(\"Comprar\")</code>"],
            ["<code class='inline'>cy.find(selector)</code>", "Busca dentro del resultado anterior", "<code class='inline'>cy.get(\".card\").find(\"button\")</code>"],
            ["<code class='inline'>cy.within(fn)</code>", "Limita los comandos siguientes a un contenedor", "<code class='inline'>cy.get(\".form\").within(() =&gt; {...})</code>"],
            ["<code class='inline'>cy.parent()</code> / <code class='inline'>cy.children()</code>", "Navega el árbol del DOM relativo al resultado actual", "<code class='inline'>cy.get(\"li\").parent()</code>"],
        ]
    )}

    <h2>Interacciones del usuario</h2>
    {table(
        ["Comando", "Qué hace", "Ejemplo"],
        [
            ["<code class='inline'>.click()</code>", "Hace clic", "<code class='inline'>cy.get(\"button\").click()</code>"],
            ["<code class='inline'>.dblclick()</code>", "Doble clic", "<code class='inline'>cy.get(\".item\").dblclick()</code>"],
            ["<code class='inline'>.type(texto)</code>", "Escribe en un input", "<code class='inline'>cy.get(\"#email\").type(\"a@a.com\")</code>"],
            ["<code class='inline'>.clear()</code>", "Vacía un input", "<code class='inline'>cy.get(\"#email\").clear()</code>"],
            ["<code class='inline'>.check()</code> / <code class='inline'>.uncheck()</code>", "Marca/desmarca checkbox o radio", "<code class='inline'>cy.get(\"#acepto\").check()</code>"],
            ["<code class='inline'>.select(valor)</code>", "Elige una opción de un &lt;select&gt;", "<code class='inline'>cy.get(\"#pais\").select(\"Argentina\")</code>"],
            ["<code class='inline'>.trigger(evento)</code>", "Dispara un evento del DOM manualmente", "<code class='inline'>cy.get(\".slider\").trigger(\"mousedown\")</code>"],
            ["<code class='inline'>.scrollIntoView()</code>", "Scrollea hasta que el elemento sea visible", "<code class='inline'>cy.get(\"#footer\").scrollIntoView()</code>"],
        ]
    )}

    <h2>Lectura de valores y utilidades</h2>
    {table(
        ["Comando", "Qué hace", "Ejemplo"],
        [
            ["<code class='inline'>.its(propiedad)</code>", "Lee una propiedad del sujeto actual", "<code class='inline'>cy.window().its(\"innerWidth\")</code>"],
            ["<code class='inline'>.invoke(metodo)</code>", "Invoca un método jQuery/JS sobre el sujeto", "<code class='inline'>cy.get(\"input\").invoke(\"val\")</code>"],
            ["<code class='inline'>.as(nombre)</code>", "Crea un alias reutilizable", "<code class='inline'>cy.get(\".total\").as(\"total\")</code>"],
            ["<code class='inline'>cy.url()</code>", "Devuelve la URL actual", "<code class='inline'>cy.url().should(\"include\", \"/ok\")</code>"],
            ["<code class='inline'>cy.location()</code>", "Devuelve detalles de la URL (path, query, etc.)", "<code class='inline'>cy.location(\"pathname\")</code>"],
            ["<code class='inline'>cy.reload()</code>", "Recarga la página", "<code class='inline'>cy.reload()</code>"],
            ["<code class='inline'>cy.viewport(w, h)</code>", "Cambia el tamaño de pantalla simulado", "<code class='inline'>cy.viewport(375, 667)</code>"],
            ["<code class='inline'>cy.request()</code>", "Hace una llamada HTTP real (sin pasar por la UI)", "<code class='inline'>cy.request(\"GET\", \"/api/ping\")</code>"],
            ["<code class='inline'>cy.wait(alias)</code>", "Espera a un request interceptado (no a tiempo fijo)", "<code class='inline'>cy.wait(\"@getUsuarios\")</code>"],
        ]
    )}

    {callout("tip", "Usá alias para reutilizar selecciones",
        '<p>Si vas a usar el mismo elemento varias veces en un test, asignale un alias en vez de '
        'repetir el selector:</p>'
        + code_block("""cy.get('[data-cy="total"]').as("total");
cy.get("@total").should("contain.text", "$0");
cy.get('[data-cy="agregar"]').click();
cy.get("@total").should("contain.text", "$10");""", "ts"))}

    <h2>Ejemplo combinando varios comandos</h2>
    {code_block("""cy.get('[data-cy="lista-productos"]').within(() => {
  cy.contains("Zapatillas").parent().find("button").click();
});

cy.get('[data-cy="carrito"]')
  .should("be.visible")
  .find("li")
  .should("have.length", 1);""", "ts")}
    '''
    return page("Referencia", 7, "Comandos esenciales de Cypress", body)


# =====================================================================
# SECCIÓN 8 — ASERCIONES
# =====================================================================
def section_08():
    body = f'''
    <p>Las aserciones son las que realmente "verifican" algo: sin ellas, un test sólo navega y
    hace clics sin comprobar nada. Cypress usa <strong>Chai</strong> (más plugins como
    chai-jquery) por debajo, expuesto principalmente a través de <code class="inline">.should()</code>.</p>

    <h2>Dos estilos de aserción</h2>
    {table(
        ["Estilo", "Sintaxis", "Cuándo usarlo"],
        [
            ["Implícito (BDD)", "<code class='inline'>cy.get(...).should(...)</code>", "El 95% de los casos: aprovecha el retry automático de Cypress"],
            ["Explícito", "<code class='inline'>expect(valor).to.equal(...)</code>", "Dentro de un <code class='inline'>.then()</code>, cuando ya tenés el valor en la mano"],
        ]
    )}
    {code_block("""// Implicito: Cypress reintenta esta asercion hasta que sea verdadera (o haga timeout)
cy.get('[data-cy="titulo"]').should("be.visible");

// Explicito: una sola comprobacion puntual, sin reintentos automaticos
cy.get('[data-cy="precio"]').then(($el) => {
  const valor = parseFloat($el.text());
  expect(valor).to.be.greaterThan(0);
});""", "ts")}

    {callout("info", "¿Por qué importa la retry-ability?",
        '<p>Si usás <code class="inline">.should("be.visible")</code>, Cypress va a re-evaluar esa '
        'condición automáticamente durante varios segundos, en vez de fallar al instante. Esto '
        'elimina la mayoría de los "tests flaky" (inestables) causados por animaciones, llamadas '
        'a APIs que tardan, o renders asíncronos.</p>')}

    <h2>Aserciones más usadas con <code class="inline">.should()</code></h2>
    {table(
        ["Aserción", "Verifica"],
        [
            ["<code class='inline'>.should(\"exist\")</code>", "El elemento existe en el DOM"],
            ["<code class='inline'>.should(\"not.exist\")</code>", "El elemento NO existe en el DOM"],
            ["<code class='inline'>.should(\"be.visible\")</code>", "El elemento es visible (no display:none, etc.)"],
            ["<code class='inline'>.should(\"be.hidden\")</code>", "El elemento existe pero no es visible"],
            ["<code class='inline'>.should(\"have.text\", \"x\")</code>", "El texto es exactamente \"x\""],
            ["<code class='inline'>.should(\"contain.text\", \"x\")</code>", "El texto contiene \"x\""],
            ["<code class='inline'>.should(\"have.value\", \"x\")</code>", "El value de un input es \"x\""],
            ["<code class='inline'>.should(\"have.length\", n)</code>", "La selección tiene exactamente n elementos"],
            ["<code class='inline'>.should(\"have.class\", \"x\")</code>", "Tiene la clase CSS \"x\""],
            ["<code class='inline'>.should(\"have.attr\", \"x\", \"y\")</code>", "El atributo \"x\" vale \"y\""],
            ["<code class='inline'>.should(\"be.disabled\")</code> / <code class='inline'>\"be.enabled\"</code>", "Estado disabled/enabled"],
            ["<code class='inline'>.should(\"be.checked\")</code>", "Checkbox/radio marcado"],
            ["<code class='inline'>.should(\"include\", \"x\")</code>", "Un string o array incluye \"x\" (útil con <code class='inline'>cy.url()</code>)"],
        ]
    )}

    <h2>Encadenando varias aserciones con <code class="inline">.and()</code></h2>
    {code_block("""cy.get('[data-cy="boton-pagar"]')
  .should("be.visible")
  .and("not.be.disabled")
  .and("have.text", "Pagar ahora");""", "ts")}

    <h2>Negando una aserción</h2>
    {code_block("""cy.get('[data-cy="spinner"]').should("not.exist");
cy.get('[data-cy="email"]').should("not.have.class", "input-error");""", "css")}
    '''
    return page("El núcleo de Cypress", 8, "Aserciones (assertions)", body)
