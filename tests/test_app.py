from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_read_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA):
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garante que A é A
    """

    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/")
    # Assert
    assert response.json() == {"message": "Olá, Mundo!"}
