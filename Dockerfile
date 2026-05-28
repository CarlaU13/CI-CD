FROM python:3.10-slim
WORKDIR /app
COPY . .

# Instalamos Flask en el momento de crear la imagen
RUN pip install flask

EXPOSE 8000

# Ahora ejecutamos nuestra nueva app en lugar del servidor genérico
CMD ["python", "app.py"]