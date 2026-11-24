# Verificación de indexación Scopus y cuartil SJR de las revistas citadas

**Fecha de consulta:** 10-11-2026
**Edición SJR consultada:** SJR 2025 (la más reciente disponible; publicada en 2026)
**Revistas revisadas:** 11 (el encargo menciona doce artículos, pero la lista recibida contiene once revistas)

## Cómo se verificó (leer antes de usar la tabla)

| Vía | Estado hoy | Qué aporta |
|---|---|---|
| Ficha HTML de Scimago (`journalsearch.php`) | **No cargó.** HTTP 403 con verificación anti-bots de Cloudflare, tanto por petición directa como en navegador. No se intentó eludirla. | Nada (no se pudo leer ninguna ficha completa). |
| Widget oficial de Scimago (`https://www.scimagojr.com/journal_img.php?id=<SID>`) | **Cargó para las 11.** Es la imagen que el propio Scimago sirve para incrustar en sitios de revistas. | Título, **mejor cuartil**, categoría de ese mejor cuartil, año SJR y valor SJR (2 decimales). |
| Scopus Preview (`https://www.scopus.com/sourceid/<SID>`) | **Cargó para las 11** (sin iniciar sesión). | Título, ISSN/E-ISSN, editorial, años de cobertura en Scopus, SJR 2025 (3 decimales), CiteScore 2025 y percentiles por categoría. |
| OpenAlex API (`api.openalex.org/sources?filter=issn:…`) | Cargó. | País de la revista/editorial (dato **no** tomado de Scimago; puede diferir del país que muestra Scimago). |
| ISSN Portal, página de MDPI | No cargaron (403 / anti-bots). | Nada. |

Control cruzado: el SJR 2025 del widget de Scimago coincide, redondeado, con el SJR 2025 de Scopus en las 11 revistas, lo que confirma que cada identificador (SID) corresponde a la revista e ISSN correctos.

Leyenda de estado:
- **VS-w** = verificado en Scimago solo mediante el widget oficial (ficha HTML no accesible hoy).
- **VA-Scopus** = verificado en fuente alternativa: Scopus Preview.
- **NV** = no verificable hoy.

## Tabla de resultados

| # | Revista (título en Scimago/Scopus) | ISSN (Scopus) | Editorial (Scopus) | País (OpenAlex, no Scimago) | Cobertura Scopus | SJR 2025 (Scopus) | Mejor cuartil SJR 2025 y categoría (widget Scimago) | Cuartil declarado | ¿Coincide? | Estado | ¿Descontinuada? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Sensors | E-ISSN 1424-8220 | MDPI | CH (Suiza) | 2001–2026 | 0.802 | **Q1** – Analytical Chemistry | Q1 | Sí | VS-w + VA-Scopus | No (activa) |
| 2 | IEEE Access | E-ISSN 2169-3536 | IEEE | US (EE. UU.) | 2013–2026 | 0.884 | **Q1** – Computer Science (miscellaneous) | Q1 | Sí | VS-w + VA-Scopus | No (activa) |
| 3 | Applied Sciences (Switzerland) | E-ISSN 2076-3417 | MDPI | CH (Suiza) | 2011–2026 | 0.555 | **Q2** – Computer Science Applications | Q2 | Sí | VS-w + VA-Scopus | No (activa) |
| 4 | Applied Computational Intelligence and Soft Computing | ISSN 1687-9724 / E-ISSN 1687-9732 | John Wiley & Sons (antes Hindawi) | GB (Reino Unido) | 2016–2026 | 0.791 | **Q1** – Civil and Structural Engineering | Q1 | Sí, con reserva (ver nota A) | VS-w + VA-Scopus | No (activa) |
| 5 | PeerJ Computer Science | E-ISSN 2376-5992 | PeerJ Inc. | US (EE. UU.) | 2015–2026 | 0.618 | **Q2** – Computer Science (miscellaneous) | Q2 | Sí (ver nota B) | VS-w + VA-Scopus | No (activa) |
| 6 | Electronics (Switzerland) | E-ISSN 2079-9292 | MDPI | CH (Suiza) | 2012–2026 | 0.623 | **Q2** – Computer Networks and Communications | Q2 | Sí | VS-w + VA-Scopus | No (activa) |
| 7 | Systems | E-ISSN 2079-8954 | MDPI | CH (Suiza) | 2013–2026 | 0.643 | **Q2** – Computer Networks and Communications | Q2 | Sí | VS-w + VA-Scopus | No (activa) |
| 8 | IAES International Journal of Artificial Intelligence | ISSN 2089-4872 / E-ISSN 2252-8938 | Institute of Advanced Engineering and Science | ID (Indonesia) | 2018–2026 | 0.247 | **Q3** – Artificial Intelligence | Q3 | Sí | VS-w + VA-Scopus | No (activa) |
| 9 | Machine Learning | ISSN 0885-6125 / E-ISSN 1573-0565 | Springer Nature | NL (Países Bajos) | 1986–2026 | 1.027 | **Q1** – Artificial Intelligence | Q1 | Sí | VS-w + VA-Scopus | No (activa) |
| 10 | Artificial Intelligence Review | ISSN 0269-2821 / E-ISSN 1573-7462 | Springer Nature | GB (Reino Unido) | 1986–2026 | 3.638 | **Q1** – Artificial Intelligence | Q1 | Sí | VS-w + VA-Scopus | No (activa) |
| 11 | Patterns | E-ISSN 2666-3899 | Elsevier (Cell Press) | US (EE. UU.) | 2020–2026 | 2.066 | **Q1** – Multidisciplinary | Q1 | Sí | VS-w + VA-Scopus | No (activa) |

