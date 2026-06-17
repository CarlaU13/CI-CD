FROM python:3.10-slim
WORKDIR /app

# Instalamos las dependencias declaradas del proyecto
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Ahora ejecutamos nuestra nueva app en lugar del servidor genérico
CMD ["python", "app.py"]
