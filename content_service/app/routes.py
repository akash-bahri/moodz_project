from fastapi import FastAPI, HTTPException
from app.models import create_post, get_posts_by_user
from pydantic import BaseModel

app = FastAPI()

# Request Models
class CreatePostRequest(BaseModel):
    user_id: str
    content: str

class GetPostsRequest(BaseModel):
    user_id: str

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
    user_id = request.user_id

    try:
        posts = get_posts_by_user(user_id)
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching posts.")
