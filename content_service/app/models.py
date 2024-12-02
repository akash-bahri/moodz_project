import boto3
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
import os

# Initialize S3 and DynamoDB clients
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
POSTS_TABLE = dynamodb.Table("Posts")
USER_TABLE = dynamodb.Table("Users")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

def upload_text_to_s3(text_content: str, post_id: str, user_id: str):
    """Upload text content to S3 in the 'text_posts' folder and return the content URL."""
    try:
        file_key = f"text_posts/{user_id}_{post_id}.txt"
        s3_client.put_object(Bucket=S3_BUCKET, Key=file_key, Body=text_content)
        return f"https://{S3_BUCKET}.s3.amazonaws.com/{file_key}"
    except ClientError as e:
        raise Exception(f"Error uploading text to S3: {e}")

def upload_image_to_s3(image_content, post_id: str, user_id: str):
    """Upload an image to S3 in the 'image_posts' folder and return the content URL."""
    try:
        file_key = f"image_posts/{user_id}_{post_id}_{image_content.filename}"
        # Use .file to get the actual file-like object for upload_fileobj
        s3_client.upload_fileobj(image_content.file, S3_BUCKET, file_key)
        return f"https://{S3_BUCKET}.s3.amazonaws.com/{file_key}"
    except ClientError as e:
        raise Exception(f"Error uploading image to S3: {e}")

def create_post(user_id: str, content, content_type: str):
    """
    Create a new post and store the metadata in the Posts table in DynamoDB.
    """
    post_id = str(uuid.uuid4())  # Generate a unique post ID
    timestamp = str(datetime.utcnow())

    # Upload content to S3
    if content_type == "text":
        content_url = upload_text_to_s3(content, post_id, user_id)
    elif content_type == "image":
        content_url = upload_image_to_s3(content, post_id, user_id)

    # Save post metadata to DynamoDB
    try:
        POSTS_TABLE.put_item(
            Item={
                "user_id": user_id,         # User ID (partition key)
                "post_id": post_id,         # Unique post ID (sort key)
                "timestamp": timestamp,     # Timestamp of when the post was created
                "content_url": content_url, # URL of the content (S3 URL)
                "content_type": content_type,  # Content type (image/text)
                "created_at": timestamp     # The creation timestamp
            }
        )
        return post_id
    except ClientError as e:
        print(f"Error storing post metadata: {e}")
        raise e


