# from flask import Flask
# from app.routes import main

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(main, url_prefix='/user')
#     return app
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
