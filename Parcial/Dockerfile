FROM public.ecr.aws/lambda/python:3.10

# Instalar tesseract directamente
RUN yum -y update && \
    yum -y install tesseract

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar tu código
COPY app.py .

# Definir el handler de Lambda
CMD ["app.lambda_handler"]
