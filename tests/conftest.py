"""Pytest configuration and shared fixtures for all tests.

Fixtures in this file are automatically available to all test modules
without explicit import.

Test Isolation Strategy:
- Each test gets a fresh, empty storage directory
- Sample fixtures provide pre-populated data for integration tests
- TabService fixtures ensure independence between test runs
"""

import json
import shutil
from pathlib import Path
from typing import Generator

import pytest

from src.models.tab import MusicTab, MusicTabCreate
from src.services.tab_service import TabService


@pytest.fixture
def fixture_empty_storage() -> Generator[Path, None, None]:
    """Create and return empty storage directory for test isolation.
    
    Clears any existing tabs to provide clean state for each test.
    Directory is created fresh and can be safely used by any test.
    
    Yields:
        Path to empty storage/tabs_test/ directory
    
    Cleanup:
        Removes directory and all files after test completion
    """
    storage_path = Path("storage/tabs_test")
    
    # Clean up any previous test run
    if storage_path.exists():
        shutil.rmtree(storage_path)
    
    storage_path.mkdir(parents=True, exist_ok=True)
    
    yield storage_path
    
    # Cleanup after test
    if storage_path.exists():
        shutil.rmtree(storage_path)


@pytest.fixture
def fixture_sample_tabs(fixture_empty_storage: Path) -> Path:
    """Pre-populate test storage with sample tabs.
    
    Creates two well-known music tabs for testing:
    - Tab 1: Wonderwall by Oasis
    - Tab 2: Blackbird by Beatles
    
    Args:
        fixture_empty_storage: Provides empty storage directory
    
    Returns:
        Path to storage directory with 2 pre-loaded tabs
    
    Tab Files Created:
        storage/tabs_test/1.json - Wonderwall tab
        storage/tabs_test/2.json - Blackbird tab
    """
    storage_path = fixture_empty_storage
    
    # Tab 1: Wonderwall
    tab1 = MusicTab(
        id=1,
        title="Wonderwall",
        artist="Oasis",
        content="Em7 Csus2 Cadd2\n|Em7 Csus2 | Cadd2 | Em7 | Csus2 | Cadd2 |",
    )
    with open(storage_path / "1.json", "w") as f:
        json.dump(tab1.model_dump(), f, indent=2)
    
    # Tab 2: Blackbird
    tab2 = MusicTab(
        id=2,
        title="Blackbird",
        artist="Beatles",
        content="G Dm Em Em(add11)\nG /      G Dm | Dm Em Em(add11)",
    )
    with open(storage_path / "2.json", "w") as f:
        json.dump(tab2.model_dump(), f, indent=2)
    
    return storage_path


@pytest.fixture
def fixture_tab_service(fixture_empty_storage: Path) -> TabService:
    """Create fresh TabService instance for each test.
    
    Uses empty storage fixture to ensure no state leakage between tests.
    Each test gets a pristine service instance.
    
    Args:
        fixture_empty_storage: Provides empty storage directory
    
    Returns:
        Fresh TabService instance with empty storage
    """
    return TabService(storage_dir=fixture_empty_storage)


@pytest.fixture
def fixture_tab_service_with_samples(fixture_sample_tabs: Path) -> TabService:
    """Create TabService with pre-loaded sample tabs.
    
    Useful for testing retrieval operations without creating tabs first.
    Service loads the sample tabs automatically on initialization.
    
    Args:
        fixture_sample_tabs: Provides storage with 2 sample tabs
    
    Returns:
        TabService instance with 2 pre-loaded tabs (IDs 1 and 2)
    """
    service = TabService(storage_dir=fixture_sample_tabs)
    # Verify samples were loaded
    assert len(service.tabs) == 2, f"Expected 2 tabs, got {len(service.tabs)}"
    return service


@pytest.fixture
def fixture_valid_tab_create() -> MusicTabCreate:
    """Create a valid MusicTabCreate object for testing.
    
    Returns:
        MusicTabCreate with valid test data (ready for POST requests)
    """
    return MusicTabCreate(
        title="Test Song",
        artist="Test Artist",
        content="Tab content here",
    )


@pytest.fixture
def fixture_invalid_tab_data() -> dict[str, str]:
    """Create invalid tab data for testing error cases.
    
    Returns:
        Dict missing required field (title) to trigger validation error
    """
    return {
        "artist": "Test Artist",
        "content": "Tab content here",
        # Missing "title" to trigger validation error
    }


# Pytest configuration for the entire test suite
def pytest_configure(config):  # noqa: ARG001
    """Configure pytest with custom markers.
    
    Allows tests to be marked with @pytest.mark.slow, @pytest.mark.integration
    for selective test execution.
    """
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration")
    config.addinivalue_line("markers", "unit: marks tests as unit")
