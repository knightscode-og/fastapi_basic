"""Pytest configuration and shared fixtures for all tests.

Fixtures in this file are automatically available to all test modules
without explicit import.

Test Strategy:
- Unit tests use fixture_tab_service with isolated service instances
- Contract/integration tests use real storage/tabs/ directory (cleaned up per test)
"""

import json
from pathlib import Path
from typing import Generator

import pytest

from src.models.tab import MusicTab, MusicTabCreate
from src.services.tab_service import TabService


@pytest.fixture(autouse=False)
def fixture_empty_storage() -> Generator[None, None, None]:
    """Ensure storage directory exists but is empty for test isolation.
    
    Clears storage/tabs/ before and after each test that uses this fixture.
    Ensures tests don't interfere with each other via persistent storage.
    Initializes tab_service for TestClient usage.
    
    Yields:
        None (fixture just ensures clean storage state)
    """
    from pathlib import Path
    
    storage_path = Path("storage/tabs")
    
    # Clear storage before test
    if storage_path.exists():
        for f in storage_path.glob("*.json"):
            f.unlink()
    
    # Initialize tab_service in src.main module (after all imports complete)
    # Delay import until after fixture setup to avoid cyclic imports
    import src.main
    import src.api.endpoints.tabs as tabs_module
    
    fresh_service = TabService(storage_dir=storage_path)
    src.main.tab_service = fresh_service
    tabs_module.tab_service = fresh_service  # Also update the endpoint reference
    
    yield
    
    # Clear storage after test
    if storage_path.exists():
        for f in storage_path.glob("*.json"):
            f.unlink()


@pytest.fixture
def fixture_tab_service() -> Generator[TabService, None, None]:
    """Create fresh TabService instance for each test.
    
    Creates a temporary storage directory unique to this test.
    Cleans up after test completion.
    
    Yields:
        Fresh TabService instance with empty storage
    """
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        service = TabService(storage_dir=tmpdir)
        yield service


@pytest.fixture
def fixture_tab_service_with_samples() -> Generator[TabService, None, None]:
    """Create TabService with pre-loaded sample tabs.
    
    Useful for testing retrieval operations without creating tabs first.
    Service loads the sample tabs automatically on initialization.
    
    Yields:
        TabService instance with 2 pre-loaded tabs (IDs 1 and 2)
    """
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample tabs
        tab1 = MusicTab(
            id=1,
            title="Wonderwall",
            artist="Oasis",
            content="Em7 Csus2 Cadd2\n|Em7 Csus2 | Cadd2 | Em7 | Csus2 | Cadd2 |",
        )
        tab2 = MusicTab(
            id=2,
            title="Blackbird",
            artist="Beatles",
            content="G Dm Em Em(add11)\nG /      G Dm | Dm Em Em(add11)",
        )
        
        storage_path = Path(tmpdir)
        with open(storage_path / "1.json", "w") as f:
            json.dump(tab1.model_dump(), f, indent=2)
        with open(storage_path / "2.json", "w") as f:
            json.dump(tab2.model_dump(), f, indent=2)
        
        service = TabService(storage_dir=storage_path)
        assert len(service.tabs) == 2, f"Expected 2 tabs, got {len(service.tabs)}"
        yield service


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
    config.addinivalue_line("markers", "contract: marks tests as contract")

