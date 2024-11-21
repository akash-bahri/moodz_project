from fastapi import FastAPI, HTTPException, Depends
from app.models import get_user_by_username, get_user_by_id, create_user, follow_user, unfollow_user
from app.utils import hash_password, verify_password, create_access_token
import uuid
from datetime import datetime

app = FastAPI()

@app.post("/register")
def register(username: str, email: str, password: str):
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
def login(username: str, password: str):
    users = get_user_by_username(username)
    if not users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = users[0]
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"user_id": user["id"]},
        secret_key="your_secret_key",
        expire_minutes=30
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/follow/{user_id}")
def follow(user_id: str, current_user_id: str):
    follow_user(current_user_id, user_id)
    return {"message": f"Started following user {user_id}"}

@app.delete("/unfollow/{user_id}")
def unfollow(user_id: str, current_user_id: str):
    unfollow_user(current_user_id, user_id)
    return {"message": f"Unfollowed user {user_id}"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
