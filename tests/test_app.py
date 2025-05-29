from http import HTTPStatus


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

    response = client.get("/users/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_update_integrity_error(client, user, token):
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
        headers={"Authorization": f"Bearer {token}"},
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


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": user.email,
            "password": user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert token["token_type"] == "bearer"


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
