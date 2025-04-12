FROM public.ecr.aws/lambda/python:3.10

RUN yum -y install epel-release
RUN yum -y install tesseract

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py . 
CMD ["app.lambda_handler"]
