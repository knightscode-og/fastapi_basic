# Research Phase: Music Tabs API

**Phase**: Phase 0 - Research & Technology Selection  
**Date**: 2025-10-27  
**Input**: Technical context from plan.md

## Technology Stack Research

### FastAPI Framework

**Decision**: Use FastAPI 0.104+ for the HTTP server framework

**Rationale**:
- **Built-in async support**: Native async/await for high performance
- **Automatic OpenAPI documentation**: Self-documenting API via docstrings
- **Pydantic validation**: Type-safe request/response handling
- **Lightweight**: Minimal dependencies; simple to deploy
- **Python-first**: Aligns with user's Python requirement

**Alternatives Considered**:
- Flask: Less performant; no built-in async; requires more manual setup
- Django: Too heavyweight for MVP; excessive boilerplate
- FastAPI won (clear winner for this use case)

**Selected Version**: FastAPI 0.104+ (stable, async support, Pydantic v2 compatible)

---

### Uvicorn ASGI Server

**Decision**: Use Uvicorn 0.24+ as the ASGI application server

**Rationale**:
- **Official recommendation**: FastAPI team recommends Uvicorn
- **Performance**: Supports async requests; handles high concurrency
- **Development**: Includes auto-reload for development workflow
- **Deployment**: Single package; easy to containerize

**Selected Version**: Uvicorn 0.24+

---

### Pydantic Models

**Decision**: Use Pydantic v2 for data validation and modeling

**Rationale**:
- **Type hints**: All models have type hints (Constitution Principle I)
- **Validation**: Built-in validation for required fields (Constitution Principle III)
- **Performance**: Fast schema validation
- **JSON serialization**: Native JSON encoding for API responses
- **FastAPI integration**: Automatic request/response validation via Pydantic

**Selected Version**: Pydantic 2.0+

---

### Testing Framework

**Decision**: Use pytest 7.4+, pytest-asyncio 0.21+, coverage.py 7.3+ for testing

**Rationale**:
- **Pytest**: Standard Python testing framework; excellent plugin ecosystem
- **pytest-asyncio**: Required for async test support (TDD with FastAPI)
- **coverage.py**: Industry-standard coverage measurement (target ≥80%)
- **pytest-mock**: Optional but recommended for mocking file I/O

**Selected Versions**: pytest 7.4+, pytest-asyncio 0.21+, coverage.py 7.3+

---

### JSON File Storage

**Decision**: Use separate JSON file per tab (one file per tab ID) with Python's built-in `json` module + `pathlib`

**Rationale**:
- **Atomic writes**: Each file is independent; no concurrent write conflicts on tab creation
- **MVP scope**: File I/O adequate for sample data
- **Phase 2 migration**: Simulates database-per-record pattern for easy migration to async DB writes
- **User requirement**: "store the tabs in json files" + "async connection to write to db in Phase 2"
- **Performance**: File I/O is fast for <10k records (MVP scope)
- **Scalability**: Per-record files scale better than single file as data grows

**Storage Layout**:
```
storage/tabs/
├── 1.json  # {"id": 1, "title": "...", "artist": "...", "content": "..."}
├── 2.json
├── 3.json
└── ...
```

**Implementation Pattern**:
- Single index file (optional): `storage/tabs/index.json` with list of IDs for fast enumeration
- Or scan directory for files to enumerate tabs (simpler, no consistency issues)
- In-memory cache (list) loaded at app startup by scanning `storage/tabs/` directory
- Write-through: After each POST, write new tab to individual file + update index
- Atomic operations: Read-modify-write pattern per file (not across files)

**Concurrency Handling**:
- File creation is atomic at OS level (one thread/process can create file first)
- No ID collisions: Each file is independent; use OS-level file creation atomicity
- If needed for Phase 2 preparation: Can add file locks per tab, but unnecessary for MVP

**Selected Approach**: Python `json` module + `pathlib.Path` + per-tab files

---

### Linting & Type Checking

**Decision**: Use pylint (score ≥8.0) + black (formatting) + mypy --strict (type checking)

**Rationale**:
- **pylint**: Enforces code quality standards (Constitution Principle I)
- **black**: Consistent formatting; removes style debates
- **mypy --strict**: Enforces type safety (Constitution Principle I)
- **Configuration**: All tools configurable via pyproject.toml

**Selected Tools**: pylint 3.0+, black 23.0+, mypy 1.7+

---

## Design Patterns

### Repository Pattern (Simplified)

The `TabService` class acts as a repository:
- Encapsulates file I/O logic
- Provides simple CRUD interface (get_all, get_by_id, create)
- Handles in-memory cache coherency
- Easy to replace with database later

**Benefits**: Testable, decoupled from FastAPI routes, reusable

---

### Pydantic Models for Validation

**Request Model** (`MusicTabCreate`):
- Fields: title (str), artist (str), content (str)
- Validation: All required; no length limits (MVP)

**Response Model** (`MusicTab`):
- Fields: id (int), title (str), artist (str), content (str)
- Used for all successful responses

**Error Model** (`ErrorResponse`):
- Fields: error (str), message (str), details (dict)
- Used for all error responses (Constitution Principle III)

---

## Performance Considerations

### In-Memory Caching Strategy

1. **Startup**: Load all tabs from `storage/tabs.json` into memory list
2. **Read operations**: Serve from memory (< 1ms latency)
3. **Write operations**: Update memory list, then persist to file
4. **Thread safety**: Use file locking for concurrent writes (optional for MVP)

**Expected Performance**:
- GET /api/v1/tabs: < 50ms (memory fetch + JSON serialization)
- GET /api/v1/tabs/{id}: < 20ms (list lookup + JSON serialization)
- POST /api/v1/tabs: < 100ms (file write + JSON encoding)

All well under Constitution thresholds (200ms GET, 500ms POST).

---

## Error Handling Strategy

**Consistent error schema** (Constitution Principle III):

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "details": {}
}
```

**Error codes**:
- `invalid_request`: 400 (missing required fields, invalid ID format)
- `not_found`: 404 (tab ID doesn't exist)
- `internal_server_error`: 500 (file I/O failure, unexpected error)

**Implementation**: FastAPI exception handlers + Pydantic validation errors

---

## Next Steps

All research items resolved. Ready for Phase 1: Design & Contracts.

**Phase 1 artifacts to generate**:
1. `data-model.md` - Entity definitions and relationships
2. `contracts/` - OpenAPI endpoint schema
3. `quickstart.md` - Developer setup guide
4. Update agent context with technology choices
