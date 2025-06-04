from http import HTTPStatus

from fastapi_zero.security import create_access_token


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


def test_get_current_user_not_found__exercicio(client):
    """
    Verifica que a autenticação falha quando o token não contém 'sub' (e-mail).
    """
    data = {"no-email": "test"}
    token = create_access_token(data)

    response = client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_current_user_does_not_exists__exercicio(client):
    """
    Verifica que a autenticação falha quando o token contém 'sub',
    mas não existe um usuário com esse email.
    """
    data = {"sub": "test@test"}
    token = create_access_token(data)

    response = client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
