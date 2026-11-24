"""Genera el conjunto fijo de mensajes para la prueba controlada con revisores humanos.

Ejecutar una sola vez desde `codigo/` (el resultado, `estudio/estimulos.csv`, se versiona):

    python estudio/generar_estimulos.py

Composición (60 mensajes, semilla 42), según lo que hizo el modelo congelado con tau = 0.70:
- revision ......... todos los mensajes que el sistema envió a revisión en validación y prueba.
                     Son los que un revisor recibiría en el uso real.
- error_confiado ... todos los errores que el sistema aceptó con confianza >= tau en validación y
                     prueba. Permiten medir si una persona habría detectado lo que el modelo no.
- control .......... mensajes de validación bien clasificados con confianza alta, mitad de cada
                     clase, elegidos al azar. Dan la referencia de desempeño humano en casos fáciles.

El modelo no se modifica. La partición de prueba sólo aporta los mensajes; no se elige nada con ella.
"""
from __future__ import annotations

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spam_sms.data import load_sms_collection  # noqa: E402
from spam_sms.decision import decide  # noqa: E402

SEMILLA = 42
N_TOTAL = 60


def main() -> None:
    df = load_sms_collection(ROOT.parent / "Dataset" / "sms+spam+collection.zip")
    df["particion"] = pd.read_csv(ROOT / "results" / "particiones.csv")["particion"].to_numpy()
    artefacto = joblib.load(ROOT / "models" / "modelo_spam_v1.joblib")
    modelo, tau = artefacto["modelo"], float(artefacto["tau"])

    d = df[df["particion"].isin(["validacion", "prueba"])].copy()
    d["msg_id"] = d.index.to_numpy()          # posición del mensaje en el archivo original
    d = d.reset_index(drop=True)
    d["p_spam"] = modelo.predict_proba(d["text"].to_numpy())[:, 1]
    y_hat, aceptado = decide(d["p_spam"].to_numpy(), tau)
    d["etiqueta_modelo"], d["aceptado"] = y_hat, aceptado
    d["acierto"] = d["etiqueta_modelo"] == d["y"]

    revision = d[~d["aceptado"]].assign(estrato="revision")
    confiados = d[d["aceptado"] & ~d["acierto"]].assign(estrato="error_confiado")

    n_control = N_TOTAL - len(revision) - len(confiados)
    faciles = d[d["aceptado"] & d["acierto"] & (d["particion"] == "validacion")]
    rng = np.random.RandomState(SEMILLA)
    por_clase = {1: n_control // 2, 0: n_control - n_control // 2}
    control = pd.concat([faciles[faciles["y"] == c].sample(n=n, random_state=rng) for c, n in por_clase.items()])
    control = control.assign(estrato="control")

    estimulos = pd.concat([revision, confiados, control])
    estimulos = estimulos[["msg_id", "particion", "estrato", "y", "etiqueta_modelo", "p_spam", "text"]]
    estimulos = estimulos.sort_values("msg_id").reset_index(drop=True)
    estimulos["p_spam"] = estimulos["p_spam"].round(6)
    destino = Path(__file__).resolve().parent / "estimulos.csv"
    estimulos.to_csv(destino, index=False)

    print(f"{len(estimulos)} mensajes guardados en {destino}")
    print(pd.crosstab([estimulos["estrato"], estimulos["particion"]], estimulos["y"]))


if __name__ == "__main__":
    main()
