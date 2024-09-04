from fastapi.testclient import TestClient


def test_get_root(client: TestClient) -> None:
    response = client.get(
        "/",
        follow_redirects=False,
    )
    assert response.status_code == 307
