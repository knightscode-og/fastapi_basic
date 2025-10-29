"""GET and POST endpoint handlers for music tabs API.

Provides endpoints for retrieving and creating tabs.
Routes mounted in src/main.py.
"""

import logging

from fastapi import APIRouter, HTTPException

from src.main import tab_service
from src.models.base import TabsListResponse
from src.models.tab import MusicTab, MusicTabCreate
from src.utils.timing import measure_latency

logger = logging.getLogger(__name__)

# Create router for tab endpoints
router: APIRouter = APIRouter()


@router.get("/tabs", response_model=TabsListResponse, status_code=200)
@measure_latency("GET /api/v1/tabs")
async def get_all_tabs() -> TabsListResponse:
    """Retrieve all stored music tabs.

    Returns a list of all tabs in the system, sorted by ID in ascending order.

    Returns:
        TabsListResponse containing list of MusicTab objects

    Raises:
        Exception: If storage read fails (will be handled by global exception handler)

    Performance:
        Expected <200ms for typical tab counts (monitored per Principle IV)
    """
    logger.debug("GET /api/v1/tabs: Retrieving all tabs")

    # Call service to get all tabs
    tabs: list[MusicTab] = tab_service.get_all()

    logger.info("GET /api/v1/tabs: Returning %d tabs", len(tabs))
    return TabsListResponse(tabs=tabs)


@router.get("/tabs/{tab_id}", response_model=MusicTab, status_code=200)
@measure_latency("GET /api/v1/tabs/{id}")
async def get_tab_by_id(tab_id: int) -> MusicTab:
    """Retrieve a single tab by ID.

    Args:
        tab_id: Unique tab identifier

    Returns:
        MusicTab object with requested ID

    Raises:
        HTTPException(404): If tab not found

    Performance:
        Expected <20ms for any tab ID (O(1) cache lookup)
    """
    logger.debug("GET /api/v1/tabs/{%s}: Looking up tab", tab_id)

    # Call service to get tab
    tab: MusicTab | None = tab_service.get_by_id(tab_id)

    if tab is None:
        logger.warning("GET /api/v1/tabs/{%s}: Tab not found", tab_id)
        # Return 404 - will be caught by endpoint and converted to ErrorResponse
        # by FastAPI's default 404 handling
        raise HTTPException(status_code=404, detail="Tab not found")

    logger.info("GET /api/v1/tabs/{%s}: Returning tab %s", tab_id, tab.title)
    return tab


@router.post("/tabs", response_model=MusicTab, status_code=201)
@measure_latency("POST /api/v1/tabs")
async def create_tab(tab_create: MusicTabCreate) -> MusicTab:
    """Create a new music tab.

    Args:
        tab_create: MusicTabCreate object with title, artist, content

    Returns:
        Created MusicTab object with auto-assigned ID

    Raises:
        HTTPException(400): If validation fails (handled by FastAPI/Pydantic)
        HTTPException(500): If storage write fails

    Performance:
        Expected <100ms including file I/O
    """
    logger.debug(
        "POST /api/v1/tabs: Creating tab '%s' by %s",
        tab_create.title,
        tab_create.artist,
    )

    # Call service to create tab
    created_tab: MusicTab = tab_service.create(tab_create)

    logger.info(
        "POST /api/v1/tabs: Created tab %d '%s'",
        created_tab.id,
        created_tab.title,
    )
    return created_tab
