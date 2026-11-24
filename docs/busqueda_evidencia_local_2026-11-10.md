# Evidencia local y nacional sobre detección de spam SMS / smishing (Perú, La Libertad)

Fecha de la búsqueda: 10-11-2026. Ventana temporal objetivo: noviembre de 2021 a 2026.
Alcance: solo lectura en la web. No se llenaron formularios ni se enviaron datos personales.

## 0. Cómo leer este informe

Cada hallazgo lleva un nivel de verificación:

| Nivel | Significado |
|---|---|
| **A** | Verificado en fuente primaria: se obtuvo el PDF o texto completo y se leyó el pasaje, tabla o artículo citado. |
| **B** | Verificado en el registro del repositorio o en la página de la fuente (metadatos y resumen leídos), pero **sin abrir el texto completo**. Los datos numéricos provienen del resumen. |
| **C** | Solo visto en un listado o resultado de búsqueda. No usar como cita sin abrirlo antes. |
| **D** | No accesible (sitio caído, bloqueo anti-bots, error 403/404). |

Advertencias generales:

- Las páginas HTML (notas de El Peruano, Andina, RPP, registros de repositorios) se leyeron con una herramienta que extrae y resume el contenido. Para esas fuentes conviene que el grupo abra la URL y confirme la cifra textual antes de citarla. Los PDF marcados con nivel A sí se leyeron directamente en texto completo.
- Los números de página indicados son los impresos en el documento cuando existen; si no, se indica «pág. del PDF».
- No se incluyen DNI ni otros datos personales que aparecen en los metadatos de los repositorios.

---

## 1. Resumen ejecutivo

1. **Sí existe un antecedente local directo de SMS** dentro de la ventana: Condori Coaquira e Ildefonso Paucar (2025), Universidad César Vallejo, sede Trujillo. Construyen un corpus propio de 8 457 SMS peruanos en español (3 604 spam, 4 853 legítimos) y comparan modelos; el mejor modelo tradicional es **TF-IDF + SVM lineal** (F1 = 0,9469), superado por BETO afinado (F1 ≈ 0,97). Nivel A.
2. **Antecedente local indirecto (phishing web con ML)**: Soto Calderon y Tirado Rios (2025), maestría de la UPN, sede Trujillo El Molino. XGBoost, SVM y AdaBoost sobre 11 054 URL; XGBoost obtiene 96,92 % de exactitud. Nivel A, con una reserva metodológica (ver 2.2).
3. **Antecedentes nacionales directos de SMS**: Salinas Bolaños (2024, ESAN; 1 740 SMS peruanos, RNN, exactitud 85,62 %) y Flores Barrios (2022, UPN Lima; app Android basada en reglas, TPR 90 % sobre 20 SMS), ambos nivel A. Mayaute Málaga (2025, UTP, app «Drako») y Vasquez Chuñe (2025, USS) quedan en nivel B porque sus repositorios bloquean el acceso automatizado.
4. **Estadística oficial del canal SMS**: no se encontró ninguna cifra oficial peruana de denuncias o fraudes **desagregada por canal SMS**. Lo más cercano y verificable es la serie de **tráfico de SMS de PUNKU-OSIPTEL** citada por el MTC (de 15 229 millones en 2016 a 4 759 millones en 2023) y las denuncias por modalidad de la DIVINDAT 2022, que no separan el smishing. Nivel A sobre el documento del MTC.
5. **Marco normativo nuevo (2026)**: Decreto Legislativo N.° 1723 (07-02-2026) sobre numeración y trazabilidad de llamadas y mensajes de texto, y Decreto Supremo N.° 018-2026-MTC (15-09-2026) que reserva la serie 500 para llamadas y SMS comerciales. Ambos nivel A.
6. **Corpus público en español**: la tesis de la UCV declara un repositorio público con su corpus, pero la URL devolvió error 404 el 10-11-2026. La alternativa accesible es una traducción automática del SMS Spam Collection (no es español nativo).

---

## 2. Evidencia LOCAL (Trujillo / La Libertad)

### 2.1 Condori Coaquira e Ildefonso Paucar (2025) — evidencia local DIRECTA de SMS — Nivel A

| Campo | Dato |
|---|---|
| Autores | Condori Coaquira, Angel Rosendo; Ildefonso Paucar, Johan Alexander |
| Año | 2025 (carátula «Trujillo - Perú 2025»; declaratoria del asesor fechada 29-11-2025; ingreso al repositorio 15-04-2026) |
| Título exacto | Diseño de un modelo basado en aprendizaje automático para la detección de mensajes maliciosos en español, Perú 2025 |
| Institución | Universidad César Vallejo, Programa de Segunda Especialidad en Ciberseguridad, sede Trujillo (modalidad a distancia) |
| Tipo | Trabajo académico para título de segunda especialidad (no es tesis de pregrado ni de maestría) |
| Asesor | Gutierrez Muñoz, Miguel Angel |
| URL | https://hdl.handle.net/20.500.12692/185506 — registro completo: https://repositorio.ucv.edu.pe/handle/20.500.12692/185506?show=full |
| PDF leído | https://repositorio.ucv.edu.pe/bitstream/handle/20.500.12692/185506/S_Condori_CAR-Ildefonso_PJA-SD.pdf?sequence=1&isAllowed=y |
| Objetivo | Diseñar un modelo de aprendizaje automático para detectar mensajes maliciosos en español con F1-score ≥ 0,85 |
| Metodología | Investigación aplicada, cuantitativa. Preprocesamiento con NLTK, extracción con TF, TF-IDF, FastText y BETO, balanceo con SMOTE, división 80 % / 20 % aleatoria |
| Población | Todos los SMS en español relevantes para Perú 2025, maliciosos y no maliciosos (universo hipotético) (pág. 10) |
| Muestra | Muestreo no probabilístico por conveniencia. Se recolectaron 34 267 SMS (exportados en XML desde 24 celulares, más 500 de páginas web de ciberseguridad; Tabla 1, pág. 13). Tras depuración quedan **8 457 SMS**: 3 604 spam (42,62 %) y 4 853 legítimos (57,38 %) (Tabla 3, pág. 24) |
| Etiquetado | «Manual asistido», con criterios de contenido (palabras clave, enlaces), remitente y frecuencia (pág. 14) |
| Algoritmos | Árbol de decisión, Random Forest, Extra Trees, regresión logística, SVM, Naive Bayes, SGD; ensambles Voting y Stacking; MLP; LSTM bidireccional; BETO |
| Resultados | Tabla 4 (pág. 27), TF-IDF + SVM: exactitud 0,9545, precisión 0,9436, recall 0,9501, F1 0,9469. Tabla 5 (pág. 28), Voting (SVM+RF+LR): exactitud 0,9563, F1 0,9486. Tabla 7 (pág. 31), BETO afinado: exactitud global 0,97. Tabla 8 (pág. 34), rangos de F1: ML tradicional 0,90–0,94; ensambles 0,94–0,95; transformers 0,96–0,97 |
| Relación con spam SMS | Directa: mismo problema, mismo idioma y mismo país; el mejor modelo clásico coincide con el enfoque TF-IDF + SVM del artículo |

