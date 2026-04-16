from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def unique_user_payload():
    unique = uuid4().hex[:8]
    return {
        "first_name": "Danielle",
        "last_name": "Evans",
        "email": f"calc_{unique}@example.com",
        "username": f"calcuser_{unique}",
        "password": "P@ssword123!",
        "confirm_password": "P@ssword123!"
    }

def register_and_login():
    payload = unique_user_payload()

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "username": payload["username"],
            "password": payload["password"]
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return payload, headers

def create_calculation(headers, calc_type="addition", inputs=None):
    if inputs is None:
        inputs = [10, 5, 2]

    response = client.post(
        "/calculations",
        json={"type": calc_type, "inputs": inputs},
        headers=headers
    )
    return response

def test_create_calculation_success():
    _, headers = register_and_login()

    response = create_calculation(headers)

    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "addition"
    assert data["inputs"] == [10, 5, 2]
    assert data["result"] == 17
    assert "id" in data

def test_list_calculations_success():
    _, headers = register_and_login()

    create_response = create_calculation(headers)
    assert create_response.status_code == 201

    response = client.get("/calculations", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_calculation_by_id_success():
    _, headers = register_and_login()

    create_response = create_calculation(headers)
    calc_id = create_response.json()["id"]

    response = client.get(f"/calculations/{calc_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["result"] == 17

def test_update_calculation_success():
    _, headers = register_and_login()

    create_response = create_calculation(headers)
    calc_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calc_id}",
        json={"inputs": [100, 4]},
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["inputs"] == [100, 4]
    assert data["result"] == 104

def test_delete_calculation_success():
    _, headers = register_and_login()

    create_response = create_calculation(headers)
    calc_id = create_response.json()["id"]

    delete_response = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/calculations/{calc_id}", headers=headers)
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Calculation not found."

def test_get_calculation_invalid_uuid_returns_400():
    _, headers = register_and_login()

    response = client.get("/calculations/not-a-uuid", headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid calculation id format."

def test_create_calculation_without_auth_returns_401():
    response = client.post(
        "/calculations",
        json={"type": "addition", "inputs": [10, 5, 2]}
    )

    assert response.status_code == 401

def test_create_calculation_missing_type_returns_422():
    _, headers = register_and_login()

    response = client.post(
        "/calculations",
        json={"inputs": [10, 5, 2]},
        headers=headers
    )

    assert response.status_code == 422

def test_create_calculation_invalid_type_returns_422():
    _, headers = register_and_login()

    response = create_calculation(headers, calc_type="banana", inputs=[10, 5])

    assert response.status_code == 422