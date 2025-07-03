from http import HTTPStatus

from freezegun import freeze_time

from fastapi_zero.security import create_access_token


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


def test_current_user_no_sub_raises_unauthorized(client):
    """
    Token sem 'sub' deve levar a credentials_exception.
    """
    data = {"no-email": "test"}
    token = create_access_token(data)
    response = client.delete(
        "/users/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_current_user_sub_not_found_raises_unauthorized(client):
    """
    Token com 'sub' mas sem usuário correspondente deve levar a
    credentials_exception.
    """
    data = {"sub": "noone@example.com"}
    token = create_access_token(data)
    response = client.delete(
        "/users/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_token_expired_after_time(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wrongwrong",
                "email": "wrong@wrong.com",
                "password": "wrong",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
