# Tasks: Music Tabs API

**Input**: Design documents from `/specs/001-music-tabs-api/`  
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/openapi.md ✓  
**Feature Branch**: `001-music-tabs-api`  
**Date Generated**: 2025-10-27

**Tests**: Full test coverage included (per Constitution Principle II - Testing Standards)

**Organization**: Tasks grouped by user story (US1, US2, US3) to enable independent implementation and testing. Each story is independently testable and deployable.

---

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete work)
- **[Story]**: Which user story (US1, US2, US3) - REQUIRED for story phases; omitted for Setup/Foundational/Polish
- **ID**: Sequential task ID (T001, T002, ...)
- **Description**: Clear action with exact file paths
- **Checkbox**: All tasks start with `- [ ]`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and modular structure setup  
**Constitution Alignment**: Principle I (Code Quality), Principle II (Testing Standards)  
**Estimated Duration**: 2-3 hours

- [ ] T001 Create project structure: `src/models/`, `src/services/`, `src/api/endpoints/`, `src/storage/tabs/`, `tests/unit/`, `tests/integration/`, `tests/contract/`, `.specify/`
- [ ] T002 Create Python files: `src/__init__.py`, `src/main.py`, `src/models/__init__.py`, `src/services/__init__.py`, `src/api/__init__.py`, `src/api/endpoints/__init__.py`
- [ ] T003 [P] Create test infrastructure files: `tests/__init__.py`, `tests/conftest.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`, `tests/contract/__init__.py`
- [ ] T004 [P] Create pyproject.toml with project metadata, dependencies (FastAPI 0.104+, Uvicorn 0.24+, Pydantic 2.0+, pytest 7.4+, pytest-asyncio 0.21+, coverage 7.3+, pylint 3.0+, black 23.0+, mypy 1.7+)
- [ ] T005 [P] Create .pylintrc with score target ≥8.0, line length 100, disable unnecessary-pass, disable missing-docstring for __init__
- [ ] T006 [P] Create pyproject.toml [tool.black] section: line-length=100, target-version=['py313']
- [ ] T007 [P] Create pyproject.toml [tool.mypy] section: strict=true, python_version="3.13", disallow_untyped_defs=true, disallow_incomplete_defs=true
- [ ] T008 [P] Create pyproject.toml [tool.pytest.ini_options] section: testpaths=["tests"], addopts="--cov=src --cov-report=term-missing:skip-covered --cov-report=html --cov-fail-under=80"
- [ ] T009 Create .env.example with ENVIRONMENT=development, PORT=8000, HOST=127.0.0.1, DEBUG=false
- [ ] T010 [P] Create README.md with project overview, quick start (venv creation, dependency install), running server, running tests, code quality checks, troubleshooting

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story implementation  
**Constitution Alignment**: Principle III (UX Consistency), Principle IV (Performance Requirements)  
**Estimated Duration**: 4-5 hours

**⚠️ CRITICAL**: No user story work can begin until this phase is 100% complete

- [ ] T011 Create base Pydantic models in `src/models/base.py`: ErrorResponse with fields error (str), message (str), details (dict) - match contracts/openapi.md schema exactly
- [ ] T012 [P] Create Pydantic model in `src/models/tab.py`: MusicTab with fields id (int), title (str), artist (str), content (str) - add docstrings, use snake_case field names
- [ ] T013 [P] Create Pydantic model in `src/models/tab.py`: MusicTabCreate with fields title (str), artist (str), content (str) - all required, extra="forbid", add docstring
- [ ] T014 [P] Create `src/models/__init__.py` exporting MusicTab, MusicTabCreate, ErrorResponse
- [ ] T015 Create response wrapper model in `src/models/base.py`: TabsListResponse with field tabs (list[MusicTab]) for GET /api/v1/tabs endpoint
- [ ] T016 [P] Create TabService in `src/services/tab_service.py`: 
  - Init method loads all tabs from `storage/tabs/` directory by scanning for *.json files
  - Load all tabs into in-memory dict keyed by id
  - Track max_id from loaded files
  - Add docstring explaining in-memory caching + file persistence strategy
- [ ] T017 [P] Implement TabService.get_all() method: returns list of all MusicTab objects from in-memory cache; include docstring with performance note (<50ms expected)
- [ ] T018 [P] Implement TabService.get_by_id(id: int) -> MusicTab | None method: lookup from in-memory cache; include docstring with performance note (<20ms expected)
- [ ] T019 [P] Implement TabService.create(tab_create: MusicTabCreate) -> MusicTab method: 
  - increment max_id, assign as new tab.id
  - persist to `storage/tabs/{id}.json` as JSON file with full MusicTab fields
  - add to in-memory cache
  - include docstring, error handling for file write failures
