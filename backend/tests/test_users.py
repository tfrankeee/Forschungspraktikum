token_header = {"Content-Type": "application/x-www-form-urlencoded"}

def test_create_user(client):
    user = {
         "username": "testuser",
        "email": "test@example.com",
        "password": "secret123"
    }
    response_create = client.post("/users/register", json=user)

    assert response_create.status_code == 201, response_create.text
    data = response_create.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_user_no_username(client):
    user = {
        "username": "",
        "email": "test@example.com",
        "password": "secret123"
    }
    response_create = client.post("/users/register", json=user)

    assert response_create.status_code == 422, response_create.text

def test_create_user_without_password(client):
    # create two users first
    user = {
        "username": "alice",
        "email": "alice@example.de"
    }
    response_create = client.post("/users/register", json=user)

    assert response_create.status_code == 422, response_create.text

def test_create_two_user_with_same_username(client):
    # create two users first
    user1 = {
        "username": "bob",
        "email": "alice@example.com",
        "password": "password123"
    }
    user2 = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123"
    }

    # create users
    response_create1 = client.post("/users/register", json=user1)
    response_create2 = client.post("/users/register", json=user2)

    assert response_create1.status_code == 201, response_create1.text
    assert response_create2.status_code == 400, response_create2.text  # Bad Request due to duplicate username
    assert response_create2.json()["detail"] == "Username already taken"

def test_get_users(client):
    # create two users first
    user1 = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    }
    user2 = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123"
    }

    # create users
    response_create1 = client.post("/users/register", json=user1)
    response_create2 = client.post("/users/register", json=user2)

    assert response_create1.status_code == 201, response_create1.text
    assert response_create2.status_code == 201, response_create2.text

    # login as one of the users to get token
    response_login = client.post("/users/login",
    data={"username": "alice", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # read users
    response_get = client.get("/users/", headers=headers)
    assert response_get.status_code == 200, response_get.text

    data = response_get.json()

    assert isinstance(data, list)
    assert len(data) == 2

    usernames = [u["username"] for u in data]
    emails = [u["email"] for u in data]

    assert "alice" in usernames
    assert "bob" in usernames
    assert "alice@example.com" in emails
    assert "bob@example.com" in emails

    # check that each user has id, created_at, updated_at
    for user in data:
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user

def test_get_user(client):
    user = {
        "username": "charlie",
        "email": "test@test.de",
        "password": "password123"
    }
    response_create = client.post("/users/register", json=user)
    assert response_create.status_code == 201, response_create.text

    created = response_create.json()
    user_id = created["id"]
    username = created["username"]
    password = user["password"]

    response_login = client.post("/users/login", 
    data={"username": username, "password": password},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response_get = client.get(f"/users/{user_id}", headers=headers)
    assert response_get.status_code == 200, response_get.text


    user = response_get.json()
    assert user["id"] == user_id
    assert user["username"] == "charlie"
    assert user["email"] == "test@test.de"
    assert "created_at" in user
    assert "updated_at" in user

def test_get_nonexistent_user(client):
    # get user with an ID that does not exist
    user = {
        "username": "charlie",
        "email": "test@test.de",
        "password": "password123"
    }
    response_create = client.post("/users/register", json=user)
    assert response_create.status_code == 201, response_create.text

    response_login = client.post("/users/login", 
    data={"username": "charlie", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text

    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response_get = client.get("/users/9999", headers=headers)
    assert response_get.status_code == 404, response_get.text
    assert response_get.json()["detail"] == "User not found"

def test_update_user(client):
    # create a user first
    user = {
        "username": "dave",
        "email": "test@test.de",
        "password": "password123"
    }
    response_create = client.post("/users/register", json=user)
    assert response_create.status_code == 201, response_create.text

    # get the created user's ID
    created = response_create.json()
    user_id = created["id"]

    response_login = client.post("/users/login", 
    data={"username": "dave", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # update the user
    update_data = {
        "username": "dave_updated",
        "email": "test@test.de",
        "password": "password123"
    }
    response_patch = client.patch(f"/users/{user_id}", json=update_data, headers=headers)
    assert response_patch.status_code == 200, response_patch.text


def test_update_user_with_empty_username(client):
    # create a user first
    user = {
        "username": "dave",
        "email": "test@test.de",
        "password": "password123"
    }
    response_create = client.post("/users/register", json=user)
    assert response_create.status_code == 201, response_create.text

    # get the created user's ID
    created = response_create.json()
    user_id = created["id"]

    response_login = client.post("/users/login", 
    data={"username": "dave", "password": "password123"},
    headers=token_header
    )
    assert response_login.status_code == 200, response_login.text
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # update the user
    update_data = {
        "username": "",
        "email": "test@test.de",
        "password": "password123"
    }
    response_patch = client.patch(f"/users/{user_id}", json=update_data, headers=headers)
    assert response_patch.status_code == 422, response_patch.text 

