# FastAPI Server Constitution

<!-- 
  Sync Impact Report (v1.0.1 - Documentation Standards added):
  - Version: 1.0.0 → 1.0.1 (new principle/section added)
  - New principle added (5 total): Documentation Standards
  - Amendment: Documentation organization guidelines (2025-10-29)
-->

## Core Principles

### I. Code Quality & Maintainability

Every API endpoint, service, and module MUST maintain high code quality standards.
Code quality is non-negotiable and verified at pull request review.

**Requirements**:
- All code MUST pass linting checks (configured in `.pylintrc` or `pyproject.toml`)
- Complexity: Cyclomatic complexity MUST be ≤ 5 per function; refactor beyond
- Type hints MUST be used on all function signatures and class attributes
- Documentation: Docstrings (Google style) REQUIRED on all public functions and classes
- No duplicated logic: Extract common patterns into utilities or base classes
- Dead code removal: All unused imports, functions, and branches MUST be removed

**Rationale**: High code quality reduces defects, accelerates onboarding, and enables safe refactoring.

---

### II. Testing Standards (NON-NEGOTIABLE)

Test-driven development (TDD) is mandatory for all new features and bug fixes.
The test suite is the contract between implementation and requirements.

**Requirements**:
- Tests MUST be written and FAIL before implementation begins (red-green-refactor cycle)
- Minimum coverage: 80% of all code paths (unit + integration combined)
- Test organization:
  - Unit tests: `tests/unit/` — test functions/methods in isolation
  - Integration tests: `tests/integration/` — test user journeys and service boundaries
  - Contract tests: `tests/contract/` — test API endpoint behavior and schemas
- All tests MUST run deterministically (no flaky tests); retry-logic is banned
- Async test support required; mark async tests with `@pytest.mark.asyncio`
- Fixtures MUST be in `tests/conftest.py` and clearly named (e.g., `fixture_user_valid`)
- Mock external dependencies (databases, HTTP calls); use `unittest.mock` or `pytest-mock`

**Rationale**: Tests ensure correctness, prevent regressions, and document expected behavior.

---

### III. User Experience Consistency

All API responses and user interactions MUST be predictable and consistent.
Users (API clients) rely on contracts; breaking them is a last-resort measure.

**Requirements**:
- Response format: All endpoints MUST return JSON with consistent structure
- Error responses MUST follow a single schema:
  ```json
  {
    "error": "error_code",
    "message": "human-readable message",
    "details": { }
  }
  ```
- Status codes MUST be HTTP-correct: 200 (success), 201 (created), 400 (client error), 500 (server error)
- Field naming: MUST use `snake_case` in JSON; consistency across all endpoints
- Versioning: Breaking changes MUST bump the API version (e.g., `/api/v1/` → `/api/v2/`)
- Deprecation: Old endpoints MUST be marked deprecated and supported for ≥2 major versions
- Documentation: All endpoints MUST be documented in OpenAPI/Swagger; auto-generated from docstrings

**Rationale**: Consistent user experience prevents surprises, reduces client-side error handling, and builds trust.

---

### IV. Performance Requirements

API MUST meet defined performance thresholds at all times.
Performance is measured, monitored, and actively optimized.

**Requirements**:
- Response time: p95 latency MUST be ≤ 200ms for all GET endpoints (exclude external I/O)
- Response time: p95 latency MUST be ≤ 500ms for all POST/PUT/DELETE endpoints
- Throughput: API MUST handle ≥ 1000 requests/second under normal load
- Database queries: No query MUST fetch > 10k records in a single call; paginate if needed
- Resource usage: Memory footprint MUST remain < 512MB under normal operation
- Monitoring: Response times MUST be logged and aggregated (e.g., via structured logging)
- Slow operations (> 100ms): MUST be marked with a comment explaining why; consider optimization
- Caching: Repeated queries for the same data MUST be cached (in-memory or Redis)

**Rationale**: Performance directly impacts user satisfaction and operational costs.
Users expect fast, responsive APIs. Monitoring enables early detection of degradation.

---

### V. Documentation Standards

All documentation MUST be organized logically and easily discoverable.
The project MUST maintain a clean root directory with documentation organized by purpose and audience.

**Requirements**:

