# -*- coding: utf-8 -*-
"""Portada e índice para la pista de Playwright."""

PW_TOC_ITEMS = [
    ("pw-1",  "¿Qué es Playwright?",                      "Arquitectura, comparación de 3 punttas"),
    ("pw-2",  "Diferencias clave para quien viene de Cypress", "async/await real, locators, browser context"),
    ("pw-3",  "Instalación del entorno completo",          "npm init playwright@latest paso a paso"),
    ("pw-4",  "Primer proyecto Playwright + TypeScript",   "Tu primer test, UI Mode, show-report"),
    ("pw-5",  "Locators: la forma Playwright",             "getByRole, getByLabel, getByText y más"),
    ("pw-6",  "Anatomía de un test",                       "test.describe, fixtures inyectados, aislamiento"),
    ("pw-7",  "Comandos esenciales",                       "click, fill, check, press y tabla de referencia"),
    ("pw-8",  "Aserciones web-first",                      "expect(locator).toBeVisible(), soft assertions"),
    ("pw-9",  "Datos de prueba y fixtures",                "JSON estáticos + sistema de fixtures con DI"),
    ("pw-10", "Page Object Model y fixtures custom",       "El reemplazo idiomático de custom commands"),
    ("pw-11", "Interceptación y mock de red",              "page.route(), waitForResponse()"),
    ("pw-12", "Multi-navegador y multi-contexto",          "projects en config, múltiples páginas"),
    ("pw-13", "Buenas prácticas",                          "Locators semánticos, web-first, evitar timeouts"),
    ("pw-14", "Errores comunes",                           "Olvidar await, no usar Trace Viewer, y más"),
    ("pw-15", "CI/CD",                                     "GitHub Actions, trace on failure, paralelización"),
    ("pw-16", "Cheat sheet final y recursos",              "Referencia compacta: locators, comandos, aserciones"),
]

PW_GROUPS = [
    ("Fundamentos",        ["pw-1", "pw-2"]),
    ("Puesta en marcha",   ["pw-3", "pw-4"]),
    ("La base: Locators",  ["pw-5"]),
    ("El núcleo de PW",    ["pw-6", "pw-7", "pw-8"]),
    ("Organización",       ["pw-9", "pw-10", "pw-11", "pw-12"]),
    ("Calidad y entrega",  ["pw-13", "pw-14", "pw-15"]),
    ("Referencia",         ["pw-16"]),
]
