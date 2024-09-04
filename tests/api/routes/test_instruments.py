from fastapi.testclient import TestClient


def test_get_main_page(client: TestClient) -> None:
    # when
    response = client.get("/instruments/")

    # then
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert b'{"entries":[{"path":"instruments/test_instrument.yaml","urn":"test_urn"}]}' in response.content.lower()
