from fastapi.testclient import TestClient


def test_get_main_page(client: TestClient) -> None:
    # when
    response = client.get("/urns/")

    # then
    assert response.status_code == 404


def test_get_urn(client: TestClient) -> None:
    # when
    response = client.get("/urns/test_urn")

    # then
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert b'{"urn":"test_urn"}' in response.content.lower()


def test_get_nonexistent_urn(client: TestClient) -> None:
    # when
    response = client.get("/urns/idonotexist")

    # then
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"
    assert b'{"detail":"unknown urn: idonotexist"}' in response.content.lower()
