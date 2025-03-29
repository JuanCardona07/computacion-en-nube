import boto3
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

BUCKET_NAME = "mi-bucket-imagenes"
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/XXXXXXXXXXXX/mi-cola"


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = f"{uuid.uuid4()}.jpg"
    s3.upload_fileobj(file, BUCKET_NAME, filename)

    # Enviar el nombre de la imagen a SQS
    sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=filename)

    return jsonify({"message": "File uploaded successfully", "filename": filename})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
