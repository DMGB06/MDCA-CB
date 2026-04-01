# ¿Qué sistema base usar?
# python:3.13-slim = Python 3.13 sobre Linux minimalista
# "slim" significa que pesa mucho menos que la versión completa
FROM python:3.13-slim

# Necesario para que Linux no pregunte cosas 
# durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# ¿Dónde dentro del contenedor va tu código?
# Es como decir "trabaja en esta carpeta"
WORKDIR /app

# Primero copia solo las dependencias
# Esto es un truco para que Docker no reinstale todo
# cada vez que cambias tu código
COPY pyproject.toml .

# Instala las dependencias de tu proyecto
RUN pip install --no-cache-dir .

# Ahora sí copia todo el código
COPY . .

# Le dice a Docker que tu app usa el puerto 8000
EXPOSE 8000

# El comando que arranca tu servidor cuando el contenedor inicia
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


