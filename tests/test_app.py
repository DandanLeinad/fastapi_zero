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
