# QA 02.2.3 — ejecución reproducible

Para revisar los cambios en una copia aislada:

1. `python3 qa/prepare-0223.py` para regenerar los activos QA desde la r4.
2. `node --check assets/index-fontfreda-0223-qa.js` para validar sintaxis.
3. Servir el directorio que contiene el repositorio bajo `/font-freda-0222-preview/`, como en GitHub Pages. No abrir el HTML con `file://` por las rutas absolutas.
4. Abrir en Chrome con WebGL2, crear un perfil de prueba, seleccionar `Activar demo` y recorrer Font Freda, Sa Calobra o Gaisberg.
5. Comprobar sin errores JavaScript nuevos, cámaras Seguimiento y Dron, arco inicial, textos y audio a 0 W.

La variante QA no dispone de servidor API. Los 404 bajo `/api/` son esperables en la versión estática y no se deben interpretar como superación de las integraciones.

Véase `AUDITORIA_02_2_3.md` para resultados, medidas y tareas pendientes.
