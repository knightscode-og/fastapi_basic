"""Integration tests for complete API workflows.

Tests multi-component flows: service + endpoint + storage + response.
Verifies end-to-end behavior from request to response.
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
    """Create TestClient with sample tabs."""
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


@pytest.mark.integration
class TestTabsWorkflow:
    """Integration tests for complete tab workflows."""

    def test_get_all_tabs_full_workflow(
        self, client_with_samples: TestClient
    ) -> None:
        """Test complete GET /api/v1/tabs workflow end-to-end.

        Scenario:
            - Storage pre-populated with 2 sample tabs
            - Execute GET /api/v1/tabs
            - Verify response

        Expected:
            - All 2 tabs returned
            - Data unchanged from storage
            - Order stable (same order on repeated calls)
        """
        # First GET request
        response1 = client_with_samples.get("/api/v1/tabs")
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1["tabs"]) == 2

        # Verify order and data
        assert data1["tabs"][0]["id"] == 1
        assert data1["tabs"][0]["title"] == "Wonderwall"
        assert data1["tabs"][1]["id"] == 2
        assert data1["tabs"][1]["title"] == "Blackbird"

        # Second GET request should return same data in same order
        response2 = client_with_samples.get("/api/v1/tabs")
        data2 = response2.json()
        assert data1 == data2

    def test_get_all_tabs_with_multiple_storage_files(
        self, client_with_samples: TestClient, fixture_valid_tab_create
    ) -> None:
        """Test GET /api/v1/tabs retrieves all tabs created via service.

        Scenario:
            - Retrieve tabs from pre-populated storage with 2 sample tabs
            - GET /api/v1/tabs
            - Verify all returned with correct data

        Expected:
            - All tabs returned
            - IDs and data match what was created
        """
        response = client_with_samples.get("/api/v1/tabs")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tabs"]) == 2
        
        # Verify first tab
        assert data["tabs"][0]["id"] == 1
        assert data["tabs"][0]["title"] == "Wonderwall"
        
        # Verify second tab
        assert data["tabs"][1]["id"] == 2
        assert data["tabs"][1]["title"] == "Blackbird"

    def test_get_all_tabs_empty_response_handling(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test GET /api/v1/tabs handles empty storage gracefully.

        Scenario:
            - Storage directory exists but no tabs

        Expected:
            - Status 200 OK
            - Empty tabs array
            - No error response
        """
        response = client_with_clean_storage.get("/api/v1/tabs")

        assert response.status_code == 200
        data = response.json()
        assert data["tabs"] == []
        assert "error" not in data
