"""Pruebas unitarias mínimas del núcleo (ejecutar desde codigo/: python -m pytest -q tests)."""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spam_sms.data import load_sms_collection, grouped_stratified_split, group_key  # noqa: E402
from spam_sms.decision import decide, selective_metrics, select_tau, REVIEW, decision_text  # noqa: E402

ZIP = ROOT.parent / "Dataset" / "sms+spam+collection.zip"


def test_regla_empate_y_umbral():
    y_hat, acc = decide([0.5, 0.7, 0.25, 0.69], tau=0.7)
    assert list(y_hat) == [0, 1, 0, 1]            # empate -> ham; p > 0.5 -> spam
    assert list(acc) == [False, True, True, False]  # c >= tau se acepta; c < tau -> revisión
    assert decision_text(0.5, 0.6) == REVIEW
    _, acc50 = decide([0.5, 0.51], tau=0.5)
    assert acc50.all()                            # con tau = 0.50 no hay abstención


def test_metricas_selectivas():
    m = selective_metrics(np.array([0, 1, 1, 0]), np.array([0.1, 0.9, 0.4, 0.65]), tau=0.7)
    assert m["n_aceptados"] == 2 and m["n_revision"] == 2 and m["errores_aceptados"] == 0


def test_seleccion_tau():
    filas = [{"tau": 0.5, "error_aceptados": 0.02, "tasa_revision": 0.0, "cobertura": 1.0},
             {"tau": 0.7, "error_aceptados": 0.009, "tasa_revision": 0.01, "cobertura": 0.99},
             {"tau": 0.9, "error_aceptados": 0.004, "tasa_revision": 0.05, "cobertura": 0.95}]
    assert select_tau(filas) == {"tau": 0.7, "factible": True}


@pytest.mark.skipif(not ZIP.exists(), reason="requiere el ZIP oficial en ../Dataset")
def test_carga_y_particion_sin_fuga():
    df = load_sms_collection(ZIP)
    assert len(df) == 5574 and int(df.y.sum()) == 747
    tr, va, te = grouped_stratified_split(df, seed=42)
    g = df["text"].map(group_key).to_numpy()
    assert not (set(g[tr]) & set(g[te])) and not (set(g[va]) & set(g[te])) and not (set(g[tr]) & set(g[va]))
    assert abs(len(te) / len(df) - 0.2) < 0.01
