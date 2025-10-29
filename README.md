# Music Tabs API

A minimal FastAPI server for managing music tabs with JSON file-based storage.

## Overview

This is an MVP (Minimum Viable Product) implementation of a music tabs API with three core endpoints:
- **GET /api/v1/tabs** - Retrieve all stored music tabs
- **GET /api/v1/tabs/{id}** - Retrieve a specific tab by ID
- **POST /api/v1/tabs** - Create a new music tab

The API stores tabs as individual JSON files for simplicity and designed for easy migration to a database in Phase 2.

## Quick Start

### Prerequisites

- Python 3.13+
- pip
- git

### 1. Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux (bash/zsh)**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

Or install manually:
```bash
pip install fastapi==0.104.1 uvicorn==0.24.0 pydantic==2.5.0
pip install pytest==7.4.3 pytest-asyncio==0.21.1 coverage==7.3.2
pip install pylint==3.0.3 black==23.12.1 mypy==1.7.1
```

### 3. Run the Server

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Then visit:
- **API**: http://localhost:8000/api/v1/tabs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_tab_service.py -v

# Run specific test
pytest tests/unit/test_tab_service.py::test_get_all -v
```

### 5. Code Quality Checks

```bash
# Run linter (target: score ≥8.0)
pylint src/

# Format code
black src/ tests/

# Type checking (target: zero errors)
mypy src/ --strict

# All checks together
pylint src/ && black --check src/ tests/ && mypy src/ --strict && pytest
```

## Project Structure

```
fastapi_basic/
├── README.md                          ← START HERE
├── requirements.txt                   ← Production dependencies
├── pyproject.toml                     ← Build metadata & tool config
├── .pylintrc                          ← Linting configuration
├── .env.example                       ← Environment variables template
│
├── src/                               ← SOURCE CODE
│   ├── main.py                        ← FastAPI app initialization
│   ├── models/
│   │   ├── base.py                    ← Error responses, list wrappers
│   │   └── tab.py                     ← MusicTab, MusicTabCreate models
│   ├── services/
│   │   └── tab_service.py             ← TabService (CRUD operations)
│   ├── api/endpoints/
│   │   └── tabs.py                    ← Route handlers for /api/v1/tabs
│   └── utils/
│       └── timing.py                  ← Performance instrumentation
│
├── tests/                             ← TEST SUITE (37 tests, 94.37% coverage)
│   ├── conftest.py                    ← Shared test fixtures
│   ├── unit/                          ← Unit tests
│   │   └── test_tab_service.py
│   ├── integration/                   ← Integration tests
│   │   ├── test_tabs_workflow.py
│   │   ├── test_tabs_create_workflow.py
│   │   └── test_full_workflow.py
│   ├── contract/                      ← Contract tests
│   │   ├── test_tabs_list.py
│   │   └── test_tabs_create.py
│   └── smoke_test.py                  ← Quick validation tests
│
├── specs/001-music-tabs-api/          ← SPECIFICATION & DOCS
│   ├── spec.md                        ← Feature specification
│   ├── plan.md                        ← Implementation plan
│   ├── tasks.md                       ← Task breakdown (100 tasks)
│   ├── research.md                    ← Technical research
│   ├── data-model.md                  ← Entity definitions
│   ├── quickstart.md                  ← Developer guide
│   ├── DEPLOYMENT.md                  ← Deployment guide
│   ├── PHASE_1_COMPLETION.md through PHASE_6_COMPLETION.md
│   ├── checklists/                    ← Phase checklists
│   └── contracts/                     ← API contract definitions
│
├── documentation/                     ← REFERENCE DOCS
│   ├── ROADMAP.md                     ← Product roadmap (Phases 7-10)
│   └── PROJECT_STATUS.md              ← Project metrics & status
│
├── storage/                           ← DATA PERSISTENCE
│   └── tabs/                          ← Individual tab JSON files
│
└── .specify/                          ← SPECIFICATION FRAMEWORK
    └── memory/
        └── constitution.md            ← Project constitution
```

## Documentation Guide

| Need | Location | Purpose |
|------|----------|---------|
| **Quick start** | `README.md` (this file) | Getting started, running tests, commands |
| **Feature details** | `specs/001-music-tabs-api/spec.md` | User stories, API contracts |
| **Architecture** | `specs/001-music-tabs-api/plan.md` | Design decisions, Constitution alignment |
| **Task status** | `specs/001-music-tabs-api/tasks.md` | 100 tasks across 6 phases |
| **Deployment** | `specs/001-music-tabs-api/DEPLOYMENT.md` | How to deploy to production |
| **Phase reports** | `specs/001-music-tabs-api/PHASE_*.md` | Phase completion status |
| **Roadmap** | `documentation/ROADMAP.md` | Phases 7-10, future features |
| **Project status** | `documentation/PROJECT_STATUS.md` | Metrics, test results, quality scores |

## API Endpoints

### GET /api/v1/tabs

Retrieve all stored music tabs.

**Request**:
```bash
curl http://localhost:8000/api/v1/tabs
```

**Response (200)**:
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

**Response (200, empty)**:
```json
{
  "tabs": []
}
```

---

### GET /api/v1/tabs/{id}

Retrieve a specific tab by ID.

**Request**:
```bash
curl http://localhost:8000/api/v1/tabs/1
```

**Response (200)**:
```json
{
  "id": 1,
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

**Response (404)** - Tab not found:
```json
{
  "error": "not_found",
  "message": "Tab not found",
  "details": {"id": 1}
}
```

**Response (400)** - Invalid ID:
```json
{
  "error": "invalid_request",
  "message": "Invalid tab ID",
  "details": {}
}
```

---

### POST /api/v1/tabs

Create a new music tab.

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/tabs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Wonderwall",
    "artist": "Oasis",
    "content": "Em7 Dsus2 A7sus4..."
  }'