Precisiones para citarlo con cuidado:

- En la Tabla 4 el texto extraído no deja claro a simple vista qué bloque es TF y cuál TF-IDF. El bloque inferior se atribuye a TF-IDF porque el párrafo que antecede a la tabla cita «95.01% y F1 Score del 94.69%», que coincide con la fila SVM de ese bloque. Conviene confirmarlo visualmente en el PDF (pág. 27).
- El trabajo es «local» por la sede que otorga el título (Trujillo). El texto describe los mensajes como «del entorno peruano»; **no afirma** que se hayan recolectado en Trujillo o La Libertad.
- Hay una discrepancia interna menor: 8 458 mensajes en un párrafo de la pág. 23 frente a 8 457 en el resto.
- No incluye revisión humana de predicciones inciertas; eso sigue siendo aporte diferencial del artículo del grupo.
- El propio trabajo cita como antecedentes a Castañeda Chávez (2013, UNT) y a Salinas Bolaños (2024, ESAN).

### 2.2 Soto Calderon y Tirado Rios (2025) — evidencia local INDIRECTA (phishing en páginas web) — Nivel A

| Campo | Dato |
|---|---|
| Autores | Soto Calderon, Jose Luis; Tirado Rios, Ronal Jimmy |
| Año | Fecha de publicación en repositorio: 14-05-2025. La carátula dice «Perú 2024» y la cita sugerida por el repositorio usa (2024). Elegir un criterio y mantenerlo |
| Título exacto | Implementación de un método de clasificación de Machine Learning para detectar páginas web de tipo phishing dentro de un entorno del Programa Nacional de Asistencia Social |
| Institución | Universidad Privada del Norte, Escuela de Posgrado y Estudios Continuos, sede Trujillo El Molino |
| Tipo | Tesis de maestría (Ingeniería de Sistemas con mención en Gerencia de Sistemas de Información) |
| Asesor | Mendoza de los Santos, Alberto Carlos |
| URL | https://hdl.handle.net/11537/44113 |
| PDF leído | https://repositorio.upn.edu.pe/backend/api/core/bitstreams/202cb20c-8630-4382-ba78-db7fb2cafeaa/content |
| Objetivo | Implementar un método de clasificación con ML para detectar páginas web de phishing que afectan al programa social |
| Metodología | Aplicada; 30 atributos extraídos por URL; división 80/20; validación cruzada k = 5 |
| Población | Páginas web legítimas o de phishing; se declara infinita (pág. 21) |
| Muestra | 11 054 registros (56 % legítimas, 44 % phishing), con fuente PhishTank (pág. 37). En la pág. 21 se escribe 11 055 |
| Algoritmos | AdaBoost, SVM, XGBoost |
| Resultados | Tablas 4–6 (págs. 34–35) y 11–13 (págs. 46–47). AdaBoost: exactitud 93,80 %, precisión 93,72 %, sensibilidad 93,36 %, F1 94,52. SVM: 95,12 %, 95,25 %, 94,13 %, F1 95,70. XGBoost: 96,92 %, 98,71 %, 96,42 %, F1 97,27 |
| Relación con spam SMS | Indirecta: mismo tipo de amenaza (phishing) y mismo enfoque supervisado con SVM, pero sobre URL y no sobre texto de SMS. Menciona el smishing solo en el marco teórico |

Reserva metodológica (observación propia al leer el código transcrito en las págs. 46–47): la línea que imprime «Precisión» usa `categorizador.score(atributos_train, etiquetas_train)`, es decir, la exactitud sobre el conjunto de entrenamiento, no la precisión sobre prueba. Además, `recall_score` y `f1_score` reciben los argumentos en orden (predicción, real). Si se cita esta tesis, conviene reportar la exactitud y señalar que las demás métricas son «las reportadas por los autores».

### 2.3 Cordova Gonzalez (2024) — evidencia local INDIRECTA (clasificación de texto) — Nivel B

- Cordova Gonzalez, Kevin Fernando (2024). *Machine learning para la identificación de noticias falsas en sitios web de noticias, Trujillo, 2024*. Tesis de pregrado (Ingeniero de Sistemas), Universidad César Vallejo, sede Trujillo. Asesor: Cieza Mostacero, Segundo Edwin.
- URL: https://hdl.handle.net/20.500.12692/195199
- Según el resumen: diseño experimental puro, 60 evaluaciones (30 grupo control, 30 experimental); indicadores de tiempo de detección, tasa de error y nivel de precisión; diferencias significativas (p < 0,001).
- Algoritmos, conjunto de datos y métricas de clasificación: **no reportados en el resumen; texto completo no verificado**.
- Relación: clasificación supervisada de textos en español hecha en Trujillo; no trata SMS.

### 2.4 Che León Antinori (2024) — contexto local, no es detección — Nivel A

- Che León Antinori, V. H. (2024). Influencia de los Delitos Cibernéticos Económicos en Perú. *SCIÉNDO*, 27(4), 415–418. https://doi.org/10.17268/sciendo.2024.071 — Universidad Nacional de Trujillo.
- PDF leído: https://revistas.unitru.edu.pe/index.php/SCIENDO/article/download/6095/6196
- Estudio cualitativo (entrevistas a abogados, fiscales y expertos; revisión documental). Señala que phishing, vishing y smishing están en aumento.
- **No usar sus cifras como estadística oficial**: atribuye datos al INEI, la PNP y el BCRP sin que se haya podido verificar esas fuentes, y contiene una inconsistencia interna (más de 30 000 casos de fraude electrónico en el primer trimestre de 2024 frente a 26 500 casos estimados para todo 2024). Sirve como cita de contexto de autor local, no como dato.

### 2.5 Huamanchumo Trujillo et al. (2024) — posible evidencia local indirecta — Nivel B

- Huamanchumo Trujillo, F. G., Campos Gamarra, A. R., Guevara Saldaña, R. A., y Mendoza De Los Santos, A. C. (2024). Implementation of an intelligent antimalware system for the detection of malicious links in QR codes. *Ingeniería Investiga*, 6. Universidad Privada de Tacna (editora de la revista).
- URL del artículo: https://revistas.upt.edu.pe/ojs/index.php/ingenieria/article/view/1078 (**no accesible** el 10-11-2026: conexión rechazada). Registro leído: https://alicia.concytec.gob.pe/vufind/Record/REVUPT_e610a9482de251d56a4f260eb30f5b9f
- Según el resumen: sistema con ML y la API de VirusTotal para clasificar enlaces en códigos QR («quishing»); 100 códigos (50 seguros, 50 maliciosos); exactitud 100 %, sensibilidad 95 %, tiempo medio 48,95 ms.
- **Afiliación de los autores no verificada**. El último autor coincide con el asesor de la tesis de la UPN Trujillo (2.2), pero no se pudo abrir el PDF para confirmar a qué universidad pertenecen. No presentarlo como «artículo de Trujillo» sin comprobarlo.

### 2.6 Cornejo Adrianzén y Requenes Querevalu (2026) — evidencia regional indirecta (PLN) — Nivel B

