from fastapi import FastAPI, HTTPException, APIRouter
from app.models import get_user_by_username, get_user_by_id, create_user, add_follower, add_following, remove_follower, remove_following, add_follower, add_following, remove_follower, remove_following
from app.utils import hash_password, verify_password, create_access_token
import uuid
from datetime import datetime
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Define the APIRouter for handling routes
router = APIRouter()

# Request Models

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class GetUserRequest(BaseModel):
    username: str

class FollowRequest(BaseModel):
    follower_id: str
    followed_id: str

class FollowRequest(BaseModel):
    follower_id: str
    followed_id: str

# Endpoints
@router.get("/")
def health():
    return {"status": "ok", "status_code": 200}

@router.post("/register")
def register(request: RegisterRequest):
    """
    Endpoint to register a new user.
    """
    username = request.username
    email = request.email
    password = request.password

    # Check if the username already exists
    if get_user_by_username(username):
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = str(uuid.uuid4())  # Generate a unique user ID
    hashed_password = hash_password(password)  # Hash the password

    # User data dictionary
    user_data = {
        "id": user_id,
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "followers": [],
        "following": [],
        "created_at": str(datetime.utcnow())
    }

    create_user(user_data)  # Store the new user in DynamoDB

    return {"message": "User registered successfully", "user": {"id": user_id, "username": username}}


@app.post("/follow")
def follow(request: FollowRequest):
    """
    Allow a user to follow another user, ensuring no duplicates.
    """
    follower_id = request.follower_id
    followed_id = request.followed_id

    if not get_user_by_id(follower_id) or not get_user_by_id(followed_id):
        raise HTTPException(status_code=404, detail="User not found")

    # Add to following and followers, and check if the relationship already exists
    following_added = add_following(follower_id, followed_id)
    follower_added = add_follower(followed_id, follower_id)

    if not following_added or not follower_added:
        raise HTTPException(
            status_code=409, 
            detail=f"User {follower_id} already follows User {followed_id}"
        )

    return {"message": f"User {follower_id} is now following User {followed_id}"}


@app.post("/unfollow")
def unfollow(request: FollowRequest):
    follower_id = request.follower_id
    followed_id = request.followed_id

    if not get_user_by_id(follower_id) or not get_user_by_id(followed_id):
        raise HTTPException(status_code=404, detail="User not found")

    remove_following(follower_id, followed_id)
    remove_follower(followed_id, follower_id)

    return {"message": f"User {follower_id} has unfollowed User {followed_id}"}

@app.post("/login")
def login(request: LoginRequest):
    """
    Endpoint to log a user in and generate a JWT token.
    """
    username = request.username
    password = request.password

    # Retrieve the user by username
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify the password
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate the JWT token
    access_token = create_access_token(
        data={"user_id": user["id"]},
        expire_minutes=30  # Token expires in 30 minutes
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/get-user")
def get_user(request: GetUserRequest):
    """
    Endpoint to retrieve a user by username.
    """
    username = request.username
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Add the router to the app
app.include_router(router)