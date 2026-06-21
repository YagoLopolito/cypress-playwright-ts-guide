# Cypress + Playwright + TypeScript — Guía interactiva

Guía de onboarding para QA/automation con dos pistas independientes:
**Cypress + TypeScript** y **Playwright + TypeScript**, en un solo documento HTML interactivo.

## Live demo

Abrí `dist/index.html` en cualquier navegador. Si el repo tiene GitHub Pages activo, la guía
está disponible en `https://<usuario>.github.io/cypress-playwright-ts-guide/`.

## Características

- Switcher de pista Cypress / Playwright en el sidebar
- Playground de selectores CSS en vivo (Cypress) y simulación de locators (Playwright)
- Checklists interactivas con progreso guardado en el navegador
- Búsqueda en toda la página con resaltado y navegación
- Tema claro / oscuro persistido
- Copiar código con un click
- Responsive mobile

## Regenerar el HTML

Requiere Python 3 estándar (sin dependencias externas).

```bash
cd scripts
python assemble_web.py
# → genera dist/index.html
```

## Arquitectura

```
/
├── dist/
│   └── index.html          # Salida final (un solo archivo autocontenido)
├── scripts/
│   ├── assemble_web.py     # Orquestador: importa ambas pistas y genera el HTML
│   ├── shared/
│   │   ├── helpers.py      # Resaltador de sintaxis + builders de componentes
│   │   ├── web_styles.py   # CSS completo (incluye switcher y ambas pistas)
│   │   └── web_js.py       # JS cliente (tema, checklist, búsqueda, switcher, playgrounds)
│   ├── cypress/
│   │   ├── content_part1..4.py  # 16 secciones de Cypress
│   │   ├── cover.py        # TOC de Cypress
│   │   ├── diagrams.py     # Diagramas SVG de Cypress
│   │   ├── playground.py   # Playground CSS en vivo
│   │   └── web_page.py     # Wrapper de sección + sidebar nav
│   └── playwright/
│       ├── content_part1..4.py  # 16 secciones de Playwright
│       ├── cover.py        # TOC de Playwright
│       ├── diagrams.py     # Diagramas SVG de Playwright
│       ├── playground.py   # Playground de locators (simulación educativa)
│       └── web_page.py     # Wrapper de sección + sidebar nav
```

### Truco clave: monkeypatch de `page`

Cada `content_partN.py` define y usa una función local `page(eyebrow, num, title, body)`
para envolver el contenido. `assemble_web.py` reemplaza esa referencia en tiempo de ejecución
con una versión que agrega `data-track="cypress"` o `data-track="playwright"`. Así las 32
secciones conviven en el mismo HTML y el switcher las muestra/oculta con CSS + JS.

## Contenido Cypress (16 secciones)

1. ¿Qué es Cypress? — arquitectura, comparación con Selenium y Playwright
2. Repaso de JavaScript y TypeScript
3. Instalación del entorno completo
4. Primer proyecto Cypress + TypeScript
5. Selectores CSS + playground en vivo
6. Anatomía de un test
7. Comandos esenciales
8. Aserciones
9. Fixtures y datos de prueba
10. Comandos personalizados
11. Interceptación de red con cy.intercept
12. Page Object Model
13. Buenas prácticas
14. Errores comunes
15. CI/CD
16. Cheat sheet final

## Contenido Playwright (16 secciones)

1. ¿Qué es Playwright? — arquitectura multi-navegador
2. Diferencias clave vs. Cypress (async/await, locators, BrowserContext)
3. Instalación con npm init playwright@latest
4. Primer proyecto, UI Mode, codegen
5. Locators — getByRole, getByLabel, getByText + playground simulado
6. Anatomía de un test — fixtures inyectadas, ciclo de vida
7. Comandos esenciales
8. Aserciones web-first
9. Fixtures de datos vs. fixtures de PW (test.extend)
10. Page Object Model + fixtures custom
11. Interceptación de red con page.route()
12. Multi-navegador (projects) y multi-contexto
13. Buenas prácticas
14. Errores comunes
15. CI/CD con GitHub Actions
16. Cheat sheet final
