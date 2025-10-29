"""Smoke test for quick pre-deployment validation.

Minimal set of tests that verify the API is fundamentally working.
Can be run pre-deployment for quick sanity check (<2 seconds total).
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.mark.usefixtures("fixture_empty_storage")
class TestSmokeTests:
    """Quick smoke tests for deployment validation."""

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_health_check(self) -> None:
        """Verify health check endpoint responds.
        
        Used by load balancers and monitoring to verify service is alive.
        """
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_endpoint_get_all_responds(self) -> None:
        """Verify GET /api/v1/tabs endpoint responds."""
        response = self.client.get("/api/v1/tabs")
        assert response.status_code == 200
        data = response.json()
        assert "tabs" in data
        assert isinstance(data["tabs"], list)

    def test_endpoint_post_responds(self) -> None:
        """Verify POST /api/v1/tabs endpoint responds."""
        response = self.client.post(
            "/api/v1/tabs",
            json={
                "title": "Test",
                "artist": "Artist",
                "content": "Content",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["id"] == 1

    def test_endpoint_get_by_id_responds(self) -> None:
        """Verify GET /api/v1/tabs/{id} endpoint responds."""

        # First create a tab
        response = self.client.post(
            "/api/v1/tabs",
            json={
                "title": "Test",
                "artist": "Artist",
                "content": "Content",
            },
        )
        assert response.status_code == 201
        tab_id = response.json()["id"]

        # Then retrieve it
        response = self.client.get(f"/api/v1/tabs/{tab_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tab_id
        assert data["title"] == "Test"
