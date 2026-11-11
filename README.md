# docker-two-services

Ejercicio Docker con dos contenedores que se comunican **por el nombre de servicio**:

| Servicio | Carpeta | Rol | Puerto |
|---|---|---|---|
| `app` | `app/` | API principal (Flask). Recibe peticiones y las delega. | 5000 (publicado) |
| `data-service` | `data-service/` | API de datos (Flask + SQLite). Guarda y procesa. | 5001 (solo red interna) |

```
cliente --> app:5000 --(http://data-service:5001, red app-net)--> data-service --> SQLite
```

`app` llama a `http://data-service:5001`: el DNS interno de Docker resuelve el nombre del servicio.

## Levantar el proyecto

```bash
cp .env.example .env        # cambiar API_TOKEN por un valor arbitraraio, se usa como ejemplo
docker compose up --build
```

## Probar la comunicación (guardar y leer un dato)

```bash
# Guardar (app -> data-service -> SQLite)
curl -X POST localhost:5000/notes -H 'Content-Type: application/json' -d '{"text":"mi primera nota"}'

# Leer (SQLite -> data-service -> app)
curl localhost:5000/notes

# Procesamiento simulado (conteo de notas y palabras)
curl localhost:5000/summary
```

## Estructura

```
.
├── app/                 # Servicio 1 (Dockerfile, app.py, requirements.txt, .dockerignore)
├── data-service/        # Servicio 2 (Dockerfile, app.py, requirements.txt, .dockerignore)
├── docker-compose.yml
├── .env.example         # plantilla de variables (el .env real va local )
└── .github/workflows/ci.yml
```