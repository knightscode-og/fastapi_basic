"""Contract tests for POST /api/v1/tabs endpoint.

Tests validate endpoint against OpenAPI specification.
Tests the endpoint as external consumer would use it (via HTTP).
"""

import pytest
from fastapi.testclient import TestClient
from typing import Generator
from pathlib import Path

from src.main import app
from src.models.tab import MusicTabCreate
from src.services.tab_service import TabService
import src.api.endpoints.tabs as tabs_module


@pytest.fixture
def client_with_clean_storage() -> Generator[TestClient, None, None]:
    """Create TestClient with clean storage (cleared before/after test)."""
    storage = Path("storage/tabs")

    # Clear storage before test
    if storage.exists():
        for f in storage.glob("*.json"):
            f.unlink()

    # Reset the app's tab service
    tabs_module.tab_service = TabService()

    yield TestClient(app)

    # Clear storage after test
    if storage.exists():
        for f in storage.glob("*.json"):
            f.unlink()


@pytest.mark.contract
class TestCreateTabsEndpoint:
    """Contract tests for POST /api/v1/tabs endpoint."""

    def test_create_tab_success(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs creates tab and returns 201.

        Scenario:
            - POST valid tab data
            - Storage is empty (ID should be 1)

        Expected:
            - Status code 201 Created
            - Response contains created tab with auto-assigned ID
            - Response schema matches MusicTab
        """
        payload = {
            "title": "Stairway to Heaven",
            "artist": "Led Zeppelin",
            "content": "Em7 - A7sus4\n...",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Stairway to Heaven"
        assert data["artist"] == "Led Zeppelin"
        assert isinstance(data["content"], str)

    def test_create_tab_response_schema(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs response matches MusicTab schema.

        Expected schema:
        {
            "id": integer,
            "title": string,
            "artist": string,
            "content": string
        }
        """
        payload = {
            "title": "Test Tab",
            "artist": "Test Artist",
            "content": "Test content",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 201
        data = response.json()

        # Validate required fields exist
        assert "id" in data
        assert "title" in data
        assert "artist" in data
        assert "content" in data

        # Validate field types
        assert isinstance(data["id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["artist"], str)
        assert isinstance(data["content"], str)

    def test_create_tab_auto_increment_id(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs auto-increments ID for multiple creates.

        Scenario:
            - POST first tab (should be ID=1)
            - POST second tab (should be ID=2)
            - POST third tab (should be ID=3)

        Expected:
            - Each tab gets sequential ID
            - IDs start at 1 and increment
        """
        # Create first tab
        response1 = client_with_clean_storage.post(
            "/api/v1/tabs",
            json={
                "title": "Tab 1",
                "artist": "Artist 1",
                "content": "Content 1",
            },
        )
        assert response1.status_code == 201
        assert response1.json()["id"] == 1

        # Create second tab
        response2 = client_with_clean_storage.post(
            "/api/v1/tabs",
            json={
                "title": "Tab 2",
                "artist": "Artist 2",
                "content": "Content 2",
            },
        )
        assert response2.status_code == 201
        assert response2.json()["id"] == 2

        # Create third tab
        response3 = client_with_clean_storage.post(
            "/api/v1/tabs",
            json={
                "title": "Tab 3",
                "artist": "Artist 3",
                "content": "Content 3",
            },
        )
        assert response3.status_code == 201
        assert response3.json()["id"] == 3

    def test_create_tab_missing_title(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs returns 400 when title missing.

        Scenario:
            - POST payload without 'title' field

        Expected:
            - Status code 400 Bad Request (custom validation handler)
        """
        payload = {
            # Missing title
            "artist": "Artist",
            "content": "Content",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400

    def test_create_tab_missing_artist(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs returns 400 when artist missing.

        Scenario:
            - POST payload without 'artist' field

        Expected:
            - Status code 400 Bad Request
        """
        payload = {
            "title": "Title",
            # Missing artist
            "content": "Content",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400

    def test_create_tab_missing_content(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs returns 400 when content missing.

        Scenario:
            - POST payload without 'content' field

        Expected:
            - Status code 400 Bad Request
        """
        payload = {
            "title": "Title",
            "artist": "Artist",
            # Missing content
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400

    def test_create_tab_empty_title(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs returns 400 when title is empty string.

        Scenario:
            - POST with empty title (violates min_length=1)

        Expected:
            - Status code 400 Bad Request
        """
        payload = {
            "title": "",  # Empty string
            "artist": "Artist",
            "content": "Content",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400

    def test_create_tab_empty_artist(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs returns 400 when artist is empty string.

        Scenario:
            - POST with empty artist

        Expected:
            - Status code 400 Bad Request
        """
        payload = {
            "title": "Title",
            "artist": "",  # Empty string
            "content": "Content",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400

    def test_create_tab_empty_content(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs returns 400 when content is empty string.

        Scenario:
            - POST with empty content

        Expected:
            - Status code 400 Bad Request
        """
        payload = {
            "title": "Title",
            "artist": "Artist",
            "content": "",  # Empty string
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400

    def test_create_tab_extra_fields_rejected(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test POST /api/v1/tabs rejects extra fields (forbid extra).

        Scenario:
            - POST with extra field 'extra_field'
            - MusicTabCreate config has extra='forbid'

        Expected:
            - Status code 400 Bad Request
        """
        payload = {
            "title": "Title",
            "artist": "Artist",
            "content": "Content",
            "extra_field": "Should be rejected",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)

        assert response.status_code == 400
