# Font Freda 02.2.2 BETA — versión de pruebas

Publicación independiente de Font Freda 02.1 y 02.2.1. No incorpora API backend ni sincronización de historial.

Cambios experimentales: 12 marchas virtuales desde 6; paneles semitransparentes y compactos; audio de bosque y pueblo basado en grabaciones de dominio público con volúmenes adaptativos; eliminado el clic de rueda libre repetitivo; ajuste provisional de altura inicial y eliminación de un elemento secundario del modelo de rueda.

Pendiente de validación: ruedas y holgura con cuadro, carretera/artefactos visuales, precisión de la altura en terreno cambiante, reproducción audible y transiciones de sonidos, integración Bluetooth T-SOX y experiencia móvil.

No utilizar para entrenamientos en los que se requiera fiabilidad de potencia o resistencia real. Ejecutar primero en modo demo.

Véase AUDIO_LICENCIAS_0222.txt para fuentes.

## Revisión visual 02.2.2 r2 (19/11/2026)
Se han separado los números y las etiquetas del panel derecho, corregido el desplazamiento fijo de altura y ampliado la holgura de la rueda delantera. La bici se alinea con la malla de la carretera bajo cada neumático. En Sa Calobra siguen existiendo geometrías superpuestas al inicio. El audio no se ha cambiado desde la 02.2.2.

## Revisión audio 02.2.2 r3 (19/11/2026)
Se ha eliminado el generador sintético de clics de rueda y el pulso de cadena modulado por cadencia. Se ha corregido el punto de cierre del bucle de ruido continuo y suavizado la unión de principio y final de las grabaciones ambientales. Se mantienen los sonidos de bosque y ciudad, rodadura y viento adaptados a la velocidad. Pendiente de confirmar con escucha humana en Chrome durante ruta real o demo.

## Revisión 02.2.2 r4 (19/11/2026)
- Audio: corregido el ataque de los sonidos sintéticos de pájaros. En r3 los osciladores arrancaban inmediatamente y con ganancia 1 durante 20 ms antes de la automatización, provocando pulsos fuertes intermitentes incluso con 0 W. En r4 ambos osciladores arrancan en la misma marca temporal que la envolvente y el volumen inicial es 0. Prueba de regresión comparativa en Chrome con OfflineAudioContext: primer tramo de 20 ms pasa de RMS ~0,50 en r3 a 0 en r4; el canto posterior permanece audible.
- Minimap: escala ahora el recorrido al ancho y alto disponibles manteniendo proporciones; trazado ligeramente más nítido. CSS del panel compactado (sin ampliar su ancho).
- Sol: halo ambiental muy suave añadido al shader del cielo, que se oculta naturalmente cuando la geometría tapa el cielo.
- Ruedas: radio de contacto ajustado al neumático y altura de respaldo interpolada cuando el cálculo exacto de la malla no encuentra superficie en curvas.
- Pendiente: escucha humana completa en rutas a 0 W y revisión visual de ruedas en vista dron. No afirmar que esas pruebas ya están superadas.
