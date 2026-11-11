"""Servicio 1: API principal. Delega almacenamiento y procesamiento en data-service."""
import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# La URL usa el NOMBRE DEL SERVICIO de docker-compose (http://data-service:5001)
DATA_SERVICE_URL = os.environ["DATA_SERVICE_URL"]
API_TOKEN = os.environ["API_TOKEN"]
HEADERS = {"X-API-Token": API_TOKEN}
TIMEOUT = 5


def call_data_service(method, path, **kwargs):
    try:
        resp = requests.request(
            method, f"{DATA_SERVICE_URL}{path}", headers=HEADERS, timeout=TIMEOUT, **kwargs
        )
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException as exc:
        return jsonify(error="data-service unreachable", detail=str(exc)), 502


@app.get("/")
def index():
    return jsonify(
        service="app",
        talks_to=DATA_SERVICE_URL,
        endpoints=["POST /notes", "GET /notes", "GET /summary", "GET /health"],
    )


@app.get("/health")
def health():
    return jsonify(status="ok", service="app")


@app.post("/notes")
def create_note():
    return call_data_service("POST", "/items", json=request.get_json(silent=True) or {})


@app.get("/notes")
def list_notes():
    return call_data_service("GET", "/items")


@app.get("/summary")
def summary():
    return call_data_service("GET", "/stats")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("APP_PORT", "5000")))