- [ ] T020 Create `src/services/__init__.py` exporting TabService
- [ ] T021 Create FastAPI app in `src/main.py`:
  - Import FastAPI, Uvicorn, TabService
  - Create app = FastAPI(title="Music Tabs API", version="1.0.0")
  - Initialize tab_service = TabService() at module level
  - Setup exception handlers for generic exceptions → ErrorResponse with 500 status
  - Add docstring for app, explain routing structure + error handling
  - DO NOT add endpoints yet (will be added in user story phases)
- [ ] T022 Create `storage/tabs/` directory (empty, for tab JSON files)
- [ ] T023 [P] Create logger setup in `src/utils/logging.py`: simple structured logging with request timing capability for Principle IV measurement (add call timing decorators for endpoints)
- [ ] T024 [P] Create `src/api/__init__.py` empty file
- [ ] T025 [P] Create `src/api/endpoints/__init__.py` empty file
- [ ] T026 Create `tests/conftest.py` with shared fixtures:
  - fixture_empty_storage: creates/clears empty `storage/tabs/` directory for test isolation
  - fixture_sample_tabs: pre-loads 2 sample tabs for testing (Wonderwall/Oasis, Blackbird/Beatles)
  - fixture_tab_service: returns fresh TabService instance for each test
  - fixture_valid_tab_create: MusicTabCreate object with valid data for testing
  - fixture_invalid_tab_data: dict with missing required fields for error testing
  - Add docstring explaining each fixture's role
- [ ] T027 Create `tests/__init__.py` empty file
- [ ] T028 Create `tests/unit/__init__.py` empty file
- [ ] T029 Create `tests/integration/__init__.py` empty file
- [ ] T030 Create `tests/contract/__init__.py` empty file

**Checkpoint**: Foundation complete. Verify all models load, TabService initializes, FastAPI app creates without errors. Ready for user story implementation.

---

## Phase 3: User Story 1 - Retrieve All Music Tabs (Priority: P1) 🎯 MVP

**Goal**: Users can retrieve all stored music tabs in a single GET request, receiving a JSON array of tab objects

**Independent Test**: Execute `curl http://localhost:8000/api/v1/tabs` → receive 200 response with {"tabs": [...]}, verify response matches contract schema exactly

**Constitution Alignment**: Principle II (TDD), Principle III (UX Consistency), Principle IV (Performance <200ms p95)

### Tests for User Story 1 (REQUIRED - Write FIRST, ensure FAIL before implementation)

- [ ] T031 [P] [US1] Contract test: GET /api/v1/tabs success case in `tests/contract/test_tabs_list.py`
  - Test request: GET /api/v1/tabs with no query params
  - Verify response status 200
  - Verify response schema matches contract: {"tabs": [{"id": int, "title": str, "artist": str, "content": str}, ...]}
  - Verify tabs array is sorted by id ascending (or document ordering)
  - Use fixture_sample_tabs to pre-populate storage
  
- [ ] T032 [P] [US1] Contract test: GET /api/v1/tabs empty case in `tests/contract/test_tabs_list.py`
  - Test request: GET /api/v1/tabs with empty storage
  - Verify response status 200
  - Verify response body: {"tabs": []}
  - Use fixture_empty_storage to ensure no tabs exist
  
- [ ] T033 [P] [US1] Contract test: GET /api/v1/tabs error case in `tests/contract/test_tabs_list.py`
  - Test request: GET /api/v1/tabs when file I/O fails (mock storage error)
  - Verify response status 500
  - Verify error schema: {"error": "internal_server_error", "message": "...", "details": {}}
  
- [ ] T034 [P] [US1] Integration test: full GET /api/v1/tabs flow in `tests/integration/test_tabs_workflow.py`
  - Setup: POST 3 valid tabs to populate storage
  - Execute: GET /api/v1/tabs
  - Verify: All 3 tabs returned, with assigned IDs, unchanged data
  - Verify order stability (same tabs always returned in same order)
  
- [ ] T035 [P] [US1] Unit test: TabService.get_all() in `tests/unit/test_tab_service.py`
  - Test: get_all() with sample tabs loaded
  - Verify: returns list of MusicTab objects
  - Verify: list length matches loaded tabs
  - Verify: all fields present and correct type (MusicTab model)
  - Use fixture_sample_tabs, fixture_tab_service
  
- [ ] T036 [P] [US1] Unit test: TabService.get_all() empty in `tests/unit/test_tab_service.py`
  - Test: get_all() with no tabs in storage
  - Verify: returns empty list []
  - Use fixture_empty_storage, fixture_tab_service

### Implementation for User Story 1

- [ ] T037 [US1] Create GET endpoint in `src/api/endpoints/tabs.py`:
  - Route: GET /api/v1/tabs
  - Handler function: get_all_tabs() -> TabsListResponse
  - Call tab_service.get_all() to retrieve tabs
  - Return TabsListResponse(tabs=[...]) wrapped response
  - Add docstring with endpoint summary, response schema reference
  - Measure response time, log p95 latency (Principle IV)
  
