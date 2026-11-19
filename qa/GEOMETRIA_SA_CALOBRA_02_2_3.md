# Sa Calobra — revisión de edificios, señales y contacto de ruedas

**Fecha:** 19/11/2026. **Estado:** cambios aislados y probados en QA, **no desplegados**. Se parte de la rama `qa/0223-visual-audit-20261119`. La r4 publicada no se modifica.

## Hallazgos

- Sa Calobra conserva en origen un giro muy cerrado en los primeros 25 m y cuenta con un trazado auxiliar de retorno. En esa zona existen polígonos de carretera solapados. Las marcas blancas siguen presentando artefactos, por lo que la geometría de la salida **no puede darse por corregida**.
- Las construcciones de OpenStreetMap no se deben eliminar indiscriminadamente: 40 polígonos de edificios se encuentran en el archivo OSM de la ruta, con hoteles y construcciones legítimas próximas al núcleo urbano.
- El filtro anterior buscaba proximidad con un margen aproximado de 3,5 m desde el eje de ruta. La nueva prueba aumenta a 8,1 m el margen **solo en Sa Calobra**, para proteger también la cuneta, y comprueba el perímetro de los edificios incluso cuando su primer vértice está más lejos. Gaisberg y el resto mantienen el margen anterior.
- Prueba geométrica independiente con una proyección métrica local: de los 40 polígonos, 1 tiene alguna arista a menos de 3,5 m y 9 tienen alguna a menos de 8,1 m. **Esto mide candidatos por proximidad; no equivale a afirmar que se han borrado 9 edificios del render**. Los edificios legítimos restantes continúan presentes en las capturas.
- Algunas señales generadas a partir del recorrido se hundían en la ladera porque el código elegía la menor entre la altura del terreno y la cota de carretera. La variante usa altura de terreno, con una cota mínima cercana a la carretera para evitar profundidades excesivas. Pendiente de inspección de señales en toda la ruta.

## Comprobación numérica de ruedas (en malla, sin rodillo)

Se situó el ciclista en 33 puntos predefinidos de cada ruta (incluidos los primeros 400 m y puntos posteriores), y se consultó la altura real de la malla de carretera bajo cada centro de rueda, descontando el radio de contacto de 0,342 m. La separación positiva indica aire bajo el neumático.

| Ruta | Puntos muestreados | Ruedas separadas más de 6 cm | Mayor separación observada |
|---|---:|---:|---:|
| Font Freda | 33 | 0 | Menos de 6 cm |
| Gaisberg | 33 | 0 | Menos de 6 cm |
| Sa Calobra | 33 | 4 observaciones de rueda | **29,6 cm** en torno al metro 15 |

En Sa Calobra el problema está concentrado en los primeros 20 m de la muestra; a partir de 30 m las superficies consultadas generalmente quedan a pocos milímetros, salvo pequeñas discrepancias de curvatura. Esta prueba de posiciones fijas no equivale a validar todos los fotogramas de una salida completa.

### Experimentos rechazados

- **Recortar 24,5 m de la ruta:** probado solo en copia. Empeoró la separación máxima a **47,1 cm** sobre el metro 8 del nuevo trazado y redujo el contador de curvas de 18 a 17. Se revirtió. No se ha alterado `routes/sa-calobra.json`.
- **Suprimir la carretera auxiliar de giro de inicio:** la prueba de carga quedó bloqueada y se interrumpió. No se ha incorporado ni se declara superada.

## Validaciones y archivos

- `python3 qa/tests/test_sa_calobra_clearance.py` comprueba por regresión el conjunto de 40 edificios y los umbrales 3,5/8,1 m.
- `node --check assets/index-fontfreda-0223-qa.js` supera sintaxis.
- Sa Calobra y Gaisberg arrancan en Chrome con aceleración Metal, modo demo, sin nuevos errores JavaScript. Las llamadas `/api/health` y `/api/strava/status` devuelven 404 por la ausencia conocida de backend en el sitio estático.
- El motor de audio `pw` de la 02.2.3 QA es **idéntico** al de la r4; ninguna grabación ambiental ha sido modificada.
- Captura de Sa Calobra con el nuevo filtro: [ver captura](capturas/sa-calobra-filtro-edificios-qa.jpg). Para comparar con la r4, véase [captura r4](capturas/sa-calobra-r4.jpg).

## Pendientes prioritarios

1. Resolver el solapamiento de geometrías de los primeros 25 m sin modificar datos GPS ni romper el retorno de ruta. Prototipar un ajuste del mallado de cruces y revisar las superficies con trazado/depuración de triángulos.
2. Revisar más edificios de Sa Calobra: los que se ven al inicio pueden ser legítimos, pero sus alturas, cimientos y escalas necesitan una auditoría por referencia real.
3. Comprobar las señales fuera del primer kilómetro y con distintas altitudes.
4. Repetir mediciones de ruedas con trazado continuo, en sentido de vuelta, y con el rodillo T-SOX real.

**Protección:** la rama QA no modifica `main`, no publica ninguna beta ni cambia `routes/sa-calobra.json` o el audio.
