from fastapi.testclient import TestClient


def test_get_urn(client: TestClient) -> None:
    # when
    response = client.get("/urn/?urn=test_urn")

    # then
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert b'{"test":"test"}' in response.content.lower()


def test_get_nonexistent_urn(client: TestClient) -> None:
    # when
    response = client.get("/urn/?urn=nonexisting_urn")

    # then
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"
    assert b'{"error":"urn does not exist in the instrument registry "}' in response.content.lower()
