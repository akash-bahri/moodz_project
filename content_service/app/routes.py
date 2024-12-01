from fastapi import FastAPI, HTTPException
from app.models import create_post, get_posts_by_user
from pydantic import BaseModel
from app import POSTS_TABLE

app = FastAPI()

# Request Models
class CreatePostRequest(BaseModel):
    user_id: str
    content: str

class GetPostsRequest(BaseModel):
    user_id: str

class DeletePostRequest(BaseModel):
    post_id: str

# Endpoints
@app.post("/posts")
def create_post_endpoint(request: CreatePostRequest):
    user_id = request.user_id
    content = request.content

    if not content:
        raise HTTPException(status_code=400, detail="Post content cannot be empty.")

    try:
        post = create_post(user_id, content)
        return {"message": "Post created successfully", "post": post}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the post.")


@app.post("/posts/user")
def get_posts_by_user_endpoint(request: GetPostsRequest):
    post_id = request.post_id

    try:
        posts = get_posts_by_user(post_id)
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching posts.")

@app.delete("/posts/{post_id}/delete")
def delete_post(post_id: str, request: DeletePostRequest):
    try:
        # Check if the post exists
        response = POSTS_TABLE.get_item(Key={"post_id": post_id})
        post = response.get("Item")

        if not post:
            raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found.")

        # Delete the post
        POSTS_TABLE.delete_item(Key={"post_id": post_id})
        return {"message": f"Post with ID {post_id} successfully deleted."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete post: {str(e)}")

