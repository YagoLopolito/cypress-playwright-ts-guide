# -*- coding: utf-8 -*-
"""Playground interactivo de selectores CSS: corre querySelectorAll en vivo sobre un DOM de ejemplo."""

CHIP_SELECTORS = [
    ".pg-card",
    "#pg-hero-title",
    '[data-cy="add-to-cart"]',
    "nav a",
    "li:nth-child(2)",
    "button:not(:disabled)",
    "h4 ~ span",
    "input:checked",
    ".pg-card:first-child",
    '[data-cy^="pg-"]',
]


def playground_html():
    chips = "".join(f'<button class="pg-chip" data-sel="{c}">{c}</button>' for c in CHIP_SELECTORS)
    return f'''
    <div class="playground">
      <div class="playground-head">
        <h3>🧪 Practicá selectores CSS en vivo</h3>
        <p>Escribí cualquier selector (o tocá un ejemplo) y mirá qué elementos matchean en el panel
        de la derecha. Corre <code class="inline">document.querySelectorAll()</code> de verdad, ahora mismo, en tu navegador.</p>
      </div>
      <div class="playground-body">
        <div class="playground-controls">
          <div class="pg-input-row">
            <input type="text" id="pgInput" placeholder='Ej: .pg-card, [data-cy^=&quot;pg-&quot;], li:nth-child(2)' autocomplete="off" spellcheck="false">
            <button id="pgRunBtn" type="button">Probar</button>
          </div>
          <div class="pg-result" id="pgResult"></div>
          <div class="pg-chip-label">Selectores de ejemplo</div>
          <div class="pg-chips">{chips}</div>
        </div>
        <div class="playground-preview">
          <div class="pg-preview-root" id="pgRoot">
            <div class="pg-nav">
              <a href="#" class="pg-link pg-active" data-cy="pg-nav-home">Inicio</a>
              <a href="#" class="pg-link" data-cy="pg-nav-products">Productos</a>
              <a href="#" class="pg-link" data-cy="pg-nav-contact">Contacto</a>
            </div>
            <h4 id="pg-hero-title" style="margin:0 0 10px 0;">Catálogo</h4>
            <div class="pg-card" data-cy="pg-card-1">
              <div>
                <h4>Zapatillas Runner</h4>
                <span class="pg-price">$15.000</span>
              </div>
              <button class="pg-btn" data-cy="add-to-cart">Agregar</button>
            </div>
            <div class="pg-card" data-cy="pg-card-2">
              <div>
                <h4>Remera Básica</h4>
                <span class="pg-price">$5.000</span>
              </div>
              <button class="pg-btn" data-cy="add-to-cart" disabled>Sin stock</button>
            </div>
            <div class="pg-form">
              <label for="pg-email">Email</label>
              <input type="email" id="pg-email" data-cy="pg-email-input" placeholder="tu@email.com">
              <label class="pg-check-label"><input type="checkbox" id="pg-terms" checked data-cy="pg-terms"> Acepto los términos</label>
              <button class="pg-btn" data-cy="pg-submit">Enviar</button>
            </div>
            <ul class="pg-list" data-cy="pg-list">
              <li>Primero</li>
              <li>Segundo</li>
              <li>Tercero</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    '''