## URL de evidencia por revista

La «URL de ficha Scimago» sigue el patrón estándar de Scimago con el identificador de fuente (SID). Solo las de IEEE Access y PeerJ Computer Science aparecieron tal cual en resultados de buscador; las demás se construyeron con el mismo patrón a partir del SID confirmado y **no pudieron abrirse hoy** (403). Las URL de widget y de Scopus sí se abrieron.

| # | Revista | SID | URL de ficha Scimago (no abierta hoy) | Widget Scimago (abierto) | Scopus Preview (abierto) |
|---|---|---|---|---|---|
| 1 | Sensors | 130124 | https://www.scimagojr.com/journalsearch.php?q=130124&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=130124 | https://www.scopus.com/sourceid/130124 |
| 2 | IEEE Access | 21100374601 | https://www.scimagojr.com/journalsearch.php?q=21100374601&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21100374601 | https://www.scopus.com/sourceid/21100374601 |
| 3 | Applied Sciences (Switzerland) | 21100829268 | https://www.scimagojr.com/journalsearch.php?q=21100829268&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21100829268 | https://www.scopus.com/sourceid/21100829268 |
| 4 | Applied Computational Intelligence and Soft Computing | 21100821307 | https://www.scimagojr.com/journalsearch.php?q=21100821307&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21100821307 | https://www.scopus.com/sourceid/21100821307 |
| 5 | PeerJ Computer Science | 21100830173 | https://www.scimagojr.com/journalsearch.php?q=21100830173&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21100830173 | https://www.scopus.com/sourceid/21100830173 |
| 6 | Electronics (Switzerland) | 21100829272 | https://www.scimagojr.com/journalsearch.php?q=21100829272&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21100829272 | https://www.scopus.com/sourceid/21100829272 |
| 7 | Systems | 21101020135 | https://www.scimagojr.com/journalsearch.php?q=21101020135&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21101020135 | https://www.scopus.com/sourceid/21101020135 |
| 8 | IAES International Journal of Artificial Intelligence | 21100901206 | https://www.scimagojr.com/journalsearch.php?q=21100901206&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21100901206 | https://www.scopus.com/sourceid/21100901206 |
| 9 | Machine Learning | 24775 | https://www.scimagojr.com/journalsearch.php?q=24775&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=24775 | https://www.scopus.com/sourceid/24775 |
| 10 | Artificial Intelligence Review | 24141 | https://www.scimagojr.com/journalsearch.php?q=24141&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=24141 | https://www.scopus.com/sourceid/24141 |
| 11 | Patterns | 21101028388 | https://www.scimagojr.com/journalsearch.php?q=21101028388&tip=sid&clean=0 | https://www.scimagojr.com/journal_img.php?id=21101028388 | https://www.scopus.com/sourceid/21101028388 |

