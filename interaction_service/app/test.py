import pytest
from unittest.mock import patch, MagicMock
from app.models import like_post, unlike_post, get_post_likes

# Mocking POSTS_TABLE
@pytest.fixture
def mock_posts_table():
    with patch("app.models.POSTS_TABLE") as mock_table:
        yield mock_table

# Test for liking a post
def test_like_post(mock_posts_table):
    mock_post = {"post_id": "post_1", "likes": {"count": 0, "users": []}}
    mock_posts_table.get_item.return_value = {"Item": mock_post}

    # Mock update response
    mock_posts_table.update_item.return_value = {}

    # Test for liking a post successfully
    success = like_post("post_1", "user_1")
    assert success is True
    assert mock_posts_table.update_item.called

    # Test for liking the same post again (should return False)
    success = like_post("post_1", "user_1")
    assert success is False

# Test for unliking a post
def test_unlike_post(mock_posts_table):
    mock_post = {"post_id": "post_1", "likes": {"count": 1, "users": ["user_1"]}}
    mock_posts_table.get_item.return_value = {"Item": mock_post}

    # Mock update response
    mock_posts_table.update_item.return_value = {}

    # Test for unliking a post successfully
    success = unlike_post("post_1", "user_1")
    assert success is True
    assert mock_posts_table.update_item.called

    # Test for unliking a post that the user hasn't liked (should return False)
    success = unlike_post("post_1", "user_1")
    assert success is False

# Test for retrieving the number of likes on a post
def test_get_post_likes(mock_posts_table):
    mock_post = {"post_id": "post_1", "likes": {"count": 3, "users": ["user_1", "user_2", "user_3"]}}
    mock_posts_table.get_item.return_value = {"Item": mock_post}

    count = get_post_likes("post_1")
    assert count == 3
