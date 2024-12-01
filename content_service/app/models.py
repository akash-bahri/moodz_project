import boto3
import os
from botocore.exceptions import ClientError

# Load environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def upload_to_s3(file, filename):
    """Upload a file to S3 and return the file URL."""
    try:
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename)
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return file_url
    except ClientError as e:
        raise Exception(f"Error uploading file to S3: {e}")

def save_text_to_s3(text_content, filename):
    """Save text content as a .txt file in S3."""
    try:
        # Convert text content to bytes
        file_data = text_content.encode("utf-8")
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=file_data)
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return file_url
    except ClientError as e:
        raise Exception(f"Error saving text to S3: {e}")
