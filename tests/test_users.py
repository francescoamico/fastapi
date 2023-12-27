import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_create_user(client):
    user = schemas.UserCreate(email="francesco@gmail.com", password="password123")
    res = client.post("/users/", json=user.model_dump())

    new_user = schemas.User(**res.json())
    assert new_user.email == "francesco@gmail.com"
    assert res.status_code == 201

def test_incorrect_create_user(test_user, client):
    user = schemas.UserCreate(email="francesco@gmail.com", password="anypassword")
    res = client.post("/users/", json=user.model_dump())

    assert res.status_code == 409

def test_login(test_user, client):
    res = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})

    login = schemas.Token(**res.json())
    payload = jwt.decode(token=login.access_token, key=settings.secret_key, algorithms=settings.algorithm)

    assert test_user["id"] == payload.get("user_id")
    assert login.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("francesco@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "wrongpassword", 422),
    ("wrongemail@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username":email, "password":password})
    assert res.status_code == status_code

def test_get_user(test_user, client):
    res = client.get(f"/users/{test_user['id']}")

    user = schemas.User(**res.json())
    assert user.id == test_user["id"]
    assert user.email == test_user["email"]
    assert res.status_code == 200

@pytest.mark.parametrize("id", [1, 10, 100, 1000, 1000000, 10000000])
def test_get_user_not_exists(client, id):
    res = client.get(f"/users/{id}")
    assert res.status_code == 404