import pytest
from jose import jwt

from app.config import settings
from app.schemas import auth_schemas, user_schemas

# from .database import client, session # not requiread after conftest.py

# session internally used, so always call
# trailing slash is important


# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Hello world"


def test_create_user(client):
    response = client.post(
        "/api/v2/user/create/", json={"email": "j@j.com", "password": "password"}
    )
    new_user = user_schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "j@j.com"


def test_login_user(test_user, client):
    response = client.post(
        "/api/v2/auth/login/",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    new_tokens = auth_schemas.AllTokenResponse(**response.json())
    payload = jwt.decode(
        new_tokens.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    user_id: str = payload.get("user_id")
    assert user_id == test_user["id"]
    assert new_tokens.token_type == "bearer"
    assert response.status_code == 202


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("j@j.com", "wrongpassword", 403),
        ("j@j1.com", "password", 403),
        ("j@j1.com", "wrongpassword", 403),
        (None, "password", 422),  # pydantic missing fields
        ("j@j.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post(
        "/api/v2/auth/login/",
        data={"username": email, "password": password},
    )
    assert response.status_code == status_code
    # assert response.json()["message"] == "Invalid Credentials"
