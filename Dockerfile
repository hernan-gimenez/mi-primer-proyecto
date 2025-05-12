FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Configurar PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/static /app/templates

# Copiar archivos estáticos y plantillas
COPY static/ /app/static/
COPY templates/ /app/templates/

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]