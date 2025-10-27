# API Contracts: Music Tabs API

**Phase**: Phase 1 - Design & Contracts  
**Date**: 2025-10-27  
**Format**: OpenAPI 3.0.0 (auto-generated from FastAPI)

## Endpoint Contracts

### 1. GET /api/v1/tabs - Retrieve All Tabs

**Summary**: Get all stored music tabs

**Method**: GET  
**Path**: `/api/v1/tabs`  
**Authentication**: None (MVP)

**Query Parameters**: None

**Request Body**: None

**Success Response** (HTTP 200):
```json
{
  "tabs": [
    {
      "id": 1,
      "title": "Wonderwall",
      "artist": "Oasis",
      "content": "Em7 Dsus2 A7sus4..."
    },
    {
      "id": 2,
      "title": "Blackbird",
      "artist": "The Beatles",
      "content": "G Dm Dm6..."
    }
  ]
}
```

**Empty Response** (HTTP 200, no tabs stored):
```json
{
  "tabs": []
}
```

**Error Response** (HTTP 500 - Server Error):
```json
{
  "error": "internal_server_error",
  "message": "Failed to retrieve tabs",
  "details": {}
}
```

**Performance Requirement**: p95 latency ≤ 200ms

**Test Cases**:
- ✓ Multiple tabs exist: return all tabs
- ✓ No tabs exist: return empty array
- ✓ Response time < 200ms

---

### 2. GET /api/v1/tabs/{id} - Retrieve Single Tab by ID

**Summary**: Get a specific music tab by ID

**Method**: GET  
**Path**: `/api/v1/tabs/{id}`  
**Authentication**: None (MVP)

**Path Parameters**:
- `id` (integer): Tab ID, must be positive integer

**Query Parameters**: None

**Request Body**: None

**Success Response** (HTTP 200):
```json
{
  "id": 1,
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

**Error Response - Not Found** (HTTP 404):
```json
{
  "error": "not_found",
  "message": "Tab not found",
  "details": {
    "id": 999
  }
}
```

**Error Response - Invalid ID** (HTTP 400):
```json
{
  "error": "invalid_request",
  "message": "Invalid tab ID",
  "details": {}
}
```

**Error Response - Server Error** (HTTP 500):
```json
{
  "error": "internal_server_error",
  "message": "Failed to retrieve tab",
  "details": {}
}
```

**Performance Requirement**: p95 latency ≤ 200ms

**Test Cases**:
- ✓ Valid ID (existing tab): return tab
- ✓ Invalid ID (does not exist): return 404
- ✓ Non-numeric ID: return 400
- ✓ Negative ID: return 400
- ✓ Response time < 200ms

---

### 3. POST /api/v1/tabs - Create New Tab

**Summary**: Create and store a new music tab

**Method**: POST  
**Path**: `/api/v1/tabs`  
**Authentication**: None (MVP)

**Request Body** (application/json):
```json
{
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

**Request Validation**:
- All fields required: title, artist, content
- No extra fields allowed
- All fields must be non-empty strings
- Field names must be snake_case

**Success Response** (HTTP 201 - Created):
```json
{
  "id": 3,
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

**Error Response - Missing Fields** (HTTP 400):
```json
{
  "error": "invalid_request",
  "message": "Missing required field: title",
  "details": {
    "missing_fields": ["title"]
  }
}
```

**Error Response - Invalid JSON** (HTTP 400):
```json
{
  "error": "invalid_request",
  "message": "Invalid JSON in request body",
  "details": {}
}
```

**Error Response - Extra Fields** (HTTP 400):
```json
{
  "error": "invalid_request",
  "message": "Unexpected field: genre",
  "details": {}
}
```

**Error Response - Server Error** (HTTP 500):
```json
{
  "error": "internal_server_error",
  "message": "Failed to create tab",
  "details": {}
}
```

**Performance Requirement**: p95 latency ≤ 500ms (includes file write)

**Test Cases**:
- ✓ Valid request: return 201 with created tab + assigned ID
- ✓ Missing title field: return 400
- ✓ Missing artist field: return 400
- ✓ Missing content field: return 400
- ✓ Empty title: return 400
- ✓ Extra fields in request: return 400
- ✓ Sequential requests get unique IDs (auto-increment)
- ✓ Response time < 500ms
- ✓ Tab persists to storage/tabs.json

---

## Error Schema (Consistent Across All Endpoints)

**Standard Error Response Format** (Constitution Principle III):

```json
{
  "error": "error_code",
  "message": "human-readable message",
  "details": {}
}
```

**Error Codes**:
- `invalid_request`: HTTP 400 (malformed request, missing fields, validation failure)
- `not_found`: HTTP 404 (resource doesn't exist)
- `internal_server_error`: HTTP 500 (server-side failure)

**Details Object**:
- Optional context depending on error type
- Examples:
  - `{"id": 999}` for not_found
  - `{"missing_fields": ["title"]}` for invalid_request
  - `{}` for generic internal errors

---

## Response Field Naming Convention

**Requirement**: All response fields use snake_case (Constitution Principle III)

**Applied to all fields**:
- ✓ id (not ID)
- ✓ title (not Title)
- ✓ artist (not Artist)
- ✓ content (not Content)
- ✓ error (not Error)
- ✓ message (not Message)
- ✓ details (not Details)
- ✓ missing_fields (not missingFields)

---

## API Versioning

**Current Version**: v1 (`/api/v1/`)

**Future Breaking Changes**: Will bump to v2 (`/api/v2/`)

**Deprecation Policy**: Old versions supported for ≥2 major releases

---

## OpenAPI/Swagger Documentation

**Auto-generated from FastAPI**:
- Accessible at `http://localhost:8000/docs` (Swagger UI)
- Accessible at `http://localhost:8000/redoc` (ReDoc)
- OpenAPI JSON at `http://localhost:8000/openapi.json`

**Generated from**:
- Endpoint docstrings (summary, description)
- Pydantic model docstrings
- Type hints and validation rules

**Maintenance**: Keep docstrings up-to-date with endpoint changes
