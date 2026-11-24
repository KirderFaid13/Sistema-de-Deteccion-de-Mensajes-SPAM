"""Prueba controlada con revisores humanos (módulo de la aplicación).

Cada participante etiqueta, a ciegas, el mismo conjunto fijo de mensajes (`estudio/estimulos.csv`)
en un orden aleatorio propio. No se le muestra la predicción del modelo ni la etiqueta del corpus.
Por cada respuesta se guarda la etiqueta elegida y el tiempo transcurrido desde que el mensaje
apareció en pantalla. No se guarda ningún dato personal: sólo un código de participante.

Rutas:
    GET  /estudio                       instrucciones y consentimiento
    POST /estudio/iniciar               crea la sesión del participante
    GET  /estudio/<sesion>/<posicion>   muestra un mensaje
    POST /estudio/<sesion>/<posicion>   guarda la respuesta y pasa al siguiente
    GET  /estudio/<sesion>/fin          cierre
    GET  /estudio/respuestas.csv        exporta todas las respuestas
"""
from __future__ import annotations

import csv
import io
import random
import sqlite3
import time
from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, abort, current_app, g, redirect, render_template, request, url_for

ESTIMULOS_CSV = Path(__file__).resolve().parents[1] / "estudio" / "estimulos.csv"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS estudio_sesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participante TEXT NOT NULL,                -- código, no el nombre
    tipo TEXT NOT NULL,                        -- integrante | externo
    nivel_ingles TEXT NOT NULL,                -- basico | intermedio | avanzado
    orden TEXT NOT NULL,                       -- msg_id separados por comas, en el orden mostrado
    iniciado_en TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS estudio_respuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sesion_id INTEGER NOT NULL REFERENCES estudio_sesiones(id),
    posicion INTEGER NOT NULL,
    msg_id INTEGER NOT NULL,
    etiqueta INTEGER NOT NULL CHECK (etiqueta IN (0, 1)),   -- 0 = legítimo, 1 = spam
    ms_cliente INTEGER,                        -- tiempo medido en el navegador
    ms_servidor INTEGER NOT NULL,              -- tiempo entre mostrar y recibir, medido en el servidor
    respondido_en TEXT NOT NULL,
    UNIQUE (sesion_id, msg_id)
);
"""

bp = Blueprint("estudio", __name__, url_prefix="/estudio")
_mostrado_en: dict[tuple[int, int], float] = {}     # (sesión, posición) -> instante en que se mostró


def cargar_estimulos() -> dict[int, dict]:
    with open(ESTIMULOS_CSV, encoding="utf-8", newline="") as f:
        return {int(fila["msg_id"]): fila for fila in csv.DictReader(f)}


def db() -> sqlite3.Connection:
    """Usa la misma base SQLite de la aplicación y crea las tablas del estudio si faltan."""
    if "db_estudio" not in g:
        ruta = Path(current_app.config["DB_PATH"])
        ruta.parent.mkdir(parents=True, exist_ok=True)
        g.db_estudio = sqlite3.connect(ruta)
        g.db_estudio.row_factory = sqlite3.Row
        g.db_estudio.executescript(ESQUEMA)
    return g.db_estudio


@bp.teardown_app_request
def cerrar(_exc):
    conn = g.pop("db_estudio", None)
    if conn is not None:
        conn.close()


def ahora() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def orden_de(sesion_id: int) -> list[int]:
    fila = db().execute("SELECT orden FROM estudio_sesiones WHERE id = ?", (sesion_id,)).fetchone()
    if fila is None:
        abort(404)
    return [int(x) for x in fila["orden"].split(",")]


@bp.route("", methods=["GET"])
def inicio():
    return render_template("estudio_inicio.html", n=len(cargar_estimulos()), error=request.args.get("error"))


@bp.route("/iniciar", methods=["POST"])
def iniciar():
    participante = (request.form.get("participante") or "").strip()[:20]
    tipo = request.form.get("tipo")
    nivel = request.form.get("nivel_ingles")
    acepta = request.form.get("consentimiento") == "si"
    if not participante or tipo not in {"integrante", "externo"} or \
            nivel not in {"basico", "intermedio", "avanzado"} or not acepta:
        return redirect(url_for("estudio.inicio", error="1"))
    orden = list(cargar_estimulos())
    random.shuffle(orden)                       # orden distinto para cada participante
    cur = db().execute(
        "INSERT INTO estudio_sesiones (participante, tipo, nivel_ingles, orden, iniciado_en) VALUES (?, ?, ?, ?, ?)",
        (participante, tipo, nivel, ",".join(map(str, orden)), ahora()))
    db().commit()
    return redirect(url_for("estudio.mensaje", sesion_id=cur.lastrowid, posicion=1))


@bp.route("/<int:sesion_id>/<int:posicion>", methods=["GET"])
def mensaje(sesion_id: int, posicion: int):
    orden = orden_de(sesion_id)
    if posicion < 1 or posicion > len(orden):
        return redirect(url_for("estudio.fin", sesion_id=sesion_id))
    _mostrado_en[(sesion_id, posicion)] = time.monotonic()
    texto = cargar_estimulos()[orden[posicion - 1]]["text"]
    return render_template("estudio_mensaje.html", sesion_id=sesion_id, posicion=posicion,
                           total=len(orden), texto=texto)


@bp.route("/<int:sesion_id>/<int:posicion>", methods=["POST"])
def responder(sesion_id: int, posicion: int):
    orden = orden_de(sesion_id)
    etiqueta = request.form.get("etiqueta")
    if posicion < 1 or posicion > len(orden) or etiqueta not in {"0", "1"}:
        return redirect(url_for("estudio.mensaje", sesion_id=sesion_id, posicion=max(1, posicion)))
    inicio_servidor = _mostrado_en.pop((sesion_id, posicion), None)
    ms_servidor = int((time.monotonic() - inicio_servidor) * 1000) if inicio_servidor else -1
    ms_cliente = request.form.get("ms_cliente", type=int)
    db().execute(
        "INSERT OR IGNORE INTO estudio_respuestas (sesion_id, posicion, msg_id, etiqueta, ms_cliente, "
        "ms_servidor, respondido_en) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sesion_id, posicion, orden[posicion - 1], int(etiqueta), ms_cliente, ms_servidor, ahora()))
    db().commit()
    return redirect(url_for("estudio.mensaje", sesion_id=sesion_id, posicion=posicion + 1))


@bp.route("/<int:sesion_id>/fin")
def fin(sesion_id: int):
    hechas = db().execute("SELECT COUNT(*) FROM estudio_respuestas WHERE sesion_id = ?", (sesion_id,)).fetchone()[0]
    return render_template("estudio_fin.html", hechas=hechas, total=len(orden_de(sesion_id)))


@bp.route("/respuestas.csv")
def respuestas_csv():
    filas = db().execute(
        "SELECT s.id AS sesion_id, s.participante, s.tipo, s.nivel_ingles, s.iniciado_en, r.posicion, r.msg_id, "
        "r.etiqueta, r.ms_cliente, r.ms_servidor, r.respondido_en "
        "FROM estudio_respuestas r JOIN estudio_sesiones s ON s.id = r.sesion_id ORDER BY s.id, r.posicion").fetchall()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["sesion_id", "participante", "tipo", "nivel_ingles", "iniciado_en", "posicion", "msg_id",
                "etiqueta", "ms_cliente", "ms_servidor", "respondido_en"])
    for f in filas:
        w.writerow(list(f))
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=respuestas_estudio.csv"})
