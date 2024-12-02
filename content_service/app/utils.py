import os
import jwt
from fastapi import HTTPException

# Dynamically load the secret key
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")  # Same key as user_service

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # Return the entire payload for more flexibility
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