- [ ] T038 [US1] Mount endpoints in `src/main.py`:
  - Import tabs router from `src/api/endpoints/tabs`
  - Add app.include_router(router, prefix="/api/v1", tags=["tabs"])
  - Verify endpoint accessible at /api/v1/tabs
  
- [ ] T039 [US1] Implement error handling in endpoint:
  - Catch exception from tab_service.get_all()
  - Return ErrorResponse(error="internal_server_error", message="Failed to retrieve tabs", details={}) with 500 status
  - Log error for debugging
  
- [ ] T040 [US1] Add type hints to all functions in `src/api/endpoints/tabs.py`:
  - get_all_tabs() -> TabsListResponse
  - All imports typed
  - Use mypy --strict compatible syntax
  
- [ ] T041 [US1] Verify response uses snake_case field names:
  - All fields: id, title, artist, content, tabs, error, message, details
  - FastAPI/Pydantic auto-handles snake_case by default
  - Test response JSON output explicitly
  
- [ ] T042 [US1] Run tests for US1 contract + integration + unit:
  - Execute: pytest tests/contract/test_tabs_list.py tests/integration/test_tabs_workflow.py tests/unit/test_tab_service.py -v
  - Verify: All tests pass (green phase after T031-T036 red phase)
  
- [ ] T043 [US1] Run linting and type checking:
  - Execute: pylint src/api/endpoints/tabs.py src/services/tab_service.py
  - Verify: Score ≥8.0
  - Execute: black --check src/api/endpoints/tabs.py src/services/tab_service.py (or format if needed)
  - Execute: mypy src/api/endpoints/tabs.py src/services/tab_service.py --strict
  - Verify: Zero errors
  
- [ ] T044 [US1] Run coverage report:
  - Execute: coverage run -m pytest tests/
  - Verify: Coverage ≥80% for src/api/endpoints/tabs.py and src/services/tab_service.py
  - Execute: coverage report, coverage html
  - Review uncovered lines, add tests if needed
  
- [ ] T045 [US1] Performance validation:
  - Write simple load test: 100 sequential GET /api/v1/tabs requests with 1000-tab storage
  - Verify p95 latency <200ms (Principle IV)
  - Log sample timing measurements in test output
  - If <200ms target not met, profile and optimize

**Checkpoint**: User Story 1 complete, fully tested, all code quality gates passed. Can deploy as MVP with single GET all-tabs endpoint.

---

## Phase 4: User Story 2 - Retrieve Single Tab by ID (Priority: P1)

**Goal**: Users can retrieve a specific music tab by its unique ID, enabling targeted single-item access

**Independent Test**: Execute `curl http://localhost:8000/api/v1/tabs/1` → receive 200 response with tab object, and `curl http://localhost:8000/api/v1/tabs/999` → receive 404 error

**Constitution Alignment**: Principle II (TDD), Principle III (UX Consistency), Principle IV (Performance <200ms p95)

### Tests for User Story 2 (REQUIRED - Write FIRST, ensure FAIL before implementation)

- [ ] T046 [P] [US2] Contract test: GET /api/v1/tabs/{id} success case in `tests/contract/test_tabs_by_id.py`
  - Test request: GET /api/v1/tabs/1
  - Setup: fixture_sample_tabs (load 2 tabs including id=1)
  - Verify response status 200
  - Verify response schema matches contract: {"id": int, "title": str, "artist": str, "content": str}
  - Verify returned tab has id=1 with correct data
  
- [ ] T047 [P] [US2] Contract test: GET /api/v1/tabs/{id} not found in `tests/contract/test_tabs_by_id.py`
  - Test request: GET /api/v1/tabs/999
  - Setup: fixture_empty_storage (no tabs)
  - Verify response status 404
  - Verify error schema: {"error": "not_found", "message": "Tab not found", "details": {"id": 999}}
  
- [ ] T048 [P] [US2] Contract test: GET /api/v1/tabs/{id} invalid ID format in `tests/contract/test_tabs_by_id.py`
  - Test request: GET /api/v1/tabs/not-a-number or GET /api/v1/tabs/abc
  - Verify response status 400
  - Verify error schema: {"error": "invalid_request", "message": "Invalid tab ID", "details": {}}
  - Test negative ID: GET /api/v1/tabs/-1 → expect 400 or handle appropriately
  
- [ ] T049 [P] [US2] Contract test: GET /api/v1/tabs/{id} error case in `tests/contract/test_tabs_by_id.py`
  - Test request: GET /api/v1/tabs/1 when file I/O fails
  - Verify response status 500
  - Verify error schema: {"error": "internal_server_error", ...}
  
