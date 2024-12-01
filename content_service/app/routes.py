from fastapi import APIRouter, HTTPException, UploadFile, Form, Depends, Header
from typing import Union
from .models import upload_to_s3, save_text_to_s3
from .utils import validate_file_type, validate_file_size, verify_jwt_token
import uuid
from datetime import datetime

# Initialize the APIRouter
router = APIRouter()

def get_current_user(authorization: str = Header(...)):
    """
    Get the current user from the JWT token in the Authorization header.
    """
    token = authorization.split("Bearer ")[-1]  # Extract token from the Bearer scheme
    user_id = verify_jwt_token(token)  # Verify the JWT token
    return user_id

@router.post("/create-post")
async def create_post(
    content_type: str = Form(...),  # Required form field
    file: Union[UploadFile, None] = None,  # Optional file for image posts
    text_content: Union[str, None] = Form(None),  # Optional form field for text posts
    current_user: str = Depends(get_current_user)  # Get the current user from the token
):
    """
    Endpoint to create a new post (text or image), only accessible to logged-in users.
    """
    # Debugging logs
    print(f"DEBUG: Received content_type={content_type}, file={file}, text_content={text_content}, user_id={current_user}")

    # Handle text post
    if content_type == "text" and text_content:
        post_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        # Save text content to S3 as a .txt file
        filename = f"text_posts/{post_id}.txt"
        file_url = save_text_to_s3(text_content, filename)

        return {"post_id": post_id, "timestamp": timestamp, "file_url": file_url}

    # Handle image post
    elif content_type == "image" and file:
        # Validate file type and size
        validate_file_type(file.filename)
        validate_file_size(file.file)

        # Generate a unique filename and upload to S3
        filename = f"image_posts/{uuid.uuid4()}_{file.filename}"
        file_url = upload_to_s3(file.file, filename)

        post_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        return {"post_id": post_id, "timestamp": timestamp, "file_url": file_url}

    # If no valid content type or content provided
    else:
        raise HTTPException(status_code=400, detail="Invalid content type or missing content.")