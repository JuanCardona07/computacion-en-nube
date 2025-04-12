import boto3
import pytesseract
from PIL import Image
import io
import json
import re

s3 = boto3.client('s3')


def extract_data(text):
    receipt_number = re.search(r'Receipt\s*#?:?\s*(\w+)', text, re.IGNORECASE)
    date = re.search(r'\d{2}/\d{2}/\d{4}', text)
    total = re.search(r'Total\s*[:$]?\s*(\d+\.\d{2})', text, re.IGNORECASE)
    restaurant = re.search(r'(?i)([A-Z\s]{3,})(?=\n)', text)

    return {
        "receipt_number": receipt_number.group(1) if receipt_number else None,
        "date": date.group(0) if date else None,
        "total": total.group(1) if total else None,
        "restaurant": restaurant.group(1).strip() if restaurant else None
    }


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    image_bytes = response['Body'].read()
    image = Image.open(io.BytesIO(image_bytes))

    text = pytesseract.image_to_string(image)
    data = extract_data(text)

    output_key = key.replace('.jpg', '.json').replace('entrada', 'salida')
    s3.put_object(
        Bucket='recibos-json-salida',
        Key=output_key,
        Body=json.dumps(data),
        ContentType='application/json'
    )

    return {'statusCode': 200, 'body': json.dumps(data)}
