import jwt
from datetime import datetime, timedelta
import os
from passlib.context import CryptContext

# Secret key for JWT signing, should be stored securely
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")

# JWT token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a plain password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT access token
def create_access_token(data: dict, expire_minutes: int = 30):
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})  # Add expiration time to the token payload
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


# Function to verify JWT token
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # Decode the token
        return payload["user_id"]  # Return the user_id from the token's payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")  # Token expired
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")  # Token is invalid
