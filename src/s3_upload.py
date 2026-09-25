import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

LOCAL_FILE = "raw/youtube_raw.json"
S3_KEY = "raw/youtube_raw.json"


def upload_to_s3():
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION
    )

    s3.upload_file(
        LOCAL_FILE,
        S3_BUCKET_NAME,
        S3_KEY
    )

    print("Successfully uploaded to S3!")
    print(f"s3://{S3_BUCKET_NAME}/{S3_KEY}")


if __name__ == "__main__":
    upload_to_s3()