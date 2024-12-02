from app import USER_TABLE
from botocore.exceptions import ClientError

# User Table Helpers

def get_user_by_username(username: str):
    """
    Retrieve a user from the USERS table by their username.
    """
    try:
        response = USER_TABLE.scan(
            FilterExpression="username = :username",
            ExpressionAttributeValues={":username": username}
        )
        items = response.get("Items", [])
        if not items:
            return None
        return items[0]  # Return the first matching user
    except ClientError as e:
        print(f"Error retrieving user by username {username}: {e}")
        raise e

def get_user_by_id(user_id: str):
    """
    Retrieve a user from the USERS table by their user ID.
    """
    try:
        response = USER_TABLE.get_item(Key={"id": user_id})
        return response.get("Item")  # Return the full user data
    except ClientError as e:
        print(f"Error retrieving user by ID {user_id}: {e}")
        raise e

def create_user(user_data: dict):
    """
    Create a new user in the USERS table.
    """
    try:
        USER_TABLE.put_item(Item=user_data)
    except ClientError as e:
        print(f"Error creating user: {e}")
        raise e
    
def add_follower(user_id: str, follower_id: str):
    try:
        USER_TABLE.update_item(
            Key={"id": user_id},
            UpdateExpression="SET followers = list_append(if_not_exists(followers, :empty_list), :new_follower)",
            ExpressionAttributeValues={":new_follower": [follower_id], ":empty_list": []}
        )
    except ClientError as e:
        raise e

def add_following(user_id: str, following_id: str):
    try:
        USER_TABLE.update_item(
            Key={"id": user_id},
            UpdateExpression="SET following = list_append(if_not_exists(following, :empty_list), :new_following)",
            ExpressionAttributeValues={":new_following": [following_id], ":empty_list": []}
        )
    except ClientError as e:
        print(f"Error following user {follower_id} -> {followed_id}: {e}")
        raise e

def remove_follower(user_id: str, follower_id: str):
    try:
        response = USER_TABLE.get_item(Key={"id": user_id})
        followers = response.get("Item", {}).get("followers", [])
        if follower_id in followers:
            followers.remove(follower_id)
            USER_TABLE.update_item(
                Key={"id": user_id},
                UpdateExpression="SET followers = :updated_list",
                ExpressionAttributeValues={":updated_list": followers}
            )
    except ClientError as e:
        raise e

def remove_following(user_id: str, following_id: str):
    try:
        response = USER_TABLE.get_item(Key={"id": user_id})
        following = response.get("Item", {}).get("following", [])
        if following_id in following:
            following.remove(following_id)
            USER_TABLE.update_item(
                Key={"id": user_id},
                UpdateExpression="SET following = :updated_list",
                ExpressionAttributeValues={":updated_list": following}
            )
    except ClientError as e:
        print(f"Error unfollowing user {follower_id} -> {followed_id}: {e}")
        raise e