"""Data models for the Music Tabs API."""

from src.models.base import ErrorResponse, TabsListResponse
from src.models.tab import MusicTab, MusicTabCreate

__all__ = ["ErrorResponse", "TabsListResponse", "MusicTab", "MusicTabCreate"]
