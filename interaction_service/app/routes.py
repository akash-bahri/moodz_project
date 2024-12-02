from fastapi import FastAPI, HTTPException, APIRouter
from app.models import like_post, unlike_post, get_post_likes
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

class LikeRequest(BaseModel):
    post_id: str
    user_id: str

# Endpoints
@router.get("/")
def health():
    return {"status": "ok", "status_code": 200}

@router.post("/like")
def like(request: LikeRequest):
    post_id = request.post_id
    user_id = request.user_id

    success = like_post(post_id, user_id)
    if not success:
        raise HTTPException(status_code=409, detail="User has already liked this post")

    return {"message": "Post liked successfully"}

@router.post("/unlike")
def unlike(request: LikeRequest):
    post_id = request.post_id
    user_id = request.user_id

    success = unlike_post(post_id, user_id)
    if not success:
        raise HTTPException(status_code=409, detail="User has not liked this post")

    return {"message": "Post unliked successfully"}

@router.get("/likes/{post_id}")
def get_likes(post_id: str):
    try:
        count = get_post_likes(post_id)
        return {"post_id": post_id, "likes": count}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

app.include_router(router)