- *Implementación y Evaluación de un Modelo de Clasificación de Palabras Ofensivas para Identificar Casos de Violencia Verbal contra Mujeres en Casos Piloto Simulados en el año 2025*. Tesis de pregrado, Universidad Privada Antenor Orrego. Asesor: Abanto Cabrera, Heber Gerson.
- URL: https://hdl.handle.net/20.500.12759/101452 — registro leído: https://alicia.concytec.gob.pe/vufind/Record/UPAO_4faefa8e2f8199b1db0685b69fe4b3bd
- Según el resumen: ajuste fino de BETO; 90 simulaciones; precisión 88 %, recall 52 %, F1 65 %.
- Sede (Trujillo o Piura): **no verificada**. El repositorio de la UPAO bloquea el acceso automatizado.
- Relación: clasificación de textos cortos en español con modelos de lenguaje; no trata spam.

### 2.7 Antecedentes locales fuera de la ventana (solo para contexto histórico)

Junto con Castañeda Chávez (2013), que el grupo ya tiene, la UNT registra dos tesis sobre mensajes de texto, ambas anteriores a noviembre de 2021 (nivel B, registro de ALICIA):

- Argomedo Pflücker, K. C., y Cóndor Ruiz, A. T. (2015). *Diseño de un sistema inteligente utilizando procesamiento de lenguaje natural (pln) para el reconocimiento de mensajes extorsivos*. Tesis de grado, UNT. https://hdl.handle.net/20.500.14414/7446
- Rojas Alarcon, J. U., y Toribio Esquivel, J. P. (2019). *Software basado en redes neuronales artificiales para la autocorrección de mensajes de texto en el proyecto PIC-13 2013 de la Universidad Nacional de Trujillo*. Tesis de grado, UNT. https://hdl.handle.net/20.500.14414/12399

Permiten afirmar que en Trujillo existe una línea previa sobre análisis automático de mensajes de texto (2013–2019), y que dentro de la ventana 2021–2026 la UNT no registra trabajos de detección de spam SMS.

### 2.8 Tesis locales de contexto jurídico o preventivo — Nivel C (solo listado)

No son de detección con ML. Podrían aportar cifras locales, pero no se abrieron.

| Autor(es) y año | Título | Institución y sede | Identificador |
|---|---|---|---|
| Acevedo Cerna y Cubas Chavarry (2024) | El delito de phishing como fenómeno criminal y la vulneración del patrimonio a las víctimas durante el año 2023 | UPN, Trujillo El Molino (Derecho) | https://hdl.handle.net/11537/41784 |
| Angeles Quiñones (2025) | Implementación del programa «Prevención al delito cibernético» en usuarios de la empresa Bizpro Solutions SAC en Trujillo, 2024 | UPN, Trujillo El Molino | https://hdl.handle.net/11537/41219 |
| Valentín Horna (2022) | Factores de incidencia en el archivo de las investigaciones preliminares por delito de fraude informático, Trujillo 2021. Mecanismos de mejora | UCV (maestría) | ALICIA: UCVV_399c4017a47bd3c2ca97ae684ed9… |
| Cabrera Sirlupu (2023) | Aplicación de la ley 30096 y el archivamiento fiscal en los delitos de fraude informático en la ciudad de Trujillo 2023 | UCV | ALICIA: UCVV_a3d66e2827b66149c169437632a0451d |
| Flores Mori (2023) | Incremento de los delitos informáticos a consecuencia de la pandemia del Covid-19 en la ciudad de Trujillo entre los años 2020-2021 | UCV | ALICIA: UCVV_54965f8343e940ea90e5b4d34808db29 |
| Rodriguez Taboada (2024) | Importancia de determinar estándares para el acopio y actuación del material probatorio en los casos de ciberdelincuencia, Trujillo - 2024 | UCV (maestría) | ALICIA: UCVV_609f4013f6f2da0e6e4081ef029… |
| Cedrón Juárez (2026) | Responsabilidad penal en las sociedades anónimas por el delito de fraude informático en aplicación de la Ley 30096 en Trujillo 2024 | U. Católica de Trujillo | handle 20.500.14520/13378 |

Los identificadores de ALICIA terminados en «…» quedaron truncados en el listado; buscar por título en https://alicia.concytec.gob.pe.

### 2.9 Hecho local documentado en prensa oficial — Nivel B

- El Peruano (14-10-2024, 14:52). «Logran prisión preventiva para presuntos integrantes de banda que estafaban mediante 'vishing' y 'smishing'». https://www.elperuano.pe/noticia/255358-logran-prision-preventiva-para-presuntos-integrantes-de-banda-que-estafaban-mediante-vishing-y-smishing
- Fiscalía Provincial Transitoria Especializada en Ciberdelincuencia de La Libertad. Hecho del 24-09-2024; perjuicio de S/ 60 569 a un ciudadano; 15 meses de prisión preventiva para dos investigados; cuatro detenidos en Lima y Trujillo.
- Posible duplicado: el grupo ya tiene «noticias de El Peruano 2024»; verificar si es la misma nota.
- La misma causa aparece mencionada en Andina (19-08-2025), ver sección 4.

---

## 3. Evidencia NACIONAL (spam SMS / smishing)

### 3.1 Salinas Bolaños (2024, ESAN) — Nivel A

| Campo | Dato |
|---|---|
| Autor | Salinas Bolaños, Yair Andrey |
| Título exacto | Propuesta de modelo predictivo para la detección de fraude en mensajes de texto mediante el uso de Redes Neuronales Recurrentes |
| Institución y tipo | Universidad ESAN, Facultad de Ingeniería. Tesis de pregrado (Ingeniero de Tecnologías de Información y Sistemas). Asesor: Mamani Ticona, Wilfredo |
| URL | https://hdl.handle.net/20.500.12640/4287 |
| PDF leído | https://repositorio.esan.edu.pe/server/api/core/bitstreams/0d0c534f-e869-4b17-8d94-ad95a6f121f5/content (301 págs.) |
| Objetivo | Encontrar el mejor clasificador de fraude en mensajes de texto en el contexto peruano |
| Población | Todos los mensajes de texto que circulan por las redes móviles en territorio peruano (Tabla 2, pág. 113) |
| Muestra | Por conveniencia, 4 475 mensajes (Tabla 2, pág. 113). Composición (págs. 164 y 176–178): 1 740 mensajes peruanos extraídos de 527 imágenes (440 compartidas por 70 voluntarios y 87 por web scraping), etiquetados manualmente con 12 criterios y validados por una experta en fraude; 1 690 del «Dataset_5971» (Mishra y Soni) y 1 045 de «Smishtank Datasets I», ambos en inglés y traducidos con GoogleTranslator |
| Algoritmos | RNN, LSTM, GRU e híbridos con CNN; vectorización Word2Vec y FastText |
| Resultados | Tabla 31 (pág. 259): RNN de 3 capas (200, 160, 1) con FastText-NewL de 300 dimensiones: exactitud 85,62 %, precisión 84,49 %, recall 88,77 %, F1 86,57 %, AUC 93,14 % |
| Relación con spam SMS | Directa. Es el antecedente nacional más sólido con SMS peruanos reales |

