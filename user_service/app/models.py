from app import USER_TABLE, FOLLOW_TABLE
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


# Follow Table Helpers

def update_following_list(user_id: str, target_user_id: str, action: str):
    """
    Update the `following` list for a user.
    """
    try:
        if action == "add":
            # Add the target_user_id to the `following` list
            USER_TABLE.update_item(
                Key={"id": user_id},
                UpdateExpression="SET following = list_append(if_not_exists(following, :empty_list), :target)",
                ExpressionAttributeValues={
                    ":target": [target_user_id],
                    ":empty_list": []
                }
            )
        elif action == "remove":
            # Fetch the current following list
            response = USER_TABLE.get_item(Key={"id": user_id})
            user = response.get("Item")
            if not user or "following" not in user:
                return  # No following list to update

            following = user["following"]
            if target_user_id in following:
                following.remove(target_user_id)  # Remove the target_user_id
                # Update the `following` list
                USER_TABLE.update_item(
                    Key={"id": user_id},
                    UpdateExpression="SET following = :updated_list",
                    ExpressionAttributeValues={":updated_list": following}
                )
    except ClientError as e:
        print(f"Error updating following list for {user_id}: {e}")
        raise e

def update_follower_list(user_id: str, follower_id: str, action: str):
    """
    Update the `followers` list for a user.
    """
    try:
        if action == "add":
            # Add the follower_id to the `followers` list
            USER_TABLE.update_item(
                Key={"id": user_id},
                UpdateExpression="SET followers = list_append(if_not_exists(followers, :empty_list), :follower)",
                ExpressionAttributeValues={
                    ":follower": [follower_id],
                    ":empty_list": []
                }
            )
        elif action == "remove":
            # Fetch the current followers list
            response = USER_TABLE.get_item(Key={"id": user_id})
            user = response.get("Item")
            if not user or "followers" not in user:
                return  # No followers list to update

            followers = user["followers"]
            if follower_id in followers:
                followers.remove(follower_id)  # Remove the follower_id
                # Update the `followers` list
                USER_TABLE.update_item(
                    Key={"id": user_id},
                    UpdateExpression="SET followers = :updated_list",
                    ExpressionAttributeValues={":updated_list": followers}
                )
    except ClientError as e:
        print(f"Error updating followers list for {user_id}: {e}")
        raise e


# Follow User Helpers (in case you are maintaining a separate table for followers/followed)

def follow_user(follower_id: str, followed_id: str):
    """
    Update the FOLLOW_TABLE when a user follows another user.
    """
    try:
        FOLLOW_TABLE.update_item(
            Key={"follower_id": follower_id},
            UpdateExpression="SET following = list_append(if_not_exists(following, :empty_list), :new_user)",
            ExpressionAttributeValues={":new_user": [followed_id], ":empty_list": []}
        )
    except ClientError as e:
        print(f"Error following user {follower_id} -> {followed_id}: {e}")
        raise e

def unfollow_user(follower_id: str, followed_id: str):
    """
    Update the FOLLOW_TABLE when a user unfollows another user.
    """
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
        print(f"Error unfollowing user {follower_id} -> {followed_id}: {e}")
        raise e
