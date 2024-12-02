from app import POSTS_TABLE
from botocore.exceptions import ClientError

def like_post(post_id: str, user_id: str):
    try:
        response = POSTS_TABLE.get_item(Key={"post_id": post_id})
        post = response.get("Item")

        if not post:
            raise Exception("Post not found")

        likes = post.get("likes", {"count": 0, "users": []})

        if user_id in likes["users"]:
            return False  # User has already liked the post

        likes["users"].append(user_id)
        likes["count"] += 1

        POSTS_TABLE.update_item(
            Key={"post_id": post_id},
            UpdateExpression="SET likes = :likes",
            ExpressionAttributeValues={":likes": likes}
        )

        return True
    except ClientError as e:
        print(f"Error liking post {post_id}: {e}")
        raise e


def unlike_post(post_id: str, user_id: str):
    try:
        response = POSTS_TABLE.get_item(Key={"post_id": post_id})
        post = response.get("Item")

        if not post:
            raise Exception("Post not found")

        likes = post.get("likes", {"count": 0, "users": []})

        if user_id not in likes["users"]:
            return False  # User has not liked the post

        likes["users"].remove(user_id)
        likes["count"] -= 1

        POSTS_TABLE.update_item(
            Key={"post_id": post_id},
            UpdateExpression="SET likes = :likes",
            ExpressionAttributeValues={":likes": likes}
        )

        return True
    except ClientError as e:
        print(f"Error unliking post {post_id}: {e}")
        raise e


def get_post_likes(post_id: str):
    try:
        response = POSTS_TABLE.get_item(Key={"post_id": post_id})
        post = response.get("Item")

        if not post:
            raise Exception("Post not found")

        likes = post.get("likes", {"count": 0, "users": []})
        return likes["count"]
    except ClientError as e:
        print(f"Error retrieving likes for post {post_id}: {e}")
        raise e
