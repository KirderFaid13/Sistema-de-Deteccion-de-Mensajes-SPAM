# Código del detector de spam SMS

Grupo 03 · Sistemas Inteligentes y Machine Learning · Universidad Privada del Norte, Trujillo – San Isidro · 2026-2.

La guía técnica completa, con arquitectura, reglas, módulos, rutas, SQLite, resultados y solución de problemas, está en el [README principal](../README.md).

Repositorio: [Sistema de Detección de Mensajes SPAM](https://github.com/KirderFaid13/Sistema-de-Deteccion-de-Mensajes-SPAM).

## Instalar e iniciar desde esta carpeta

Si tu terminal está en `codigo/`, ejecuta en PowerShell:

```powershell
py -3.13 -m venv ..\.venv
..\.venv\Scripts\python.exe -m pip install -r requirements-app.txt
..\.venv\Scripts\python.exe app/app.py
```

Abre [http://127.0.0.1:5000](http://127.0.0.1:5000). La base SQLite se crea automáticamente en `app/instance/` al primer acceso. Detén el servidor con Ctrl+C.

El modelo ya está entrenado. No necesitas ejecutar el notebook ni tener Jupyter para iniciar la web. Conserva scikit-learn 1.9.1 para cargar el artefacto; una incompatibilidad se resuelve en el entorno, preservando el modelo congelado.

## Ejecutar pruebas desde esta carpeta

```powershell
..\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
..\.venv\Scripts\python.exe -m pytest -q tests/test_nucleo.py
```

El test de carga/partición necesita `../Dataset/sms+spam+collection.zip`. Los otros tres verifican la regla y las métricas con datos de ejemplo. Las pruebas no entrenan ni evalúan el modelo con la prueba existente.

## Reproducción del experimento

`requirements.txt` conserva las versiones del entorno experimental original. Su uso y las precauciones para reproducir el notebook se explican en el README principal. El notebook escribe en `models/` y `results/`; usa una copia separada si necesitas ejecutarlo. La prueba ya fue observada y no debe emplearse para elegir nuevas decisiones.

## Asistencia de IA e integridad

El código fue generado con asistencia de IA a partir de las instrucciones del grupo. Los integrantes deben revisarlo, comprenderlo y documentar sus contribuciones antes de presentarlo como avance propio.

El modelo congelado y los resultados originales se conservan. SHA-256 del ZIP: `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3`.
