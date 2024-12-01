import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# AWS DynamoDB Setup
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION")

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
)

# Define DynamoDB Table for Posts
POSTS_TABLE = dynamodb.Table("Posts")
USER_TABLE = dynamodb.Table("Users")

# Expose resources
__all__ = ["USER_TABLE", "POSTS_TABLE"]
