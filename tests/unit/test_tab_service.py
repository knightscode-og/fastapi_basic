"""Unit tests for TabService business logic.

Tests TabService methods in isolation without FastAPI/HTTP layer.
Uses fixtures to ensure test isolation and repeatability.
"""

import pytest

from src.models.tab import MusicTab, MusicTabCreate
from src.services.tab_service import TabService


@pytest.mark.unit
class TestTabServiceGetAll:
    """Tests for TabService.get_all() method."""

    def test_get_all_with_sample_tabs(
        self, fixture_tab_service_with_samples: TabService
    ) -> None:
        """Test get_all() returns all loaded tabs in ID order.

        Scenario:
            - Service pre-loaded with 2 sample tabs (Wonderwall, Blackbird)
        
        Expected:
            - Returns list of exactly 2 MusicTab objects
            - Sorted by ID ascending (tab 1, then tab 2)
            - All fields present and correct
        """
        tabs = fixture_tab_service_with_samples.get_all()

        assert isinstance(tabs, list)
        assert len(tabs) == 2
        assert tabs[0].id == 1
        assert tabs[0].title == "Wonderwall"
        assert tabs[1].id == 2
        assert tabs[1].title == "Blackbird"

    def test_get_all_returns_musicTab_objects(
        self, fixture_tab_service_with_samples: TabService
    ) -> None:
        """Test get_all() returns proper MusicTab objects with all fields.

        Scenario:
            - Service pre-loaded with sample tabs

        Expected:
            - Each item is MusicTab instance
            - All required fields present (id, title, artist, content)
            - All fields have correct types
        """
        tabs = fixture_tab_service_with_samples.get_all()

        for tab in tabs:
            assert isinstance(tab, MusicTab)
            assert isinstance(tab.id, int)
            assert isinstance(tab.title, str)
            assert isinstance(tab.artist, str)
            assert isinstance(tab.content, str)
            assert len(tab.title) > 0
            assert len(tab.artist) > 0

    def test_get_all_empty_storage(self, fixture_tab_service: TabService) -> None:
        """Test get_all() with no tabs in storage returns empty list.

        Scenario:
            - Service initialized with empty storage directory

        Expected:
            - Returns empty list []
            - Does not raise exception
        """
        tabs = fixture_tab_service.get_all()

        assert isinstance(tabs, list)
        assert len(tabs) == 0


@pytest.mark.unit
class TestTabServiceGetById:
    """Tests for TabService.get_by_id() method."""

    def test_get_by_id_found(self, fixture_tab_service_with_samples: TabService) -> None:
        """Test get_by_id() returns correct tab when ID exists.

        Scenario:
            - Service loaded with 2 sample tabs
            - Looking up ID 1 (Wonderwall)

        Expected:
            - Returns MusicTab with id=1
            - All fields match loaded tab
        """
        tab = fixture_tab_service_with_samples.get_by_id(1)

        assert tab is not None
        assert isinstance(tab, MusicTab)
        assert tab.id == 1
        assert tab.title == "Wonderwall"
        assert tab.artist == "Oasis"

    def test_get_by_id_not_found(self, fixture_tab_service_with_samples: TabService) -> None:
        """Test get_by_id() returns None when ID does not exist.

        Scenario:
            - Service loaded with 2 sample tabs (IDs 1, 2)
            - Looking up non-existent ID 999

        Expected:
            - Returns None
            - Does not raise exception
        """
        tab = fixture_tab_service_with_samples.get_by_id(999)

        assert tab is None

    def test_get_by_id_empty_storage(self, fixture_tab_service: TabService) -> None:
        """Test get_by_id() with empty storage returns None.

        Scenario:
            - Service initialized with empty storage

        Expected:
            - Returns None for any ID
        """
        tab = fixture_tab_service.get_by_id(1)

        assert tab is None


@pytest.mark.unit
class TestTabServiceCreate:
    """Tests for TabService.create() method."""

    def test_create_success(
        self, fixture_tab_service: TabService, fixture_valid_tab_create: MusicTabCreate
    ) -> None:
        """Test create() successfully persists tab and returns with assigned ID.

        Scenario:
            - Service with empty storage
            - Creating valid tab with title, artist, content

        Expected:
            - Returns MusicTab with assigned id=1
            - All fields match input
            - ID is positive integer
        """
        created_tab = fixture_tab_service.create(fixture_valid_tab_create)

        assert isinstance(created_tab, MusicTab)
        assert created_tab.id == 1
        assert created_tab.title == fixture_valid_tab_create.title
        assert created_tab.artist == fixture_valid_tab_create.artist
        assert created_tab.content == fixture_valid_tab_create.content

    def test_create_increments_id(self, fixture_tab_service: TabService) -> None:
        """Test create() auto-increments ID across multiple calls.

        Scenario:
            - Service with empty storage
            - Creating 3 tabs sequentially

        Expected:
            - First tab gets ID 1
            - Second tab gets ID 2
            - Third tab gets ID 3
            - IDs are unique and monotonically increasing
        """
        tab1_create = MusicTabCreate(
            title="Tab 1", artist="Artist 1", content="Content 1"
        )
        tab2_create = MusicTabCreate(
            title="Tab 2", artist="Artist 2", content="Content 2"
        )
        tab3_create = MusicTabCreate(
            title="Tab 3", artist="Artist 3", content="Content 3"
        )

        tab1 = fixture_tab_service.create(tab1_create)
        tab2 = fixture_tab_service.create(tab2_create)
        tab3 = fixture_tab_service.create(tab3_create)

        assert tab1.id == 1
        assert tab2.id == 2
        assert tab3.id == 3
        assert len(set([tab1.id, tab2.id, tab3.id])) == 3  # All unique

    def test_create_persists_to_file(
        self, fixture_tab_service: TabService, fixture_valid_tab_create: MusicTabCreate
    ) -> None:
        """Test create() writes tab to storage file.

        Scenario:
            - Service with empty storage
            - Creating valid tab

        Expected:
            - File storage/tabs_test/{id}.json is created
            - File contains valid JSON with MusicTab fields
        """
        created_tab = fixture_tab_service.create(fixture_valid_tab_create)
        
        tab_file = fixture_tab_service.storage_dir / f"{created_tab.id}.json"
        assert tab_file.exists()

        # Verify file contents
        import json
        with open(tab_file, encoding="utf-8") as f:
            data = json.load(f)
            assert data["id"] == created_tab.id
            assert data["title"] == created_tab.title
            assert data["artist"] == created_tab.artist
            assert data["content"] == created_tab.content

    def test_create_persists_to_cache(
        self, fixture_tab_service: TabService, fixture_valid_tab_create: MusicTabCreate
    ) -> None:
        """Test create() adds tab to in-memory cache.

        Scenario:
            - Service with empty storage
            - Creating valid tab

        Expected:
            - Tab immediately retrievable via get_by_id()
            - Tab appears in get_all() results
        """
        created_tab = fixture_tab_service.create(fixture_valid_tab_create)

        # Verify in cache
        cached_tab = fixture_tab_service.get_by_id(created_tab.id)
        assert cached_tab == created_tab

        # Verify in get_all()
        all_tabs = fixture_tab_service.get_all()
        assert len(all_tabs) == 1
        assert all_tabs[0].id == created_tab.id
