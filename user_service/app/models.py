from app import USER_TABLE, FOLLOW_TABLE
from botocore.exceptions import ClientError

# User Table Helpers
def get_user_by_username(username: str):
    try:
        response = USER_TABLE.scan(
            FilterExpression="username = :username",
            ExpressionAttributeValues={":username": username}
        )
        return response.get("Items", [])
    except ClientError as e:
        raise e

def get_user_by_id(user_id: str):
    try:
        response = USER_TABLE.get_item(Key={"id": user_id})
        return response.get("Item")
    except ClientError as e:
        raise e

def create_user(user_data: dict):
    try:
        USER_TABLE.put_item(Item=user_data)
    except ClientError as e:
        raise e

# Follow Table Helpers
def follow_user(follower_id: str, followed_id: str):
    try:
        FOLLOW_TABLE.update_item(
            Key={"follower_id": follower_id},
            UpdateExpression="SET following = list_append(if_not_exists(following, :empty_list), :new_user)",
            ExpressionAttributeValues={":new_user": [followed_id], ":empty_list": []}
        )
    except ClientError as e:
        raise e

def unfollow_user(follower_id: str, followed_id: str):
    try:
        response = FOLLOW_TABLE.get_item(Key={"follower_id": follower_id})
        following = response.get("Item", {}).get("following", [])
        if followed_id in following:
            following.remove(followed_id)
            FOLLOW_TABLE.update_item(
                Key={"follower_id": follower_id},
                UpdateExpression="SET following = :updated_list",
                ExpressionAttributeValues={":updated_list": following}
            )
    except ClientError as e:
        raise e
