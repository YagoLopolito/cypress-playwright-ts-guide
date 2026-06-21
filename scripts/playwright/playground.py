# -*- coding: utf-8 -*-
"""Playground SIMULADO de locators de Playwright.

Los locators de Playwright (getByRole, getByLabel, etc.) viven en el runtime de Node.js,
NO en el navegador. Este playground aproxima su comportamiento contra el DOM de ejemplo
usando roles ARIA implícitos y atributos accesibles, con una nota didáctica visible.
"""

PW_CHIP_LOCATORS = [
    ("getByRole('button', { name: 'Agregar' })", "role:button:Agregar"),
    ("getByRole('button', { name: 'Enviar' })",  "role:button:Enviar"),
    ("getByLabel('Email')",                        "label:Email"),
    ("getByLabel('Acepto los términos')",           "label:Acepto"),
    ("getByText('Catálogo')",                       "text:Catálogo"),
    ("getByText('Zapatillas Runner')",              "text:Zapatillas Runner"),
    ("getByPlaceholder('tu@email.com')",            "placeholder:tu@email.com"),
    ("getByRole('link', { name: 'Inicio' })",       "role:link:Inicio"),
    ("getByRole('checkbox')",                       "role:checkbox:"),
    ("getByTestId('pw-submit')",                    "testid:pw-submit"),
]


def pw_playground_html():
    chips = "".join(
        f'<button class="pg-chip pw-pg-chip" data-pw-sel="{d}">{label}</button>'
        for label, d in PW_CHIP_LOCATORS
    )
    return f'''
    <div class="playground pw-playground">
      <div class="playground-head">
        <h3>🔬 Practicá locators de Playwright (simulación didáctica)</h3>
        <p>Seleccioná un locator de ejemplo o escribí uno en el campo. La función de abajo
        <em>aproxima</em> cómo Playwright resuelve <code class="inline">getByRole</code>,
        <code class="inline">getByLabel</code>, <code class="inline">getByText</code> y
        <code class="inline">getByPlaceholder</code> contra el DOM de ejemplo.</p>
        <div class="callout callout-warning" style="margin-top:10px">
          <div class="callout-head"><span class="callout-badge">ATENCIÓN</span> Esto es una aproximación educativa</div>
          <div class="callout-body"><p>La implementación real de los locators vive en el motor de
          Playwright (Node.js), no en el navegador. Esta simulación usa roles ARIA implícitos
          y atributos accesibles de forma simplificada. No es lo que corre en producción:
          es una herramienta para <strong>entender el modelo mental</strong> de los locators.</p></div>
        </div>
      </div>
      <div class="playground-body">
        <div class="playground-controls">
          <div class="pg-input-row">
            <input type="text" id="pwPgInput"
              placeholder='Ej: getByRole(&quot;button&quot;, &#123; name: &quot;Enviar&quot; &#125;)'
              autocomplete="off" spellcheck="false">
            <button id="pwPgRunBtn" type="button">Probar</button>
          </div>
          <div class="pg-result" id="pwPgResult"></div>
          <div class="pg-chip-label">Locators de ejemplo</div>
          <div class="pg-chips">{chips}</div>
        </div>
        <div class="playground-preview">
          <div class="pg-preview-root" id="pwPgRoot">
            <nav class="pg-nav">
              <a href="#" class="pg-link pg-active" aria-current="page">Inicio</a>
              <a href="#" class="pg-link">Productos</a>
              <a href="#" class="pg-link">Contacto</a>
            </nav>
            <h4 id="pw-pg-hero-title" style="margin:0 0 10px 0;">Catálogo</h4>
            <div class="pg-card">
              <div>
                <h4>Zapatillas Runner</h4>
                <span class="pg-price">$15.000</span>
              </div>
              <button class="pg-btn" data-testid="pw-add-1">Agregar</button>
            </div>
            <div class="pg-card">
              <div>
                <h4>Remera Básica</h4>
                <span class="pg-price">$5.000</span>
              </div>
              <button class="pg-btn" disabled>Sin stock</button>
            </div>
            <div class="pg-form">
              <label for="pw-pg-email">Email</label>
              <input type="email" id="pw-pg-email" placeholder="tu@email.com">
              <label class="pg-check-label">
                <input type="checkbox" id="pw-pg-terms" checked> Acepto los términos
              </label>
              <button class="pg-btn" data-testid="pw-submit">Enviar</button>
            </div>
            <ul class="pg-list">
              <li>Primero</li><li>Segundo</li><li>Tercero</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    '''
