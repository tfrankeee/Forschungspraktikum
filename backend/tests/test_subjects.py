def test_create_subject(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subject
    r2 = client.post("/subjects/", json={
        "name": "testSubject",
        "user_id": 1
    })

    assert r2.status_code == 201
    data = r2.json()

    assert data["name"] == "testSubject"
    assert data["user_id"] == 1
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_subject_no_name(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "",
        "user_id": 1
    })

    assert r2.status_code == 422

def test_create_subject_no_user_id(client):
    # same case as none existing user id

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "",
        "user_id": 0
    })

    assert r2.status_code == 422

def test_create_two_subjects_same_name(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })
    r3 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201
    assert r3.status_code == 409

def test_read_subjects(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })
    r3 = client.post("/subjects/", json={
        "name": "DBS2",
        "user_id": 1
    })

    assert r2.status_code == 201
    assert r3.status_code == 201

    # read subjects
    response = client.get("/subjects/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    names = [u["name"] for u in data]

    assert "DBS" in names
    assert "DBS2" in names

    # check that each subject has id, created_at, updated_at
    for subject in data:
        assert "id" in subject
        assert "created_at" in subject
        assert "updated_at" in subject

def test_read_subjects_byUser(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })
    r3 = client.post("/subjects/", json={
        "name": "DBS2",
        "user_id": 1
    })

    assert r2.status_code == 201
    assert r3.status_code == 201

    # read subject
    user = r1.json()
    user_id = user["id"]
    response = client.get(f"/subjects/byUser/{user_id}")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    names = [u["name"] for u in data]

    assert "DBS" in names
    assert "DBS2" in names

    # check that each subject has id, created_at, updated_at
    for subject in data:
        assert "id" in subject
        assert "created_at" in subject
        assert "updated_at" in subject

def test_read_subjects_byUser_noexistent_user_id(client):
    user_id = 42
    response = client.get(f"/subjects/byUser/{user_id}")
    assert response.status_code == 404

def test_read_subject(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subjects
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # read subject
    subject_id = r2.json()["id"]
    response = client.get(f"/subjects/{subject_id}")

    assert response.status_code == 200

    subject = response.json()
    assert subject["id"] == subject_id
    assert subject["name"] == "DBS"
    assert subject["user_id"] == r1.json()["id"]
    assert "created_at" in subject
    assert "updated_at" in subject

def test_read_subject_noexistent_id(client):
    subject_id = 42
    response = client.get(f"/subjects/{subject_id}")
    assert response.status_code == 404

def test_update_subject(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subject
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # update subject
    subject_id = r2.json()["id"]
    r3 = client.patch(f"/subjects/{subject_id}", json={
        "name": "DBS2"
    })

    assert r3.status_code == 200

    assert r3.json()["name"] == "DBS2"

def test_update_subject_noexistent_id(client):
     # update subject
    subject_id = 42
    r3 = client.patch(f"/subjects/{subject_id}", json={
        "name": "DBS2"
    })
    assert r3.status_code == 404

def test_update_subject_name_user_id_combo_already_exists(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subject
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })
    r3 = client.post("/subjects/", json={
        "name": "DBS2",
        "user_id": 1
    })

    assert r2.status_code == 201
    assert r3.status_code == 201

    # update subject
    subject_id = r2.json()["id"]
    r4 = client.patch(f"/subjects/{subject_id}", json={
        "name": "DBS2"
    })

    assert r4.status_code == 409

def test_delete_subject(client):
    # create user for subject
    r1 = client.post("/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    assert r1.status_code == 201

    # create subject
    r2 = client.post("/subjects/", json={
        "name": "DBS",
        "user_id": 1
    })

    assert r2.status_code == 201

    # delete subject
    subject_id = r2.json()["id"]
    r3 = client.delete(f"/subjects/{subject_id}")

    assert r3.status_code == 204

def test_delete_subject_noexistent_id(client):
    # delete subject
    subject_id = 42
    r3 = client.delete(f"/subjects/{subject_id}")

    assert r3.status_code == 404