- [ ] T050 [P] [US2] Integration test: GET single tab workflow in `tests/integration/test_tabs_workflow.py`
  - Setup: POST a tab and record its ID
  - Execute: GET /api/v1/tabs/{id}
  - Verify: Returned tab matches posted tab exactly (including id, title, artist, content)
  - Execute: GET /api/v1/tabs/{invalid_id}
  - Verify: 404 returned with appropriate error
  
- [ ] T051 [P] [US2] Unit test: TabService.get_by_id() success in `tests/unit/test_tab_service.py`
  - Test: get_by_id(1) with sample tabs loaded
  - Verify: returns MusicTab object with id=1
  - Verify: all fields present and correct
  - Use fixture_sample_tabs, fixture_tab_service
  
- [ ] T052 [P] [US2] Unit test: TabService.get_by_id() not found in `tests/unit/test_tab_service.py`
  - Test: get_by_id(999) with sample tabs
  - Verify: returns None
  - Use fixture_sample_tabs, fixture_tab_service

### Implementation for User Story 2

- [ ] T053 [US2] Implement TabService.get_by_id(id: int) method in `src/services/tab_service.py`:
  - Validate id is positive integer (add type hint validation)
  - Lookup id in in-memory cache dict
  - Return MusicTab if found, None if not found
  - Add docstring with expected p95 latency <20ms
  - Add logging for cache hit/miss (debug level)
  
- [ ] T054 [US2] Create GET /{id} endpoint in `src/api/endpoints/tabs.py`:
  - Route: GET /api/v1/tabs/{id}
  - Path parameter: id (int), use FastAPI Path() for validation
  - Handler function: get_tab_by_id(id: int) -> MusicTab
  - Call tab_service.get_by_id(id)
  - Return MusicTab if found
  - Add docstring with endpoint summary
  - Measure response time for p95 latency tracking
  
- [ ] T055 [US2] Implement error handling for GET /{id} in endpoint:
  - If get_by_id returns None: return ErrorResponse(error="not_found", message="Tab not found", details={"id": id}) with 404 status
  - If id validation fails (invalid format): FastAPI auto-returns 422, but override with 400 + ErrorResponse(error="invalid_request", message="Invalid tab ID", details={})
  - If exception from service: return 500 ErrorResponse
  - Log errors for debugging
  
- [ ] T056 [US2] Add type hints to GET /{id} handler:
  - get_tab_by_id(id: int) -> MusicTab
  - Use mypy --strict compatible syntax
  - All imports typed
  
- [ ] T057 [US2] Override FastAPI 422 validation error for invalid id:
  - Create custom exception handler for RequestValidationError
  - Convert 422 to 400 with ErrorResponse(error="invalid_request", message="Invalid tab ID", details={})
  - Apply to all path parameters for consistency
  
- [ ] T058 [US2] Run tests for US2:
  - Execute: pytest tests/contract/test_tabs_by_id.py tests/integration/test_tabs_workflow.py::test_get_single_tab tests/unit/test_tab_service.py::test_get_by_id -v
  - Verify: All tests pass
  
- [ ] T059 [US2] Run linting, type checking, formatting:
  - Execute: pylint src/api/endpoints/tabs.py src/services/tab_service.py
  - Verify: Score ≥8.0
  - Execute: black --check src/api/endpoints/tabs.py src/services/tab_service.py
  - Execute: mypy src/api/endpoints/tabs.py src/services/tab_service.py --strict
  - Verify: Zero errors
  
- [ ] T060 [US2] Run coverage report:
  - Execute: coverage run -m pytest tests/ && coverage report
  - Verify: Coverage ≥80% for US2 code paths
  - Review uncovered lines (edge cases, error paths)
  
- [ ] T061 [US2] Performance validation for GET /{id}:
  - Load test: 100 sequential GET /api/v1/tabs/1 requests
  - Verify p95 latency <200ms (well under constraint)
  - Log sample timings

**Checkpoint**: User Story 1 + User Story 2 complete. API now supports both full list retrieval and single-item access. Both endpoints tested, typed, linted, and performant.

---

## Phase 5: User Story 3 - Create New Music Tab (Priority: P1)

**Goal**: Users can create and persist new music tabs with POST requests, with system-assigned unique IDs

**Independent Test**: Execute `curl -X POST http://localhost:8000/api/v1/tabs -H "Content-Type: application/json" -d '{"title":"Test","artist":"Artist","content":"content"}'` → receive 201 response with created tab including unique id

**Constitution Alignment**: Principle II (TDD), Principle III (UX Consistency), Principle IV (Performance <500ms p95)

### Tests for User Story 3 (REQUIRED - Write FIRST, ensure FAIL before implementation)

