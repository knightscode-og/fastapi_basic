"""Base models for error responses and common structures."""

from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response format for all API error cases.
    
    Provides consistent error schema across all endpoints for better client
    error handling and debugging.
    
    Attributes:
        error: Machine-readable error code (e.g., 'not_found', 'invalid_request')
        message: Human-readable error description
        details: Additional error context (field names, validation info, etc.)
    """

    error: str = Field(..., description="Error code identifier")
    message: str = Field(..., description="Error description")
    details: dict[str, Any] = Field(default_factory=dict, description="Additional error context")


class TabsListResponse(BaseModel):
    """Response wrapper for GET /api/v1/tabs endpoint.
    
    Provides consistent structure for list responses with potential
    for future pagination metadata.
    
    Attributes:
        tabs: List of MusicTab objects returned from storage
    """

    tabs: list[Any] = Field(..., description="List of music tabs")
