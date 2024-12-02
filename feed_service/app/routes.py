from fastapi import APIRouter, HTTPException
from app.models import generate_feed

router = APIRouter()

# Endpoint to get the feed for the current user
@router.get("/feed")
def get_feed(user_id: str, max_posts_per_user: int = 10):
    """Fetch and aggregate posts for the users the current user is following"""
    try:
        feed = generate_feed(user_id, max_posts_per_user)
        return {"feed": feed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating feed: {str(e)}")
