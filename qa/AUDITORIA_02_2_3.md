# Font Freda Ride Studio — Auditoría técnica y visual 02.2.3

Fecha: 19 de noviembre de 2026.
Estado: QA aislada, **no publicada ni fusionada**.
Base: r4 pública, commit `96a423e81fa969a3bb8d2f959629c05aa4f77d49`.
Rama de trabajo: `qa/0223-visual-audit-20261119`.

## Alcance

Auditoría sobre el código efectivo de la r4 y ejecución en Chrome con WebGL2/ANGLE Metal (Apple M4, 1512×940, modo demo). Pruebas de conducción en Font Freda, Sa Calobra y Gaisberg. Se conserva la r4 como referencia inmutable. No se han conectado rodillos reales ni se ha utilizado una cuenta privada del navegador.

## Hallazgos de la r4

| ID | Severidad | Hallazgo verificado | Evidencia |
|---|---|---|---|
| V-01 | Alta | `THREE.Object3D.add: object not an instance of THREE.Object3D. undefined` al generar vallas. La función mediterránea podía devolver un array vacío y se llamaba igualmente `add(...[])`. | Stack de Chrome en `EC.fences`; reproducido en Font Freda r4. |
| V-02 | Media | Dron muestra al ciclista demasiado pequeño, y el follaje llega a taparlo completamente en algunas escenas. | Captura comparativa de Font Freda r4 con Metal. |
| V-03 | Media | En Seguimiento el ciclista queda muy abajo respecto del mapa y la banda de perfil. | Captura en ruta en movimiento, 180 W demo. |
| V-04 | Alta visual | Gran arco de salida de KOM ocupa la cámara al iniciar Sa Calobra. | Captura de los primeros metros de Sa Calobra. |
| V-05 | Baja | Descripción de varias etapas en inglés (`climb`, `easy lead-in`, `of climbing`). | HUD y banner en Sa Calobra y Gaisberg. |
| V-06 | Alta antes de comercializar | La publicación es estática; `/api/health` y `/api/strava/status` devuelven 404. No hay backend de historial ni Strava. | Respuestas HTTP 404 observadas en pruebas locales. |
| V-07 | Abierta | Edificios, señalización y marcas de carretera todavía presentan artefactos en ciertos puntos de Sa Calobra; queda pendiente la corrección de su geometría y colisiones. | Captura de salida de Sa Calobra incluso tras eliminar el arco. |

## Correcciones concretas en esta QA

1. Guardar los elementos de vallas generados y llamar `add` solamente cuando la lista no está vacía; evita el error 3D sin eliminar vallas válidas.
2. Reencuadrar Seguimiento un poco más atrás y alto para mostrar al ciclista y la calzada a la vez.
3. Reencuadrar Dron sobre el eje de circulación, a menor altura y distancia: el ciclista se distingue y la copa de árboles deja de ocultarlo en la prueba.
4. Omitir el arco KOM de inicio cuando empieza a menos de 30 m del arranque del recorrido. Se conservan los hitos posteriores.
5. Traducir `Subida a ...`, el texto de aproximación de ascensos y el banner general de desnivel positivo.
6. Etiquetar claramente la variante como `02.2.3 QA` para evitar confundirla con una versión publicada.

## Validaciones realizadas

- [x] Se crea la variante a partir de la r4 sin sobrescribir los archivos r4.
- [x] `node --check` sobre la variante JavaScript.
- [x] Motor de audio `pw` **idéntico byte a byte** al de la r4.
- [x] Font Freda abre la ruta y permite circular en modo demo, con cámara Seguimiento, Lateral y Dron.
- [x] Error 3D anterior presente en la r4 y ausente en la QA.
- [x] Sa Calobra carga, se mueve y ya no muestra el arco gigante en la salida.
- [x] Gaisberg carga y se mueve, sin nuevos errores de aplicación.
- [x] Se comprueba la presencia de audio ambiental sin modificar los recursos ni el motor de audio (la escucha real r4 ya fue validada por el usuario).
- [ ] Prueba física con rodillo FTMS T-SOX, resistencia, ERG y reconexión.
- [ ] Ronda visual exhaustiva de Sa Calobra y otras rutas, incluyendo edificios, señales, cruces y carretera.
- [ ] Análisis de rueda delantera/trasera en pendientes fuertes y curvas cerradas durante recorrido prolongado.
- [ ] Pruebas en Safari, dispositivos móviles y distintas resoluciones.
- [ ] Prueba de carga/performance con el mismo hardware y condiciones en varias sesiones.

## Rendimiento de pruebas

La ejecución headless con SwiftShader por software produjo tiempos artificialmente lentos y pocas imágenes por segundo; **no debe utilizarse como referencia de rendimiento del producto**. Con Chrome y Metal en Mac M4, la preparación de ruta local en caliente osciló aproximadamente entre 2,5 y 5,5 segundos en las rutas probadas. Son mediciones de laboratorio con cachés locales, no tiempos prometidos para el usuario.

HUD de Font Freda en escritorio a 1512×940: panel derecho ~265×411 px; canvas de mapa ~237×150 px.

El catálogo leído contiene quince rutas seleccionables más el índice JSON. La reproducción de audio sintético se ha preservado porque el usuario confirmó que el fallo de clics había desaparecido en la r4.

## Próximas prioridades

1. P0 — probar con el T-SOX real: FTMS, vatios, cadencia, ERG, inclinaciones, marchas y recuperación de conexión. No afirmar fiabilidad deportiva antes de esa prueba.
2. P1 — geometría: resolver edificios muy próximos a la carretera, señales atravesadas y marcas superpuestas; validar contacto de ambas ruedas con la malla en todos los recorridos.
3. P1 — navegación: comparar perfiles de cámara en pantallas pequeñas y permitir ajustar vista Dron cuando sea necesario.
4. P2 — iluminación, vegetación, calidad de paisajes y optimización de carga antes de explorar vídeo real.
5. P2 — evaluar fuente editable del proyecto, licencias, backend e historial antes de comercializar.

## Restricciones de publicación

**No publicar ni fusionar la 02.2.3 QA** por el mero hecho de que estas pruebas hayan pasado. Conservar la r4 pública y las versiones 02.1/02.2.1. Para pasar a una siguiente beta de usuario, revisar primero las evidencias visuales y autorizar el cambio.

## Capturas de comparación en el mismo navegador y aceleración Metal

Las capturas son de sesiones demo, no de entrenamientos físicos. No son comparaciones pixel a pixel del mismo instante exacto; sirven para verificar el cambio de encuadre y los defectos visibles.

### Seguimiento

- [r4: plano anterior](capturas/seguimiento-r4.jpg)
- [02.2.3 QA: ciclista mejor encuadrado](capturas/seguimiento-qa.jpg)

### Dron

- [r4: ciclista oculto por el follaje](capturas/dron-r4.jpg)
- [02.2.3 QA: cámara centrada sobre la calzada](capturas/dron-qa.jpg)

### Sa Calobra

- [r4: arco inicial sobredimensionado](capturas/sa-calobra-r4.jpg)
- [02.2.3 QA: salida sin arco que estorbe](capturas/sa-calobra-qa.jpg)
