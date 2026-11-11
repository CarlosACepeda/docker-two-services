# Imagen base oficial con versión fija (no "latest")
FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Usuario sin privilegios + carpeta para la base SQLite
RUN adduser -D appuser && mkdir /data && chown appuser /data
USER appuser

EXPOSE 5001
CMD ["python", "app.py"]
