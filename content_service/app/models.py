from app import POSTS_TABLE, USER_TABLE
from botocore.exceptions import ClientError
from datetime import datetime
import uuid

# Helper Functions for Posts Table

def create_post(user_id: str, content: str):
    """Create a new post."""
    # Check if user exists in the Users table
    try:
        user = USER_TABLE.get_item(Key={"id": user_id}).get("Item")
        if not user:
            raise ValueError(f"User with id {user_id} does not exist.")
    except ClientError as e:
        raise e

    post_id = str(uuid.uuid4())
    post_data = {
        "post_id": post_id,
        "user_id": user_id,
        "content": content,
        "created_at": str(datetime.utcnow()),
    }

    try:
        POSTS_TABLE.put_item(Item=post_data)
        return post_data
    except ClientError as e:
        raise e


def get_posts_by_user(user_id: str):
    """Fetch all posts by a user."""
    try:
        response = POSTS_TABLE.scan(
            FilterExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id},
        )
        return response.get("Items", [])
    except ClientError as e:
        raise e
