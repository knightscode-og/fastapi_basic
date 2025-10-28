"""Contract tests for GET /api/v1/tabs endpoint.

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


@pytest.fixture
def client_with_samples() -> Generator[TestClient, None, None]:
    """Create TestClient with sample tabs pre-loaded."""
    storage = Path("storage/tabs")
    
    # Clear storage before test
    if storage.exists():
        for f in storage.glob("*.json"):
            f.unlink()
    
    # Create sample tabs
    service = TabService()
    service.create(MusicTabCreate(title="Wonderwall", artist="Oasis", content="Em7 Csus2\n..."))
    service.create(MusicTabCreate(title="Blackbird", artist="Beatles", content="G D A7\n..."))
    
    # Update the module's tab_service
    tabs_module.tab_service = service
    
    yield TestClient(app)
    
    # Clear storage after test
    if storage.exists():
        for f in storage.glob("*.json"):
            f.unlink()


@pytest.mark.contract
class TestGetAllTabsEndpoint:
    """Contract tests for GET /api/v1/tabs endpoint."""

    def test_get_all_tabs_success_with_samples(
        self, client_with_samples: TestClient
    ) -> None:
        """Test GET /api/v1/tabs returns 200 with tab list.

        Scenario:
            - Storage pre-populated with 2 sample tabs (Wonderwall, Blackbird)

        Expected:
            - Status code 200 OK
            - Response schema: {"tabs": [{"id": int, "title": str, ...}, ...]}
            - Array contains 2 tabs
            - Tabs sorted by ID ascending
        """
        response = client_with_samples.get("/api/v1/tabs")

        assert response.status_code == 200
        data = response.json()
        assert "tabs" in data
        assert isinstance(data["tabs"], list)
        assert len(data["tabs"]) == 2
        
        # Verify sorting
        assert data["tabs"][0]["id"] == 1
        assert data["tabs"][0]["title"] == "Wonderwall"
        assert data["tabs"][1]["id"] == 2
        assert data["tabs"][1]["title"] == "Blackbird"

    def test_get_all_tabs_response_schema(
        self, client_with_samples: TestClient
    ) -> None:
        """Test GET /api/v1/tabs response matches contract schema.

        Expected schema per contracts/openapi.md:
        {
            "tabs": [
                {
                    "id": integer,
                    "title": string,
                    "artist": string,
                    "content": string
                }
            ]
        }
        """
        response = client_with_samples.get("/api/v1/tabs")

        assert response.status_code == 200
        data = response.json()

        # Root has "tabs" key
        assert list(data.keys()) == ["tabs"]

        # Each tab has required fields
        for tab in data["tabs"]:
            assert isinstance(tab, dict)
            assert "id" in tab
            assert "title" in tab
            assert "artist" in tab
            assert "content" in tab
            
            # Field types correct
            assert isinstance(tab["id"], int)
            assert isinstance(tab["title"], str)
            assert isinstance(tab["artist"], str)
            assert isinstance(tab["content"], str)

    def test_get_all_tabs_empty_storage(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test GET /api/v1/tabs with no tabs returns empty list.

        Scenario:
            - Storage directory exists but is empty

        Expected:
            - Status code 200 OK
            - Response: {"tabs": []}
        """
        response = client_with_clean_storage.get("/api/v1/tabs")

        assert response.status_code == 200
        data = response.json()
        assert data == {"tabs": []}


@pytest.mark.contract
class TestGetTabByIdEndpoint:
    """Contract tests for GET /api/v1/tabs/{id} endpoint."""

    def test_get_tab_by_id_success(
        self, client_with_samples: TestClient
    ) -> None:
        """Test GET /api/v1/tabs/{id} returns single tab.

        Scenario:
            - Storage has 2 sample tabs
            - Request GET /api/v1/tabs/1

        Expected:
            - Status code 200 OK
            - Response: {"id": 1, "title": "Wonderwall", "artist": "Oasis", "content": "..."}
        """
        response = client_with_samples.get("/api/v1/tabs/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Wonderwall"
        assert data["artist"] == "Oasis"
        assert isinstance(data["content"], str)

    def test_get_tab_by_id_second_tab(
        self, client_with_samples: TestClient
    ) -> None:
        """Test GET /api/v1/tabs/{id} for second tab.

        Scenario:
            - Storage has 2 sample tabs
            - Request GET /api/v1/tabs/2

        Expected:
            - Status code 200 OK
            - Returns Blackbird tab
        """
        response = client_with_samples.get("/api/v1/tabs/2")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert data["title"] == "Blackbird"
        assert data["artist"] == "Beatles"

    def test_get_tab_by_id_not_found(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test GET /api/v1/tabs/{id} returns 404 when tab not found.

        Scenario:
            - Storage is empty
            - Request GET /api/v1/tabs/999

        Expected:
            - Status code 404 Not Found
        """
        response = client_with_clean_storage.get("/api/v1/tabs/999")

        assert response.status_code == 404

    def test_get_tab_by_id_invalid_id(
        self, client_with_samples: TestClient
    ) -> None:
        """Test GET /api/v1/tabs/{id} with invalid ID.

        Scenario:
            - Request GET /api/v1/tabs/99 (tab doesn't exist)

        Expected:
            - Status code 404 Not Found
        """
        response = client_with_samples.get("/api/v1/tabs/99")

        assert response.status_code == 404


@pytest.mark.contract
class TestHealthEndpoint:
    """Contract tests for health check endpoint."""

    def test_health_check(self) -> None:
        """Test GET /health returns 200 with ok status.

        Scenario:
            - Request GET /health

        Expected:
            - Status code 200 OK
            - Response: {"status": "ok"}
        """
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "ok"}

