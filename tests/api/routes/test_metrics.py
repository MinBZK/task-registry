import pytest
from fastapi.testclient import TestClient


def test_metrics_endpoint(client: TestClient) -> None:
    try:
        response = client.get("/metrics")
    except TypeError as e:
        # Known issue: prometheus_client ProcessCollector has a bug on some Linux environments
        # (e.g., GitHub Actions runners) where it fails with "must be str or None, not bytes"
        # when reading /proc/[pid]/stat. This works correctly in Kubernetes clusters.
        # See: https://github.com/prometheus/client_python/issues
        if "must be str or None, not bytes" in str(e):
            pytest.skip("Skipping due to known ProcessCollector bug on this platform")
        raise

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Check for expected Prometheus metrics
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text
    assert "python_info" in response.text
