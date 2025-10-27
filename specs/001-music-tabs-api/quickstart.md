# Quickstart: Music Tabs API Development

**Phase**: Phase 1 - Design & Contracts  
**Date**: 2025-10-27  
**Audience**: Developers implementing this feature

## Project Setup

### Prerequisites

- Python 3.10+ (verify: `python --version`)
- pip (verify: `pip --version`)
- git (already in repository)

### 1. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (bash/zsh)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install from requirements.txt (to be created in Phase 2)
pip install -r requirements.txt

# Core dependencies:
# - fastapi==0.104.0
# - uvicorn==0.24.0
# - pydantic==2.0.0
# - pytest==7.4.0
# - pytest-asyncio==0.21.0
# - coverage==7.3.0
```

### 3. Project Structure Setup

```bash
# Create directories
mkdir -p src/models src/services src/api/endpoints src/storage
mkdir -p tests/unit tests/integration tests/contract

# Create files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/api/__init__.py
touch src/api/endpoints/__init__.py
touch src/storage/tabs.json
touch tests/__init__.py
touch tests/conftest.py
touch .env.example
```

---

## Development Workflow

### TDD Workflow (Required per Constitution)

**Order of execution** (test-driven development):

1. **Write test first** (red phase):
   ```bash
   # Create test file (e.g., tests/unit/test_tab_service.py)
   # Write failing test
   pytest tests/unit/test_tab_service.py  # Red: test fails
   ```

2. **Implement code** (green phase):
   ```bash
   # Edit src/services/tab_service.py
   # Write minimal code to pass test
   pytest tests/unit/test_tab_service.py  # Green: test passes
   ```

3. **Refactor** (refactor phase):
   ```bash
   # Improve code quality without changing behavior
   pytest tests/unit/test_tab_service.py  # Still green
   ```

4. **Repeat** for each function/feature

---

## Running the Application

### Start Development Server

```bash
# From project root
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Access:
# - API: http://localhost:8000/api/v1/tabs
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Example Requests

**GET all tabs**:
```bash
curl http://localhost:8000/api/v1/tabs
```

**GET single tab**:
```bash
curl http://localhost:8000/api/v1/tabs/1
```

**POST new tab**:
```bash
curl -X POST http://localhost:8000/api/v1/tabs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Wonderwall",
    "artist": "Oasis",
    "content": "Em7 Dsus2 A7sus4..."
  }'
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Category

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Contract tests only
pytest tests/contract/

# Specific file
pytest tests/unit/test_tab_service.py

# Specific test
pytest tests/unit/test_tab_service.py::test_create_tab
```

### Run with Coverage

```bash
# Generate coverage report
coverage run -m pytest
coverage report

# HTML report
coverage html
# Open htmlcov/index.html in browser
```

**Target**: ≥80% coverage (Constitution Principle II)

### Run with Verbose Output

```bash
pytest -v          # Show test names
pytest -v -s       # Show print statements
pytest --tb=short  # Short traceback format
```

---

## Code Quality Checks

### Linting (pylint)

```bash
# Lint entire src/ directory
pylint src/

# Target score: ≥8.0 (Constitution Principle I)
```

**Configuration**: `.pylintrc` (to be created)

### Code Formatting (black)

```bash
# Format all Python files
black src/ tests/

# Check formatting (don't modify)
black --check src/ tests/
```

**Configuration**: `pyproject.toml`

### Type Checking (mypy)

```bash
# Check types with strict mode
mypy src/ --strict

# Target: Zero errors (Constitution Principle I)
```

**Configuration**: `pyproject.toml`

### All Quality Checks (Combined)

```bash
# Run all quality gates
pylint src/ && black --check src/ tests/ && mypy src/ --strict && pytest --cov=src tests/
```

**Pass criteria**: All tools succeed (exit code 0)

---

## Data Persistence

### Initial Data

**File**: `src/storage/tabs.json`

**Initial content** (empty):
```json
[]
```

**Seed with sample data** (optional):
```json
[
  {
    "id": 1,
    "title": "Wonderwall",
    "artist": "Oasis",
    "content": "Em7 Dsus2 A7sus4...\n[verse]"
  },
  {
    "id": 2,
    "title": "Blackbird",
    "artist": "The Beatles",
    "content": "G Dm..."
  }
]
```

### Loading & Saving

- **Startup**: Load all tabs from `src/storage/tabs.json` into memory
- **POST**: Add new tab to memory, write updated array to file (write-through)
- **GET**: Serve from memory (no file I/O)

---

## Environment Configuration

### .env File (Optional for MVP)

**File**: `.env`

**Example**:
```
ENVIRONMENT=development
PORT=8000
HOST=127.0.0.1
```

**Template**: `.env.example` (check into git, .env in .gitignore)

### Environment Variables

```python
# In src/main.py
import os
environment = os.getenv("ENVIRONMENT", "development")
port = int(os.getenv("PORT", 8000))
```

---

## Debugging

### Print Debugging

```python
# In FastAPI routes
@app.get("/api/v1/tabs")
def get_all_tabs():
    print(f"DEBUG: Loading tabs from storage")  # Will appear in console
    return {"tabs": all_tabs}
```

**Console output**: Visible in terminal where uvicorn is running

### Logging (Future Enhancement)

```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Loading tabs from storage")
```

### IDE Debugging

Use your IDE's debugger (VS Code, PyCharm, etc.):
- Set breakpoints (click line number)
- Run: `python -m pdb src/main.py`
- Or configure IDE's run configuration for debugger

---

## Common Commands Reference

| Task | Command |
|------|---------|
| Create venv | `python -m venv venv` |
| Activate venv | `.\venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux) |
| Install deps | `pip install -r requirements.txt` |
| Start server | `uvicorn src.main:app --reload` |
| Run tests | `pytest` |
| Coverage report | `coverage run -m pytest && coverage report` |
| Lint code | `pylint src/` |
| Format code | `black src/ tests/` |
| Type check | `mypy src/ --strict` |
| Quality gates | `pylint src/ && black --check src/ tests/ && mypy src/ --strict && pytest` |

---

## Troubleshooting

### ModuleNotFoundError

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: 
1. Verify venv is activated (prompt shows `(venv)`)
2. Reinstall: `pip install -r requirements.txt`

### Port Already in Use

**Problem**: `Address already in use: ('127.0.0.1', 8000)`

**Solution**:
1. Kill process: `lsof -i :8000` (Mac/Linux) or `netstat -ano | findstr :8000` (Windows)
2. Use different port: `uvicorn src.main:app --port 8001`

### Test Discovery Issues

**Problem**: `pytest: command not found`

**Solution**:
1. Verify pytest installed: `pip list | grep pytest`
2. Reinstall: `pip install pytest pytest-asyncio`

### Import Errors

**Problem**: `ImportError: cannot import name 'MusicTab' from 'src.models'`

**Solution**:
1. Verify `src/models/__init__.py` imports and exports the class
2. Check file structure matches imports

---

## Next Steps

1. **Implement Phase 2**: Create `src/models/tab.py`, `src/services/tab_service.py`, etc.
2. **Write tests**: Follow TDD workflow in Phase 2
3. **Run quality gates**: Ensure code passes linting, typing, coverage
4. **Run `/speckit.tasks`**: Generate detailed implementation tasks

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Pytest Docs**: https://docs.pytest.org/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **PEP 8 Style Guide**: https://www.python.org/dev/peps/pep-0008/
