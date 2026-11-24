# Guion de exposición · Detector de spam SMS con revisión humana

Grupo 03 · Sistemas Inteligentes y Machine Learning · UPN 2026-2
Duración sugerida: **10 a 12 minutos** + preguntas.

---

## 0. Antes de empezar (5 min antes, no se dice en voz alta)

1. Abre PowerShell en la carpeta del repositorio y arranca la app:

   ```powershell
   .\.venv\Scripts\python.exe codigo/app/app.py
   ```

2. Abre **http://127.0.0.1:5000** en el navegador. Deja la terminal abierta.
3. Ten copiados estos 3 mensajes (están también como botones en la pantalla):
   - Legítimo: `Are we still meeting for lunch tomorrow at 1pm?`
   - Spam: `Congratulations! You have won a 500 GBP voucher. Text CLAIM to 80086 now to collect your prize`
   - Dudoso: `You have been selected for a special offer, reply to this number`
4. Si quieres empezar con el historial vacío: detén la app (Ctrl+C), mueve la carpeta `codigo/app/instance/` a otro lugar fuera del repositorio y vuelve a arrancar.

---

## 1. El problema (1 min)

> "Todos recibimos SMS de premios falsos, ofertas o cobros que no reconocemos. Revisarlos a mano no escala, y un filtro automático que se equivoca tampoco es aceptable: si bloquea un mensaje real, alguien pierde información importante.
>
> Nuestro sistema hace dos cosas: **clasifica automáticamente** los mensajes cuando está seguro, y **cuando duda, no adivina**: se los pasa a una persona para que decida. A eso le llamamos **revisión humana de predicciones inciertas**."

Título del trabajo: *Detección de spam en mensajes SMS mediante aprendizaje supervisado y revisión humana de predicciones inciertas.*

---

## 2. Los datos (1 min)

> "Para que una máquina aprenda qué es spam, necesita ejemplos ya etiquetados. Usamos un dataset público y conocido."

- **Dataset:** UCI SMS Spam Collection (licencia CC BY 4.0), SMS reales **en inglés**.
- **5574 mensajes:** 4827 legítimos (86.6 %) y 747 spam (13.4 %). Hay muchos más mensajes normales que spam: el dataset está **desbalanceado**.
- **403 duplicados exactos.** Los agrupamos para que un mismo mensaje no aparezca a la vez en entrenamiento y en prueba (eso inflaría los resultados).
- **División:** entrenamiento 3344 · validación 1115 · prueba 1115 (semilla 42, estratificada y agrupada).

> "Pensemos en un examen: el **entrenamiento** son los ejercicios que el modelo estudia, la **validación** es el simulacro para elegir la mejor estrategia y la **prueba** es el examen final, que se toma una sola vez."

---

## 3. Cómo predecimos (3 min) — el corazón de la expo

El proceso tiene **tres pasos**: convertir el texto en números → calcular una probabilidad → decidir.

### Paso 1 · Convertir texto en números (TF-IDF)

> "Una computadora no entiende palabras, entiende números. TF-IDF le da a cada palabra un peso:
> - **TF:** cuántas veces aparece la palabra en *este* mensaje.
> - **IDF:** qué tan rara es la palabra en *todos* los mensajes. Palabras comunes como *the* o *to* pesan poco; palabras raras y llamativas como *voucher* o *claim* pesan mucho."

Detalles que usamos:
- Palabras sueltas **y pares de palabras** (unigramas + bigramas), por ejemplo *"have won"* o *"text claim"*.
- Conservamos **números y símbolos** como `£ $ € ! ? %`, porque el spam los usa mucho ("£500", "FREE!!!").

### Paso 2 · Calcular la probabilidad (SVM lineal calibrada)

> "Con esos números, el modelo **SVM lineal** traza una frontera que separa lo que se parece a spam de lo que se parece a un mensaje normal. Eso da un puntaje, pero un puntaje no es una probabilidad. Por eso lo **calibramos** (método de Platt) para que diga algo como: *este mensaje tiene 99.7 % de probabilidad de ser spam*."

Por qué elegimos SVM:
- Comparamos **Regresión logística** contra **SVM lineal**, probando distintas configuraciones (C = 0.1, 1, 10; con y sin pares de palabras) con validación cruzada de 5 pliegues.
- Ganó **SVM con C = 10 y unigramas + bigramas**.
- En validación: F1 spam **0.948** con SVM vs **0.921** con regresión logística. Además, las probabilidades de SVM salieron mejor calibradas (Brier 0.010 vs 0.015).

### Paso 3 · Decidir (regla de confianza con τ = 0.70)

> "Aquí está la idea propia del sistema. No basta con saber si es spam: también importa **qué tan seguro** está el modelo."

