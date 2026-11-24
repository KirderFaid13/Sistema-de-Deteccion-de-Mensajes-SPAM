# Registro de uso de IA generativa — Grupo 03
Herramienta: Claude (Anthropic), sesión configurada con el modelo claude-opus-5-5 (el modelo que atendió cada respuesta puede diferir).
Fecha: 18-10-2026 (America/Lima).

## 1. Instrucción principal del grupo (resumen fiel)
Actuar como investigador estudiantil de Ingeniería de Sistemas y desarrollar el artículo de investigación aplicada «Detección de spam en mensajes SMS mediante aprendizaje supervisado y revisión humana de predicciones inciertas», siguiendo: (1) tema, alcance y dataset UCI SMS Spam Collection; (2) estructura institucional obligatoria (I–VIII); (3) APA 7; (4) diseño editorial del PDF de ejemplo (RIED, 2024). Incluye protocolo experimental (partición 60/20/20, semilla 42, RL vs SVM lineal, TF-IDF, C∈{0.1,1,10}, n-gramas, calibración, τ∈{0.50…0.95}), metas F1≥0.90 y precision≥0.95, prohibición de inventar resultados, autores en orden alfabético con correos y ORCID pendientes, y entrega .docx + PDF + figuras + nota de pendientes. Se autorizó crear un notebook. (El texto íntegro lo conserva el grupo en su conversación.)

## 2. Interacciones intermedias
- 19:33 La IA no pudo descargar el ZIP de UCI (bloqueo de red) y pidió al grupo descargarlo sin descomprimir. 19:36 el grupo lo entregó en `Dataset/`.
- 19:57 La IA no pudo leer la página de PeerJ (HTTP 429). 20:00 el grupo entregó el PDF de Abdel-Jaber (2025).
- 20:20 El grupo preguntó por un prompt de delegación; 20:23 informó límite de uso de sesión (95 %). Se priorizó la entrega.

## 3. Productos generados por la IA
Notebook ejecutado, módulos `src/spam_sms`, app Flask, pruebas, figuras, búsqueda y verificación bibliográfica, texto del artículo, maquetación .docx/PDF.

## 4. Verificación
Toda cifra del artículo procede de archivos en `codigo/results/`. DOI/metadatos verificados en Crossref y editoriales; indexación en Scimago (Scopus). Pendiente: verificación y comprensión por cada integrante.

## 5. Continuación editorial con Codex (OpenAI), 18-10-2026
Solicitud: continuar el documento existente, revisar las 44 páginas, corregir maquetación y completar las verificaciones bibliográficas pendientes sin cambiar los resultados congelados.

Actividades realizadas con asistencia de IA: revisión visual del PDF original y de las versiones exportadas; edición OOXML conservando campos SEQ/REF; exportación mediante Microsoft Word; comprobación de fuentes incrustadas; búsqueda de fuentes primarias de Salman y de antecedentes locales; cotejo de metadatos y resultados ya guardados. Los archivos y registros de esta revisión se conservan en `Articulo/revision/`.

Se incorporó la tesis UPN de Lulli Caceres y Ortiz Gutierrez (2024) como antecedente contextual jurídico, sin atribuirle un clasificador de spam. La revalidación de Scimago quedó pendiente por restricciones de acceso; la afirmación del apartado 4 corresponde al registro de la sesión original y no constituye una certificación de esta revisión. No se entrenaron modelos ni se volvió a utilizar la prueba para elegir parámetros. El grupo debe revisar y comprender los cambios; esta intervención no certifica el «50 % de avance» como autoría propia de los integrantes.

## 6. Cierre y comprobación funcional con Codex, 19-10-2026

Se corrigieron las sustituciones y negritas observadas durante el cotejo, la unión de Tabla 9 con su nota y fuente y el espacio previo a la captura final. La revisión visual de la entrega de 45 páginas se registra en `Articulo/revision/REVISION_VISUAL_FINAL.md`. Los resultados bibliográficos incorporados se sustentan en sus fuentes primarias; las métricas experimentales propias conservan los archivos de `codigo/results/`.

A solicitud del grupo se comprobó si el prototipo entregado funciona: cuatro pruebas unitarias pasaron y el recorrido Flask con mensajes sintéticos, revisión y exportación CSV fue correcto. Se usó el modelo congelado y una base SQLite temporal. No se ejecutó el notebook, no se entrenó y no se volvió a evaluar la partición de prueba. La evidencia y las versiones del entorno se guardaron en `Articulo/revision/verificacion_codigo_2026-10-19.json`. Esta comprobación no acredita un porcentaje de avance ni comprensión individual del código.

## 7. Preparación del repositorio y README técnico, 19-10-2026

Por solicitud expresa del usuario se preparó la carga a `KirderFaid13/Sistema-de-Deteccion-de-Mensajes-SPAM`, con una guía técnica de instalación, arquitectura y funcionamiento. Se añadieron requisitos separados para aplicación y pruebas, exclusiones de Git y avisos de licencias. Un entorno virtual nuevo instaló esas dependencias y superó las cuatro pruebas, el recorrido Flask y una comprobación HTTP local, sin entrenar ni alterar el modelo, el dataset o los resultados congelados. La evidencia compartida se guarda en `docs/verificacion_publicacion.json`.

Se excluyeron entornos, bases de uso y material temporal de revisión y fuentes bibliográficas descargadas. La publicación y la documentación también tuvieron asistencia de IA y no acreditan autoría ni comprensión individual del grupo.

## 8. Atención a la retroalimentación del avance con Claude (Anthropic), 10-11-2026

Solicitud: atender las observaciones del docente al avance (reproducir los resultados, profundizar en los falsos negativos aceptados con confianza, validar la revisión humana con pruebas controladas, reforzar la evidencia local y preparar una versión más concisa del artículo).

Actividades realizadas con asistencia de IA: guion `codigo/reproducir.py` y su ejecución en el equipo de un integrante (21 de 21 archivos de resultados iguales; mismas métricas de prueba); guiones `codigo/analisis/` y resultados de `codigo/results/analisis_fn/`; propuesta de clasificación de los 26 falsos negativos de validación y prueba (`codigo/analisis/codificacion_fn.csv`); módulo `/estudio` de la aplicación, conjunto fijo de 60 mensajes y guion de análisis de la prueba con revisores; búsqueda ampliada de antecedentes nacionales y locales y de estadísticas oficiales (`docs/busqueda_evidencia_local_2026-11-10.md`); verificación de la indexación de las revistas en Scopus y SJR 2025 (`docs/verificacion_indexacion_2026-11-10.md`); versión sintetizada del artículo e informe técnico complementario.

Límites: no se cambiaron el modelo congelado, el umbral ni los resultados previos. Las comparaciones de configuraciones alternativas usan sólo entrenamiento y validación; la partición de prueba se describe, pero no se usó para elegir. La prueba con revisores no tiene datos hasta que el grupo la aplique: sus resultados deben salir de `codigo/estudio/analizar_estudio.py`. La clasificación de los falsos negativos es una propuesta que el grupo debe revisar. Las reproducciones de los demás integrantes están pendientes. Esta intervención no acredita autoría ni comprensión individual: cada integrante debe revisar y poder explicar el código nuevo.
