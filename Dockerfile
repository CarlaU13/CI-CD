# 1. Usamos una imagen base oficial y liviana de Linux con Python 3.10 ya instalado
FROM python:3.10-slim

# 2. Creamos un directorio de trabajo dentro de este contenedor
WORKDIR /app

# 3. Copiamos nuestro código desde tu PC hacia el directorio /app del contenedor
COPY mate.py .

# 4. Definimos el comando que se ejecutará al "encender" el contenedor 
# (Hacemos que imprima el resultado de cebar un mate a 85 grados (la temperatura ideal) para ver que funciona)
CMD ["python", "-c", "import mate; print(mate.cebar_mate(85))"]