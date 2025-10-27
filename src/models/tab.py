"""Music tab data models for storage and API contracts."""

from pydantic import BaseModel, Field


class MusicTab(BaseModel):
    """Represents a music tab stored in the system.
    
    A complete tab includes the unique system-assigned ID plus the user-provided
    content for the musical piece.
    
    Attributes:
        id: Unique integer identifier (system-assigned on creation)
        title: Name of the musical piece
        artist: Name of the artist or composer
        content: The actual tab content (text format, e.g., ASCII tab notation)
    """

    id: int = Field(..., ge=1, description="Unique tab identifier")
    title: str = Field(..., min_length=1, description="Title of the musical piece")
    artist: str = Field(..., min_length=1, description="Artist or composer name")
    content: str = Field(..., min_length=1, description="Tab content in text format")

    class Config:
        """Pydantic configuration for JSON serialization."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Wonderwall",
                "artist": "Oasis",
                "content": "Em7 Csus2 Cadd2\n[tab notation here]",
            }
        }


class MusicTabCreate(BaseModel):
    """Request model for creating a new music tab (POST /api/v1/tabs).
    
    Clients provide only the tab content; the system assigns the unique ID.
    Rejects any extra fields for API contract consistency.
    
    Attributes:
        title: Name of the musical piece (required)
        artist: Name of the artist or composer (required)
        content: The tab content in text format (required)
    """

    title: str = Field(..., min_length=1, description="Title of the musical piece")
    artist: str = Field(..., min_length=1, description="Artist or composer name")
    content: str = Field(..., min_length=1, description="Tab content in text format")

    class Config:
        """Pydantic configuration."""

        extra = "forbid"  # Reject any fields not explicitly defined
        json_schema_extra = {
            "example": {
                "title": "Wonderwall",
                "artist": "Oasis",
                "content": "Em7 Csus2 Cadd2\n[tab notation here]",
            }
        }
