# Cambios realizados y pendientes — Grupo 03

Fecha de cierre: 19 de octubre de 2026, America/Lima.

## Archivos de entrega

- `Articulo_Grupo03_Deteccion_spam_SMS_revisado.docx`: documento editable con fuentes incrustadas y campos actualizados.
- `Articulo_Grupo03_Deteccion_spam_SMS_revisado.pdf`: exportación del Word revisado.
- Este archivo: cambios, límites de la revisión y datos que faltan.

Se conservaron las secciones I–VIII, los anexos A–H, el título y el orden y grafía de los cuatro autores. Los originales permanecen en el directorio.

## Cambios realizados

1. Se revisaron visualmente las 44 páginas originales y se corrigieron la paginación de tablas cortas, las notas y fuentes aisladas y la unión entre figuras, rótulos y fuentes. La matriz extensa conserva su encabezado y un rótulo «Tabla 30 (continuación)» en la segunda parte. La tabla de correspondencia del protocolo se mantiene completa.
2. Se mantuvieron A4, márgenes de 2 cm, cuerpo EB Garamond 12/14.4 pt, justificación y sangría de 4 mm, resumen 10/12 pt y la jerarquía editorial solicitada. Se ajustaron algunas figuras y espacios para mejorar el flujo de las páginas.
3. Se uniformaron los pies con línea fina y número a la derecha. Se comprobó cuantitativamente la posición de las cabeceras alternadas; su aparente variación en una revisión preliminar era un artefacto de visualización.
4. Se corrigió la representación de la ecuación ECE mediante la exportación de sus ecuaciones editables desde Word. Se ajustó la ecuación de decisión para mantener su número a la derecha.
5. Se incrustaron las fuentes usadas, incluidas las variantes de EB Garamond. Se conservaron los campos SEQ y REF y se corrigieron los identificadores duplicados de marcadores; los campos se actualizaron en Word antes de exportar.
6. Se completó Salman et al. (2024) a partir de su PDF primario: Tablas 4, 12 y 14, con sus páginas de origen. Se distinguieron la prueba convencional y el conjunto adversarial y se declaró la discrepancia entre el resumen y el corpus de 67 018 mensajes detallado en el cuerpo del artículo.
7. Se incorporó Lulli Caceres y Ortiz Gutierrez (2024), UPN–Trujillo, como antecedente contextual jurídico. Se indicaron objetivo, método, población sin tamaño total reportado, muestra de 11 carpetas y tres fiscales, y el caso iniciado por SMS. Esta tesis no evalúa un clasificador ni estima prevalencia del spam. La bibliografía pasa de 33 a 34 referencias.
8. Se cotejaron citas y referencias y se corrigieron el año del capítulo publicado de Platt (2000), el fascículo de Hendrickx, los editores del volumen de Reyes y la atribución del ECE. Se acotaron inferencias sobre las 5572 filas de otra versión del corpus, las sondas exploratorias y los intervalos bootstrap.
9. Se retiró la certificación de indexación que no pudo revalidarse: la tabla identifica doce artículos recientes y conserva como declarados los valores anteriores de cobertura y cuartil, con una nota explícita de verificación pendiente.
10. Se corrigieron las sustituciones accidentales detectadas durante el cotejo final y las negritas de párrafos completos. Se actualizó el registro de asistencia de IA en el Anexo H y en `anexos/registro_uso_IA.md`.

La entrega final tiene **45 páginas, revisadas visualmente**. La Tabla 9 quedó íntegra con su nota y fuente en la página 16 y la Figura 13 quedó completa en la página 44. Se conserva espacio inferior en la página 41 para mantener entera la Tabla 33 en la 42; la página 45 termina con el Anexo H. El registro por página está en `revision/REVISION_VISUAL_FINAL.md`.

El 19 de octubre se verificó también el código entregado: **cuatro pruebas unitarias superadas** y recorrido Flask completo con clasificación spam/legítimo/pendiente, confirmación de revisión, bandeja y exportación CSV, usando SQLite temporal. El modelo cargó con scikit-learn 1.9.1 y mantuvo su huella. No se ejecutó el notebook. La comprobación funcional usó las dependencias disponibles en este equipo; no equivale a verificar una instalación limpia de todas las versiones de `requirements.txt`. Evidencias y comandos: `revision/verificacion_codigo_2026-10-19.md` y el JSON del mismo nombre.

