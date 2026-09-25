import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION")
)

bucket = os.getenv("S3_BUCKET_NAME")

response = s3.list_objects_v2(Bucket=bucket)

print("Successfully connected to S3!")
print("Bucket:", bucket)
print("Objects:", response.get("KeyCount", 0))