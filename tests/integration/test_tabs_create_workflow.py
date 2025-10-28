"""Integration tests for POST /api/v1/tabs workflow.

Tests multi-component flows: service + endpoint + storage + response.
Verifies end-to-end behavior from POST request to verification via GET.
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


@pytest.mark.integration
class TestCreateTabsWorkflow:
    """Integration tests for complete create tab workflows."""

    def test_create_and_retrieve_workflow(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test complete workflow: POST tab → GET /tabs → verify in list.

        Scenario:
            - POST a new tab
            - GET /api/v1/tabs
            - Verify the tab appears in the list

        Expected:
            - POST returns 201 with tab data
            - GET returns 200 with tabs array containing the created tab
            - Tab data matches what was posted
        """
        # POST a new tab
        payload = {
            "title": "Wonderwall",
            "artist": "Oasis",
            "content": "Em7 Csus2 Cadd2\n...",
        }
        create_response = client_with_clean_storage.post(
            "/api/v1/tabs", json=payload
        )
        assert create_response.status_code == 201
        created_tab = create_response.json()
        assert created_tab["id"] == 1
        assert created_tab["title"] == "Wonderwall"

        # GET all tabs to verify it was stored
        list_response = client_with_clean_storage.get("/api/v1/tabs")
        assert list_response.status_code == 200
        tabs_data = list_response.json()
        assert len(tabs_data["tabs"]) == 1
        assert tabs_data["tabs"][0]["id"] == 1
        assert tabs_data["tabs"][0]["title"] == "Wonderwall"
        assert tabs_data["tabs"][0]["artist"] == "Oasis"

    def test_create_multiple_tabs_id_sequence(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test multiple creates verify ID sequence and GET returns all.

        Scenario:
            - POST 3 tabs sequentially
            - GET /api/v1/tabs
            - Verify all 3 appear with correct IDs

        Expected:
            - Each POST returns 201 with sequential ID
            - GET returns all 3 tabs in ID order
        """
        # Create 3 tabs
        for i in range(1, 4):
            payload = {
                "title": f"Tab {i}",
                "artist": f"Artist {i}",
                "content": f"Content {i}",
            }
            response = client_with_clean_storage.post("/api/v1/tabs", json=payload)
            assert response.status_code == 201
            assert response.json()["id"] == i

        # GET all tabs
        response = client_with_clean_storage.get("/api/v1/tabs")
        assert response.status_code == 200
        tabs_data = response.json()
        assert len(tabs_data["tabs"]) == 3

        # Verify order and IDs
        for i in range(0, 3):
            assert tabs_data["tabs"][i]["id"] == i + 1
            assert tabs_data["tabs"][i]["title"] == f"Tab {i + 1}"

    def test_create_persists_across_service_restart(
        self, client_with_clean_storage: TestClient
    ) -> None:
        """Test created tab persists after tab_service restart.

        Scenario:
            - POST a tab
            - Simulate service restart by creating new TabService
            - GET /api/v1/tabs
            - Verify tab still exists

        Expected:
            - Tab is loaded from storage/tabs/*.json
            - Tab appears in list after restart
            - ID is preserved
        """
        # POST a tab
        payload = {
            "title": "Test Tab",
            "artist": "Test Artist",
            "content": "Test Content",
        }
        response = client_with_clean_storage.post("/api/v1/tabs", json=payload)
        assert response.status_code == 201
        created_id = response.json()["id"]

        # Simulate service restart - create new TabService
        # (this will load tabs from storage/tabs/*.json files)
        storage = Path("storage/tabs")
        new_service = TabService(storage_dir=storage)

        # Verify tab was loaded
        assert len(new_service.tabs) == 1
        assert created_id in new_service.tabs
        loaded_tab = new_service.tabs[created_id]
        assert loaded_tab.title == "Test Tab"
        assert loaded_tab.artist == "Test Artist"

        # Also verify via endpoint
        tabs_module.tab_service = new_service
        response = client_with_clean_storage.get("/api/v1/tabs")
        assert response.status_code == 200
        tabs_data = response.json()
        assert len(tabs_data["tabs"]) == 1
        assert tabs_data["tabs"][0]["title"] == "Test Tab"
