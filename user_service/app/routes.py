from fastapi import FastAPI, HTTPException
from app.models import get_user_by_username, get_user_by_id, create_user, follow_user, unfollow_user
from app.utils import hash_password, verify_password, create_access_token
import uuid
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

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

# Endpoints
@app.post("/register")
def register(request: RegisterRequest):
    username = request.username
    email = request.email
    password = request.password

    if get_user_by_username(username):
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = str(uuid.uuid4())
    hashed_password = hash_password(password)

    user_data = {
        "id": user_id,
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "created_at": str(datetime.utcnow())
    }
    create_user(user_data)

    return {"message": "User registered successfully", "user": {"id": user_id, "username": username}}

@app.post("/login")
def login(request: LoginRequest):
    username = request.username
    password = request.password

    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"user_id": user["id"]},
        secret_key="your_secret_key",
        expire_minutes=30
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/get-user")
def get_user(request: GetUserRequest):
    username = request.username
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
