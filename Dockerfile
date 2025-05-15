# Usa la imagen oficial de Python 3.12 slim (menos vulnerabilidades)
FROM python:3.12-slim

# Para evitar buffers
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements y los instala
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el código de la app
COPY . .

# Exponer puerto 8000
EXPOSE 8000

# CMD: migrar y lanzar Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn bookstore_manager.wsgi:application --bind 0.0.0.0:8000"]