Dato útil para la justificación: la tesis afirma que se recurrió a datos en inglés «debido a la escaza data pública en español» (pág. 176). Disponibilidad pública de su dataset: no reportada.

### 3.2 Flores Barrios (2022, UPN Lima) — Nivel A

| Campo | Dato |
|---|---|
| Autor | Flores Barrios, Pablo Fernando |
| Título exacto | Desarrollo de aplicativo móvil para la detección de phishing en mensajes de texto (SMS) de dispositivos con sistema operativo Android |
| Institución y tipo | Universidad Privada del Norte, Facultad de Ingeniería, sede Breña (Lima). Tesis de pregrado (Ingeniero de Sistemas Computacionales). Asesor: Guevara Jiménez, Jorge Alfredo. Publicada el 29-09-2022 |
| URL | https://hdl.handle.net/11537/31675 |
| PDF leído | https://repositorio.upn.edu.pe/backend/api/core/bitstreams/10de2d93-36c3-48e5-b70d-cd3ff7b372d0/content (150 págs.) |
| Objetivo | Desarrollar un aplicativo móvil que mejore la detección de phishing en SMS en Android |
| Metodología | Explicativa, cuasi experimental, cuantitativa, aplicada; desarrollo incremental; pre-test y post-test |
| Muestra | 20 SMS (50 % con dominios maliciosos de PhishTank y 50 % de autoría propia con URL sospechosas) y 5 profesionales en TIC para los requerimientos (págs. 67–68, Tabla 12) |
| Algoritmos | **No usa aprendizaje automático**. Dos reglas: comparación con una base cargada de PhishTank y marcado de enlaces que empiezan con `http://` (pág. 66) |
| Resultados | TPR de detección: 35 % (7 de 20) en pre-test y 90 % (18 de 20) en post-test (Tabla 19, págs. 79–80). Mismo resultado para generación de alertas (Tabla 20, pág. 82) |
| Relación con spam SMS | Directa en el canal, distinta en el método. Es además un antecedente de la misma universidad del grupo. Sirve para contrastar reglas fijas frente a un clasificador supervisado |

### 3.3 Mayaute Málaga (2025, UTP) — Nivel B

- Mayaute Málaga, Luis Enrique (2025). *Eficiencia del aplicativo 'DRAKO' con tecnología machine learning para la detección automatizada de smishing bancario en dispositivos android en Perú*. Tesis de pregrado, Universidad Tecnológica del Perú. Asesora: Arana Castañeda, Edith.
- URL: https://hdl.handle.net/20.500.12867/13659 — registro leído: https://alicia.concytec.gob.pe/vufind/Record/UTPD_51e92bcdcf11d82f992824fc0fa44104
- Según el resumen: app Android «Drako» con ML; 17 entidades bancarias registradas en la SBS; 128 mensajes de texto; «100 % de efectividad» en la identificación y notificación.
- Algoritmo concreto, partición de datos y tabla de resultados: **no verificado** (el repositorio de la UTP presenta un control anti-bots; no se abrió el PDF).
- Reserva: un 100 % sobre 128 mensajes debe citarse con cautela y solo como lo reporta el autor.

### 3.4 Vasquez Chuñe (2025, USS, Lambayeque) — Nivel B

- Vasquez Chuñe, Edwar Jeffery Kler (2025). *Evaluación de Técnicas de Minería de texto para identificación de mensajes Spam en la mensajería SMS de correo electrónico*. Tesis de pregrado, Universidad Señor de Sipán. Asesor: Atalaya Urrutia, Carlos William.
- URL: https://hdl.handle.net/20.500.12802/14817 — registro leído: https://alicia.concytec.gob.pe/vufind/Record/USSS_3081229e0fbc7b87a0e7c50f6c87bedd
- Según el resumen: cuantitativa, cuasi experimental; «tasa de precisión del 97.8% al utilizar Naive Bayes para filtrar mensajes SMS».
- Conjunto de datos, tamaño de muestra y demás algoritmos: **no reportados en el resumen; texto completo no verificado** (control anti-bots).
- Reserva: el título mezcla «SMS» y «correo electrónico» y el resumen también; hay que abrir el PDF para saber qué datos usó en realidad.
- Es la evidencia de la macrorregión norte más cercana a La Libertad fuera de Trujillo.

### 3.5 Meneses-Claudio et al. (2022) — Nivel A

- Lee Huamaní, E., Meneses-Claudio, B., Velarde-Molina, J. F., Mirji, H., y Bhavsar, D. N. (2022). Development of Mobile Application that Detects Phishing Messages to Decrease the Percentage of Data Theft during the COVID-19 Pandemic. *International Journal on Recent and Innovation Trends in Computing and Communication*, 10(10), 45–51. https://doi.org/10.17762/ijritcc.v10i10.5733
- Afiliaciones peruanas según los metadatos de la revista: Universidad de Ciencias y Humanidades (Lima), Universidad Tecnológica del Perú (Lima), Escuela de Posgrado Newman (Tacna). ALICIA lo lista con Meneses Claudio como primer autor; la revista pone primero a Lee Huamaní.
- PDF leído: https://ijritcc.org/index.php/ijritcc/article/download/5733/5479
- Aplicación móvil desarrollada con Scrum que analiza URL dentro de mensajes de texto contra una base MySQL de números y enlaces fraudulentos. **No usa ML y no reporta métricas de detección**; población y muestra: no reportadas.
- Relación: mismo canal (mensajes de texto), enfoque de lista negra.

### 3.6 Otros trabajos peruanos cercanos — Nivel B o C

| Trabajo | Qué es | Nivel |
|---|---|---|
| Atuncar Flores et al. (2024). Algorithms based on artificial intelligence for the detection and prevention of social engineering attacks: Systematic review. LACCEI 2024 (UTP). ALICIA: UTPD_990c080d26700ae3d139f593f90e878e | Revisión sistemática (phishing y smishing) | C |
| Mayhuasca et al. (2024). Modelo Sectrabank para mitigar el fraude informático… *Revista Peruana de Computación y Sistemas* (UNMSM). https://revistasinvestigacion.unmsm.edu.pe/index.php/rpcsis/article/view/29031 | Autenticación contra SIM swapping y apps falsas; 50 usuarios; mitiga 98 % y 88 % | B |
| Cabezas Diaz y Gutierrez Sisniegas (2023). Detección de phishing en correos electrónicos mediante procesamiento de lenguaje natural del contenido y URLs ofuscadas. Tesis, U. de Lima. ALICIA: RULI_e0e2cd197b576857d24479092c168983 | Phishing por correo con PLN | C |
| Icochea Rivera (2022). Aplicación RPA para la clasificación de correos electrónicos como phishing y fake news. Tesis, UCV (sede Lima). https://hdl.handle.net/20.500.12692/104470 | Algoritmo ELM – K-step CD-K; eficacia 100 % según resumen | B |
| Oropeza Negrón (2024). Modelo FFNN-Bi-LSTM para evitar ataques de suplantación de identidad en la web… Tesis, UCV (Lima Norte). https://hdl.handle.net/20.500.12692/165204 | URL de phishing con deep learning; métricas > 95 % según resumen | B |
| Mamani Lacuta (2024). Modelo Naive Bayes Multinomial para la clasificación de comentarios spam en español de videos sobre finanzas de la plataforma YouTube. Tesis, UNA Puno. ALICIA: RNAP_0ca91c96849b5b9d9651c3c58b4fb9e3 | Spam en español, pero en YouTube | C |
| OSIPTEL (2022). Webinar: Amenazas y desafíos de la seguridad en las telecomunicaciones. ALICIA: OSIP_02610339ff417e0b951103e3359a93d1 | Objeto de conferencia; aparece al buscar «smishing» | C |

