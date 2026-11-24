# Prueba controlada con revisores humanos

Mide lo que el artículo todavía no tiene: **cuánto tarda una persona en revisar un mensaje y con qué frecuencia se equivoca**. Con eso se reemplaza la «revisión ideal simulada» por resultados de revisores reales.

## Qué se mide

| Pregunta | Indicador |
|---|---|
| ¿Cuánto tarda la revisión? | Tiempo por mensaje (mediana y percentil 90) y tiempo total |
| ¿Cuánto se equivoca la persona? | Exactitud frente a la etiqueta del corpus, por tipo de mensaje |
| ¿Los revisores coinciden entre sí? | Kappa de Fleiss |
| ¿Cuánto mejora el sistema con revisores reales? | Precision, recall y F1 en prueba, resolviendo los pendientes con cada revisor |
| ¿Una persona detecta lo que el modelo no? | Exactitud en los errores que el modelo aceptó con confianza alta |

## Material

60 mensajes fijos (`estimulos.csv`), los mismos para todos, en orden aleatorio distinto por persona:

- **13 de revisión:** todos los que el sistema envió a revisión en validación (7) y prueba (6).
- **21 de error confiado:** todos los errores que el sistema aceptó con confianza ≥ 0.70 en validación (10) y prueba (11).
- **26 de control:** mensajes de validación bien clasificados con confianza alta, 13 de cada clase.

La persona no ve la predicción del modelo ni la etiqueta del corpus.

## Participantes

- Mínimo: los cinco integrantes.
- Recomendado: sumar de 3 a 5 personas externas al grupo. Los integrantes ya conocen el proyecto y vieron algunos de estos mensajes en el artículo, así que sus resultados se informan aparte.
- Cada persona usa un código (R01, R02…), no su nombre.

## Procedimiento

1. Arranca la aplicación y abre `http://127.0.0.1:5000/estudio`.
2. El participante lee las instrucciones, escribe su código, indica si es integrante o externo, su nivel de inglés y acepta participar.
3. Etiqueta los 60 mensajes de corrido, sin traductor y sin ayuda. Toma entre 10 y 15 minutos.
4. Al terminar, quien conduce la prueba descarga el CSV con **Descargar respuestas** (o desde `/estudio/respuestas.csv`).
5. Si se usan varias computadoras, cada una exporta su CSV con un nombre distinto.

Condiciones iguales para todos: una sola sesión, sin interrupciones, pantalla de computadora (no celular) y sin comentar los mensajes con quienes aún no participan.

## Análisis

Copia los CSV en `codigo/estudio/respuestas/` y ejecuta desde `codigo/`:

```powershell
..\.venv\Scripts\python.exe estudio/analizar_estudio.py
```

Las tablas quedan en `codigo/results/estudio_revisores/`. Sólo cuentan las sesiones completas (60 respuestas).

## Límites que deben declararse en el artículo

- Muestra pequeña y por conveniencia; no representa a usuarios reales de telefonía.
- Mensajes en inglés leídos por hispanohablantes: parte del error humano puede deberse al idioma.
- La etiqueta de referencia es la del corpus, que en algunos mensajes es discutible.
- Es una prueba de laboratorio: no mide fatiga, carga real de trabajo ni uso prolongado.
