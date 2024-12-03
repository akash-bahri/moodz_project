import requests

BASE_URL = "http://localhost:5001"  

def test_account_creation_flow():
    print("Testing Account Creation Flow...")
    
    data = {
        "username": "testuser",
        "email": "user@example.com",
        "password": "StrongPassword123"
    }
    
    # First, make the request to create the account
    response = requests.post(f"{BASE_URL}/register", json=data)
    
    # Check if the status code is 400 (Bad Request) because the user already exists
    assert response.status_code == 400, "Expected status code 400, but got {response.status_code}"
    
    # Ensure the response message indicates the user already exists
    response_data = response.json()
    assert response_data["detail"] == "User already exists", f"Expected 'User already exists', but got {response_data['detail']}"
    
    print("Account creation passed!")

# Running the test
test_account_creation_flow()
