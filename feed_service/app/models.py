import boto3
from botocore.exceptions import ClientError
from app import POSTS_TABLE, USER_TABLE

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Get the following list for a user from the User table
def get_following_list(user_id: str):
    """Fetch the list of users the given user is following"""
    try:
        response = USER_TABLE.get_item(Key={"id": user_id})
        user = response.get("Item")
        if user:
            return user.get("following", [])
        else:
            return []
    except ClientError as e:
        print(f"Error fetching following list for user {user_id}: {e}")
        raise e

def fetch_user_posts(user_id: str, max_posts: int = 10):
    """
    Fetch the posts of a user from the Posts table using scan (no sort key).
    """
    try:
        response = POSTS_TABLE.scan(
            FilterExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id},
            Limit=max_posts  # Optionally limit the number of posts returned
        )
        return response.get("Items", [])
    except ClientError as e:
        print(f"Error fetching posts for user {user_id}: {e}")
        raise e


# Generate the feed for the current user by aggregating posts from users they follow
def generate_feed(user_id: str, max_posts_per_user: int = 10):
    """Generate the feed for the user by fetching posts from the users they follow."""
    following_list = get_following_list(user_id)
    all_posts = []

    # Fetch posts from all users the current user is following
    for followed_user_id in following_list:
        user_posts = fetch_user_posts(followed_user_id, max_posts_per_user)
        all_posts.extend(user_posts)

    # Sort posts by timestamp (latest posts first)
    all_posts.sort(key=lambda x: x["timestamp"], reverse=True)

    return all_posts
