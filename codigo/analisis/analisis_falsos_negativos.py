"""Análisis de los falsos negativos que el modelo congelado acepta con confianza alta.

Ejecutar desde `codigo/`, con el entorno de `requirements.txt`:

    python analisis/analisis_falsos_negativos.py

Es un análisis DESCRIPTIVO Y EXPLORATORIO posterior a la evaluación final:
- No modifica el modelo congelado, el umbral ni ningún archivo previo de `results/`.
- La partición de prueba sólo se describe; no se usa para elegir nada.
- Las comparaciones de configuraciones alternativas (sección 4) usan únicamente
  entrenamiento (predicciones fuera de pliegue) y validación.

Salidas en `results/analisis_fn/`.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spam_sms.data import group_key, load_sms_collection  # noqa: E402
from spam_sms.decision import binary_metrics, confidence, selective_metrics  # noqa: E402
from spam_sms.modeling import SEED, TOKEN_PATTERN, make_calibrated_svm, make_vectorizer  # noqa: E402

OUT = ROOT / "results" / "analisis_fn"
OUT.mkdir(parents=True, exist_ok=True)

# Los tres indicadores textuales descritos en el diagnóstico del corpus (Tabla 8 del artículo).
RE_ENLACE = re.compile(r"http|www|\.com", re.I)
RE_DIGITOS = re.compile(r"\d{5,}")
RE_MONEDA = re.compile(r"[£$€]")


def marcadores(texto: str) -> dict:
    m = {"enlace": bool(RE_ENLACE.search(texto)), "digitos_5mas": bool(RE_DIGITOS.search(texto)),
         "moneda": bool(RE_MONEDA.search(texto))}
    m["n_marcadores"] = sum(m.values())
    return m


def pliegues_agrupados(textos, y, n_splits, seed=SEED):
    grupos = np.array([group_key(t) for t in textos])
    cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    return list(cv.split(np.arange(len(y)), y, grupos))


def svm_calibrada(vectorizador, C, cv_splits):
    base = Pipeline([("vec", vectorizador),
                     ("clf", LinearSVC(C=C, loss="squared_hinge", dual="auto", max_iter=20000, random_state=SEED))])
    return CalibratedClassifierCV(estimator=base, method="sigmoid", cv=cv_splits, ensemble=True)


def vec_palabras():
    return make_vectorizer((1, 2))


def vec_caracteres():
    return TfidfVectorizer(lowercase=True, analyzer="char_wb", ngram_range=(2, 5), min_df=1,
                           sublinear_tf=False, norm="l2", use_idf=True, smooth_idf=True)


def vec_union():
    return FeatureUnion([("palabras", vec_palabras()), ("caracteres", vec_caracteres())])


def similitud_maxima(vectorizador_ajustado, textos_ref, textos):
    """Mayor similitud coseno de cada texto con los mensajes de referencia (TF-IDF con norma L2)."""
    ref = vectorizador_ajustado.transform(textos_ref)
    x = vectorizador_ajustado.transform(textos)
    sim = (x @ ref.T).tocsr()
    maximo = np.zeros(x.shape[0])
    indice = np.zeros(x.shape[0], dtype=int)
    for i in range(x.shape[0]):
        fila = sim.getrow(i)
        if fila.nnz:
            j = fila.data.argmax()
            maximo[i], indice[i] = fila.data[j], fila.indices[j]
    return maximo, indice


def fuera_de_pliegue(constructor, C, textos, y, con_similitud=False):
    """Probabilidades del entrenamiento obtenidas sin que el modelo haya visto cada mensaje."""
    p = np.zeros(len(y))
    sim = np.zeros(len(y))
    for ajuste, excluido in pliegues_agrupados(textos, y, 5):
        internos = pliegues_agrupados(textos[ajuste], y[ajuste], 4)
        modelo = svm_calibrada(constructor(), C, internos).fit(textos[ajuste], y[ajuste])
        p[excluido] = modelo.predict_proba(textos[excluido])[:, 1]
        if con_similitud:
            v = vec_palabras().fit(textos[ajuste])
            sim[excluido], _ = similitud_maxima(v, textos[ajuste], textos[excluido])
    return (p, sim) if con_similitud else p


def contribuciones(modelo, texto: str, k: int = 4):
    """Términos que más empujan la decisión, promediando los cinco clasificadores calibrados.

    Cada clasificador calcula f(x) = w·x + b y su sigmoide p = 1 / (1 + exp(a·f + b')).
    La contribución de un término al logit de spam es -a · w_t · x_t.
    """
    total: dict[str, float] = {}
    desconocidos = []
    n = len(modelo.calibrated_classifiers_)
    for cc in modelo.calibrated_classifiers_:
        tfidf, clf = cc.estimator.named_steps["tfidf"], cc.estimator.named_steps["clf"]
        a = cc.calibrators[0].a_
        x = tfidf.transform([texto])
        nombres = tfidf.get_feature_names_out()
        for j, valor in zip(x.indices, x.data):
            total[nombres[j]] = total.get(nombres[j], 0.0) + (-a * clf.coef_[0, j] * valor) / n
        unigramas = [t for t in tfidf.build_analyzer()(texto) if " " not in t]
        desconocidos.append(np.mean([t not in tfidf.vocabulary_ for t in unigramas]) if unigramas else 0.0)
    orden = sorted(total.items(), key=lambda kv: kv[1])
    hacia_ham = [f"{t} ({v:+.2f})" for t, v in orden[:k] if v < 0]
    hacia_spam = [f"{t} ({v:+.2f})" for t, v in orden[::-1][:k] if v > 0]
    return "; ".join(hacia_ham), "; ".join(hacia_spam), float(np.mean(desconocidos))


def main() -> None:
    df = load_sms_collection(ROOT.parent / "Dataset" / "sms+spam+collection.zip")
    part = pd.read_csv(ROOT / "results" / "particiones.csv")
    assert (part["msg_id"].to_numpy() == np.arange(len(df))).all()
    df["particion"] = part["particion"].replace({"validacion": "validación"}).to_numpy()
    df = pd.concat([df, pd.DataFrame([marcadores(t) for t in df["text"]])], axis=1)

    artefacto = joblib.load(ROOT / "models" / "modelo_spam_v1.joblib")
    modelo, tau = artefacto["modelo"], float(artefacto["tau"])

    tr = (df["particion"] == "entrenamiento").to_numpy()
    X, y = df["text"].to_numpy(), df["y"].to_numpy()

    # ---------- 1. Probabilidades por partición ----------
    df["p"] = np.nan
    df["sim_max"] = np.nan
    for nombre in ("validación", "prueba"):
        m = (df["particion"] == nombre).to_numpy()
        df.loc[m, "p"] = modelo.predict_proba(X[m])[:, 1]
    v_tr = vec_palabras().fit(X[tr])
    for nombre in ("validación", "prueba"):
        m = (df["particion"] == nombre).to_numpy()
        df.loc[m, "sim_max"], _ = similitud_maxima(v_tr, X[tr], X[m])
    p_oof, sim_oof = fuera_de_pliegue(vec_palabras, 10.0, X[tr], y[tr], con_similitud=True)
    df.loc[tr, "p"], df.loc[tr, "sim_max"] = p_oof, sim_oof
    df["conjunto"] = df["particion"].replace({"entrenamiento": "entrenamiento (fuera de pliegue)"})
    df["pred"] = (df["p"] > 0.5).astype(int)
    df["confianza"] = confidence(df["p"].to_numpy())
    df["aceptado"] = df["confianza"] >= tau
    df["fn"] = (df["y"] == 1) & (df["pred"] == 0)
    df["fn_confiado"] = df["fn"] & df["aceptado"]

    conjuntos = ["entrenamiento (fuera de pliegue)", "validación", "prueba"]

    # ---------- 2. Recall de spam según los marcadores presentes ----------
    filas = []
    for c in conjuntos + ["los tres"]:
        d = df if c == "los tres" else df[df["conjunto"] == c]
        s = d[d["y"] == 1]
        for etiqueta, sel in (("0", s["n_marcadores"] == 0), ("1", s["n_marcadores"] == 1),
                              ("2 o 3", s["n_marcadores"] >= 2), ("todos", s["n_marcadores"] >= 0)):
            g = s[sel]
            filas.append({"conjunto": c, "marcadores_en_el_mensaje": etiqueta, "spam": len(g),
                          "detectado": int((g["pred"] == 1).sum()), "fn": int(g["fn"].sum()),
                          "fn_confianza_ge_tau": int(g["fn_confiado"].sum()),
                          "recall": float((g["pred"] == 1).mean()) if len(g) else np.nan,
                          "pct_del_spam": len(g) / len(s) if len(s) else np.nan})
    tabla_marcadores = pd.DataFrame(filas)
    tabla_marcadores.to_csv(OUT / "recall_por_marcadores.csv", index=False)

    # Contrapartida en mensajes legítimos: ¿los marcadores provocan falsos positivos?
    filas = []
    for c in conjuntos + ["los tres"]:
        d = df if c == "los tres" else df[df["conjunto"] == c]
        h = d[d["y"] == 0]
        for etiqueta, sel in (("0", h["n_marcadores"] == 0), ("1 o más", h["n_marcadores"] >= 1)):
            g = h[sel]
            filas.append({"conjunto": c, "marcadores_en_el_mensaje": etiqueta, "ham": len(g),
                          "fp": int((g["pred"] == 1).sum()),
                          "tasa_fp": float((g["pred"] == 1).mean()) if len(g) else np.nan})
    pd.DataFrame(filas).to_csv(OUT / "falsos_positivos_por_marcadores.csv", index=False)

    # ---------- 3. Detalle de cada falso negativo de validación y prueba ----------
    etiquetas_tr = y[tr]
    detalle = []
    for i, r in df[df["fn"] & df["particion"].isin(["validación", "prueba"])].iterrows():
        hacia_ham, hacia_spam, desconocidos = contribuciones(modelo, r["text"])
        sim, idx = similitud_maxima(v_tr, X[tr], np.array([r["text"]]))
        detalle.append({"msg_id": i, "particion": r["particion"], "p_spam": round(r["p"], 4),
                        "confianza": round(r["confianza"], 4),
                        "destino": "automático" if r["aceptado"] else "revisión",
                        "longitud": len(r["text"]), "enlace": r["enlace"], "digitos_5mas": r["digitos_5mas"],
                        "moneda": r["moneda"], "pct_palabras_desconocidas": round(desconocidos, 3),
                        "vecino_mas_parecido_clase": "spam" if etiquetas_tr[idx[0]] == 1 else "ham",
                        "vecino_similitud": round(float(sim[0]), 3),
                        "terminos_hacia_legitimo": hacia_ham, "terminos_hacia_spam": hacia_spam,
                        "text": r["text"]})
    detalle = pd.DataFrame(detalle).sort_values(["particion", "p_spam"])
    cod_path = Path(__file__).resolve().parent / "codificacion_fn.csv"
    if cod_path.exists():      # codificación cualitativa hecha por el grupo
        detalle = detalle.merge(pd.read_csv(cod_path), on="msg_id", how="left")
        detalle["sin_marcadores"] = ~(detalle["enlace"] | detalle["digitos_5mas"] | detalle["moneda"])
        (detalle.groupby("categoria")
         .agg(fn=("msg_id", "size"), validacion=("particion", lambda s: int((s == "validación").sum())),
              prueba=("particion", lambda s: int((s == "prueba").sum())),
              aceptados_con_confianza=("destino", lambda s: int((s == "automático").sum())),
              sin_marcadores=("sin_marcadores", "sum"), p_spam_mediana=("p_spam", "median"))
         .sort_values("fn", ascending=False).reset_index()
         .to_csv(OUT / "categorias_fn.csv", index=False))
    detalle.to_csv(OUT / "falsos_negativos_detalle.csv", index=False)

    # ---------- 4. ¿La novedad distingue los falsos negativos confiados? ----------
    # Entre los mensajes aceptados como legítimos, ¿los que eran spam se parecen menos al entrenamiento?
    filas = []
    for c in conjuntos + ["los tres"]:
        d = df if c == "los tres" else df[df["conjunto"] == c]
        a = d[d["aceptado"] & (d["pred"] == 0)]
        n_fn = int(a["fn"].sum())
        fila = {"conjunto": c, "aceptados_como_legitimos": len(a), "fn_confiados": n_fn,
                "auc_novedad": float(roc_auc_score(a["fn"], -a["sim_max"])) if 0 < n_fn < len(a) else np.nan,
                "sim_mediana_fn": float(a.loc[a["fn"], "sim_max"].median()),
                "sim_mediana_legitimos": float(a.loc[~a["fn"], "sim_max"].median())}
        orden = a.sort_values("sim_max")          # del más novedoso al menos
        for pct in (1, 5, 10, 20):
            k = int(np.ceil(len(a) * pct / 100))
            fila[f"fn_recuperados_revisando_{pct}pct"] = int(orden["fn"].head(k).sum())
        filas.append(fila)
    tabla_novedad = pd.DataFrame(filas)
    tabla_novedad.to_csv(OUT / "novedad_fn_confiados.csv", index=False)

    # ---------- 5. Configuraciones alternativas (exploratorio; sin la prueba) ----------
    va = (df["particion"] == "validación").to_numpy()
    configuraciones = [("palabras (1,2), C=10 [congelada]", vec_palabras, 10.0),
                       ("palabras (1,2), C=30", vec_palabras, 30.0),
                       ("palabras (1,2), C=100", vec_palabras, 100.0),
                       ("caracteres (2-5), C=1", vec_caracteres, 1.0),
                       ("caracteres (2-5), C=10", vec_caracteres, 10.0),
                       ("palabras + caracteres, C=10", vec_union, 10.0)]
    filas = []
    for nombre, constructor, C in configuraciones:
        p_tr = p_oof if nombre.endswith("[congelada]") else fuera_de_pliegue(constructor, C, X[tr], y[tr])
        m_va = svm_calibrada(constructor(), C, pliegues_agrupados(X[tr], y[tr], 5)).fit(X[tr], y[tr])
        for conjunto, yy, pp in (("entrenamiento (fuera de pliegue)", y[tr], p_tr),
                                 ("validación", y[va], m_va.predict_proba(X[va])[:, 1])):
            b = binary_metrics(yy, (pp > 0.5).astype(int))
            s = selective_metrics(yy, pp, tau)
            filas.append({"configuracion": nombre, "conjunto": conjunto, "n": len(yy),
                          "fp": b["fp"], "fn": b["fn"], "precision": b["precision_spam"],
                          "recall": b["recall_spam"], "f1": b["f1_spam"],
                          "revision_tau": s["n_revision"], "errores_aceptados_tau": s["errores_aceptados"],
                          "fn_confiados_tau": s["acc_fn"], "fp_confiados_tau": s["acc_fp"]})
    tabla_alt = pd.DataFrame(filas)
    tabla_alt.to_csv(OUT / "configuraciones_alternativas.csv", index=False)

    # Comprobación: el modelo congelado reproduce las cifras ya publicadas.
    te = df[df["particion"] == "prueba"]
    resumen = {
        "tau": tau,
        "comprobacion_prueba": {"fn": int(te["fn"].sum()), "fn_confiados": int(te["fn_confiado"].sum()),
                                "fp": int(((te["y"] == 0) & (te["pred"] == 1)).sum())},
        "spam_sin_marcadores_pct": float((df.loc[df["y"] == 1, "n_marcadores"] == 0).mean()),
        "nota": "Análisis descriptivo y exploratorio; no altera el modelo ni las decisiones congeladas.",
    }
    (OUT / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")

    pd.set_option("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 60)
    print(tabla_marcadores.round(3).to_string(index=False))
    print(tabla_novedad.round(3).to_string(index=False))
    print(tabla_alt.round(3).to_string(index=False))
    print(json.dumps(resumen, ensure_ascii=False))


if __name__ == "__main__":
    main()
