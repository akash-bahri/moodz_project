import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.models import get_user_by_username, get_user_by_id, create_user, add_follower, add_following, remove_follower, remove_following
from app.utils import hash_password, verify_password, create_access_token

# Initialize the test client
client = TestClient(app)

# Mock data and functions
def mock_get_user_by_username(username: str):
    if username == "testuser":
        return {"id": "123", "username": "testuser", "email": "user@example.com", "password_hash": hash_password("StrongPassword123")}
    return None

def mock_get_user_by_id(user_id: str):
    if user_id == "123":
        return {"id": "123", "username": "testuser", "email": "user@example.com", "password_hash": hash_password("StrongPassword123")}
    return None

def mock_create_user(user_data):
    return True

def mock_add_follower(followed_id, follower_id):
    return True

def mock_add_following(follower_id, followed_id):
    return True

def mock_remove_follower(followed_id, follower_id):
    return True

def mock_remove_following(follower_id, followed_id):
    return True

# Override models with mocks
app.dependency_overrides[get_user_by_username] = mock_get_user_by_username
app.dependency_overrides[get_user_by_id] = mock_get_user_by_id
app.dependency_overrides[create_user] = mock_create_user
app.dependency_overrides[add_follower] = mock_add_follower
app.dependency_overrides[add_following] = mock_add_following
app.dependency_overrides[remove_follower] = mock_remove_follower
app.dependency_overrides[remove_following] = mock_remove_following

# Test Class using unittest
class TestAPI(unittest.TestCase):

    def test_health(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "status_code": 200})

    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123"
        }
        response = client.post("/register", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User registered successfully")
        self.assertIn("user", response.json())

    def test_register_user_existing(self):
        data = {
            "username": "testuser",
            "email": "user@example.com",
            "password": "StrongPassword123"
        }
        response = client.post("/register", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User already exists")

    def test_login_valid(self):
        data = {
            "username": "testuser",
            "password": "StrongPassword123"
        }
        response = client.post("/login", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_login_invalid_credentials(self):
        data = {
            "username": "testuser",
            "password": "WrongPassword"
        }
        response = client.post("/login", json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Invalid credentials")

    def test_get_user(self):
        data = {"username": "testuser"}
        response = client.post("/get-user", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "testuser")

    def test_get_user_not_found(self):
        data = {"username": "nonexistentuser"}
        response = client.post("/get-user", json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "User not found")

    def test_follow_user(self):
        data = {
            "follower_id": "123",
            "followed_id": "456"
        }
        response = client.post("/follow", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_follow_user_not_found(self):
        data = {
            "follower_id": "123",
            "followed_id": "nonexistent"
        }
        response = client.post("/follow", json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "User not found")

    def test_unfollow_user(self):
        data = {
            "follower_id": "123",
            "followed_id": "456"
        }
        response = client.post("/unfollow", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_unfollow_user_not_found(self):
        data = {
            "follower_id": "123",
            "followed_id": "nonexistent"
        }
        response = client.post("/unfollow", json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "User not found")

# Run the tests
if __name__ == "__main__":
    unittest.main()
