"""Pipelines TF-IDF + clasificador y calibración.

Decisiones de representación (fijadas antes de experimentar, no ajustadas con validación ni prueba):
- Minúsculas: sí. Tildes: se conservan (el corpus está en inglés; no afecta).
- Números, enlaces y símbolos NO se eliminan: los códigos cortos, teléfonos, montos y
  símbolos como £, $, €, !, ? y % son indicios habituales de spam en SMS.
- Patrón de tokens: palabras alfanuméricas de 1 o más caracteres (incluye "u", "2", "4",
  abreviaturas frecuentes en SMS) y los símbolos £ $ € ! ? % & como tokens individuales.
- Vocabulario e IDF se aprenden sólo con los datos de ajuste de cada pliegue / del entrenamiento,
  porque el vectorizador forma parte del Pipeline.
"""
from __future__ import annotations

from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

SEED = 42
TOKEN_PATTERN = r"(?u)\b\w+\b|[£$€!?%&]"

PARAM_GRID = {
    "clf__C": [0.1, 1.0, 10.0],
    "tfidf__ngram_range": [(1, 1), (1, 2)],
}


def make_vectorizer(ngram_range=(1, 1)) -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=True,
        token_pattern=TOKEN_PATTERN,
        ngram_range=ngram_range,
        min_df=1,
        sublinear_tf=False,
        norm="l2",
        use_idf=True,
        smooth_idf=True,
    )


def make_pipeline(algorithm: str, C: float = 1.0, ngram_range=(1, 1)) -> Pipeline:
    if algorithm == "logreg":
        clf = LogisticRegression(C=C, solver="lbfgs", max_iter=2000)
    elif algorithm == "linsvm":
        clf = LinearSVC(C=C, loss="squared_hinge", dual="auto", max_iter=20000, random_state=SEED)
    else:
        raise ValueError(algorithm)
    return Pipeline([("tfidf", make_vectorizer(ngram_range)), ("clf", clf)])


def make_calibrated_svm(C: float, ngram_range, cv_splits) -> CalibratedClassifierCV:
    """SVM lineal + calibración sigmoide (Platt) con validación cruzada agrupada interna.

    cv_splits: lista de (idx_ajuste, idx_calibracion) calculada SOLO sobre el entrenamiento.
    Cada modelo se ajusta en k-1 pliegues y su sigmoide se ajusta en el pliegue excluido;
    la predicción final promedia los k modelos calibrados (ensemble=True).
    """
    base = make_pipeline("linsvm", C=C, ngram_range=ngram_range)
    return CalibratedClassifierCV(estimator=base, method="sigmoid", cv=cv_splits, ensemble=True)
