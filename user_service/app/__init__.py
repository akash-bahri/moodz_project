
import boto3
import os

# Initialize DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Define DynamoDB Tables
USER_TABLE = dynamodb.Table("Users")
FOLLOW_TABLE = dynamodb.Table("Follows")

# Expose resources
__all__ = ["USER_TABLE", "FOLLOW_TABLE"]
