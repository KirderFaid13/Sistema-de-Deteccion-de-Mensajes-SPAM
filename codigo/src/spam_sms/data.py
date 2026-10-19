"""Carga, diagnóstico y partición del corpus SMS Spam Collection (UCI, DOI 10.24432/C5CC84).

Decisiones documentadas:
- El archivo se lee directamente desde el ZIP oficial, sin modificarlo.
- Se usa csv.QUOTE_NONE: con el comillado por defecto de pandas, las comillas dobles
  internas de algunos mensajes fusionan líneas y se obtienen 5572 filas en lugar de 5574.
- Etiquetas observadas: ham = 0 (legítimo), spam = 1. "Pendiente de revisión" NO es una clase.
- Los mensajes duplicados se agrupan con una clave normalizada (minúsculas y espacios
  colapsados) para que nunca queden en particiones distintas.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

LABEL_MAP = {"ham": 0, "spam": 1}
MEMBER_NAME = "SMSSpamCollection"


def sha256_of(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_sms_collection(zip_path: str | Path) -> pd.DataFrame:
    """Lee el ZIP oficial y devuelve un DataFrame con columnas: label, text, y."""
    with zipfile.ZipFile(zip_path) as zf:
        raw = zf.read(MEMBER_NAME).decode("utf-8")
    df = pd.read_csv(
        io.StringIO(raw),
        sep="\t",
        header=None,
        names=["label", "text"],
        quoting=csv.QUOTE_NONE,
        dtype=str,
        keep_default_na=False,
    )
    if not set(df["label"]).issubset(LABEL_MAP):
        raise ValueError(f"Etiquetas inesperadas: {set(df['label']) - set(LABEL_MAP)}")
    df["y"] = df["label"].map(LABEL_MAP).astype(int)
    df.index.name = "msg_id"
    return df


def group_key(text: str) -> str:
    """Clave para agrupar duplicados: minúsculas y espacios colapsados (no altera el texto modelado)."""
    return re.sub(r"\s+", " ", text.strip().lower())


def diagnose(df: pd.DataFrame) -> dict:
    """Diagnóstico reproducible del corpus."""
    keys = df["text"].map(group_key)
    exact_dup_rows = int(df.duplicated(subset=["text"]).sum())
    norm_dup_rows = int(keys.duplicated().sum())
    labels_per_text = df.groupby("text")["y"].nunique()
    labels_per_key = df.assign(k=keys).groupby("k")["y"].nunique()
    unique = df.drop_duplicates(subset=["text"])
    lengths = df["text"].str.len()
    return {
        "n_mensajes": int(len(df)),
        "n_ham": int((df["y"] == 0).sum()),
        "n_spam": int((df["y"] == 1).sum()),
        "pct_spam": float(df["y"].mean()),
        "mensajes_vacios": int((df["text"].str.strip() == "").sum()),
        "filas_duplicadas_exactas": exact_dup_rows,
        "textos_unicos_exactos": int(df["text"].nunique()),
        "filas_duplicadas_normalizadas": norm_dup_rows,
        "grupos_normalizados": int(keys.nunique()),
        "textos_con_etiquetas_contradictorias": int((labels_per_text > 1).sum()),
        "grupos_normalizados_contradictorios": int((labels_per_key > 1).sum()),
        "unicos_ham": int((unique["y"] == 0).sum()),
        "unicos_spam": int((unique["y"] == 1).sum()),
        "longitud_media_ham": float(lengths[df["y"] == 0].mean()),
        "longitud_media_spam": float(lengths[df["y"] == 1].mean()),
        "longitud_mediana_ham": float(lengths[df["y"] == 0].median()),
        "longitud_mediana_spam": float(lengths[df["y"] == 1].median()),
    }


def grouped_stratified_split(df: pd.DataFrame, seed: int = 42):
    """Partición 60/20/20 estratificada por clase y agrupada por duplicados.

    1) StratifiedGroupKFold(5) -> el primer pliegue es la prueba (~20 %).
    2) Sobre el resto, StratifiedGroupKFold(4) -> el primer pliegue es validación (~20 % del total).
    Devuelve índices posicionales (train, val, test).
    """
    groups = df["text"].map(group_key).to_numpy()
    y = df["y"].to_numpy()
    idx = np.arange(len(df))

    outer = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
    rest, test = next(outer.split(idx, y, groups))

    inner = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=seed)
    tr_rel, va_rel = next(inner.split(rest, y[rest], groups[rest]))
    train, val = rest[tr_rel], rest[va_rel]

    # Verificaciones de no fuga por duplicados
    g_tr, g_va, g_te = set(groups[train]), set(groups[val]), set(groups[test])
    assert not (g_tr & g_va) and not (g_tr & g_te) and not (g_va & g_te), "Duplicados entre particiones"
    assert len(train) + len(val) + len(test) == len(df)
    return np.sort(train), np.sort(val), np.sort(test)
