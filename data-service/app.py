"""Servicio 2: API de datos con SQLite (simula el procesamiento/almacenamiento)."""
import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/data/data.db")
API_TOKEN = os.environ.get("API_TOKEN", "")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS items ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "text TEXT NOT NULL, "
            "created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )


def authorized():
    return API_TOKEN and request.headers.get("X-API-Token") == API_TOKEN


@app.get("/health")
def health():
    return jsonify(status="ok", service="data-service")


@app.post("/items")
def add_item():
    if not authorized():
        return jsonify(error="unauthorized"), 401
    text = (request.get_json(silent=True) or {}).get("text", "").strip()
    if not text:
        return jsonify(error="'text' is required"), 400
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO items (text) VALUES (?)", (text,))
    return jsonify(id=cur.lastrowid, text=text), 201


@app.get("/items")
def list_items():
    if not authorized():
        return jsonify(error="unauthorized"), 401
    with get_conn() as conn:
        rows = conn.execute("SELECT id, text, created_at FROM items ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/stats")
def stats():
    """Procesamiento simulado: cuenta notas y palabras."""
    if not authorized():
        return jsonify(error="unauthorized"), 401
    with get_conn() as conn:
        rows = conn.execute("SELECT text FROM items").fetchall()
    words = sum(len(r["text"].split()) for r in rows)
    longest = max((r["text"] for r in rows), key=len, default=None)
    return jsonify(total_items=len(rows), total_words=words, longest_item=longest)


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("DATA_PORT", "5001")))