```
P(spam)    = probabilidad que da el modelo
etiqueta   = spam si P(spam) > 0.5, si no legítimo
confianza  = la mayor entre P(spam) y P(legítimo)

Si confianza ≥ 0.70  →  decisión automática (spam o legítimo)
Si confianza < 0.70  →  pendiente de revisión humana
```

> "El umbral **τ = 0.70** no lo inventamos: lo elegimos en validación buscando que, de los mensajes que el sistema decide solo, se equivoque en **1 % o menos**, y que no mande a revisión más del **15 %**. Entre las opciones que cumplían eso, escogimos la que deja más mensajes en automático."

"Pendiente de revisión" **no es una tercera clase**: es el sistema diciendo *"no estoy seguro, que lo vea una persona"*.

---

## 4. Ejemplo explicado paso a paso (1 min)

Mensaje:

> `Congratulations! You have won a 500 GBP voucher. Text CLAIM to 80086 now to collect your prize`

1. **TF-IDF:** lo parte en palabras y pares: *congratulations*, *won*, *voucher*, *claim*, *prize*, *80086*, el símbolo *!*, y pares como *"have won"* o *"text claim"*. Son palabras raras en mensajes normales y muy frecuentes en spam, así que reciben pesos altos.
2. **SVM calibrada:** con esos pesos el mensaje cae claramente del lado spam → **P(spam) = 0.997**.
3. **Regla de decisión:** la etiqueta es spam (0.997 > 0.5) y la confianza es 0.997, que es **mayor que 0.70** → **Spam (automático)**. No necesita revisión.

Contraste rápido (para la demo):

| Mensaje | P(spam) | Confianza | Decisión |
|---|---|---|---|
| Are we still meeting for lunch tomorrow at 1pm? | 0.002 | 0.998 | Legítimo (automático) |
| Congratulations! You have won a 500 GBP voucher… | 0.997 | 0.997 | Spam (automático) |
| You have been selected for a special offer, reply to this number | 0.576 | 0.576 | **Pendiente de revisión** (0.576 < 0.70) |

---

## 5. Demostración en vivo (3 min)

Ve diciendo lo que haces mientras lo haces.

1. **Pantalla Clasificar.** "Aquí el usuario pega el SMS. El modelo corre en la misma computadora: no usa internet ni ninguna API."
2. Pulsa **Conversación normal** → **Analizar mensaje**. Muestra: *Legítimo (automático)*, P(spam) 0.002, confianza, τ 0.70.
3. **Analizar otro mensaje** → **Premio no solicitado** → *Spam (automático)*, P(spam) 0.997.
4. **Analizar otro mensaje** → pega el **mensaje dudoso** → *Pendiente de revisión humana*. "Fíjense que el modelo *cree* que es spam (0.576), pero no está lo bastante seguro, así que no decide solo."
5. Ve a **Bandeja de revisión**. "Aquí llegan solo los mensajes en los que el sistema dudó." Escribe tu nombre como revisor, un comentario corto y marca **Spam**.
6. Ve a **Revisiones**. "Queda registrado quién revisó, qué etiqueta puso el modelo y qué decidió la persona." Muestra el botón **Exportar CSV**.
7. Ve a **Historial**. "Aquí está todo lo clasificado, con filtros y un resumen de legítimos, spam y pendientes."

Frase de cierre de la demo:
> "Guardar una revisión **no reentrena** el modelo. Queda registrada en la base de datos para usarla en una versión futura."

### Cómo está construido (si hay tiempo, 30 s)

- **Python + scikit-learn** para el modelo (guardado en `modelo_spam_v1.joblib`, ya entrenado y congelado).
- **Flask** para la aplicación web.
- **SQLite** como base de datos, con dos tablas: `mensajes` (cada predicción) y `revisiones` (cada decisión humana).
- Flujo: formulario → modelo → regla τ → se guarda en `mensajes` → si es dudoso aparece en la bandeja → la persona revisa → se guarda en `revisiones` → se puede exportar a CSV.

---

## 6. Resultados (1.5 min)

Evaluados **una sola vez** sobre los **1115 mensajes de prueba**, que el modelo nunca vio:

| Métrica (spam = clase positiva) | Valor | Meta fijada antes |
|---|---|---|
| **Precision** (de lo que marcó spam, cuánto era spam) | **0.986** (IC 95 %: 0.963–1.000) | ≥ 0.95 ✔ |
| **Recall** (del spam real, cuánto atrapó) | **0.913** (IC 95 %: 0.865–0.956) | — |
| **F1** (equilibrio entre ambas) | **0.948** (IC 95 %: 0.920–0.972) | ≥ 0.90 ✔ |
| Accuracy | 0.987 | — |

