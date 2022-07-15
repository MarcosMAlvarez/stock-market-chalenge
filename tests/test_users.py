from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def mock_post(endpoint, json):
    field_names = json.keys()
    good_mock_response = {'status_code': 201}
    bad_mock_response = {'status_code': 500}
    if endpoint == "/sign-up":
        if all(field in field_names for field in ['username', 'name', 'last_name', "email", "password"]):
            return good_mock_response
    return bad_mock_response


@patch('fastapi.testclient.TestClient.post', side_effect=mock_post)
def test_create_user(*args, **kwargs):
    user = {
        "username": "test_username",
        "name": "name",
        "last_name": "last_name",
        "email": "test@example.com",
        "password": "password"
    }

    response = client.post("/sign-up", json=user)
    assert response["status_code"] == 201


def test_get_token():
    response = client.post("/token", data={"username": "test_username", "password": "password"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