- [ ] T062 [P] [US3] Contract test: POST /api/v1/tabs success case in `tests/contract/test_tabs_create.py`
  - Test request: POST /api/v1/tabs with valid MusicTabCreate body
  - Verify response status 201
  - Verify response schema matches contract: {"id": int, "title": str, "artist": str, "content": str}
  - Verify id is assigned (not null) and is unique
  - Verify id is positive integer
  
- [ ] T063 [P] [US3] Contract test: POST /api/v1/tabs missing field in `tests/contract/test_tabs_create.py`
  - Test request: POST /api/v1/tabs with title missing
  - Verify response status 400
  - Verify error schema: {"error": "invalid_request", "message": "Missing required field: title", "details": {"missing_fields": ["title"]}}
  - Repeat for missing artist, missing content
  
- [ ] T064 [P] [US3] Contract test: POST /api/v1/tabs extra fields in `tests/contract/test_tabs_create.py`
  - Test request: POST /api/v1/tabs with extra field "genre": "rock"
  - Verify response status 400
  - Verify error schema: {"error": "invalid_request", "message": "Unexpected field: genre", "details": {}}
  
- [ ] T065 [P] [US3] Contract test: POST /api/v1/tabs empty required field in `tests/contract/test_tabs_create.py`
  - Test request: POST /api/v1/tabs with title: "" (empty string)
  - Verify response status 400
  - Verify error message indicates empty field
  
- [ ] T066 [P] [US3] Contract test: POST /api/v1/tabs error case in `tests/contract/test_tabs_create.py`
  - Test request: POST /api/v1/tabs when file write fails (mock storage error)
  - Verify response status 500
  - Verify error schema: {"error": "internal_server_error", "message": "Failed to create tab", "details": {}}
  
- [ ] T067 [P] [US3] Contract test: POST /api/v1/tabs unique IDs in `tests/contract/test_tabs_create.py`
  - Test: POST 3 valid tabs sequentially
  - Verify: Each returns 201
  - Verify: IDs are 1, 2, 3 (auto-incrementing)
  - Verify: No duplicate IDs
  
- [ ] T068 [P] [US3] Integration test: create and retrieve workflow in `tests/integration/test_tabs_workflow.py`
  - Execute: POST new tab with valid data
  - Capture returned id
  - Execute: GET /api/v1/tabs/{id}
  - Verify: Retrieved tab matches posted data exactly
  - Execute: GET /api/v1/tabs
  - Verify: New tab appears in full list
  
- [ ] T069 [P] [US3] Integration test: concurrent POST test in `tests/integration/test_tabs_workflow.py`
  - Execute: 5 concurrent POST requests (use threading or asyncio)
  - Verify: All succeed with 201 status
  - Verify: 5 different IDs assigned (no collisions)
  - Verify: All tabs persisted to storage
  
- [ ] T070 [P] [US3] Unit test: TabService.create() success in `tests/unit/test_tab_service.py`
  - Test: create(MusicTabCreate(...)) with valid data
  - Verify: returns MusicTab with assigned id
  - Verify: id is positive integer
  - Verify: all fields match input + id assigned
  - Use fixture_valid_tab_create
  
- [ ] T071 [P] [US3] Unit test: TabService.create() increments ID in `tests/unit/test_tab_service.py`
  - Test: create() called twice sequentially
  - Verify: first returns id=1, second returns id=2
  - Verify: IDs are unique, monotonically increasing
  - Use fixture_tab_service
  
- [ ] T072 [P] [US3] Unit test: TabService.create() persists to file in `tests/unit/test_tab_service.py`
  - Test: create(tab) succeeds
  - Verify: storage/tabs/{id}.json file created
  - Verify: file contains correct JSON with all tab fields
  - Use pathlib to check file exists and read content

### Implementation for User Story 3

- [ ] T073 [US3] Implement TabService.create(tab_create: MusicTabCreate) in `src/services/tab_service.py`:
  - Increment self.max_id
  - Create MusicTab(id=new_id, title=..., artist=..., content=...)
  - Write to file storage/tabs/{id}.json using json.dump()
  - Ensure JSON formatted with indent=2 for readability
  - Add to in-memory cache dict
  - Return created MusicTab
  - Add docstring explaining auto-increment strategy, file persistence, expected latency <100ms
  - Add error handling: catch file write exceptions, log and re-raise as appropriate service exception
  
- [ ] T074 [US3] Create POST endpoint in `src/api/endpoints/tabs.py`:
  - Route: POST /api/v1/tabs
  - Handler function: create_tab(tab_create: MusicTabCreate) -> MusicTab
  - Request body: automatically validated by Pydantic (MusicTabCreate)
  - Call tab_service.create(tab_create)
  - Return MusicTab with 201 status code (FastAPI: response_model=MusicTab, status_code=201)
  - Add docstring with endpoint summary, request/response schema reference
  - Measure response time for latency tracking
  
