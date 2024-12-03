
# import boto3
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()


# aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
# aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
# region_name = os.getenv("AWS_REGION")

# print(f"AWS_ACCESS_KEY_ID: {aws_access_key_id}")
# print(f"AWS_SECRET_ACCESS_KEY: {aws_secret_access_key}")
# print(f"AWS_REGION: {region_name}")


# # Validate environment variables
# if not aws_access_key_id or not aws_secret_access_key:
#     raise ValueError("AWS credentials are missing from environment variables")

# # Initialize DynamoDB resource
# dynamodb = boto3.resource(
#     'dynamodb',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     region_name=region_name
# )
# # Define DynamoDB Tables
# USER_TABLE = dynamodb.Table("Users")

# # Expose resources
# __all__ = ["USER_TABLE", "FOLLOW_TABLE"]

import boto3
import os

# Use the credentials automatically managed by CodeBuild
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

USER_TABLE = dynamodb.Table("Users")

__all__ = ["USER_TABLE"]
