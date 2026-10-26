# branthia-content

Sistema desasistido de contenido de Branthia para LinkedIn.

- `GENERADOR.md` — qué hace la tarea programada cada mañana (fuente única del proceso).
- `kit/` — plantillas tipográficas con la identidad de branthia.com (Satoshi + JetBrains Mono) y `render.py` (Playwright) que genera tarjetas PNG, carruseles PDF y pantallas enmarcadas.
- `piezas/` — especificaciones JSON de los visuales.

Las fuentes de `kit/fonts/` son las de branthia.com (Satoshi, ITF Free Font License; JetBrains Mono, OFL). Este repo es privado; los visuales ya generados se publican en `branthia-visuals` (público) porque Buffer necesita URLs públicas.

Flujo: notas del fundador (Notion) → generador (tarea programada) → base «Contenidos» (Notion) → Buffer (borrador o programado) → LinkedIn página Branthia.
