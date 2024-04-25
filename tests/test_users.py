import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    print(f'Message Print: {res.json().get("message")}')
    assert res.json().get("message") == "Hellow Worlds"
    assert res.status_code == 200


def test_create_user(client):
    # Test repeated user (email)
    res = client.post(
        "/users/", json={"email": "test_user_email@gmail.com", "password": "password123"}
    )
    res = client.post(
        "/users/", json={"email": "test_user_email@gmail.com", "password": "password123"}
    )
    print(f"Check duplicate user: {res.json()}")
    assert res.status_code == 409
    # Test new user
    res2 = client.post(
        "/users/", json={"email": "test_user_email2@gmail.com", "password": "password123"}
    )
    print(f"Check new user insert {res2.json()}")
    assert res2.json().get("email") == "test_user_email2@gmail.com"
    print(f"Status Code {res2}")
    assert res2.status_code == 201

    # Using Schemas to test
    print("Checking for Email using Schemas")
    new_user = schemas.UserOut(**res2.json())
    assert new_user.email == "test_user_email2@gmail.com"

def test_login_user(client, test_user):  # noqa: F811
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    
    login_res = schemas.Token(**res.json())
    # Same code we have in oauth2.py
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test_user_email@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test_user_email@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # This below wont work because we also are providing a 422 code
    #assert res.json().get('detail') == 'Invalid Credentials'
