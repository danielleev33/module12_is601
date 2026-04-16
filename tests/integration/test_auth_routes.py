from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def unique_user_payload():
    unique = uuid4().hex[:8]
    return {
        "first_name": "Danielle",
        "last_name": "Evans",
        "email": f"danielle_{unique}@example.com",
        "username": f"danielleev33_{unique}",
        "password": "P@ssword123!",
        "confirm_password": "P@ssword123!"
    }

def test_register_user_success():
    payload = unique_user_payload()

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data

def test_register_duplicate_user_returns_400():
    payload = unique_user_payload()

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert "already exists" in second_response.json()["detail"].lower()

def test_login_success():
    payload = unique_user_payload()

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_payload = {
        "username": payload["username"],
        "password": payload["password"]
    }

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == payload["username"]

def test_login_invalid_password_returns_401():
    payload = unique_user_payload()

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    bad_login_payload = {
        "username": payload["username"],
        "password": "WrongPassword123!"
    }

    response = client.post("/auth/login", json=bad_login_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"