# test.py

import pytest
from unittest import mock
from app.models import create_post, upload_text_to_s3, upload_image_to_s3
from botocore.exceptions import ClientError


# Mock AWS SDK (boto3)
@pytest.fixture
def mock_s3_client():
    with mock.patch("app.models.s3_client") as mock_s3:
        mock_s3.Bucket = "moodz-content-bucket"  # Set the bucket name explicitly
        yield mock_s3


@pytest.fixture
def mock_dynamodb_table():
    with mock.patch("app.models.POSTS_TABLE") as mock_dynamo:
        yield mock_dynamo


# Test the upload_text_to_s3 function
def test_upload_text_to_s3(mock_s3_client):
    post_id = "123"
    user_id = "user_1"
    text_content = "This is a text post"
    mock_s3_client.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    
    result = upload_text_to_s3(text_content, post_id, user_id)
    
    # Now, we expect the bucket name to be the one we set above
    assert result == f"https://{mock_s3_client.Bucket}.s3.amazonaws.com/text_posts/{user_id}_{post_id}.txt"
    mock_s3_client.put_object.assert_called_once_with(
        Bucket="moodz-content-bucket",
        Key=f"text_posts/{user_id}_{post_id}.txt",
        Body=text_content
    )


# Test the upload_image_to_s3 function
def test_upload_image_to_s3(mock_s3_client):
    post_id = "123"
    user_id = "user_1"
    mock_image_file = mock.Mock()
    mock_image_file.filename = "image.jpg"
    mock_image_file.file = mock.Mock()

    mock_s3_client.upload_fileobj.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    
    result = upload_image_to_s3(mock_image_file, post_id, user_id)

    # Now, we expect the bucket name to be the one we set above
    assert result == f"https://{mock_s3_client.Bucket}.s3.amazonaws.com/image_posts/{user_id}_{post_id}_image.jpg"
    mock_s3_client.upload_fileobj.assert_called_once_with(
        mock_image_file.file,
        "moodz-content-bucket",
        f"image_posts/{user_id}_{post_id}_image.jpg"
    )


# Test creating a post (for both text and image)
def test_create_post_text(mock_s3_client, mock_dynamodb_table):
    user_id = "user_1"
    text_content = "This is a text post"
    
    post_id = create_post(user_id, text_content, "text")
    
    assert post_id is not None
    mock_s3_client.put_object.assert_called_once()
    mock_dynamodb_table.put_item.assert_called_once()


def test_create_post_image(mock_s3_client, mock_dynamodb_table):
    user_id = "user_1"
    mock_image_file = mock.Mock()
    mock_image_file.filename = "image.jpg"
    mock_image_file.file = mock.Mock()
    
    post_id = create_post(user_id, mock_image_file, "image")
    
    assert post_id is not None
    mock_s3_client.upload_fileobj.assert_called_once()
    mock_dynamodb_table.put_item.assert_called_once()