- [ ] T075 [US3] Implement error handling for POST in endpoint:
  - Pydantic validation errors (missing field, extra field, empty string): FastAPI auto-converts to 422, override to 400 with custom ErrorResponse
  - Service exceptions from create(): return 500 ErrorResponse(error="internal_server_error", message="Failed to create tab", details={})
  - Log all errors for debugging
  
- [ ] T076 [US3] Create custom Pydantic validation error handler:
  - Create exception handler for RequestValidationError in src/main.py
  - Extract missing/extra fields from error details
  - Return 400 ErrorResponse with appropriate message and missing_fields/extra_fields in details
  - Apply to all POST/PUT endpoints for consistency
  
- [ ] T077 [US3] Add type hints to POST handler:
  - create_tab(tab_create: MusicTabCreate) -> MusicTab
  - All imports typed, mypy --strict compatible
  
- [ ] T078 [US3] Implement storage directory creation:
  - Ensure storage/tabs/ directory exists on app startup
  - In src/main.py: pathlib.Path("storage/tabs").mkdir(parents=True, exist_ok=True)
  - Add to app startup event or at module init
  
- [ ] T079 [US3] Implement ID persistence (optional for MVP but recommended):
  - Strategy: Track max_id across restarts by scanning storage/tabs/ files on startup
  - In TabService.__init__: scan all *.json files, extract max id
  - If storage empty: start with max_id=0
  - First create() assigns id=1
  - Add docstring explaining recovery strategy
  
- [ ] T080 [US3] Run tests for US3:
  - Execute: pytest tests/contract/test_tabs_create.py tests/integration/test_tabs_workflow.py::test_create_tab tests/unit/test_tab_service.py::test_create -v
  - Verify: All tests pass (green phase)
  
- [ ] T081 [US3] Run linting, type checking, formatting:
  - Execute: pylint src/api/endpoints/tabs.py src/services/tab_service.py src/models/tab.py
  - Verify: Score ≥8.0 across all modified files
  - Execute: black --check src/
  - Execute: mypy src/ --strict
  - Verify: Zero errors
  
- [ ] T082 [US3] Run full coverage report:
  - Execute: coverage run -m pytest tests/ && coverage report --include=src/
  - Verify: Overall coverage ≥80%
  - Verify: All endpoint paths covered (success + error cases)
  - Verify: All service methods covered
  
- [ ] T083 [US3] Performance validation for POST:
  - Load test: 50 sequential POST /api/v1/tabs requests
  - Verify p95 latency <500ms (Principle IV)
  - Log sample timings
  - If target not met, profile file I/O and optimize JSON serialization
  
- [ ] T084 [US3] Verify concurrent POST handling:
  - Execute tests/integration/test_tabs_workflow.py::test_concurrent_posts
  - Verify: No ID collisions despite concurrent creates
  - Verify: All tabs persisted correctly
  - Verify: No file corruption or data loss

**Checkpoint**: All three user stories complete. Full MVP API functional: GET all, GET by ID, POST create. All endpoints tested, typed, linted, performant.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final polish, comprehensive testing, documentation, and quality validation across all user stories  
**Constitution Alignment**: Principle I (Code Quality), Principle IV (Performance Optimization)  
**Estimated Duration**: 2-3 hours

- [ ] T085 [P] Review all docstrings in src/ for completeness:
  - All modules have module-level docstrings
  - All functions have docstrings with parameters, return type, exceptions
  - All classes have docstrings explaining purpose
  - Use format: """Summary. Detailed description. Args: ... Returns: ..."""
  
- [ ] T086 [P] Refactor for cyclomatic complexity (Principle I):
  - Analyze all functions using pylint complexity metrics
  - Ensure all functions have complexity ≤5
  - If any exceed 5, break into smaller helper functions
  - Run: pylint --load-plugins=pylint.extensions.mccabe src/
  
- [ ] T087 [P] Add performance instrumentation:
  - Create src/utils/timing.py with request timing decorator
  - Wrap all endpoint handlers to log request/response time
  - Emit p95, p99 latency metrics per endpoint
  - Add to startup: Initialize timing stats collector
  
- [ ] T088 [P] Validate all error responses:
  - Audit all error paths in src/api/endpoints/tabs.py
  - Verify each returns ErrorResponse with correct schema
  - Verify HTTP status codes correct per contracts/openapi.md
  - Test: POST invalid JSON, missing headers, malformed requests
  
- [ ] T089 [P] Create integration test: full workflow with all endpoints in `tests/integration/test_full_workflow.py`:
  - POST 5 tabs sequentially
  - GET /api/v1/tabs, verify all 5 returned
  - GET /api/v1/tabs/3, verify correct tab returned
  - Test error cases: GET /api/v1/tabs/999, POST missing field
  - Verify no side effects between tests
  
