# Usar base slim con versión fija, evitar latest
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar primero requirements.txt e instalar dependencias (aprovechar caché de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código después de las dependencias
COPY process.py .

# Crear usuario sin privilegios y cambiar a él
RUN useradd -m appuser
USER appuser

# CMD en formato exec
CMD ["python", "process.py"]