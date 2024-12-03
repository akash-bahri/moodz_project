from unittest.mock import patch
from app.models import get_following_list, fetch_user_posts, generate_feed
from app import USER_TABLE, POSTS_TABLE
import pytest


@patch("app.USER_TABLE.get_item")
def test_get_following_list(mock_get_item):
    # Mock response from USER_TABLE
    mock_get_item.return_value = {"Item": {"id": "user_1", "following": ["user_2", "user_3"]}}

    following_list = get_following_list("user_1")
    assert following_list == ["user_2", "user_3"]
    mock_get_item.assert_called_once_with(Key={"id": "user_1"})


@patch("app.POSTS_TABLE.scan")
def test_fetch_user_posts(mock_scan):
    # Mock response from POSTS_TABLE
    mock_scan.return_value = {
        "Items": [
            {"post_id": "post_1", "timestamp": "2024-12-01T12:00:00Z", "user_id": "user_2"},
            {"post_id": "post_2", "timestamp": "2024-12-01T11:00:00Z", "user_id": "user_2"},
        ]
    }

    posts = fetch_user_posts("user_2", max_posts=5)
    assert len(posts) == 2
    assert posts[0]["post_id"] == "post_1"
    mock_scan.assert_called_once_with(
        FilterExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": "user_2"},
        Limit=5,
    )


@patch("app.models.get_following_list")
@patch("app.models.fetch_user_posts")
def test_generate_feed(mock_fetch_user_posts, mock_get_following_list):
    # Mock responses
    mock_get_following_list.return_value = ["user_2", "user_3"]
    mock_fetch_user_posts.side_effect = [
        [{"post_id": "post_1", "timestamp": "2024-12-01T12:00:00Z", "user_id": "user_2"}],
        [{"post_id": "post_2", "timestamp": "2024-12-01T11:00:00Z", "user_id": "user_3"}],
    ]

    feed = generate_feed("user_1", max_posts_per_user=5)
    assert len(feed) == 2
    assert feed[0]["post_id"] == "post_1"  # Sorted by timestamp
    mock_get_following_list.assert_called_once_with("user_1")
    assert mock_fetch_user_posts.call_count == 2