- [ ] T090 [P] Create smoke test: quick validation in `tests/smoke_test.py`:
  - Single test that verifies all 3 endpoints respond
  - Can be run pre-deployment for quick sanity check
  - Fast execution (<2 seconds total)
  
- [ ] T091 Run full test suite:
  - Execute: pytest tests/ -v --tb=short
  - Verify: All tests pass
  - Fix any failures
  
- [ ] T092 Run full coverage report with detailed summary:
  - Execute: coverage run -m pytest tests/ && coverage report && coverage html
  - Generate HTML report
  - Verify: ≥80% coverage overall
  - Verify: No critical paths uncovered
  - Review uncovered lines, document why (e.g., defensive error handling)
  
- [ ] T093 Run full quality gate suite (one command):
  - Execute: `pylint src/ && black --check src/ tests/ && mypy src/ --strict && coverage run -m pytest tests/ && coverage report --fail-under=80`
  - Verify: All gates pass (exit code 0)
  - This command confirms Constitution compliance for Principles I, II, IV
  
- [ ] T094 [P] Add OpenAPI/Swagger documentation validation:
  - Run server: uvicorn src.main:app --reload
  - Access http://localhost:8000/docs (Swagger UI)
  - Verify: All 3 endpoints listed with correct methods
  - Verify: Request/response schemas displayed correctly
  - Verify: All fields present in documentation
  - Verify: Error responses documented
  
- [ ] T095 [P] Create usage documentation in README.md:
  - Add "API Endpoints" section with all 3 endpoints + example curl commands
  - Add "Running Tests" section with commands
  - Add "Code Quality" section: how to run linters, targets (≥8.0 pylint, 80%+ coverage)
  - Add "Performance" section: expected latencies per endpoint
  - Add "Development" section: TDD workflow, file structure, how to extend
  
- [ ] T096 Update .specify/memory/constitution.md if needed:
  - Verify all 4 principles integrated in implementation
  - Document how each principle was met:
    - Principle I: Type hints on all functions, complexity ≤5, pylint ≥8.0
    - Principle II: 80%+ coverage, all paths tested
    - Principle III: Consistent ErrorResponse schema, snake_case fields
    - Principle IV: <200ms p95 GET, <500ms p95 POST, <100MB memory
  
- [ ] T097 [P] Create deployment checklist in DEPLOYMENT.md:
  - Environment variables to set (ENVIRONMENT, PORT, HOST, DEBUG)
  - Python version requirement: 3.13+
  - Dependencies to install (from requirements.txt)
  - Commands to run before deployment (quality gates)
  - How to start server: uvicorn src.main:app --host 0.0.0.0 --port 8000
  - Health check endpoint recommendation (future: GET /health)
  
- [ ] T098 [P] Document future extensions in ROADMAP.md:
  - Phase 2: Database migration (PostgreSQL async)
  - Phase 3: Authentication/Authorization
  - Phase 4: Pagination for GET /api/v1/tabs
  - Phase 5: PUT/PATCH/DELETE endpoints
  - Phase 6: Caching layer (Redis optional)
  - Phase 7: Rate limiting and API keys
  
- [ ] T099 Create requirements.txt with pinned versions:
  - FastAPI==0.104.1
  - Uvicorn==0.24.0
  - Pydantic==2.5.0
  - pytest==7.4.3
  - pytest-asyncio==0.21.1
  - coverage==7.3.2
  - pylint==3.0.3
  - black==23.12.1
  - mypy==1.7.1
  - Include exact versions from development environment
  
