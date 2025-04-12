FROM python:3.10-slim-bullseye

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr-eng \
    poppler-utils \
    && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Comando para ejecución
CMD ["python", "app.py"]
