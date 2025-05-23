from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_read_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA):
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garante que A é A
    """

    response = client.get("/")

    assert response.json() == {"message": "Olá, Mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "bob",
        "email": "bob@example.com",
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_update_user_not_found(client):
    response = client.put(
        "/users/999",
        json={
            "username": "no_user",
            "email": "no_user@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_read_user_success(client):
    create_resp = client.post(
        "/users/",
        json={
            "username": "xavier",
            "email": "xavier@example.com",
            "password": "secret",
        },
    )
    assert create_resp.status_code == HTTPStatus.CREATED
    user_data = create_resp.json()

    get_resp = client.get(f"/users/{user_data['id']}")
    assert get_resp.status_code == HTTPStatus.OK
    assert get_resp.json() == user_data


def test_read_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f"/users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        "detail": "Username or Email already exists"
    }


def test_create_user_username_conflict(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "unique@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Username already exists"


def test_create_user_email_conflict(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "uniqueuser",
            "email": user.email,
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"