---

## 4. Estadísticas y normas oficiales

### 4.1 Resultado principal

**No se encontró ninguna cifra oficial peruana (OSIPTEL, PNP/DIVINDAT, Ministerio Público, ASBANC, SBS, Indecopi, Defensoría) de denuncias, reclamos o montos desagregada por canal SMS o por smishing, ni a nivel nacional ni para La Libertad.** Las fuentes oficiales agrupan por tipo penal (fraude informático, suplantación de identidad) o por modalidad general (phishing, vishing, SIM swapping). Esta ausencia es en sí un hallazgo citable, siempre que se documente con el registro de búsqueda de la sección 6.

### 4.2 Cifras verificadas

| # | Cifra | Periodo | Entidad origen del dato | Documento donde se leyó | Fecha de publicación | URL | Nivel |
|---|---|---|---|---|---|---|---|
| 1 | Tráfico de SMS en millones: 11 512 (2014); 12 687 (2015); 15 229 (2016); 11 846 (2017); 11 072 (2018); 12 311 (2019); 11 581 (2020); 8 859 (2021); 6 600 (2022); 4 759 (2023); 3 146 (al 3T-2024). Caída promedio anual de 9,3 % en 2014–2023 | 2014 a 3T-2024 | PUNKU-OSIPTEL, elaboración del MTC | Exposición de Motivos del proyecto de Decreto Supremo que aprueba el Marco Normativo para la lucha contra las llamadas y los mensajes de texto con fines ilícitos, Gráfico 5, pág. 9 del PDF | Proyecto prepublicado por R. M. N.° 344-2025-MTC/01.03 (Lima, 04-06-2025; El Peruano, 05-06-2025) | https://cdn.www.gob.pe/uploads/document/file/8172048/6837677-exposicion-de-motivos.pdf | A |
| 2 | 2 382 denuncias por fraude informático. Por modalidad: phishing 720; compras en línea/carding 472; SIM swapping 238; thief transfer 210; vishing 181; otros 561. **El smishing no figura como categoría** | 2022 | DIVINDAT (el MTC lo toma de una nota de El Peruano) | Misma Exposición de Motivos, Gráfico 22, págs. 23–24 del PDF | 2025 | misma URL | A (dato de segunda mano) |
| 3 | 9 403 casos de delitos informáticos atendidos en Lima Centro y 16 distritos; se menciona vishing, phishing y smishing como modalidades frecuentes | Hasta 31-10-2022 | Ministerio Público (el MTC lo toma de una publicación en LinkedIn) | Misma Exposición de Motivos, pág. 24 del PDF | 2025 | misma URL | A (dato de segunda mano) |
| 4 | 41 % de las llamadas catalogadas como spam en Perú fueron fraudulentas (dato de llamadas, no de SMS) | 4T-2023 | Hiya, Global Call Threat Report Q4 2023 (fuente privada) | Misma Exposición de Motivos, pág. 21 del PDF | 2025 | misma URL | A (fuente privada) |
| 5 | 29 118 denuncias por delitos informáticos; 19 602 por fraude informático; 7 431 por suplantación de identidad; 712 contra datos y sistemas | Enero a julio de 2026 | Ministerio Público | El Peruano, «Estos son los ciberdelitos más denunciados en el Perú durante el 2026» | 02-09-2026 | https://elperuano.pe/noticia/303867-ciberdelitos-mas-denunciados-en-el-peru | B |
| 6 | 19 651 denuncias por ciberdelincuencia ante el Ministerio Público | Hasta junio de 2025 | Ministerio Público | Andina, «Crecen denuncias de suplantación y no tienes que ser CEO o influencer para ser víctima» | 19-08-2025 | https://andina.pe/agencia/noticia-crecen-denuncias-suplantacion-y-no-tienes-ser-ceo-o-influencer-para-ser-victima-1041332.aspx | B |
| 7 | Unas 42 mil denuncias por delitos informáticos en 2024 (casi 40 % más que en 2023). Por región: Lima Metropolitana 23 mil; Piura 2 mil; **La Libertad 1 900**; Arequipa 1 900. Fraude informático 69 % y suplantación 22 % | 2024 (la nota no precisa el periodo de las cifras regionales) | Sidpol, PNP, vía RPP Data | RPP, «Ciberdelincuencia en Perú aumentó un 40% en 2024…» | Fecha original no visible; «actualizado el 23-11-2025» | https://rpp.pe/peru/actualidad/fraudes-digitales-y-suplantacion-de-identidad-alarmantes-cifras-de-la-pnp-revelan-el-impacto-de-la-ciberdelincuencia-en-peru-noticia-1620466 | B (prensa, cifras redondeadas) |
| 8 | Más de 700 condenas a más de 900 personas por ciberdelincuencia desde 2021; fiscalías especializadas solo en Lima Centro, Arequipa y Trujillo | 2021 a agosto de 2026 | Unidad Fiscal Especializada en Ciberdelincuencia | El Peruano, «Más de 900 personas condenadas por ciberdelincuencia…» | 14-10-2026 | https://elperuano.pe/noticia/306842-mas-de-900-personas-condenadas-por-ciberdelincuencia-conoce-los-avances-del-ministerio-publico | B |
| 9 | S/ 60 569 sustraídos mediante vishing y smishing; caso de la fiscalía de ciberdelincuencia de La Libertad | Hecho del 24-09-2024 | Ministerio Público | El Peruano (ver 2.9) | 14-10-2024 | ver 2.9 | B |

Ninguna de las cifras 5 a 8 distingue el canal SMS. La cifra 7 es la única con dato para La Libertad y proviene de prensa.

### 4.3 Normas y alertas oficiales sobre SMS

