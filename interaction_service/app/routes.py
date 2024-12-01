import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
POSTS_TABLE = dynamodb.Table("Posts")
USER_TABLE = dynamodb.Table("Users")

# Request model for feed generation
class LikeRequest(BaseModel):
    user_id: str
    post_id: str

# Request model for feed generation
class LikeRequest(BaseModel):
    user_id: str
    post_id: str

# Helper function to check if a user is following the post author
def is_user_following(user_id: str, post_author_id: str) -> bool:
    try:
        # Fetch the post author from the USER_TABLE to check if the user is in the author's followers list
        user_response = USER_TABLE.get_item(Key={"id": post_author_id})
        if "Item" not in user_response:
            raise HTTPException(status_code=404, detail="Post author not found")
        
        author_item = user_response["Item"]
        followers = author_item.get("followers", [])

        # Return True if the user is in the post author's followers list
        return user_id in followers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/like")
def like_post(request: LikeRequest):
    user_id = request.user_id
    post_id = request.post_id
    try:
        # Fetch the post
        response = POSTS_TABLE.get_item(Key={"post_id": post_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Post not found")

        post_item = response["Item"]
        post_author_id = post_item.get("user_id")  # Get the author of the post
        likes = post_item.get("likes", {})

        # Check if the user is following the post author
        if not is_user_following(user_id, post_author_id):
            raise HTTPException(status_code=403, detail="User must follow the post author to like their post")

        # Ensure 'likes' is a dictionary
        if not isinstance(likes, dict):
            likes = {}  # Reset to an empty dictionary if it's not valid

        # Check if the user has already liked the post
        if user_id in likes:
            return {"message": "User already liked this post"}

        # Add the user to the likes
        likes[user_id] = True  # Using user_id as a key to prevent duplicates

        # Update the post with the new likes
        POSTS_TABLE.update_item(
            Key={"post_id": post_id},
            UpdateExpression="SET likes = :likes",
            ExpressionAttributeValues={
                ":likes": likes,
            },
        )

        return {"message": "Post liked successfully", "total_likes": len(likes)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/unlike")
def unlike_post(request: LikeRequest):
    user_id = request.user_id
    post_id = request.post_id
    try:
        # Fetch the post
        response = POSTS_TABLE.get_item(Key={"post_id": post_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Post not found")

        post_item = response["Item"]
        post_author_id = post_item.get("user_id")  # Get the author of the post
        likes = post_item.get("likes", {})

        # Check if the user is following the post author
        if not is_user_following(user_id, post_author_id):
            raise HTTPException(status_code=403, detail="User must follow the post author to unlike their post")

        # Ensure 'likes' is a dictionary
        if not isinstance(likes, dict):
            likes = {}  # Reset to an empty dictionary if it's not valid

        # Check if the user has not liked the post
        if user_id not in likes:
            return {"message": "User has not liked this post yet"}

        # Remove the user from the likes
        del likes[user_id]

        # Update the post with the new likes
        POSTS_TABLE.update_item(
            Key={"post_id": post_id},
            UpdateExpression="SET likes = :likes",
            ExpressionAttributeValues={
                ":likes": likes,
            },
        )

        return {"message": "Post unliked successfully", "total_likes": len(likes)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")