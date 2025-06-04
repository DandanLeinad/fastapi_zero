from http import HTTPStatus


def test_read_deve_retornar_ola_mundo(client):
    """
    Testa apenas o endpoint raiz retornando 'Olá, Mundo!'.
    """
    response = client.get("/")

    assert response.json() == {"message": "Olá, Mundo!"}
    assert response.status_code == HTTPStatus.OK
