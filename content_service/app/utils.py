import jwt
import os
from fastapi import HTTPException

# Secret key should be the same as the one used in user_service
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")

# Max file size for image uploads (5MB by default)
MAX_FILE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 5242880))  # 5 MB

# Function to verify JWT token
def verify_jwt_token(token: str):
    """
    Verify the JWT token and return the user_id.
    
    Args:
        token (str): The JWT token to verify.
    
    Returns:
        str: The user_id extracted from the token payload.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # Decode the token
        return payload["user_id"]  # Return the user_id from the token's payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")  # Token expired
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")  # Token is invalid


# Validate file type (only jpeg, png)
def validate_file_type(filename: str, allowed_extensions: list = ["jpg", "jpeg", "png"]):
    file_extension = filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file format. Only JPEG, PNG are allowed.")

# Validate file size
def validate_file_size(file):
    """
    Validate the file size. The file is passed as a `file` object (SpooledTemporaryFile).
    The `file` object's size is calculated by seeking to the end and then checking the position.
    """
    file.seek(0, os.SEEK_END)  # Move to the end of the file
    file_size = file.tell()  # Get the current position, which is the file size
    file.seek(0, os.SEEK_SET)  # Reset the pointer to the beginning of the file
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large. Maximum size is 5MB.")

from app import USER_TABLE

def get_user_from_db(user_id):
    response = USER_TABLE.get_item(Key={"user_id": user_id})
    return response.get("Item")