- [ ] T100 Final validation:
  - Delete all storage/tabs/*.json files (clean state)
  - Restart app fresh
  - POST 3 new tabs via curl
  - GET all tabs, verify all 3 returned
  - GET each tab by ID, verify correct data
  - Run full test suite again: pytest tests/ -v
  - Run quality gates: pylint, black, mypy, coverage
  - Verify all pass
  - Celebrate! MVP complete and production-ready 🎉

**Checkpoint**: MVP complete, fully tested, documented, and ready for production deployment.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No prerequisites - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - **BLOCKS all user stories**
- **Phase 3 (US1)**: Depends on Phase 2 completion
- **Phase 4 (US2)**: Depends on Phase 2 completion; can run parallel to US1 (if staffed)
- **Phase 5 (US3)**: Depends on Phase 2 completion; can run parallel to US1/US2 (if staffed)
- **Phase 6 (Polish)**: Depends on all desired user stories completion

### Within Each User Story

- **Tests first**: Write all contract/integration/unit tests (T031-T052 for US2) → verify FAIL (red phase)
- **Models before services**: Services depend on models being defined
- **Services before endpoints**: Endpoints call service methods
- **Implementation after testing**: Write code to pass tests (green phase)
- **Linting/typing/coverage**: Verify quality gates before considering story complete
- **Performance validation**: Confirm latency targets met

### Parallel Opportunities

- **Phase 1**: All [P] marked tasks can run in parallel (different files)
- **Phase 2**: All [P] marked tasks can run in parallel (different models/fixtures)
- **After Phase 2**: All 3 user stories can proceed in parallel (different endpoints)
- **Within US1 tests**: All [P] tasks can run in parallel (different test files)
- **Within US1 models**: All [P] tasks can run in parallel (different model files)

---

## Parallel Example: Full Team Development

**Scenario**: 3 developers (Alice, Bob, Charlie), start after Phase 2 complete

```
Timeline:
Day 1-2:   All 3 developers complete Phase 1 & Phase 2 together
           Foundation ready for user story work

Day 3-4:   Parallel development (can run simultaneously):
  Alice:   US1 (Retrieve All) - T031-T045
  Bob:     US2 (Retrieve Single) - T046-T061
  Charlie: US3 (Create) - T062-T084

Day 5:     All merge branches, resolve any conflicts, run full test suite
           Phase 6 Polish together - T085-T100
           
Day 6:     Quality gates, documentation, deployment prep
```

**Key**: Each story is independent until Phase 6. No blocking dependencies between US1/US2/US3.

---

## MVP Scope vs. Full Implementation

### MVP (Minimum Viable Product) - User Story 1 Only

Delivers basic working API with:
- ✓ GET /api/v1/tabs (retrieve all tabs)
- ✓ Can POST 2-3 sample tabs manually to populate storage
- ✓ Full test coverage for GET endpoint
- ✓ All code quality gates passed
- ✓ Runnable locally with uvicorn

**Completion**: After T045 (US1 checkpoint)  
**Deployment**: Can push to staging for validation  
**Time**: ~1-2 days for single developer

### Incremental Delivery

- **Increment 1**: Complete US1 → Deploy (MVP baseline)
- **Increment 2**: Add US2 → Deploy (now has retrieval)
- **Increment 3**: Add US3 → Deploy (now has full CRUD read+create)
- **Each increment**: Independently testable, no breaking changes

### Full Implementation

All 3 user stories + Phase 6 Polish  
- ✓ All endpoints functional
- ✓ All error cases handled
- ✓ Full documentation
- ✓ Production-ready
- ✓ Deploy to production with confidence

**Time**: ~3-4 days for single developer, 2-3 days for team of 3

---

## Task Checklist Validation

**Format compliance** (all tasks follow strict format):
- ✓ All tasks start with `- [ ]` (checkbox)
- ✓ All tasks have sequential ID (T001, T002, ...)
- ✓ [P] marker used only for parallelizable tasks (different files, no dependencies)
- ✓ [Story] label on all user story phase tasks (US1, US2, US3)
- ✓ No [Story] label on Setup/Foundational/Polish phases
- ✓ All tasks have clear description with exact file paths
- ✓ 100 total tasks (T001-T100)
- ✓ All tasks specific enough for LLM/developer execution without additional context

**User Story Mapping**:
- ✓ US1: T031-T045 (15 tasks: 6 tests + 9 implementation)
- ✓ US2: T046-T061 (16 tasks: 7 tests + 9 implementation)
- ✓ US3: T062-T084 (23 tasks: 11 tests + 12 implementation)
- ✓ Setup: T001-T010 (10 tasks)
- ✓ Foundational: T011-T030 (20 tasks)
- ✓ Polish: T085-T100 (16 tasks)
- ✓ **Total**: 100 tasks

**Constitution Alignment**:
- ✓ Principle I (Code Quality): Type hints enforced (T012-T014, T040, T056, T077), linting tasks (T043, T059, T081), complexity checks (T086)
- ✓ Principle II (Testing Standards): TDD workflow emphasized, tests written first (T031-T036 before T037-T045), 80%+ coverage (T044, T060, T082), full test suite (T091)
- ✓ Principle III (UX Consistency): ErrorResponse schema standardized (T011), snake_case enforcement (T041, T057), consistent validation (T055, T075)
- ✓ Principle IV (Performance Requirements): Latency targets (<200ms GET, <500ms POST, <100MB memory) measured (T045, T061, T083-T084, T087), load testing (T045, T061, T083)

---

## Notes

- All tasks written to be executable by a developer or AI agent without ambiguity
- File paths are absolute within the project root (src/, tests/, storage/, etc.)
- Tests marked with [P] can execute in parallel; run all in same file together for efficiency
- Each user story independently deployable after its checkpoint
- Quality gates must pass before moving to next task/phase
- Performance targets are measurable and testable (not subjective)
- Future Phase 2 database migration path clear (TabService interface doesn't change, only file I/O → DB query swap)
