FROM python:3.10-slim

WORKDIR /app

# Instalamos las dependencias declaradas del proyecto.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Gunicorn sirve la aplicacion Flask en un entorno de produccion.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
