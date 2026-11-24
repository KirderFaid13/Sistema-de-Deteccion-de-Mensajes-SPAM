"""Analiza las respuestas de la prueba controlada con revisores humanos.

1. Cada equipo exporta su CSV desde la aplicación (/estudio/respuestas.csv).
2. Copia todos los CSV en `codigo/estudio/respuestas/` (con nombres distintos).
3. Ejecuta desde `codigo/`:

       python estudio/analizar_estudio.py

Salidas en `results/estudio_revisores/`:
- por_revisor.csv ........ exactitud y tiempos de cada participante.
- por_estrato.csv ........ exactitud y tiempos según el tipo de mensaje.
- acuerdo.json ........... acuerdo entre revisores (kappa de Fleiss) y con la etiqueta del corpus.
- sistema_con_revision.csv  desempeño del sistema en prueba cuando los mensajes pendientes
                            los resuelve cada revisor real (y el voto de la mayoría).
- por_mensaje.csv ........ votos y tiempo mediano de cada mensaje.

Sólo cuentan las sesiones completas (un participante que respondió todos los mensajes).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spam_sms.decision import binary_metrics  # noqa: E402

AQUI = Path(__file__).resolve().parent
OUT = ROOT / "results" / "estudio_revisores"


def kappa_fleiss(votos_spam: np.ndarray, n_revisores: int) -> float:
    """Kappa de Fleiss para dos categorías. `votos_spam[i]` = revisores que marcaron spam en el mensaje i."""
    n, N = n_revisores, len(votos_spam)
    cuentas = np.column_stack([votos_spam, n - votos_spam])
    p_i = ((cuentas ** 2).sum(axis=1) - n) / (n * (n - 1))        # acuerdo observado por mensaje
    p_j = cuentas.sum(axis=0) / (N * n)                            # proporción de cada categoría
    p_obs, p_azar = p_i.mean(), (p_j ** 2).sum()
    return float((p_obs - p_azar) / (1 - p_azar)) if p_azar < 1 else float("nan")


def resumen_tiempos(ms: pd.Series) -> dict:
    s = ms / 1000
    return {"tiempo_mediana_s": round(float(s.median()), 2), "tiempo_p90_s": round(float(s.quantile(0.9)), 2)}


def main() -> int:
    global OUT
    ap = argparse.ArgumentParser(description="Analiza la prueba controlada con revisores.")
    ap.add_argument("--respuestas", default=str(AQUI / "respuestas"), help="Carpeta con los CSV exportados")
    ap.add_argument("--salida", default=str(OUT), help="Carpeta donde se escriben las tablas")
    args = ap.parse_args()
    OUT = Path(args.salida)
    archivos = sorted(Path(args.respuestas).glob("*.csv"))
    if not archivos:
        print("No hay archivos en estudio/respuestas/. Exporta los CSV desde /estudio/respuestas.csv.")
        return 1
    partes = []
    for a in archivos:
        d = pd.read_csv(a)
        d["sesion"] = a.stem + "#" + d["sesion_id"].astype(str)   # la misma numeración puede repetirse entre equipos
        partes.append(d)
    resp = pd.concat(partes, ignore_index=True)
    est = pd.read_csv(AQUI / "estimulos.csv")

    completas = resp.groupby("sesion")["msg_id"].nunique()
    completas = completas[completas == len(est)].index
    descartadas = sorted(set(resp["sesion"]) - set(completas))
    resp = resp[resp["sesion"].isin(completas)].merge(est, on="msg_id", how="left")
    if resp.empty:
        print("Ninguna sesión está completa todavía.")
        return 1
    # Tiempo: el del navegador; si faltó, el medido en el servidor.
    resp["ms"] = resp["ms_cliente"].where(resp["ms_cliente"].notna() & (resp["ms_cliente"] > 0), resp["ms_servidor"])
    resp["acierto"] = resp["etiqueta"] == resp["y"]
    OUT.mkdir(parents=True, exist_ok=True)
    n_rev = resp["sesion"].nunique()

    # ---------- Por revisor ----------
    filas = []
    for sesion, g in resp.groupby("sesion"):
        m = binary_metrics(g["y"], g["etiqueta"])
        fila = {"sesion": sesion, "participante": g["participante"].iloc[0], "tipo": g["tipo"].iloc[0],
                "nivel_ingles": g["nivel_ingles"].iloc[0], "mensajes": len(g),
                "exactitud": round(g["acierto"].mean(), 4),
                "spam_marcado_legitimo": m["fn"], "legitimo_marcado_spam": m["fp"],
                "tiempo_total_min": round(g["ms"].sum() / 60000, 1), **resumen_tiempos(g["ms"])}
        for estrato, ge in g.groupby("estrato"):
            fila[f"exactitud_{estrato}"] = round(ge["acierto"].mean(), 4)
        filas.append(fila)
    por_revisor = pd.DataFrame(filas)
    por_revisor.to_csv(OUT / "por_revisor.csv", index=False)

    # ---------- Por estrato ----------
    filas = []
    for estrato, g in list(resp.groupby("estrato")) + [("todos", resp)]:
        por_ses = g.groupby("sesion")["acierto"].mean()
        filas.append({"estrato": estrato, "mensajes": g["msg_id"].nunique(), "respuestas": len(g),
                      "exactitud_media": round(por_ses.mean(), 4), "exactitud_min": round(por_ses.min(), 4),
                      "exactitud_max": round(por_ses.max(), 4), **resumen_tiempos(g["ms"])})
    por_estrato = pd.DataFrame(filas)
    por_estrato.to_csv(OUT / "por_estrato.csv", index=False)

    # ---------- Por mensaje y acuerdo ----------
    por_msg = (resp.groupby("msg_id")
               .agg(votos_spam=("etiqueta", "sum"), revisores=("etiqueta", "size"),
                    tiempo_mediana_s=("ms", lambda s: round(s.median() / 1000, 2)))
               .reset_index().merge(est, on="msg_id"))
    por_msg["mayoria"] = (por_msg["votos_spam"] * 2 > por_msg["revisores"]).astype(int)
    por_msg["empate"] = por_msg["votos_spam"] * 2 == por_msg["revisores"]
    por_msg["mayoria_coincide_con_corpus"] = por_msg["mayoria"] == por_msg["y"]
    por_msg.to_csv(OUT / "por_mensaje.csv", index=False)

    acuerdo = {"revisores": int(n_rev), "mensajes": int(len(est)), "sesiones_incompletas_descartadas": descartadas,
               "kappa_fleiss": {}, "mayoria_coincide_con_corpus": {}}
    if n_rev >= 2:
        for estrato, g in list(por_msg.groupby("estrato")) + [("todos", por_msg)]:
            acuerdo["kappa_fleiss"][estrato] = round(kappa_fleiss(g["votos_spam"].to_numpy(), n_rev), 4)
    for estrato, g in list(por_msg.groupby("estrato")) + [("todos", por_msg)]:
        acuerdo["mayoria_coincide_con_corpus"][estrato] = f"{int(g['mayoria_coincide_con_corpus'].sum())} de {len(g)}"
    (OUT / "acuerdo.json").write_text(json.dumps(acuerdo, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------- Sistema con revisión real (partición de prueba) ----------
    # Los mensajes aceptados conservan la decisión del modelo; los pendientes toman la etiqueta humana.
    final = json.loads((ROOT / "results" / "evaluacion_final_prueba.json").read_text(encoding="utf-8"))
    sel = final["selectiva_tau_elegido"]
    pend = est[(est["particion"] == "prueba") & (est["estrato"] == "revision")]
    filas = []

    def sistema(nombre: str, etiquetas: pd.Series) -> dict:
        e = pend.set_index("msg_id")["y"].to_frame().join(etiquetas.rename("humano"))
        tp = sel["acc_tp"] + int(((e["y"] == 1) & (e["humano"] == 1)).sum())
        fn = sel["acc_fn"] + int(((e["y"] == 1) & (e["humano"] == 0)).sum())
        fp = sel["acc_fp"] + int(((e["y"] == 0) & (e["humano"] == 1)).sum())
        tn = sel["acc_tn"] + int(((e["y"] == 0) & (e["humano"] == 0)).sum())
        p = tp / (tp + fp) if tp + fp else float("nan")
        r = tp / (tp + fn)
        return {"revisor": nombre, "pendientes": len(e), "aciertos_en_pendientes": int((e["y"] == e["humano"]).sum()),
                "vp": tp, "fp": fp, "fn": fn, "vn": tn, "precision": round(p, 4), "recall": round(r, 4),
                "f1": round(2 * p * r / (p + r), 4)}

    for sesion, g in resp.groupby("sesion"):
        filas.append(sistema(g["participante"].iloc[0], g.set_index("msg_id")["etiqueta"]))
    if n_rev >= 3:
        filas.append(sistema("voto de la mayoría", por_msg.set_index("msg_id")["mayoria"]))
    ideal = final["sistema_con_revision_ideal_simulada"]
    filas.append({"revisor": "revisión ideal simulada (referencia)", "pendientes": len(pend),
                  "aciertos_en_pendientes": len(pend), "vp": ideal["tp"], "fp": ideal["fp"], "fn": ideal["fn"],
                  "vn": ideal["tn"], "precision": round(ideal["precision_spam"], 4),
                  "recall": round(ideal["recall_spam"], 4), "f1": round(ideal["f1_spam"], 4)})
    filas.append({"revisor": "sin revisión (referencia)", "pendientes": 0, "aciertos_en_pendientes": 0,
                  "vp": final["tp"], "fp": final["fp"], "fn": final["fn"], "vn": final["tn"],
                  "precision": round(final["precision_spam"], 4), "recall": round(final["recall_spam"], 4),
                  "f1": round(final["f1_spam"], 4)})
    sistema_df = pd.DataFrame(filas)
    sistema_df.to_csv(OUT / "sistema_con_revision.csv", index=False)

    pd.set_option("display.width", 220, "display.max_columns", 30)
    print(f"Revisores con sesión completa: {n_rev}. Sesiones incompletas descartadas: {len(descartadas)}")
    for titulo, tabla in (("Por revisor", por_revisor), ("Por estrato", por_estrato),
                          ("Sistema con revisión real en prueba", sistema_df)):
        print(f"\n{titulo}\n{tabla.to_string(index=False)}")
    print("\nAcuerdo:", json.dumps(acuerdo, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
