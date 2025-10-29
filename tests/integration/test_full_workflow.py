"""Integration test covering the complete workflow with all endpoints.

Tests the full lifecycle: creating tabs, retrieving all tabs, and retrieving
individual tabs, verifying that all operations work together correctly
without side effects.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


class TestFullWorkflow:
    """Test complete API workflow spanning all three endpoints."""

    def test_full_workflow_post_list_get(self, fixture_empty_storage) -> None:
        """Test complete workflow: POST tabs, GET all, GET individual.
        
        Verifies:
        - POST creates tabs with auto-assigned IDs
        - GET /tabs returns all created tabs
        - GET /tabs/{id} retrieves individual tabs correctly
        - All data persists and remains consistent across requests
        """
        client = TestClient(app)

        # Step 1: Create first tab
        response = client.post(
            "/api/v1/tabs",
            json={
                "title": "Wonderwall",
                "artist": "Oasis",
                "content": "Em7 Csus2 Cadd2",
            },
        )
        assert response.status_code == 201
        tab1_data = response.json()
        tab1_id = tab1_data["id"]
        assert tab1_id == 1
        assert tab1_data["title"] == "Wonderwall"

        # Step 2: Create second tab
        response = client.post(
            "/api/v1/tabs",
            json={
                "title": "Stairway to Heaven",
                "artist": "Led Zeppelin",
                "content": "D Dsus4 D D Dsus4",
            },
        )
        assert response.status_code == 201
        tab2_data = response.json()
        tab2_id = tab2_data["id"]
        assert tab2_id == 2
        assert tab2_data["title"] == "Stairway to Heaven"

        # Step 3: Create third tab
        response = client.post(
            "/api/v1/tabs",
            json={
                "title": "Comfortably Numb",
                "artist": "Pink Floyd",
                "content": "Bm Bb F#m Fm",
            },
        )
        assert response.status_code == 201
        tab3_data = response.json()
        tab3_id = tab3_data["id"]
        assert tab3_id == 3

        # Step 4: GET all tabs - verify all 3 returned
        response = client.get("/api/v1/tabs")
        assert response.status_code == 200
        all_tabs = response.json()
        assert len(all_tabs["tabs"]) == 3
        assert all_tabs["tabs"][0]["id"] == 1
        assert all_tabs["tabs"][1]["id"] == 2
        assert all_tabs["tabs"][2]["id"] == 3

        # Step 5: GET individual tabs - verify correct data
        response = client.get(f"/api/v1/tabs/{tab1_id}")
        assert response.status_code == 200
        retrieved_tab1 = response.json()
        assert retrieved_tab1["id"] == tab1_id
        assert retrieved_tab1["title"] == "Wonderwall"
        assert retrieved_tab1["artist"] == "Oasis"

        response = client.get(f"/api/v1/tabs/{tab2_id}")
        assert response.status_code == 200
        retrieved_tab2 = response.json()
        assert retrieved_tab2["id"] == tab2_id
        assert retrieved_tab2["title"] == "Stairway to Heaven"

        response = client.get(f"/api/v1/tabs/{tab3_id}")
        assert response.status_code == 200
        retrieved_tab3 = response.json()
        assert retrieved_tab3["id"] == tab3_id
        assert retrieved_tab3["title"] == "Comfortably Numb"

    def test_full_workflow_error_cases(self, fixture_empty_storage) -> None:
        """Test error paths in complete workflow.
        
        Verifies:
        - POST with missing field returns 400
        - POST with extra field returns 400
        - GET non-existent tab returns 404
        - System continues working after errors
        """
        client = TestClient(app)

        # Test POST with missing field
        response = client.post(
            "/api/v1/tabs",
            json={"title": "Test", "artist": "Artist"},
            # Missing "content"
        )
        assert response.status_code == 400
        error = response.json()
        assert error["error"] == "invalid_request"
        assert "missing_fields" in error["details"]

        # Test POST with extra field
        response = client.post(
            "/api/v1/tabs",
            json={
                "title": "Test",
                "artist": "Artist",
                "content": "Content",
                "genre": "Rock",  # Extra field
            },
        )
        assert response.status_code == 400
        error = response.json()
        assert error["error"] == "invalid_request"
        assert "extra_fields" in error["details"]

        # Test GET non-existent tab
        response = client.get("/api/v1/tabs/999")
        assert response.status_code == 404

        # Verify system still works - create a tab successfully
        response = client.post(
            "/api/v1/tabs",
            json={
                "title": "Valid Tab",
                "artist": "Valid Artist",
                "content": "Valid Content",
            },
        )
        assert response.status_code == 201
        tab_id = response.json()["id"]
        assert tab_id == 1

        # Verify GET works after errors
        response = client.get(f"/api/v1/tabs/{tab_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Valid Tab"

    def test_full_workflow_no_side_effects(self, fixture_empty_storage) -> None:
        """Test that operations have no unintended side effects.
        
        Verifies:
        - GET operations don't modify state
        - Multiple GETs return same data
        - Tab counts remain stable
        """
        client = TestClient(app)

        # Create a tab
        response = client.post(
            "/api/v1/tabs",
            json={
                "title": "Test",
                "artist": "Artist",
                "content": "Content",
            },
        )
        assert response.status_code == 201
        created_tab = response.json()

        # GET all multiple times
        for _ in range(3):
            response = client.get("/api/v1/tabs")
            assert response.status_code == 200
            all_tabs = response.json()
            assert len(all_tabs["tabs"]) == 1
            assert all_tabs["tabs"][0]["id"] == created_tab["id"]

        # GET by ID multiple times
        for _ in range(3):
            response = client.get(f"/api/v1/tabs/{created_tab['id']}")
            assert response.status_code == 200
            retrieved = response.json()
            assert retrieved == created_tab

        # Verify still only 1 tab
        response = client.get("/api/v1/tabs")
        assert response.status_code == 200
        all_tabs = response.json()
        assert len(all_tabs["tabs"]) == 1
