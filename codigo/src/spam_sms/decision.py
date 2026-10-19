"""Regla de decisión con abstención (clasificación selectiva) y métricas asociadas.

Definiciones:
- p1 = P(spam | x) estimada por el modelo calibrado; p0 = 1 - p1.
- Confianza c(x) = max(p0, p1).
- Si c(x) < tau -> "pendiente de revisión" (abstención). Si c(x) >= tau -> decisión automática.
- Etiqueta automática: spam (1) si p1 > 0.5; en caso contrario ham (0).
  Empate p1 == 0.5: se asigna ham (0) y, como c = 0.5 < tau para todo tau > 0.5, el mensaje
  se envía a revisión. Con tau = 0.50 no hay abstención posible (c >= 0.5 siempre).
"""
from __future__ import annotations

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

TAU_GRID = (0.50, 0.60, 0.70, 0.80, 0.90, 0.95)

AUTO_HAM = "legitimo"
AUTO_SPAM = "spam"
REVIEW = "pendiente_revision"


def predict_label(p_spam):
    p_spam = np.asarray(p_spam, dtype=float)
    return (p_spam > 0.5).astype(int)


def confidence(p_spam):
    p_spam = np.asarray(p_spam, dtype=float)
    return np.maximum(p_spam, 1.0 - p_spam)


def decide(p_spam, tau: float):
    """Devuelve (etiqueta_predicha, aceptado) para cada mensaje."""
    y_hat = predict_label(p_spam)
    accepted = confidence(p_spam) >= tau
    return y_hat, accepted


def decision_text(p_spam: float, tau: float) -> str:
    y_hat, acc = decide([p_spam], tau)
    if not acc[0]:
        return REVIEW
    return AUTO_SPAM if y_hat[0] == 1 else AUTO_HAM


def binary_metrics(y_true, y_pred) -> dict:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "n": int(len(y_true)),
        "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
        "precision_spam": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall_spam": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "f1_spam": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "precision_ham": float(precision_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "recall_ham": float(recall_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "f1_ham": float(f1_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "accuracy": float((y_true == y_pred).mean()) if len(y_true) else float("nan"),
    }


def selective_metrics(y_true, p_spam, tau: float) -> dict:
    """Métricas de clasificación selectiva para un umbral tau."""
    y_true = np.asarray(y_true)
    y_hat, acc = decide(p_spam, tau)
    n = len(y_true)
    n_acc = int(acc.sum())
    out = {
        "tau": float(tau),
        "n_total": int(n),
        "n_aceptados": n_acc,
        "n_revision": int(n - n_acc),
        "cobertura": n_acc / n if n else float("nan"),
        "tasa_revision": (n - n_acc) / n if n else float("nan"),
        "aceptados_ham": int(((y_true == 0) & acc).sum()),
        "aceptados_spam": int(((y_true == 1) & acc).sum()),
        "revision_ham": int(((y_true == 0) & ~acc).sum()),
        "revision_spam": int(((y_true == 1) & ~acc).sum()),
        "errores_aceptados": int(((y_hat != y_true) & acc).sum()),
        "errores_en_revision_si_automatico": int(((y_hat != y_true) & ~acc).sum()),
    }
    out["error_aceptados"] = out["errores_aceptados"] / n_acc if n_acc else float("nan")
    m = binary_metrics(y_true[acc], y_hat[acc]) if n_acc else {}
    for k, v in m.items():
        out[f"acc_{k}"] = v
    return out


def select_tau(rows: list[dict], max_error: float = 0.010, max_review: float = 0.15) -> dict:
    """Regla preregistrada para elegir tau en VALIDACIÓN.

    1) Factibles: error entre aceptados <= max_error y tasa de revisión <= max_review.
    2) Entre factibles, máxima cobertura; empate -> menor tau.
    3) Si no hay factibles: entre los tau con revisión <= max_review, menor error entre
       aceptados; empate -> menor tau.
    """
    feas = [r for r in rows if r["error_aceptados"] <= max_error and r["tasa_revision"] <= max_review]
    if feas:
        best = sorted(feas, key=lambda r: (-r["cobertura"], r["tau"]))[0]
        return {"tau": best["tau"], "factible": True}
    cand = [r for r in rows if r["tasa_revision"] <= max_review]
    best = sorted(cand, key=lambda r: (r["error_aceptados"], r["tau"]))[0]
    return {"tau": best["tau"], "factible": False}
