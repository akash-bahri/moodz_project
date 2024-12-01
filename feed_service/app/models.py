from app import USER_TABLE, POSTS_TABLE
from botocore.exceptions import ClientError


# Get the list of followers for a user
def get_follow_list(user_id: str):
    try:
        response = USER_TABLE.get_item(Key={"id": user_id})
        user = response.get("Item", {})
        return user.get("following", [])
    except ClientError as e:
        raise e


# Fetch posts for a list of user_ids
def get_posts_by_user_ids(user_ids: list):
    posts = []
    try:
        for user_id in user_ids:
            response = POSTS_TABLE.scan(
                FilterExpression="user_id = :user_id",
                ExpressionAttributeValues={":user_id": user_id}
            )
            posts.extend(response.get("Items", []))
        return posts
    except ClientError as e:
        raise e
