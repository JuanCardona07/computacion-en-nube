import boto3
import time

rekognition = boto3.client('rekognition')
sqs = boto3.client('sqs')

SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/XXXXXXXXXXXX/mi-cola"
BUCKET_NAME = "juan-cardonabucket"


def process_images():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=10)

        if 'Messages' in response:
            message = response['Messages'][0]
            filename = message['Body']

            result = rekognition.detect_labels(
                Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': filename}})

            print(f"Resultados para {filename}: {result}")

            sqs.delete_message(QueueUrl=SQS_QUEUE_URL,
                               ReceiptHandle=message['ReceiptHandle'])


if __name__ == "__main__":
    process_images()
