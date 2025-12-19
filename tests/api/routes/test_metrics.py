from fastapi.testclient import TestClient


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Check for expected Prometheus metrics
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text
    assert "python_info" in response.text
