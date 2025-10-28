"""API route endpoints for the Music Tabs API.

Route handlers organized by resource (tabs, health checks, etc.).
Each module exports a FastAPI APIRouter that can be included in the main app.
"""

from src.api.endpoints.tabs import router as tabs_router

__all__ = ["tabs_router"]