```

**Response (201)**:
```json
{
  "id": 3,
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

**Response (400)** - Missing required field:
```json
{
  "error": "invalid_request",
  "message": "Missing required field: title",
  "details": {"missing_fields": ["title"]}
}
```

**Response (400)** - Extra fields:
```json
{
  "error": "invalid_request",
  "message": "Unexpected field: genre",
  "details": {}
}
```

---

## Development Workflow (TDD)

Follow Test-Driven Development (TDD) for all features:

1. **Red Phase**: Write failing tests first
   ```bash
   pytest tests/unit/test_tab_service.py -v  # Tests fail (red)
   ```

2. **Green Phase**: Write minimal code to pass tests
   ```bash
   # Edit src/services/tab_service.py
   pytest tests/unit/test_tab_service.py -v  # Tests pass (green)
   ```

3. **Refactor Phase**: Improve code quality
   ```bash
   black src/
   pylint src/
   mypy src/ --strict
   pytest tests/unit/test_tab_service.py -v  # Tests still pass
   ```

## Code Quality Standards

All code must meet these quality gates before merging:

| Standard | Target | Check Command |
|----------|--------|---------------|
| Linting | Score ≥8.0 | `pylint src/` |
| Type Hints | Zero errors | `mypy src/ --strict` |
| Test Coverage | ≥80% | `coverage run -m pytest && coverage report` |
| Formatting | Black-compliant | `black --check src/ tests/` |
| Complexity | ≤5 per function | Built into pylint |

## Performance Requirements

All endpoints meet these latency targets (p95):

| Endpoint | Target | Check |
|----------|--------|-------|
| GET /api/v1/tabs | <200ms | Load test: `pytest tests/integration/` |
| GET /api/v1/tabs/{id} | <200ms | Load test: `pytest tests/integration/` |
| POST /api/v1/tabs | <500ms | Load test: `pytest tests/integration/` |

## Testing

### Test Organization

- **`tests/unit/`** - Unit tests for models, services, business logic
- **`tests/integration/`** - End-to-end workflow tests
- **`tests/contract/`** - API contract tests (request/response schemas)

### Running Tests

```bash
# All tests
pytest

# By category
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/

# Verbose with output
pytest -v -s

# With coverage
pytest --cov=src --cov-report=html
# View report: open htmlcov/index.html
```

## Troubleshooting

### ModuleNotFoundError: No module named 'fastapi'

**Solution**: Verify venv is activated and dependencies are installed
```bash
# Windows
.\venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# macOS/Linux
source venv/bin/activate
pip install -e ".[dev]"
```

### Port Already in Use

**Solution**: Use a different port
```bash
uvicorn src.main:app --port 8001
```

### Tests Fail: "Cannot find module src"

**Solution**: Install package in development mode
```bash
pip install -e .
```

### Coverage Below 80%

**Solution**: Add tests for uncovered lines
```bash
coverage html
open htmlcov/index.html  # Review uncovered lines
```

## Data Persistence

### Storage Location

Tabs are stored as individual JSON files in `storage/tabs/`:
```
storage/tabs/
├── 1.json
├── 2.json
└── 3.json
```

### File Format

Each file contains a single tab object:
```json
{
  "id": 1,
  "title": "Wonderwall",
  "artist": "Oasis",
  "content": "Em7 Dsus2 A7sus4..."
}
```

### In-Memory Cache

On startup, all tabs are loaded into memory for fast access. When you POST a new tab:
1. New tab added to in-memory cache
2. Written to `storage/tabs/{id}.json`
3. Returned in response with assigned ID

## Common Commands Reference

```bash
# Activation
.\venv\Scripts\Activate.ps1          # Windows PowerShell
source venv/bin/activate            # macOS/Linux

# Dependencies
pip install -e ".[dev]"             # Install all deps
pip install -e .                    # Install runtime deps only
pip freeze > requirements.txt       # Export deps

# Running
uvicorn src.main:app --reload       # Dev server
uvicorn src.main:app --host 0.0.0.0 --port 8000  # Production config

# Testing
pytest                              # All tests
pytest --cov=src                    # With coverage
coverage html                       # HTML coverage report
pytest -v -s                        # Verbose with output

# Code Quality
pylint src/                         # Linting
black src/ tests/                   # Format code
mypy src/ --strict                  # Type checking
black --check src/                  # Check without formatting

# All at once
pylint src/ && black --check src/ tests/ && mypy src/ --strict && pytest --cov=src
```

## Environment Configuration

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit `.env` to customize:
```
ENVIRONMENT=development
HOST=127.0.0.1
PORT=8000
DEBUG=false
```

## Next Steps

1. **Implement Phase 2**: Create data models (MusicTab, MusicTabCreate, ErrorResponse)
2. **Add Endpoints**: Implement GET /api/v1/tabs, GET /api/v1/tabs/{id}, POST /api/v1/tabs
3. **Write Tests**: Follow TDD workflow for all features
4. **Phase 2 Database Migration**: Replace file I/O with async database queries

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Pytest Documentation**: https://docs.pytest.org/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **PEP 8 Style Guide**: https://www.python.org/dev/peps/pep-0008/

## License

MIT

## Support

For issues, questions, or contributions, please refer to the project specification:
- **Specification**: `specs/001-music-tabs-api/spec.md`
- **Implementation Plan**: `specs/001-music-tabs-api/plan.md`
- **API Contracts**: `specs/001-music-tabs-api/contracts/openapi.md`
