
FROM python:3.10
WORKDIR /app
COPY app.py /app/
RUN pip install flask boto3
EXPOSE 5000
CMD ["python", "app.py"]
