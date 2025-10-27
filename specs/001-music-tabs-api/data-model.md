# Data Model: Music Tabs API

**Phase**: Phase 1 - Design & Contracts  
**Date**: 2025-10-27  
**Input**: Feature spec + research findings

## Entity Definitions

### MusicTab (Core Entity)

**Purpose**: Represents a single music tab/chord chart for a song

**Fields**:
- `id` (int): Unique identifier, auto-assigned, incrementing
  - Constraint: Primary key, positive integer, immutable
  - Assignment: Auto-increment starting from 1
  
- `title` (str): Song title
  - Constraint: Required, non-empty, max 255 characters (practical limit)
  - Validation: Non-null, trimmed whitespace
  
- `artist` (str): Artist/band name
  - Constraint: Required, non-empty, max 255 characters
  - Validation: Non-null, trimmed whitespace
  
- `content` (str): Tab notation/chord chart
  - Constraint: Required, can be multi-line
  - Validation: Non-null, no specific format requirements for MVP

**State Transitions**:
- **Created**: Tab receives unique ID upon first POST
- **Retrieved**: ID never changes after creation
- **Persisted**: Written to `storage/tabs.json` immediately after creation

**Relationships**:
- None (MVP scope - no related entities)

---

### MusicTabCreate (Request Model)

**Purpose**: Validates incoming POST requests

**Fields**:
- `title` (str): Required
- `artist` (str): Required  
- `content` (str): Required

**Validation Rules**:
- All fields required (no defaults)
- All fields non-empty strings
- No additional fields allowed (FastAPI strict mode)

**Pydantic Configuration**:
```python
class Config:
    extra = "forbid"  # Reject extra fields
```

---

### ErrorResponse (Response Model)

**Purpose**: Standardized error response (Constitution Principle III)

**Fields**:
- `error` (str): Machine-readable error code
  - Allowed values: "invalid_request", "not_found", "internal_server_error"
  
- `message` (str): Human-readable error description
  
- `details` (dict): Optional context
  - Example: `{"id": 999}` for not_found
  - Example: `{"missing_fields": ["title"]}` for invalid_request

---

## Storage Schema

### JSON File Format (Per-Tab Files)

Each tab is stored in its own JSON file at `storage/tabs/{id}.json`:

**Example: `storage/tabs/1.json`**:
```json
{
  "id": 1,
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

**Example: `storage/tabs/2.json`**:
```json
{
  "id": 2,
  "title": "Blackbird",
  "artist": "The Beatles",
  "content": "G Dm Dm6..."
}
```

**Directory Layout**:
```
storage/
└── tabs/
    ├── 1.json
    ├── 2.json
    ├── 3.json
    └── ...
```

**Persistence Rules**:
- Each file is independent (atomic writes at file level)
- File is created after successful tab creation
- Format: JSON object (single tab per file), indented for readability
- Encoding: UTF-8
- File naming: `{id}.json` where id is the tab's numeric ID
- Directory scanned at startup to load all tabs into memory

**Benefits for Phase 2 Migration**:
- Simulates database-per-record pattern (each tab = one "row")
- When migrating to database: Replace file I/O with async DB queries (one query per tab ID)
- No changes needed to service layer interface, only implementation swapped

---

## ID Assignment Strategy

**Auto-increment mechanism**:
1. On startup: Load all tabs from JSON, track max ID
2. On POST: Increment max ID by 1, assign to new tab
3. On write: Persist tabs with IDs to JSON file

**Example sequence**:
- Start: max_id = 0
- POST tab 1: Assign id=1, max_id=1
- POST tab 2: Assign id=2, max_id=2
- Delete tab 1 (future feature): max_id stays 2
- POST tab 3: Assign id=3, max_id=3

**No gaps** guarantee: IDs increment monotonically within a session.

---

## Validation Rules Summary

| Field | Required | Type | Max Length | Validation |
|-------|----------|------|-----------|-----------|
| id | Yes | int | N/A | Positive, unique, auto-assigned |
| title | Yes | str | 255 | Non-empty, trimmed |
| artist | Yes | str | 255 | Non-empty, trimmed |
| content | Yes | str | N/A | Non-empty, can be multi-line |

---

## Evolution Path

**Future enhancements** (out of scope for MVP):
- Add `created_at` (timestamp) for audit trails
- Add `updated_at` for modification tracking
- Add `tags` (array) for categorization
- Add `difficulty` (enum) for skill level
- Add `tuning` (string) for guitar tuning info
- Add database migration (tabbed data → PostgreSQL)

**Current scope**: 4 fields (id, title, artist, content) only
