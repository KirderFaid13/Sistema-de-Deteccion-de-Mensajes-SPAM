"""Figura del análisis de falsos negativos (lee las tablas de `results/analisis_fn/`).

Ejecutar desde `codigo/` después de `analisis/analisis_falsos_negativos.py`:

    python analisis/figura_falsos_negativos.py
"""
from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "analisis_fn"

# Misma tipografía y colores que las figuras del notebook.
if "EB Garamond" not in {f.name for f in font_manager.fontManager.ttflist}:
    zip_fuentes = ROOT.parent / "Articulo" / "fuentes_EB_Garamond.zip"
    if zip_fuentes.exists():
        tmp = Path(tempfile.mkdtemp())
        zipfile.ZipFile(zip_fuentes).extractall(tmp)
        for ttf in tmp.rglob("*.ttf"):
            font_manager.fontManager.addfont(str(ttf))
fuentes = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams.update({
    "font.family": "EB Garamond" if "EB Garamond" in fuentes else "serif",
    "font.size": 10, "axes.titlesize": 10.5, "axes.labelsize": 10, "legend.fontsize": 9,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e", "ytick.color": "#52514e",
    "axes.grid": True, "grid.color": "#e4e3df", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "savefig.dpi": 300, "savefig.bbox": "tight", "figure.dpi": 110,
})
C_SPAM, C_SVM, C_REV, INK2, NEGRO = "#eb6834", "#1baf7a", "#8a8984", "#52514e", "#0b0b0b"

marc = pd.read_csv(OUT / "recall_por_marcadores.csv")
cat = pd.read_csv(OUT / "categorias_fn.csv")

fig, axs = plt.subplots(1, 2, figsize=(6.5, 3.5), gridspec_kw={"width_ratios": [1, 1.15]})

# a) Recall de spam según cuántos indicadores típicos contiene el mensaje
ax = axs[0]
grupos = ["0", "1", "2 o 3"]
series = [("entrenamiento (fuera de pliegue)", "Entrenamiento (fuera de pliegue)", C_REV),
          ("validación", "Validación", C_SVM), ("prueba", "Prueba (descriptivo)", NEGRO)]
x, ancho = np.arange(len(grupos)), 0.26
for k, (clave, nombre, color) in enumerate(series):
    t = marc[marc["conjunto"] == clave].set_index("marcadores_en_el_mensaje").loc[grupos]
    pos = x + (k - 1) * ancho
    ax.bar(pos, 100 * t["recall"], width=ancho - 0.03, color=color, label=nombre)
    for xi, (_, fila) in zip(pos, t.iterrows()):
        ax.text(xi, 100 * fila["recall"] + 1.5, f"{int(fila['detectado'])}/{int(fila['spam'])}",
                ha="center", va="bottom", fontsize=6.5, color=INK2, rotation=90)
ax.set_xticks(x, grupos)
ax.set_ylim(0, 130); ax.set_yticks([0, 25, 50, 75, 100])
ax.set_xlabel("Indicadores típicos en el mensaje spam")
ax.set_ylabel("Spam detectado (%)")
ax.set_title("a) Detección según los indicadores presentes")
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), frameon=False, fontsize=8, handlelength=1.4)

# b) Falsos negativos de validación y prueba por tipo de mensaje
ax = axs[1]
cat = cat.sort_values("fn")
y = np.arange(len(cat))
revision = cat["fn"] - cat["aceptados_con_confianza"]
ax.barh(y, cat["aceptados_con_confianza"], color=C_SPAM, label="Aceptado con confianza ≥ 0.70")
ax.barh(y, revision, left=cat["aceptados_con_confianza"], color=C_REV, label="Enviado a revisión")
for yi, total in zip(y, cat["fn"]):
    ax.text(total + 0.15, yi, str(int(total)), va="center", fontsize=8.5, color=NEGRO)
etiquetas = [c.replace(" en tono ", "\nen tono ").replace(" de entretenimiento", "\nde entretenimiento")
             .replace(" truncado u ", "\ntruncado u ") for c in cat["categoria"]]
ax.set_yticks(y, etiquetas, fontsize=8)
ax.set_xlim(0, cat["fn"].max() + 1.2)
ax.set_xlabel("Falsos negativos (validación y prueba)")
ax.set_title("b) Tipo de mensaje no detectado")
ax.grid(axis="y", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), frameon=False, fontsize=8, handlelength=1.4)

fig.tight_layout(w_pad=1.2)
for ext in ("png", "svg"):
    fig.savefig(OUT / f"fig_falsos_negativos.{ext}")
print("Figura guardada en", OUT)