Los resultados congelados se conservaron. No se entrenaron modelos ni se seleccionaron parámetros con la prueba ya observada. Se cotejaron los archivos guardados y las huellas originales:

- ZIP del dataset: `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3`.
- Modelo: `de87978042e6c821cb8a4fb2dff3cee4ada58ac3ff1ef65ef0ea703e55482705`.

## Datos y evidencias que debe completar el grupo

- Correos y ORCID de los cuatro autores.
- Hardware de los integrantes y fechas reales del cronograma.
- Dificultades de aprendizaje, decisiones finales y evidencias de comprensión de cada integrante; otras consultas a IA realizadas por el grupo.
- Historial de contribuciones que permita documentar autoría y evolución del proyecto. El repositorio remoto de entrega ya es [Sistema de Detección de Mensajes SPAM](https://github.com/KirderFaid13/Sistema-de-Deteccion-de-Mensajes-SPAM); la publicación no reconstruye contribuciones anteriores.
- Certificaciones externas, únicamente cuando exista una evidencia acreditable.
- Revisión y comprensión del código y del artículo por cada integrante. La asistencia de IA no certifica el «50 % de avance» como trabajo propio del grupo.

Todos los marcadores correspondientes permanecen visibles. Si el grupo reproduce el notebook, debe conservar la configuración congelada y tratarlo como reproducción; la prueba existente ya no puede utilizarse para elegir nuevas decisiones.

## Verificaciones externas que siguen pendientes

- Conservar las fichas individuales de Scimago/Scopus, con URL, ISSN, año y cuartil. Crossref confirma identidad bibliográfica; no acredita por sí solo indexación. Los accesos a Scimago fueron restringidos y no se certifica el cumplimiento del mínimo de artículos indexados.
- Completar la consulta manual de RENATI y de los repositorios institucionales con acceso restringido. Se encontró un antecedente local contextual; sigue pendiente verificar un experimento local reciente de clasificación de spam SMS. No se afirma que no exista.
- Acceder al texto completo de Reyes et al. (2026) para verificar muestra y métricas. Sus editores bibliográficos ya se completaron.
- Verificar la afiliación de Abdel-Jaber y, si se requiere, la indexación en Web of Science.
- Localizar estadísticas oficiales recientes desagregadas de spam SMS para Perú o Trujillo.
- El PDF de ejemplo RIED (2024) no se encontró en el directorio entregado. Se aplicaron las especificaciones editoriales escritas; no se certifica una comparación visual con ese ejemplo.

## Trabajo experimental futuro, opcional

La rejilla ampliada, los n-gramas de caracteres y el rechazo por novedad o idioma no se ejecutaron en este cierre. Deben plantearse como exploratorios usando entrenamiento y validación, con un protocolo adecuado —por ejemplo, CV anidada— y sin volver a seleccionar con la prueba actual. La evaluación externa, los SMS en español con consentimiento y las pruebas con revisores humanos reales siguen pendientes.

## Uso y trazabilidad

Después de cualquier edición en Word: Ctrl+A y F9, revisar las referencias cruzadas y volver a exportar el PDF. La incrustación de fuentes está activada; `fuentes_EB_Garamond.zip` permanece como respaldo para su instalación si otro editor sustituye la tipografía.

Las fuentes primarias descargadas, sus huellas, la búsqueda documentada, los informes de cotejo y las imágenes de revisión se conservan en `revision/`. Los detalles de integridad de la entrega final se guardan en `revision/verificacion_final.json` y su registro visual en `revision/REVISION_VISUAL_FINAL.md`.

## Actualización para la publicación en GitHub

El 19-10-2026 se preparó el repositorio de entrega con el código, el modelo, el dataset público, los resultados guardados y los documentos finales. El README raíz explica instalación y funcionamiento; `requirements-app.txt` y `requirements-test.txt` separan el uso del prototipo del entorno histórico del experimento. La instalación en un entorno limpio, las cuatro pruebas, el recorrido Flask y una petición HTTP local fueron correctos; su evidencia compartida está en `docs/verificacion_publicacion.json` del repositorio.

Los archivos de trabajo de `Articulo/revision/`, los PDFs bibliográficos descargados y las futuras bases de datos de uso se excluyen de Git. Sus registros permanecen en la carpeta local de trabajo. El Word y el PDF revisados se conservan como la versión editorial cerrada; sus marcadores sobre un repositorio pendiente corresponden al estado anterior a esta publicación. Sigue pendiente acreditar las contribuciones individuales del grupo.
