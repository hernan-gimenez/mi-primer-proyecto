FROM python:3.9-slim

WORKDIR /app

# Copiar los archivos necesarios
COPY server.py .
COPY index.html .

# Instalar dependencias (solo necesitamos Python estándar)
# No se necesitan dependencias adicionales

# Puerto expuesto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]
