import pytest
from app import schemas

from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "idrees00111@gmail.com", "password": "namal786"})
    new_user = schemas.UserOut(**res.json())
    assert res.json().get("email") == 'idrees0011@gmail.com'
    assert new_user.email == 'idrees00111@gmail.com'
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
        
    id = payload.get("user_id")
    #print(res.json())
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'namal786', 403),
    ('idrees0011@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('idrees@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, 
                                      "password": password})
    assert res.status_code ==status_code
    #assert res.json().get('detail') == 'Invalid Credential'