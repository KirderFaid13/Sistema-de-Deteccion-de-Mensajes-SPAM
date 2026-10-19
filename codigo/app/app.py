"""Aplicación web (prototipo) para clasificar SMS con abstención y revisión humana.

Ejecutar desde la carpeta `codigo/`:
    python app/app.py
y abrir http://127.0.0.1:5000

Componentes:
- Formulario: el usuario escribe un mensaje.
- Predicción: el pipeline congelado (models/modelo_spam_v1.joblib) estima P(spam);
  la regla de decisión con umbral tau decide: legítimo, spam o pendiente de revisión.
- Bandeja: lista los mensajes pendientes de revisión.
- Revisión: un revisor confirma la etiqueta (ham/spam); se guarda en SQLite.
Guardar revisiones NO reentrena el modelo (el reentrenamiento es una etapa futura).
"""
from __future__ import annotations

import csv
import io
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import joblib
from flask import Flask, Response, g, redirect, render_template, request, url_for

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from spam_sms.decision import AUTO_HAM, AUTO_SPAM, REVIEW, confidence, decide  # noqa: E402

MODEL_PATH = ROOT / "models" / "modelo_spam_v1.joblib"
DB_PATH = Path(__file__).resolve().parent / "instance" / "spam_app.db"
MAX_LEN = 1000

SCHEMA = """
CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto TEXT NOT NULL,
    p_spam REAL NOT NULL,
    confianza REAL NOT NULL,
    etiqueta_modelo INTEGER NOT NULL,          -- 0 = ham, 1 = spam (predicción del modelo)
    decision TEXT NOT NULL,                    -- legitimo | spam | pendiente_revision
    tau REAL NOT NULL,
    version_modelo TEXT NOT NULL,
    creado_en TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS revisiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mensaje_id INTEGER NOT NULL UNIQUE REFERENCES mensajes(id),
    etiqueta_revisor INTEGER NOT NULL CHECK (etiqueta_revisor IN (0, 1)),
    revisor TEXT NOT NULL,
    comentario TEXT,
    revisado_en TEXT NOT NULL
);
"""

app = Flask(__name__)
ARTEFACTO = joblib.load(MODEL_PATH)
MODELO, TAU, VERSION = ARTEFACTO["modelo"], float(ARTEFACTO["tau"]), ARTEFACTO.get("version", "v1")


def db() -> sqlite3.Connection:
    if "db" not in g:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.executescript(SCHEMA)
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def clasificar(texto: str) -> dict:
    p = float(MODELO.predict_proba([texto])[0, 1])
    y_hat, aceptado = decide([p], TAU)
    if not aceptado[0]:
        decision = REVIEW
    else:
        decision = AUTO_SPAM if y_hat[0] == 1 else AUTO_HAM
    return {"p_spam": p, "confianza": float(confidence([p])[0]), "etiqueta_modelo": int(y_hat[0]),
            "decision": decision}


@app.route("/", methods=["GET"])
def inicio():
    n_pend = db().execute(
        "SELECT COUNT(*) FROM mensajes m LEFT JOIN revisiones r ON r.mensaje_id = m.id "
        "WHERE m.decision = ? AND r.id IS NULL", (REVIEW,)).fetchone()[0]
    return render_template("index.html", tau=TAU, version=VERSION, n_pend=n_pend, max_len=MAX_LEN)


@app.route("/clasificar", methods=["POST"])
def clasificar_mensaje():
    texto = (request.form.get("texto") or "").strip()
    if not texto:
        return render_template("index.html", tau=TAU, version=VERSION, n_pend=0, max_len=MAX_LEN,
                               error="Escribe un mensaje antes de clasificar.")
    texto = texto[:MAX_LEN]
    r = clasificar(texto)
    cur = db().execute(
        "INSERT INTO mensajes (texto, p_spam, confianza, etiqueta_modelo, decision, tau, version_modelo, creado_en) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (texto, r["p_spam"], r["confianza"], r["etiqueta_modelo"], r["decision"], TAU, VERSION, now()))
    db().commit()
    return render_template("resultado.html", texto=texto, r=r, tau=TAU, mensaje_id=cur.lastrowid)


@app.route("/pendientes")
def pendientes():
    filas = db().execute(
        "SELECT m.* FROM mensajes m LEFT JOIN revisiones r ON r.mensaje_id = m.id "
        "WHERE m.decision = ? AND r.id IS NULL ORDER BY m.id", (REVIEW,)).fetchall()
    return render_template("pendientes.html", filas=filas, tau=TAU)


@app.route("/revisar/<int:mensaje_id>", methods=["POST"])
def revisar(mensaje_id: int):
    etiqueta = request.form.get("etiqueta")
    revisor = (request.form.get("revisor") or "").strip()[:60] or "revisor_sin_nombre"
    comentario = (request.form.get("comentario") or "").strip()[:300]
    if etiqueta not in {"0", "1"}:
        return redirect(url_for("pendientes"))
    db().execute(
        "INSERT OR IGNORE INTO revisiones (mensaje_id, etiqueta_revisor, revisor, comentario, revisado_en) "
        "VALUES (?, ?, ?, ?, ?)", (mensaje_id, int(etiqueta), revisor, comentario, now()))
    db().commit()
    return redirect(url_for("revisiones"))


@app.route("/revisiones")
def revisiones():
    filas = db().execute(
        "SELECT m.id, m.texto, m.p_spam, m.confianza, m.etiqueta_modelo, r.etiqueta_revisor, r.revisor, "
        "r.comentario, r.revisado_en FROM revisiones r JOIN mensajes m ON m.id = r.mensaje_id ORDER BY r.id DESC"
    ).fetchall()
    return render_template("revisiones.html", filas=filas)


@app.route("/revisiones.csv")
def revisiones_csv():
    filas = db().execute(
        "SELECT m.id, m.texto, m.p_spam, m.etiqueta_modelo, r.etiqueta_revisor, r.revisor, r.revisado_en "
        "FROM revisiones r JOIN mensajes m ON m.id = r.mensaje_id ORDER BY r.id").fetchall()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["mensaje_id", "texto", "p_spam", "etiqueta_modelo", "etiqueta_revisor", "revisor", "revisado_en"])
    for f in filas:
        w.writerow(list(f))
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=revisiones.csv"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
