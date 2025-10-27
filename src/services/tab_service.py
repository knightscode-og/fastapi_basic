"""Tab storage and retrieval service.

Implements repository pattern with in-memory cache + file persistence.
Tabs are stored as individual JSON files in storage/tabs/ directory,
enabling future migration to async database with no interface changes.
"""

import json
import logging
from pathlib import Path

from src.models.tab import MusicTab, MusicTabCreate

logger = logging.getLogger(__name__)


class TabService:
    """Service for managing music tabs with file-based persistence.
    
    Maintains in-memory cache of all tabs for fast retrieval (<50ms),
    persists each tab to individual JSON file for durability and
    future database migration compatibility.
    
    Strategy:
    - On initialization: Load all tabs from storage/tabs/*.json into memory dict
    - On retrieval: Return from in-memory cache (fast, <50ms expected)
    - On creation: Write to file AND update memory (durable + fast)
    - Max ID tracked in memory, recovered from file system on startup
    
    This design enables Phase 2 migration: Replace file I/O with DB queries
    while keeping service interface identical.
    """

    def __init__(self, storage_dir: str | Path = "storage/tabs") -> None:
        """Initialize TabService and load existing tabs from storage.
        
        Args:
            storage_dir: Path to directory containing tab JSON files.
                        Directory will be created if it doesn't exist.
        
        Attributes:
            storage_dir: Pathlib Path object for the storage directory
            tabs: In-memory dict keyed by tab ID for fast O(1) retrieval
            max_id: Highest tab ID seen (used for auto-increment on create)
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.tabs: dict[int, MusicTab] = {}
        self.max_id: int = 0

        # Load all existing tabs from storage on startup
        self._load_tabs_from_storage()

        logger.debug(
            "TabService initialized: %d tabs loaded, max_id=%d",
            len(self.tabs),
            self.max_id,
        )

    def _load_tabs_from_storage(self) -> None:
        """Scan storage directory and load all tabs into memory cache.
        
        Called on service initialization to recover persistent state.
        Scans for *.json files in storage_dir, parses each as MusicTab.
        
        Side Effects:
            - Populates self.tabs dict with all found tabs
            - Updates self.max_id to highest ID encountered
        
        Error Handling:
            - Logs warning for malformed JSON files, continues loading others
            - If storage dir empty, starts with empty cache and max_id=0
        """
        json_files = sorted(self.storage_dir.glob("*.json"))

        if not json_files:
            logger.debug("No tabs found in %s", self.storage_dir)
            return

        for file_path in json_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    tab = MusicTab(**data)  # Validate with Pydantic
                    self.tabs[tab.id] = tab
                    self.max_id = max(self.max_id, tab.id)
                    logger.debug("Loaded tab %d from %s", tab.id, file_path.name)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Failed to load %s: %s", file_path.name, e)

    def get_all(self) -> list[MusicTab]:
        """Retrieve all stored tabs.
        
        Returns tabs from in-memory cache in ID order (ascending).
        
        Returns:
            List of all MusicTab objects sorted by ID.
            Empty list if no tabs stored.
        
        Performance:
            Expected <50ms for typical tab counts (<1000 tabs)
            O(n log n) due to sorting, but very fast in practice
        
        Raises:
            No exceptions raised. Empty list returned if storage empty.
        """
        tabs_list = sorted(self.tabs.values(), key=lambda t: t.id)
        logger.debug("get_all() returned %d tabs", len(tabs_list))
        return tabs_list

    def get_by_id(self, tab_id: int) -> MusicTab | None:
        """Retrieve a single tab by its unique ID.
        
        Lookup from in-memory cache for constant-time retrieval.
        
        Args:
            tab_id: Unique tab identifier to look up
        
        Returns:
            MusicTab object if found, None if not found.
        
        Performance:
            Expected <20ms for any tab ID (O(1) dict lookup)
        
        Log Behavior:
            - Debug level: Cache hit/miss tracking
        """
        tab = self.tabs.get(tab_id)
        hit_miss = "hit" if tab else "miss"
        logger.debug("get_by_id(%d): cache %s", tab_id, hit_miss)
        return tab

    def create(self, tab_create: MusicTabCreate) -> MusicTab:
        """Create and persist a new music tab.
        
        Assigns next auto-incremented ID, creates MusicTab object,
        persists to JSON file, and adds to in-memory cache.
        
        Args:
            tab_create: MusicTabCreate object with title, artist, content
        
        Returns:
            Created MusicTab object with assigned ID
        
        Performance:
            Expected <100ms including file I/O
        
        Side Effects:
            - Increments self.max_id
            - Adds tab to self.tabs dict
            - Creates storage/tabs/{id}.json file
        
        Raises:
            OSError: If file write fails (disk full, permission denied, etc.)
            ValueError: If JSON serialization fails (shouldn't occur with Pydantic models)
        """
        # Auto-increment ID
        self.max_id += 1
        new_id = self.max_id

        # Create tab object with assigned ID
        new_tab = MusicTab(
            id=new_id,
            title=tab_create.title,
            artist=tab_create.artist,
            content=tab_create.content,
        )

        # Persist to file
        file_path = self.storage_dir / f"{new_id}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(new_tab.model_dump(), f, indent=2)
            logger.info("Created tab %d: %s by %s", new_id, new_tab.title, new_tab.artist)
        except OSError as e:
            # Roll back ID increment if file write fails
            self.max_id -= 1
            logger.error("Failed to persist tab %d: %s", new_id, e)
            raise

        # Add to memory cache
        self.tabs[new_id] = new_tab
        return new_tab
