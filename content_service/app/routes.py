from fastapi import APIRouter, HTTPException, UploadFile, Form, Depends
from pydantic import BaseModel
from app.models import create_post
from app.utils import verify_jwt_token  # Utility to verify and decode JWT token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# Initialize OAuth2PasswordBearer (for token extraction)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Request Models
class PostContentRequest(BaseModel):
    content_type: str  # 'text' or 'image'
    text_content: str = None  # Only for text posts
    file: UploadFile = None  # Only for image posts

from app.utils import verify_jwt_token  # Import the verify function

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt_token(token)  # Decodes the token
        return payload["user_id"]  # Extract user_id from payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Endpoints
@router.get("/")
def health():
    return {"status": "ok", "status_code": 200}

# Endpoint for creating posts (text or image)
@router.post("/create-post")
async def create_post_endpoint(
    content_type: str = Form(...),
    text_content: str = Form(None),
    file: UploadFile = None,
    user_id: str = Depends(get_current_user)  # Inject user_id
):
    """
    Create a post for the logged-in user.
    """
    # Validate content type
    if content_type == "text":
        if not text_content:
            raise HTTPException(status_code=400, detail="Text content is required for text posts.")
        post_id = create_post(user_id, text_content, "text")
        return {"message": "Text post created successfully", "post_id": post_id}

    elif content_type == "image":
        if not file:
            raise HTTPException(status_code=400, detail="Image file is required for image posts.")
        post_id = create_post(user_id, file, "image")
        return {"message": "Image post created successfully", "post_id": post_id}

    else:
        raise HTTPException(status_code=400, detail="Invalid content type. Please use 'text' or 'image'.")