| Documento | Contenido verificado | Fecha | URL | Nivel |
|---|---|---|---|---|
| **Decreto Legislativo N.° 1723** | Establece reglas para el uso de la numeración en llamadas y mensajes de texto y su trazabilidad (art. 1). Obliga a las operadoras a adoptar medidas para evitar el progreso de llamadas y SMS con uso inadecuado de la numeración y a permitir que los usuarios adviertan esas comunicaciones (art. 4.1). Sanciones: amonestación o multa (art. 8). Modifica la Ley N.° 32323 para que los usuarios puedan identificar llamadas **y mensajes de texto (spam)** | Dado el 06-02-2026; El Peruano, 07-02-2026, Normas Legales pág. 14 | https://cdn.www.gob.pe/uploads/document/file/9418827/7717016-d-leg-1723.pdf | A |
| Vigencia del D. Leg. 1723 | Primera Disposición Complementaria Final: entra en vigencia al día siguiente de la publicación de su Reglamento. Segunda: el MTC aprueba el Reglamento en no más de 90 días calendario. **Algunas notas de prensa dicen que rige desde el 08-02-2026; el texto oficial dice otra cosa.** El proyecto de reglamento se prepublicó en abril de 2026 (El Peruano, 16-04-2026: https://www.elperuano.pe/noticia/293678-peru-a-un-paso-de-eliminar-el-anonimato-en-las-llamadas-telefonicas-y-mensajes-de-texto). Aprobación final del reglamento: no verificada | — | misma URL | A |
| **Decreto Supremo N.° 018-2026-MTC** | Aprueba la norma sobre numeración para identificar llamadas y mensajes de texto con fines comerciales o publicitarios. Art. 5.1: se atribuye la serie no geográfica «500» como rango exclusivo para originar llamadas y/o SMS comerciales o publicitarios; formato 500 XXX XXX. Plazo de adecuación de 180 días calendario; evaluación a los 18 meses | El Peruano, 15-09-2026 | Copia del diario oficial alojada en https://img.lpderecho.pe/wp-content/uploads/2026/09/Decreto-Supremo-018-2026-MTC-LPDerecho.pdf | A (copia en sitio de terceros; citar El Peruano) |
| R. M. N.° 344-2025-MTC/01.03 | Dispone publicar el proyecto de Decreto Supremo del Marco Normativo contra llamadas y mensajes de texto con fines ilícitos, por 15 días calendario | Lima, 04-06-2025; El Peruano, 05-06-2025 | https://cdn.www.gob.pe/uploads/document/file/8171448/6837677-resolucion-ministerial-n-344-2025-mtc-01-03.pdf | A |
| **Alerta Integrada de Seguridad Digital N.° 117-2025-CNSD** | Alerta titulada «Fraude por medio de mensajes de texto son cada vez más recurrentes» (pág. 4). Reporta el Centro Nacional de Seguridad Digital (PCM). Describe el smishing y sus señales (enlaces acortados, errores, urgencia). **No contiene cifras** | 20-05-2025 | https://cdn.www.gob.pe/uploads/document/file/8101552/6792106-alerta-integrada-de-seguridad-digital-117-2025-cnsd.pdf | A |

### 4.4 Cifras vistas que NO conviene citar como oficiales

- «1 360 millones de llamadas spam en el Perú en 2025» (El Peruano, 16-09-2026, https://elperuano.pe/noticia/304853-mtc-estima-que-en-marzo-del-2027-se-podra-acceder-al-prefijo-500-para-llamadas-spam): es de llamadas, no de SMS, y la fuente primaria de la cifra no se identificó en la nota.
- «44 703 denuncias por delitos informáticos en 2025; aumento de 134 % desde 2021» (La República, 03-05-2026): la nota no nombra la fuente de los totales.
- «31 028 denuncias entre enero y setiembre de 2025; 21 371 por fraude informático (68,88 %)»: vista solo en resultados de búsqueda; la página (lpderecho.pe) devolvió error 403.
- Cifras de ASBANC (aumento de 32 % del fraude digital en el primer semestre de 2024; S/ 96 millones evitados): vistas solo en resultados de búsqueda, sin desagregación por SMS.
- Nota de prensa N.° 7-2024 de OSIPTEL (17-01-2024): trata del envío de SMS informativos sobre líneas a nombre del usuario, no de SMS fraudulentos. No sirve como estadística de smishing.
- Resolución N.° 033-2026-TSC/OSIPTEL (Fravatel contra Viettel): es un caso de libre competencia sobre bloqueo de SMS A2P, no una estadística de fraude.

---

## 5. Corpus de SMS spam en español (trabajo futuro)

| Recurso | Qué es | Estado verificado |
|---|---|---|
| Corpus de Condori Coaquira e Ildefonso Paucar (2025) | 8 457 SMS peruanos en español, etiquetados spam / legit (ver 2.1) | La tesis declara la URL https://github.com/AngelDX/SMS_SPAMPerunano (pág. 26). **El 10-11-2026 la URL devolvió error 404** y no aparece entre los repositorios públicos de esa cuenta. Se puede mencionar como «corpus declarado por los autores, no disponible públicamente a la fecha de consulta»; para usarlo habría que escribir a los autores |
| SMS Spam Multilingual Collection Dataset (Hugging Face) | 5 572 mensajes del SMS Spam Collection con columnas traducidas, entre ellas `text_es`. Licencia indicada: GPL. https://huggingface.co/datasets/dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset | Accesible. **Es traducción automática del inglés, no español nativo**; el método de traducción no figura en la parte de la ficha que se pudo leer. Lo usa Esquea Osorio et al. (2025) |
| Esquea Osorio, C., Riascos Carvajal, M., y Guevara Ibarra, D. (2025). Modelo de aprendizaje supervisado para la identificación automática de spam en entornos de mensajería móvil. *Mundo Fesc*, 15(32), 385–399. https://doi.org/10.61799/2216-0388.1797 | Artículo colombiano (UFPS, Cúcuta) que usa la columna `text_es`: 5 572 mensajes (4 825 normales, 747 spam), CountVectorizer + Random Forest, exactitud 96 %, F1 de spam 0,82, validación cruzada 94,4 % | Nivel A (PDF leído: https://fesc.edu.co/Revistas/OJS/index.php/mundofesc/article/download/1797/1517/8182). No es peruano; sirve como referencia de uso del corpus traducido |
| Dataset de Salinas Bolaños (2024) | 1 740 SMS peruanos etiquetados (ver 3.1) | Disponibilidad pública no reportada en la tesis |
| Smishing-4C (Martínez-Mendoza et al., SEPLN 2024) | 120 muestras de smishing en cuatro categorías | Nivel C. El PDF (besaya.infor.uva.es/sepln24/paper06.pdf) no se pudo descargar; **idioma de las muestras no verificado** |
| SpaPhish (Mendeley Data) | Correos de phishing en español, no SMS. https://data.mendeley.com/datasets/hz2d6gz7pc | Nivel C |
| Colección en español de Gómez Hidalgo et al. (2006) | Colección de SMS spam en inglés y español | Nivel C; fuera de ventana y sin constancia de que sea pública |

Conclusión para el artículo: a la fecha de consulta no se verificó ningún corpus público de SMS spam en **español nativo**; la opción reproducible es la traducción automática del SMS Spam Collection, con la limitación de que no refleja el lenguaje ni las entidades suplantadas en el Perú.

---

## 6. Registro de búsquedas (10-11-2026)

### 6.1 ALICIA (alicia.concytec.gob.pe), búsqueda en todos los campos

| Términos | Resultados | Pertinentes dentro de la ventana |
|---|---|---|
| spam SMS | 3 | Vasquez Chuñe 2025 (USS). Los otros: Castañeda 2013 y un artículo de spam de correo (UPC, 2022) |
| smishing | 13 | Mayaute Málaga 2025 (UTP), Flores Barrios 2022 (UPN), Salinas Bolaños 2024 (ESAN), Calero Sinche 2024 (ya conocido), Mayhuasca 2024 (UNMSM); el resto son tesis de Derecho |
| spam | 14 | Los anteriores más Mamani Lacuta 2024 (YouTube) y Cabezas Diaz 2023 (correo) |
| phishing | 97 | Revisados los 97 títulos; solo los ya citados tratan detección automática |
| phishing "machine learning" | 10 | Ninguno de SMS ni de Trujillo, salvo el artículo de códigos QR (2.5) |
| phishing aprendizaje automático | 5 | Ninguno nuevo |
| "mensajes de texto" spam | 1 | Solo Castañeda 2013 |
| "mensajes de texto" fraudulentos | 2 | ESAN 2024 y UTP 2025 |
| SMS fraude detección | 0 | **Sin resultados** |
| SMS "aprendizaje automático" | 2 | No pertinentes (reconocimiento facial) |
| SMS "machine learning" | 5 | UTP 2025 y Calero Sinche 2024 |
| "correo no deseado" | 0 | **Sin resultados** |
| "mensajes fraudulentos" | 2 | UTP 2025 y ESAN 2024 |
| smishing detección | 3 | UTP 2025, UPN 2022, ESAN 2024 |
| "mensajes SMS" clasificación | 1 | USS 2025 |
| spam "máquinas de soporte vectorial" | 0 | **Sin resultados** |
| spam clasificación texto | 1 | USS 2025 |
| URL maliciosas "machine learning" | 0 | **Sin resultados** |
| "fake news" detección | 0 | **Sin resultados** |

ALICIA con filtro de institución:

| Institución | Términos | Resultado |
|---|---|---|
| Universidad Nacional de Trujillo | phishing (2), spam (2), smishing (1), SMS (2), "mensajes de texto" (3), ciberseguridad (4), "machine learning" (17), "aprendizaje automático" (10), "lenguaje natural" (1), "minería de texto(s)" (1), fraude detección (1), malware (0), "clasificación de textos" (0), "análisis de sentimientos" (0) | **Ningún trabajo de detección de spam, smishing o phishing con ML en 2021–2026.** Solo las tesis de 2013, 2015 y 2019 y el artículo de Che León (2024). Los trabajos de ML son agrícolas o médicos |
| Universidad Privada Antenor Orrego | phishing (0), spam (0), smishing (0), SMS (2), "mensajes de texto" (1), ciberseguridad (5), "machine learning" (11), "aprendizaje automático" (6), "lenguaje natural" (8), malware (1) | **Sin resultados para phishing, spam y smishing.** Lo más cercano: Cornejo Adrianzén 2026 (2.6) |
| Universidad César Vallejo | phishing Trujillo (4, todas de Derecho), smishing Trujillo (0), spam Trujillo (0), "machine learning" Trujillo "Ingeniería de Sistemas" (18, ninguna de texto o seguridad), "mensajes de texto" Trujillo fraude (0), estafa SMS Trujillo (0) | ALICIA no devolvió la tesis de Condori (2.1); apareció solo en el repositorio propio de la UCV |
| U. Católica de Trujillo, U. Privada de Trujillo, U. Privada Leonardo Da Vinci | phishing, spam | 0 resultados (no se confirmó que el nombre de institución coincida con el que usa ALICIA) |

### 6.2 Repositorios institucionales

| Repositorio | Términos | Resultado |
|---|---|---|
| UPN (repositorio.upn.edu.pe, API pública del repositorio; búsqueda en texto completo) | phishing (96), spam (97), smishing (20), "mensajes de texto" fraude (57), "machine learning" (487), "aprendizaje automático" (447), "procesamiento de lenguaje natural" (77), ciberseguridad (417), "fraude informático" (45), "red neuronal" clasificación (114); filtrado por sede que contiene «Trujillo» y año ≥ 2021 | Sede Trujillo: solo Soto Calderon y Tirado Rios (2.2) trata detección con ML de una amenaza de phishing. **Ninguna tesis de la sede Trujillo sobre spam SMS o smishing con ML.** Sede Lima: Flores Barrios 2022 (3.2) |
| UCV (repositorio.ucv.edu.pe/discover; texto completo) | smishing (87); smishing "machine learning" (21); "spam" "SMS" "machine learning" (5); "mensajes de texto" phishing detección "aprendizaje automático" (13); (phishing OR spam OR smishing) "machine learning" "TRUJILLO - PERÚ" (16); "spam" (SVM OR "TF-IDF" OR "Naive Bayes") (SMS OR "mensajes de texto" OR correo) clasificación (13) | Condori Coaquira e Ildefonso Paucar 2025 (2.1) y Cordova Gonzalez 2024 (2.3). El resto son tesis de Derecho o de otras sedes |
| U. Católica de Trujillo (repositorio.uct.edu.pe, API) | spam (0), smishing (0), phishing (0), SMS (0), "mensajes de texto" (0), "machine learning" (1), "aprendizaje automático" (1), ciberseguridad (2), "fraude informático" (3) | **Sin resultados pertinentes.** Solo tesis de Derecho |
| ESAN (repositorio.esan.edu.pe, API) | registro por handle | Salinas Bolaños 2024 (3.1) |
| UNT (dspace.unitru.edu.pe) | spam SMS | **No accesible**: el dominio no resolvió (error DNS) y la API no respondió. Cobertura obtenida vía ALICIA |
| UPAO (repositorio.upao.edu.pe) | phishing | **No consultado**: presenta verificación anti-bots, que no se intentó sortear. Cobertura vía ALICIA |
| UTP (repositorio.utp.edu.pe) | registro por handle | **No consultado en texto completo**: verificación anti-bots. Solo metadatos vía ALICIA |
| USS (repositorio.uss.edu.pe) | registro por handle | **No consultado en texto completo**: verificación anti-bots. Solo metadatos vía ALICIA |
| U. Privada de Trujillo (repositorio.uprit.edu.pe) | — | La API devolvió 404; no consultado |
| RENATI (renati.sunedu.gob.pe) | smishing | **No accesible**: verificación anti-bots. ALICIA cosecha los mismos repositorios |
| Google Scholar | — | **No consultado directamente** (exige verificación anti-bots). Se usó un buscador web general |

### 6.3 Buscador web general

| Consulta (resumen) | Resultado |
|---|---|
| tesis detección spam SMS machine learning Trujillo (UNT, UPAO, UCV, UPN) | Sin tesis locales nuevas; solo las de la UNT de 2013–2019 |
| tesis smishing "machine learning" Perú | Trabajos de la UTP ya conocidos |
| tesis phishing "machine learning" Trujillo | **Sin resultados locales** |
| "Mendoza de los Santos" UNT phishing/smishing/spam | Solo el artículo de códigos QR |
| Perú detección spam SMS español, revista peruana, LACCEI, IEEE INTERCON | Sin artículos peruanos de clasificación de SMS en español; apareció el artículo colombiano de Mundo Fesc |
| OSIPTEL SMS fraudulentos, bloqueo de mensajes con enlaces, cifras 2025 | **Sin cifras de SMS fraudulentos.** Solo bloqueo de equipos por IMEI |
| OSIPTEL smishing, reportes de usuarios, nota de prensa | **Sin resultados pertinentes** |
| OSIPTEL encuesta ERESTEL, porcentaje de usuarios que reciben SMS fraudulentos | **Sin resultados** |
| OSIPTEL tráfico SMS PUNKU 2025 | Sin serie 2025; la serie hasta 3T-2024 se obtuvo del documento del MTC |
| DIVINDAT denuncias 2025, smishing, La Libertad | Sin desagregación por smishing; dato regional solo en RPP |
| La Libertad denuncias delitos informáticos 2025 | **Sin cifra oficial regional de 2025** |
| Ministerio Público, boletín estadístico de ciberdelincuencia por distrito fiscal, La Libertad | **No se localizó el boletín primario ni el desglose por distrito fiscal** |
| ASBANC smishing, porcentaje por canal SMS | **Sin desagregación por canal** |
| Indecopi, reportes de SMS spam | Sin cifras de SMS; solo llamadas (7 millones de audios procesados en 2024, según Canal N) |
| Decreto Legislativo y normas MTC 2026 sobre llamadas y mensajes | D. Leg. 1723 y D. S. 018-2026-MTC (4.3) |
| Corpus SMS spam en español (Zenodo, Kaggle, Mendeley, arXiv) | Ver sección 5; ninguno nativo verificado |

Fuentes no consultadas por falta de resultados o de tiempo: portales estadísticos de SBS y Defensoría del Pueblo, y el portal de datos del Observatorio de Criminalidad del Ministerio Público.

---

## 7. Cómo aprovecharlo en el artículo

- **Para «fortalecer la evidencia local»**: citar a Condori Coaquira e Ildefonso Paucar (2025) como antecedente directo de la sede Trujillo de la UCV, y a Soto Calderon y Tirado Rios (2025) como antecedente de la propia UPN Trujillo en detección de phishing con SVM. Dejar constancia de que la UNT, la UPAO y la UCT no registran trabajos de detección de spam SMS en 2021–2026, según el registro de búsqueda.
- **Para el vacío que cubre el artículo**: ninguno de los antecedentes locales o nacionales verificados incorpora revisión humana de predicciones inciertas; todos reportan solo métricas automáticas.
- **Para la comparación de resultados**: el TF-IDF + SVM de Condori (F1 0,9469 sobre SMS peruanos) es el punto de comparación más cercano; Salinas Bolaños (exactitud 85,62 % con RNN) y Flores Barrios (TPR 90 % con reglas sobre 20 SMS) completan el cuadro nacional.
- **Para el contexto estadístico**: la serie PUNKU-OSIPTEL muestra que el SMS sigue activo (4 759 millones en 2023) aunque en descenso, y el marco normativo de 2026 demuestra que el Estado trata el SMS como canal de fraude. Decir expresamente que no existe estadística oficial desagregada por SMS.
- **Para trabajo futuro**: señalar la falta de un corpus público de SMS en español peruano y mencionar el corpus declarado por la tesis de la UCV, indicando que no estaba disponible al 10-11-2026.

## 8. Referencias sugeridas (formato cercano a APA 7; verificar antes de entregar)

- Che León Antinori, V. H. (2024). Influencia de los delitos cibernéticos económicos en Perú. *SCIÉNDO, 27*(4), 415–418. https://doi.org/10.17268/sciendo.2024.071
- Condori Coaquira, A. R., e Ildefonso Paucar, J. A. (2025). *Diseño de un modelo basado en aprendizaje automático para la detección de mensajes maliciosos en español, Perú 2025* [Trabajo académico de segunda especialidad, Universidad César Vallejo]. Repositorio Institucional UCV. https://hdl.handle.net/20.500.12692/185506
- Decreto Legislativo N.° 1723. (2026, 7 de febrero). *Diario Oficial El Peruano*, Normas Legales, p. 14.
- Decreto Supremo N.° 018-2026-MTC. (2026, 15 de setiembre). Decreto Supremo que aprueba la norma sobre la numeración para la identificación de llamadas y mensajes de texto realizados para brindar información con fines comerciales y/o publicitarios. *Diario Oficial El Peruano*.
- Esquea Osorio, C., Riascos Carvajal, M., y Guevara Ibarra, D. (2025). Modelo de aprendizaje supervisado para la identificación automática de spam en entornos de mensajería móvil. *Mundo Fesc, 15*(32), 385–399. https://doi.org/10.61799/2216-0388.1797
- Flores Barrios, P. F. (2022). *Desarrollo de aplicativo móvil para la detección de phishing en mensajes de texto (SMS) de dispositivos con sistema operativo Android* [Tesis de pregrado, Universidad Privada del Norte]. Repositorio UPN. https://hdl.handle.net/11537/31675
- Lee Huamaní, E., Meneses-Claudio, B., Velarde-Molina, J. F., Mirji, H., y Bhavsar, D. N. (2022). Development of mobile application that detects phishing messages to decrease the percentage of data theft during the COVID-19 pandemic. *International Journal on Recent and Innovation Trends in Computing and Communication, 10*(10), 45–51. https://doi.org/10.17762/ijritcc.v10i10.5733
- Ministerio de Transportes y Comunicaciones. (2025). *Exposición de motivos del proyecto de Decreto Supremo que aprueba el Marco Normativo para la lucha contra las llamadas y los mensajes de texto con fines ilícitos* (prepublicado por Resolución Ministerial N.° 344-2025-MTC/01.03). https://cdn.www.gob.pe/uploads/document/file/8172048/6837677-exposicion-de-motivos.pdf
- Presidencia del Consejo de Ministros, Centro Nacional de Seguridad Digital. (2025, 20 de mayo). *Alerta Integrada de Seguridad Digital N.° 117-2025-CNSD*. https://cdn.www.gob.pe/uploads/document/file/8101552/6792106-alerta-integrada-de-seguridad-digital-117-2025-cnsd.pdf
- Salinas Bolaños, Y. A. (2024). *Propuesta de modelo predictivo para la detección de fraude en mensajes de texto mediante el uso de Redes Neuronales Recurrentes* [Tesis de pregrado, Universidad ESAN]. Repositorio ESAN. https://hdl.handle.net/20.500.12640/4287
- Soto Calderon, J. L., y Tirado Rios, R. J. (2025). *Implementación de un método de clasificación de Machine Learning para detectar páginas web de tipo phishing dentro de un entorno del Programa Nacional de Asistencia Social* [Tesis de maestría, Universidad Privada del Norte]. Repositorio UPN. https://hdl.handle.net/11537/44113

Pendientes de abrir el texto completo antes de citarlos con cifras: Mayaute Málaga (2025, UTP), Vasquez Chuñe (2025, USS), Cordova Gonzalez (2024, UCV), Huamanchumo Trujillo et al. (2024), Cornejo Adrianzén y Requenes Querevalu (2026, UPAO).

## 9. Nota sobre archivos de trabajo

Para leer los PDF se guardaron copias temporales y sus extracciones de texto en las subcarpetas `pdfs`, `txt` y `scripts` de la misma carpeta temporal de este informe. No se modificó ningún archivo del proyecto.