**Project Root** (Keep minimal - only essential files):
- `README.md` — Project overview, quick start, commands reference, project structure, documentation guide
- `pyproject.toml` — Project metadata, build configuration, tool settings
- `requirements.txt` — Production dependencies with pinned versions
- `.pylintrc` — Linting configuration
- `.env.example` — Environment variables template

**Specification & Implementation Documentation** (`/specs/{feature}/`):
- Store all feature-specific documentation in the feature directory
- Include: `spec.md`, `plan.md`, `tasks.md`, data models, research, contracts
- Include: Phase completion reports (`PHASE_*.md`)
- Include: Feature-specific deployment guides (e.g., `DEPLOYMENT.md`)
- Rationale: Ties documentation to feature, easy to find feature-related files

**Strategic Reference Documentation** (`/documentation/`):
- Store cross-cutting, project-level documentation
- Include: Product roadmap (`ROADMAP.md`), project status, strategic plans
- Include: Documents that span multiple features or phases
- Rationale: Separates strategic planning from feature-specific docs

**Code Documentation** (Embedded in source files):
- All public functions, classes, and modules MUST have docstrings (Google style)
- Docstrings MUST include: summary, detailed description, Args, Returns, Raises
- FastAPI endpoints MUST include OpenAPI documentation in docstrings
- Rationale: Code is the source of truth; documentation lives with code

**README.md Requirements**:
- MUST include: Project overview, quick start guide, how to run tests, code quality checks
- MUST include: Complete project structure tree with descriptions
- MUST include: Documentation guide table (where to find what)
- MUST include: API endpoint examples with curl commands
- MUST include: Troubleshooting guide for common issues
- MUST include: Reference to specification documents
- Rationale: Single entry point for all users

**Documentation Maintenance Rule**:
- When creating new documentation, classify it first: spec-specific or strategic?
- If spec-specific → add to `/specs/{feature}/`
- If strategic/cross-cutting → add to `/documentation/`
- If belongs in code → add docstring to source file
- If belongs in README → update README.md
- **Never add `.md` files to project root (except README.md)**

**Rationale**: Clean project structure improves discoverability, reduces cognitive load, and makes documentation easier to maintain. Users know exactly where to look for information based on its type.

---

## Development Quality Standards

All code contributions MUST pass the following gates before merging:

1. **Linting**: `pylint` (score ≥ 8.0) and `black` formatting (auto-checked)
2. **Type Checking**: `mypy` with `--strict` flag (zero errors)
3. **Test Coverage**: Minimum 80% (measured via `coverage.py` or similar)
4. **Security**: No hardcoded secrets; use environment variables; run SAST (e.g., `bandit`)
5. **Performance Baseline**: No endpoint regression; new endpoints meet thresholds in Principle IV
6. **Documentation**: All new public APIs documented with docstring + OpenAPI example

**Rationale**: Quality gates prevent technical debt and ensure consistency across the codebase.

---

## Review & Deployment Process

All pull requests (PRs) MUST:

1. Reference a spec document (feature spec, bug description, or design doc)
2. Include links to passing CI runs (linting, tests, coverage, security)
3. Be reviewed by ≥1 maintainer; verify principle compliance before approval
4. Address comments before merge; do not force-push during review
5. Squash or rebase to keep history clean (one commit per logical change)

Deployment MUST occur via CI/CD pipeline, never manual. Rollback procedure MUST be tested.

---

## Governance

This constitution supersedes all other development practices and guidelines.
Principle violations MUST be justified in writing and require exception approval.

**Amendment Process**:
- Amendments MUST be documented with rationale and impact analysis
- Version bumps follow semantic versioning (MAJOR = principle removal/redefinition,
  MINOR = new principle/section added, PATCH = clarifications/typos)
- All amendments MUST update dependent templates (plan, spec, tasks)
- Changes take effect after merge to main; retroactive enforcement applies to new PRs only

**Compliance Review**:
- Every PR review MUST check: does this violate any principle?
- If violation exists: reject with reference to principle + remediation path
- If exception needed: document in issue + get explicit approval before merge

**Version**: 1.0.1 | **Ratified**: 2025-10-27 | **Last Amended**: 2025-10-29

---

## Development Notes

**Don't forget**:
- Using PowerShell for terminal commands
- Don't use `utils` dir (may conflict with other Python packages)
- Don't use Python eggs