**Matriz de confusión:** 137 spam bien detectados · 963 legítimos bien detectados · **2** legítimos marcados como spam · **13** spam que se escaparon.

**Efecto de la revisión humana (τ = 0.70):**
- El sistema decide solo el **99.46 %** de los mensajes; solo **6 de 1115** van a revisión.
- El error en lo que decide solo baja de **1.35 %** a **0.99 %**.
- Los **2 falsos positivos** (mensajes normales marcados como spam) fueron **ambos a revisión**: ningún mensaje legítimo se bloqueó automáticamente.

> "En spam es peor bloquear un mensaje real que dejar pasar un spam. Por eso nos importa tanto la precision."

---

## 7. Limitaciones y trabajo futuro (1 min)

Dilo con honestidad, suma puntos:

- **Solo inglés.** Ejemplo: *"Hola, ganaste un premio, responde YA"* sale legítimo (P = 0.009), porque el modelo nunca vio español.
- **Quedan 11 spam que se escapan con confianza alta.** La revisión atrapa la duda, no todos los errores. Ejemplo real: *"Money i have won wining number 946 wot do i do next"* → P(spam) = 0.001.
- Dataset antiguo: no incluye fraudes recientes, links de phishing ni operadores peruanos.
- Es un prototipo local: no tiene login de revisores ni cifrado de la base.
- **Futuro:** datos en español (con consentimiento), detector de idioma, reentrenar con las revisiones humanas y probar con revisores reales.

---

## 8. Cierre (20 s)

> "En resumen: convertimos el texto en números con TF-IDF, una SVM calibrada nos da la probabilidad de spam, y una regla de confianza decide si actuar solo o pedir ayuda a una persona. Con eso logramos 98.6 % de precision y 0.948 de F1, y ningún mensaje legítimo fue bloqueado automáticamente en la prueba. Gracias."

---

## Preguntas probables (respuestas cortas)

**¿Por qué no usaron deep learning o un LLM?**
Con 5574 mensajes cortos, TF-IDF + SVM da muy buen resultado (F1 0.948), corre en cualquier PC sin GPU ni internet y se puede explicar. Un modelo grande sería más pesado sin una ganancia clara para este caso.

**¿Qué significa "calibrada"?**
La SVM da un puntaje de distancia a la frontera. La calibración lo convierte en una probabilidad real entre 0 y 1, que es lo que necesitamos para comparar con τ.

**¿Por qué τ = 0.70 y no 0.90?**
Lo escogimos en validación con dos condiciones: error ≤ 1 % en lo automático y ≤ 15 % a revisión. 0.70 cumplía ambas mandando lo mínimo a revisión. Un τ más alto manda más mensajes a las personas.

**¿Por qué no usaron accuracy como métrica principal?**
Porque el 86.6 % de los mensajes son legítimos. Un modelo que diga "todo es legítimo" ya tendría 86.6 % de accuracy sin detectar ningún spam. Precision, recall y F1 miran directamente al spam.

**¿Qué pasa con las revisiones? ¿El modelo aprende?**
Hoy no. Se guardan en SQLite y se exportan a CSV. Reentrenar con ellas es trabajo futuro.

**¿Cómo evitaron hacer trampa con los datos?**
Agrupamos los duplicados para que no estén a la vez en entrenamiento y prueba, elegimos modelo y τ solo con validación, congelamos todo (modelo con huella SHA-256) y recién ahí evaluamos una vez en prueba.

**¿Qué es un bigrama?**
Un par de palabras seguidas, como *"have won"*. Ayuda porque el par dice más que cada palabra por separado.

---

## Ficha de datos (para tener a mano)

| Dato | Valor |
|---|---|
| Dataset | UCI SMS Spam Collection, inglés, CC BY 4.0 |
| Mensajes | 5574 (4827 legítimos · 747 spam) |
| Duplicados exactos | 403 |
| División | 3344 entrenamiento · 1115 validación · 1115 prueba |
| Representación | TF-IDF, unigramas + bigramas, conserva números y £$€!?%& |
| Modelo | SVM lineal, C = 10, calibración sigmoide (Platt), 5 pliegues |
| F1 validación cruzada | 0.960 |
| Umbral | τ = 0.70 |
| Precision / Recall / F1 (prueba) | 0.986 / 0.913 / 0.948 |
| VP / FP / FN / VN | 137 / 2 / 13 / 963 |
| Cobertura automática | 99.46 % (6 a revisión) |
| Error en lo automático | 0.99 % (sin revisión: 1.35 %) |
| Tecnologías | Python 3.13, scikit-learn 1.9.1, Flask 3.1.3, SQLite |
| Integrantes | Baca Flores, Flavio · Espinoza Marquez, Adriano · Goray Gonzales, Nicolás · Paredes Moya, Pablo · Vigo Aleman, Jorge |
