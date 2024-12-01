from fastapi import FastAPI, HTTPException
from app.models import get_follow_list, get_posts_by_user_ids
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


# Request model for feed generation
class FeedRequest(BaseModel):
    user_id: str


@app.post("/feed")
def generate_feed(request: FeedRequest):
    user_id = request.user_id

    try:
        # Get the follow list of the user
        follow_list = get_follow_list(user_id)
        if not follow_list:
            raise HTTPException(status_code=404, detail="Follow list is empty")

        # Fetch posts for the follow list
        posts = get_posts_by_user_ids(follow_list)

        # Sort posts by created_at (most recent first)
        posts.sort(key=lambda x: x["created_at"], reverse=True)

        # Select the top 10 most recent posts
        feed = posts[:10]

        return {"feed": feed}

    except HTTPException as e:
        raise e
    except Exception as e:
        return {
            "error": "An error occurred while generating the feed. Please refresh the page.",
            "details": str(e),
        }
