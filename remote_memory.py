import os
import logging
import json
from uuid import uuid4
from dotenv import load_dotenv
import boto3

load_dotenv()

SHARED_OBJECT_NAME = "my_object.json"
AWS_S3_HOST_URI = os.environ.get("AWS_S3_HOST_URI")
AWS_S3_BUCKET_NAME = os.environ.get("S3_PRIVATE_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
)

def read_json_from_s3():
    json_obj = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=SHARED_OBJECT_NAME)
    json_file = json_obj['Body'].read().decode('utf-8')

    return json.loads(json_file)

def upload_json_to_s3(file):
    file_name = SHARED_OBJECT_NAME
    try:
        s3.put_object(
            Bucket=AWS_S3_BUCKET_NAME,
            Key=file_name,
            Body=file
        )
        return file_name
    except Exception as e:
        logging.exception(e)
