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
    
def add_follower(user_id: str, follower_id: str) -> bool:
    """
    Add a follower to the user's followers list, ensuring no duplicates.
    Returns True if the follower was added, False if it already exists.
    """
    try:
        # Get current followers list
        response = USER_TABLE.get_item(Key={"id": user_id})
        user_data = response.get("Item", {})
        followers = user_data.get("followers", [])

        if follower_id in followers:
            return False  # Follower already exists

        followers.append(follower_id)
        # Update the followers list in DynamoDB
        USER_TABLE.update_item(
            Key={"id": user_id},
            UpdateExpression="SET followers = :updated_list",
            ExpressionAttributeValues={":updated_list": followers}
        )
        return True
    except ClientError as e:
        raise e


def add_following(user_id: str, following_id: str) -> bool:
    """
    Add a user to the following list, ensuring no duplicates.
    Returns True if the following was added, False if it already exists.
    """
    try:
        # Get current following list
        response = USER_TABLE.get_item(Key={"id": user_id})
        user_data = response.get("Item", {})
        following = user_data.get("following", [])

        if following_id in following:
            return False  # Following already exists

        following.append(following_id)
        # Update the following list in DynamoDB
        USER_TABLE.update_item(
            Key={"id": user_id},
            UpdateExpression="SET following = :updated_list",
            ExpressionAttributeValues={":updated_list": following}
        )
        return True
    except ClientError as e:
        raise e


def remove_follower(user_id: str, follower_id: str):
    """
    Remove a follower from the user's followers list, if they exist.
    """
    try:
        # Get current followers list
        response = USER_TABLE.get_item(Key={"id": user_id})
        user_data = response.get("Item", {})
        followers = user_data.get("followers", [])

        if follower_id in followers:
            followers.remove(follower_id)
            # Update the followers list in DynamoDB
            USER_TABLE.update_item(
                Key={"id": user_id},
                UpdateExpression="SET followers = :updated_list",
                ExpressionAttributeValues={":updated_list": followers}
            )
    except ClientError as e:
        raise e


def remove_following(user_id: str, following_id: str):
    """
    Remove a user from the following list, if they exist.
    """
    try:
        # Get current following list
        response = USER_TABLE.get_item(Key={"id": user_id})
        user_data = response.get("Item", {})
        following = user_data.get("following", [])

        if following_id in following:
            following.remove(following_id)
            # Update the following list in DynamoDB
            USER_TABLE.update_item(
                Key={"id": user_id},
                UpdateExpression="SET following = :updated_list",
                ExpressionAttributeValues={":updated_list": following}
            )
    except ClientError as e:
        raise e
