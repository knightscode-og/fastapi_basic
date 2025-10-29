"""FastAPI application entry point for Music Tabs API.

Initializes the FastAPI app with exception handlers, middleware,
and routing structure. Service initialization happens at module level
to ensure single instance shared across all requests.

Architecture:
- Single FastAPI app instance created at module level
- TabService initialized with default storage directory
- Exception handlers convert service errors to ErrorResponse
- Endpoints mounted via include_router (added in subsequent phases)
"""

import json
import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.models.base import ErrorResponse
from src.services.tab_service import TabService

# Configure logging for the application
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Music Tabs API",
    version="1.0.0",
    description="REST API for storing and retrieving music tabs",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Initialize storage directory
storage_dir = Path("storage/tabs")
storage_dir.mkdir(parents=True, exist_ok=True)

# Service instance initialized at module load time
# This ensures tab_service is never None during request handling
tab_service: TabService = TabService(storage_dir=storage_dir)

logger.info("FastAPI app initialized: Music Tabs API v1.0.0")
logger.info("Storage directory: %s", storage_dir.absolute())
logger.info("Loaded %d tabs from storage", len(tab_service.tabs))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors with consistent ErrorResponse format.
    
    Converts FastAPI's default 422 Unprocessable Entity response to 400 Bad Request
    with custom ErrorResponse schema for consistency across all endpoints.
    
    Extracts detailed validation error information including:
    - Missing required fields
    - Extra unexpected fields
    - Type validation failures
    
    Args:
        request: HTTP request that triggered the validation error
        exc: RequestValidationError from FastAPI/Pydantic
    
    Returns:
        JSONResponse with 400 status and ErrorResponse body
    """
    errors = exc.errors()

    # Extract field names from validation errors
    missing_fields = []
    extra_fields = []

    for error in errors:
        if error["type"] == "missing":
            field_name = (
                error["loc"][-1]
                if error["loc"]
                else "unknown"
            )
            missing_fields.append(field_name)
        elif error["type"] == "extra_forbidden":
            field_name = (
                error["loc"][-1]
                if error["loc"]
                else "unknown"
            )
            extra_fields.append(field_name)

    # Build error response details
    details: dict[str, list[str]] = {}
    if missing_fields:
        details["missing_fields"] = missing_fields
    if extra_fields:
        details["extra_fields"] = extra_fields

    # Determine error code and message
    if missing_fields:
        error_code = "invalid_request"
        message = f"Missing required field: {missing_fields[0]}"
    elif extra_fields:
        error_code = "invalid_request"
        message = f"Unexpected field: {extra_fields[0]}"
    else:
        error_code = "invalid_request"
        message = "Invalid request data"

    error_response = ErrorResponse(
        error=error_code,
        message=message,
        details=details,
    )

    logger.warning(
        "Validation error for %s %s: %s",
        request.method,
        request.url.path,
        message,
    )

    return JSONResponse(
        status_code=400,
        content=json.loads(error_response.model_dump_json()),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions with generic 500 error response.
    
    Catches any unhandled exception and returns consistent ErrorResponse
    with 500 Internal Server Error status. Logs exception for debugging.
    
    Args:
        request: HTTP request that triggered the exception
        exc: Unhandled exception
    
    Returns:
        JSONResponse with 500 status and ErrorResponse body
    """
    logger.error(
        "Unhandled exception for %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )

    error_response = ErrorResponse(
        error="internal_server_error",
        message="An unexpected error occurred",
        details={},
    )

    return JSONResponse(
        status_code=500,
        content=json.loads(error_response.model_dump_json()),
    )


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint for deployment monitoring.
    
    Returns:
        JSON object with status "ok" if service is running
    """
    return {"status": "ok"}


# Mount tab endpoints (import after tab_service is initialized)
from src.api.endpoints import tabs_router

app.include_router(tabs_router, prefix="/api/v1", tags=["tabs"])