## Datos complementarios de Scopus Preview (CiteScore 2025)

| # | Revista | CiteScore 2025 | Mejor percentil CiteScore 2025 (categoría) | Percentil en la categoría más afín al artículo |
|---|---|---|---|---|
| 1 | Sensors | 9.4 | 91 (Instrumentation) | 83 (Information Systems) |
| 2 | IEEE Access | 9.3 | 91 (General Engineering) | 84 (General Computer Science) |
| 3 | Applied Sciences (Switzerland) | 6.1 | 82 (Fluid Flow and Transfer Processes) | 70 (Computer Science Applications) |
| 4 | Applied Computational Intelligence and Soft Computing | 9.4 | 92 (Computational Mechanics) | 81 (Artificial Intelligence) |
| 5 | PeerJ Computer Science | 6.1 | 71 (General Computer Science) | 71 (General Computer Science) |
| 6 | Electronics (Switzerland) | 7.0 | 83 (Signal Processing) | 78 (Computer Networks and Communications) |
| 7 | Systems | 5.4 | 80 (Modeling and Simulation) | 70 (Computer Networks and Communications) |
| 8 | IAES International Journal of Artificial Intelligence | 2.9 | 63 (Information Systems and Management) | 49 (Artificial Intelligence) |
| 9 | Machine Learning | 7.5 | 77 (Software) | 75 (Artificial Intelligence) |
| 10 | Artificial Intelligence Review | 36.1 | 99 (Linguistics and Language) | 98 (Artificial Intelligence) |
| 11 | Patterns | 18.0 | 95 (Multidisciplinary) | 95 (Multidisciplinary) |

Nota: el percentil CiteScore es una métrica de Scopus distinta del cuartil SJR de Scimago; no son intercambiables.

## Notas y reservas

- **Nota A (revista 4).** El Q1 de *Applied Computational Intelligence and Soft Computing* es su **mejor cuartil** y Scimago lo asigna a la categoría *Civil and Structural Engineering*, no a *Artificial Intelligence*. El widget solo muestra la mejor categoría, así que el cuartil SJR en las categorías de computación/IA **no es verificable hoy**. Si el artículo afirma «Q1» sin especificar categoría, es correcto; si afirma «Q1 en Inteligencia Artificial», queda sin respaldo. Además, la editorial vigente en Scopus es John Wiley & Sons (la revista era de Hindawi).
- **Nota B (revista 5).** *PeerJ Computer Science* es Q2 en SJR 2025, igual que lo declarado. Un fragmento de buscador de la ficha de Scimago indica que fue Q1 en 2023 y 2024; ese dato histórico no pudo confirmarse directamente hoy.
- **Limitación del widget.** Muestra un único cuartil (el mejor) y una única categoría. No permite ver los cuartiles de las demás categorías ni la serie histórica, ni el país que registra Scimago.
- **País.** Proviene de OpenAlex, no de Scimago. Scimago puede mostrar otro país para algunas revistas (por ejemplo, las de Springer o la número 4).
- **Descontinuación.** Las 11 fichas de Scopus Preview muestran cobertura vigente «hasta 2026» y ninguna muestra aviso de cobertura descontinuada. No se descargó la lista oficial de títulos descontinuados de Scopus (archivo Excel).
- **Cuartil por año.** Lo verificado corresponde a SJR 2025. No se verificó el cuartil del año de publicación de cada artículo citado.

## Conclusión

- 11 de 11 revistas están indexadas y activas en Scopus (verificado en Scopus Preview).
- 11 de 11 tienen su mejor cuartil SJR 2025 confirmado en Scimago mediante el widget oficial; la ficha HTML completa no fue accesible.
- Ningún cuartil difiere del declarado. Única reserva: la categoría del Q1 de la revista 4 (nota A).
- Ninguna revista aparece descontinuada.
