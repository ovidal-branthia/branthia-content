# Generador de contenido de Branthia — instrucciones de ejecución

Este documento lo lee la tarea programada «Branthia · Contenido LinkedIn» cada mañana. Es la única especificación del sistema: si algo cambia, se cambia aquí.

## Fuentes y destinos (IDs fijos)

| Qué | Dónde | ID |
|---|---|---|
| Cerebro de contenido (tesis, límites, voz, pilares, guía visual) | Claude Docs | proyecto `0631da28-4a9c-454e-bc44-a751109c0bb0` · https://claude.ai/artifact/1mNJNbVUz4wCGreCZNvh6P |
| Cola de piezas | Notion · base «Contenidos» | data source `collection://fdfdf2a4-7ca1-40f2-9a3c-292196de8d3b` |
| Notas del fundador | Notion · página «Notas de la semana» | `40553a78-a1b5-812f-bd55-d9aaaa25c58a` |
| Kit visual | este repo · `kit/` | `python3 kit/render.py <spec.json> <salida>` |
| Visuales públicos | repo `ovidal-branthia/branthia-visuals` (público) | URL: `https://raw.githubusercontent.com/ovidal-branthia/branthia-visuals/main/<ruta>` |
| Publicación | Buffer · organización «My organization» `6adf3e887f3fb615d1e7a63d` | canal LinkedIn página **Branthia** `6adf3ee72f1f5ed648d7ebbc` |

Nunca publicar en los canales `oshcarvidal` (perfil) ni `athria-io` (Athria).

## Estados en Notion

- **Borrador**: generada por el sistema o pendiente de algo (captura, cifra). No se programa.
- **Aprobada**: el fundador la ha dado por buena. Se programa en Buffer en su fecha.
- **Programada**: ya está en Buffer (campo «Buffer ID» relleno).
- **Publicada**: Buffer la ha enviado.
- **Descartada**: no se toca.

## Ejecución diaria (cada mañana)

1. **Preparar entorno.** Clonar `branthia-content` y `branthia-visuals` (shallow). Playwright y Chromium ya están instalados.
2. **Sincronizar con Buffer.** Para cada pieza «Programada», consultar su post en Buffer; si `status = sent`, pasarla a «Publicada» y guardar la URL si la hay. Si `status = error`, dejarla en «Programada» y avisar.
3. **Programar lo aprobado de los próximos 7 días.** Piezas con Estado = Aprobada, Fecha entre hoy y hoy+7, sin «Buffer ID»:
   - Si Formato = Pantalla y no hay archivo en «Captura» → saltar y avisar («falta captura de la pieza X»).
   - Generar el visual si aplica (ver «Visuales»), subirlo a `branthia-visuals` y guardar «Visual URL».
   - Crear el post en Buffer con `create_post`: `channelId` Branthia, `schedulingType: automatic`, `mode: customScheduled`, `dueAt` = Fecha a las **08:45 Europe/Madrid** con su offset (+01:00 en invierno, +02:00 en verano). Texto = cuerpo de la página de Notion tal cual, con saltos de línea.
   - Asset: Tarjeta/Pantalla → `{image:{url, metadata:{altText: <frase de la tarjeta>}}}`. Carrusel → `{document:{url: <pdf>, title: <gancho corto>, thumbnailUrl: <png página 01>}}`. **Toda pieza lleva visual**: si una pieza antigua tiene Formato = Texto, generarle una tarjeta con su frase más recordable y publicarla como Tarjeta.
   - Guardar «Buffer ID» y pasar Estado a «Programada».
   - Límite del plan gratuito: **10 posts programados a la vez**. No superar 9; si se llega, parar y esperar al día siguiente.
4. **Lunes: generar la semana siguiente.** Solo los lunes:
   - Leer el cerebro de contenido completo (tesis, límites, voz, pilares, casos) y la página «Notas de la semana» (lo nuevo desde el lunes anterior).
   - Contar las piezas Aprobadas/Programadas de la semana que empieza en 7 días (lunes a viernes). Si hay menos de 5, generar las que falten como **Borrador**, una por día laborable sin pieza.
   - Cada pieza nueva: respetar la mezcla de pilares de la sección 7 (nunca dos seguidas del mismo pilar; Construido al menos cada dos días), una tesis de la sección 3, los límites de la sección 4 y la voz de la sección 5 (120–220 palabras, gancho en dos líneas, sin emojis, máximo 3 hashtags, siempre #IAaplicada). Priorizar lo que venga de las notas del fundador (Origen = Nota de voz).
   - Rellenar en Notion: Gancho, Fecha, Pilar, Formato, Tesis, Origen, «Cifras a confirmar» si introduce una cifra no listada en la biblioteca de casos, y el texto completo en el cuerpo de la página. Si es Pantalla, marcar «Falta captura».
   - Crear también un **borrador en Buffer** (`saveToDraft: true`, mismo canal y `dueAt`) para que el fundador lo revise desde la app; guardar su «Buffer ID». Cuando el fundador lo apruebe en Buffer o cambie el Estado en Notion a «Aprobada», el paso 3 de días siguientes lo programa (si el borrador ya existe en Buffer, editarlo con `edit_post` en vez de crear otro).
5. **Informe.** Terminar con un mensaje corto: qué se ha programado (fecha · gancho), qué borradores hay para revisar, qué falta (capturas, cifras).

## Visuales

- **Regla: en la página de Branthia toda pieza lleva visual** (tarjeta, carrusel o pantalla). Nunca se genera Formato = Texto.
- Especificación: JSON como en `piezas/*.json` (tipos `tarjeta`, `carrusel`, `pantalla`). Las piezas del plan inicial ya tienen su spec en `piezas/`; «Spec visual» en Notion indica el fichero y el id.
- Piezas nuevas: escribir su spec en `piezas/AAAA-MM-DD.json` y hacer commit.
- Tarjeta: la frase más recordable del post, ≤ 70 caracteres, con la segunda mitad envuelta en `<q>…</q>` (sale en gris). Método y portadas de carrusel: `"dark": true`.
- Pantalla: descargar el archivo de «Captura» (Notion `get_file_download_urls`), guardarlo en `/tmp` y pasarlo como `img`.
- Render: `python3 kit/render.py spec.json out/`. Revisar el PNG resultante (abrirlo) antes de subirlo: texto cortado o desbordado → reducir la frase.
- Subida: copiar a `branthia-visuals/AAAA/MM/<id>-<tipo>.png|pdf` (y `-carrusel-01.png` como miniatura), commit y push a `main`.

## Reglas que no se rompen

- No publicar nada que no esté en Estado «Aprobada» (los borradores van a Buffer solo como draft).
- No nombrar competidores, ni clientes actuales, ni precios. No mencionar Xygeni. No datos de atletas.
- No cambiar el cerebro de contenido. Si una nota del fundador contradice una tesis, generar la pieza como Borrador y señalarlo en el informe.
- Ante cualquier error de Buffer o Notion, no reintentar en bucle: anotar y avisar en el informe.
