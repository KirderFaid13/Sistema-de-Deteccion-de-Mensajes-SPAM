"""Reproduce el experimento completo en una copia aislada y lo compara con los resultados guardados.

Uso, desde la raíz del repositorio (Windows, PowerShell):

    py -3.13 codigo/reproducir.py --integrante "Apellidos, Nombres"

Qué hace:
1. Copia `codigo/` y `Dataset/` a una carpeta temporal (no toca los resultados originales).
2. Crea un entorno virtual nuevo e instala las versiones de `requirements.txt`.
3. Ejecuta el notebook de principio a fin: partición, validación cruzada, calibración,
   elección de tau, congelamiento y evaluación en prueba.
4. Ejecuta las pruebas unitarias.
5. Compara cada archivo de `results/` con el original (igualdad numérica con tolerancia 1e-9)
   y las huellas SHA-256 del dataset y del modelo.
6. Guarda la evidencia en `docs/reproduccion/reproduccion_<integrante>_<fecha>.json`.

Es una reproducción: no cambia hiperparámetros ni decisiones, y no se usa para elegir nada.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]          # raíz del repositorio
TOLERANCIA = 1e-9
# Archivos que dependen del momento o del equipo y por eso no se comparan valor a valor.
NO_COMPARABLES = {"entorno_ejecucion.json", "latencia_inferencia.json", "pytest_salida.txt"}
# Resultados que no produce el notebook (análisis posteriores, demostración y prueba con revisores).
FUERA_DEL_NOTEBOOK = ("analisis_fn/", "estudio_revisores/", "tablas/sondas_exploratorias.csv")
# Claves que cambian en cada ejecución aunque el experimento sea idéntico: fechas, la huella del
# archivo serializado (se compara aparte) y la ruta del modelo, que usa "\" en Windows y "/" en Linux.
CLAVES_VARIABLES = {"fecha_congelamiento", "fecha_ejecucion", "sha256_modelo", "ruta_modelo"}


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def ejecutar(cmd, cwd=None) -> tuple[int, str, float]:
    t0 = time.perf_counter()
    p = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout + p.stderr), time.perf_counter() - t0


def aplanar(obj, prefijo=""):
    """Convierte un JSON anidado en pares (ruta, valor) para compararlo campo a campo."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in CLAVES_VARIABLES:
                continue
            yield from aplanar(v, f"{prefijo}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from aplanar(v, f"{prefijo}{i}.")
    else:
        yield prefijo.rstrip("."), obj


def como_numero(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def diferencia(a, b) -> float:
    """0 si son iguales; diferencia absoluta si ambos son números; infinito si difieren."""
    if a == b:
        return 0.0
    fa, fb = como_numero(a), como_numero(b)
    if fa is None or fb is None:
        return math.inf
    if math.isnan(fa) and math.isnan(fb):
        return 0.0
    return abs(fa - fb)


def comparar_json(original: Path, nuevo: Path) -> dict:
    a = dict(aplanar(json.loads(original.read_text(encoding="utf-8"))))
    b = dict(aplanar(json.loads(nuevo.read_text(encoding="utf-8"))))
    if a.keys() != b.keys():
        return {"iguales": False, "max_diferencia": None, "detalle": "campos distintos"}
    difs = {k: diferencia(a[k], b[k]) for k in a}
    peor = max(difs.values(), default=0.0)
    return {"iguales": peor <= TOLERANCIA, "max_diferencia": None if math.isinf(peor) else peor,
            "campos": len(difs)}


def comparar_csv(original: Path, nuevo: Path) -> dict:
    with open(original, encoding="utf-8", newline="") as f:
        a = list(csv.reader(f))
    with open(nuevo, encoding="utf-8", newline="") as f:
        b = list(csv.reader(f))
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        return {"iguales": False, "max_diferencia": None, "detalle": "forma distinta"}
    peor = max((diferencia(x, y) for fa, fb in zip(a, b) for x, y in zip(fa, fb)), default=0.0)
    return {"iguales": peor <= TOLERANCIA, "max_diferencia": None if math.isinf(peor) else peor,
            "filas": len(a)}


def memoria_gb() -> float | None:
    try:
        if platform.system() == "Windows":
            import ctypes

            class Estado(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            e = Estado()
            e.dwLength = ctypes.sizeof(Estado)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(e))
            return round(e.ullTotalPhys / 2**30, 1)
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30, 1)
    except Exception:
        return None


def nombre_procesador() -> str:
    if platform.system() == "Windows":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as k:
                return winreg.QueryValueEx(k, "ProcessorNameString")[0].strip()
        except OSError:
            pass
    return platform.processor() or platform.machine()


def comparables(carpeta_resultados: Path) -> list[str]:
    """Archivos de resultados que el notebook debe volver a generar, como rutas relativas."""
    rutas = []
    for f in sorted(carpeta_resultados.rglob("*")):
        rel = f.relative_to(carpeta_resultados).as_posix()
        if f.suffix in {".json", ".csv"} and f.name not in NO_COMPARABLES and not rel.startswith(FUERA_DEL_NOTEBOOK):
            rutas.append(rel)
    return rutas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--integrante", required=True, help='Quien ejecuta, por ejemplo "Goray Gonzales, Nicolás"')
    ap.add_argument("--carpeta", help="Carpeta de trabajo (por defecto, una temporal nueva)")
    ap.add_argument("--conservar", action="store_true", help="No borrar la carpeta de trabajo al terminar")
    args = ap.parse_args()

    inicio = datetime.now().astimezone()
    trabajo = Path(args.carpeta) if args.carpeta else Path(tempfile.mkdtemp(prefix="repro_spam_"))
    trabajo.mkdir(parents=True, exist_ok=True)
    print(f"[1/6] Copiando el proyecto a {trabajo}")
    ignorar = shutil.ignore_patterns(".venv", "__pycache__", "instance", ".pytest_cache", "*.pyc")
    shutil.copytree(RAIZ / "codigo", trabajo / "codigo", ignore=ignorar, dirs_exist_ok=True)
    shutil.copytree(RAIZ / "Dataset", trabajo / "Dataset", dirs_exist_ok=True)
    copia = trabajo / "codigo"
    # Se borran de la copia los resultados que se van a comparar: así cada uno tiene que
    # generarlo de nuevo el notebook y ninguna coincidencia puede venir de un archivo copiado.
    originales = comparables(RAIZ / "codigo" / "results")
    for rel in originales:
        (copia / "results" / rel).unlink(missing_ok=True)

    print("[2/6] Creando el entorno virtual e instalando dependencias (puede tardar unos minutos)")
    venv = trabajo / ".venv"
    cod, salida, t_venv = ejecutar([sys.executable, "-m", "venv", venv])
    if cod:
        print(salida)
        return 1
    py = venv / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")
    # Playwright sólo sirve para las capturas de pantalla; no interviene en el experimento.
    requisitos = [ln for ln in (copia / "requirements.txt").read_text(encoding="utf-8").splitlines()
                  if ln.strip() and not ln.startswith("#") and not ln.startswith("playwright")]
    (trabajo / "requisitos_reproduccion.txt").write_text("\n".join(requisitos) + "\n", encoding="utf-8")
    cod, salida, t_pip = ejecutar([py, "-m", "pip", "install", "--disable-pip-version-check", "-q",
                                   "-r", trabajo / "requisitos_reproduccion.txt"])
    if cod:
        print(salida[-3000:])
        return 1
    _, congelado, _ = ejecutar([py, "-m", "pip", "freeze"])
    versiones = dict(ln.split("==", 1) for ln in congelado.splitlines() if "==" in ln)

    print("[3/6] Ejecutando el notebook completo (entrenamiento, calibración, tau y prueba)")
    cod, salida, t_nb = ejecutar(
        [py, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--output", "01_reproduccion",
         "--ExecutePreprocessor.timeout=1800", "notebooks/01_experimento_spam_sms.ipynb"], cwd=copia)
    if cod:
        print(salida[-4000:])
        return 1

    print("[4/6] Ejecutando las pruebas unitarias")
    cod_test, salida_test, t_test = ejecutar([py, "-m", "pytest", "-q", "tests/test_nucleo.py"], cwd=copia)
    resumen_test = (re.findall(r"^.*(?:passed|failed|error).*$", salida_test, flags=re.M) or ["sin resumen"])[-1]

    print("[5/6] Comparando con los resultados guardados")
    comparacion = {}
    for rel in originales:
        original = RAIZ / "codigo" / "results" / rel
        nuevo = copia / "results" / rel
        if not nuevo.exists():
            comparacion[rel] = {"iguales": False, "detalle": "no se generó"}
        elif original.suffix == ".json":
            comparacion[rel] = comparar_json(original, nuevo)
        else:
            comparacion[rel] = comparar_csv(original, nuevo)
    iguales = sum(1 for v in comparacion.values() if v["iguales"])
    distintos = sorted(k for k, v in comparacion.items() if not v["iguales"])

    final = json.loads((copia / "results" / "evaluacion_final_prueba.json").read_text(encoding="utf-8"))
    decisiones = json.loads((copia / "results" / "decisiones_congeladas.json").read_text(encoding="utf-8"))
    sha_modelo_original = sha256(RAIZ / "codigo" / "models" / "modelo_spam_v1.joblib")
    sha_modelo_nuevo = sha256(copia / "models" / "modelo_spam_v1.joblib")

    evidencia = {
        "integrante": args.integrante,
        "fecha": inicio.isoformat(timespec="seconds"),
        "equipo": {
            "sistema": f"{platform.system()} {platform.release()} ({platform.version()})",
            "arquitectura": platform.machine(),
            "procesador": nombre_procesador(),
            "nucleos_logicos": os.cpu_count(),
            "memoria_gb": memoria_gb(),
        },
        "python": platform.python_version(),
        "versiones": {k: versiones.get(k) for k in
                      ("numpy", "scipy", "pandas", "scikit-learn", "joblib", "matplotlib", "nbconvert", "pytest")},
        "tiempos_s": {"entorno": round(t_venv + t_pip, 1), "notebook": round(t_nb, 1), "pruebas": round(t_test, 1)},
        "sha256_dataset": sha256(RAIZ / "Dataset" / "sms+spam+collection.zip"),
        "sha256_modelo_original": sha_modelo_original,
        "sha256_modelo_reproducido": sha_modelo_nuevo,
        "modelo_identico_byte_a_byte": sha_modelo_original == sha_modelo_nuevo,
        "decisiones_reproducidas": {"modelo": decisiones["modelo_elegido"],
                                    "hiperparametros": decisiones["hiperparametros"], "tau": decisiones["tau"]},
        "metricas_prueba_reproducidas": {k: final[k] for k in
                                         ("tp", "fp", "fn", "tn", "precision_spam", "recall_spam", "f1_spam")},
        "selectiva_reproducida": {k: final["selectiva_tau_elegido"][k] for k in
                                  ("n_aceptados", "n_revision", "errores_aceptados", "error_aceptados")},
        "archivos_comparados": len(comparacion),
        "archivos_iguales": iguales,
        "archivos_distintos": distintos,
        "max_diferencia_numerica": max((v.get("max_diferencia") or 0.0) for v in comparacion.values()),
        "tolerancia_numerica": TOLERANCIA,
        "detalle_comparacion": comparacion,
        "pruebas_unitarias": resumen_test.strip(),
    }
    destino = RAIZ / "docs" / "reproduccion"
    destino.mkdir(parents=True, exist_ok=True)
    apellido = re.sub(r"[^a-z0-9]+", "_", args.integrante.split(",")[0].lower()).strip("_") or "integrante"
    archivo = destino / f"reproduccion_{apellido}_{inicio:%Y-%m-%d}.json"
    archivo.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2), encoding="utf-8")

    print("[6/6] Resultado")
    print(f"  Archivos de resultados iguales: {iguales} de {len(comparacion)}")
    if distintos:
        print("  Distintos:", ", ".join(distintos))
    m = evidencia["metricas_prueba_reproducidas"]
    print(f"  Prueba: VP/FP/FN/VN = {m['tp']}/{m['fp']}/{m['fn']}/{m['tn']}; "
          f"precision {m['precision_spam']:.3f}; recall {m['recall_spam']:.3f}; F1 {m['f1_spam']:.3f}")
    print(f"  Pruebas unitarias: {evidencia['pruebas_unitarias']}")
    print(f"  Evidencia guardada en: {archivo}")
    if not args.conservar and not args.carpeta:
        shutil.rmtree(trabajo, ignore_errors=True)
    return 0 if not distintos and cod_test == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
