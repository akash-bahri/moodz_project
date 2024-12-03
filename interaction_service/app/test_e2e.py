import pytest
from fastapi.testclient import TestClient
from app.routes import app
from unittest.mock import patch

# Initialize the TestClient
client = TestClient(app)

@pytest.fixture
def mock_posts_table():
    with patch("app.routes.POSTS_TABLE") as mock_table:
        yield mock_table

# Test the health endpoint
def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "status_code": 200}

# Test for liking a post
@patch("app.routes.like_post")
def test_like_post(mock_like_post):
    mock_like_post.return_value = True

    data = {"post_id": "post_1", "user_id": "user_1"}
    response = client.post("/like", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Post liked successfully"}

    # Test if user tries to like the same post again
    mock_like_post.return_value = False
    response = client.post("/like", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User has already liked this post"}

# Test for unliking a post
@patch("app.routes.unlike_post")
def test_unlike_post(mock_unlike_post):
    mock_unlike_post.return_value = True

    data = {"post_id": "post_1", "user_id": "user_1"}
    response = client.post("/unlike", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Post unliked successfully"}

    # Test if user tries to unlike a post they haven't liked
    mock_unlike_post.return_value = False
    response = client.post("/unlike", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User has not liked this post"}

# Test for getting the number of likes for a post
@patch("app.routes.get_post_likes")
def test_get_post_likes(mock_get_post_likes):
    mock_get_post_likes.return_value = 5

    response = client.get("/likes/post_1")
    assert response.status_code == 200
    assert response.json() == {"post_id": "post_1", "likes": 5}

    # Test when post is not found
    mock_get_post_likes.side_effect = Exception("Post not found")
    response = client.get("/likes/post_1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
