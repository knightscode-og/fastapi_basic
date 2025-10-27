---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Constitution Alignment**: Principle I (Code Quality), Principle II (Testing Standards)

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools (pylint, black, mypy --strict)
- [ ] T004 [P] Setup test infrastructure: pytest, pytest-asyncio, pytest-cov, coverage.py
- [ ] T005 Create conftest.py with common fixtures and test utilities
- [ ] T006 Configure CI/CD pipeline (GitHub Actions / GitLab CI) for quality gates

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Constitution Alignment**: Principle III (UX Consistency), Principle IV (Performance Requirements)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T007 Create base response schema and error handling middleware (for Principle III)
- [ ] T008 Setup database connection pooling and query monitoring (for Principle IV)
- [ ] T009 [P] Implement authentication/authorization framework with type hints
- [ ] T010 [P] Setup API routing and middleware structure; enforce snake_case naming
- [ ] T011 Create base models/entities with full type hints; all public methods documented
- [ ] T012 Configure structured logging with response time tracking (for Principle IV)
- [ ] T013 Setup environment configuration management (secrets, feature flags)
- [ ] T014 Create contracts/ directory and add OpenAPI schema generation
- [ ] T015 Setup database migrations framework and write first migration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

**Constitution Alignment**: All 4 principles apply; emphasis on Principle II (TDD) and Principle III (consistent API response)

### Tests for User Story 1 (REQUIRED - per Principle II) ⚠️

> **MANDATORY**: Write these tests FIRST, ensure they FAIL before implementation

- [ ] T016 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py (verify response schema)
- [ ] T017 [P] [US1] Contract test for error cases in tests/contract/test_[name].py (verify error schema per Principle III)
- [ ] T018 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py (end-to-end validation)
- [ ] T019 [P] [US1] Unit test for [Service] business logic in tests/unit/test_[service].py

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create [Entity1] model in src/models/[entity1].py (with full type hints, docstring)
- [ ] T021 [P] [US1] Create [Entity2] model in src/models/[entity2].py (with full type hints, docstring)
- [ ] T022 [US1] Implement [Service] in src/services/[service].py (depends on T020, T021; add logging)
- [ ] T023 [US1] Implement [endpoint/feature] in src/api/endpoints/[file].py; validate response matches contract
- [ ] T024 [US1] Add validation and error handling; verify errors follow schema from Principle III
- [ ] T025 [US1] Add performance logging and verify p95 latency meets Principle IV thresholds
- [ ] T026 [US1] Run linting (pylint ≥8.0), type check (mypy --strict), coverage (≥80%)

**Checkpoint**: At this point, User Story 1 should be fully functional, tested, and compliant with all principles

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

**Constitution Alignment**: All principles apply; same quality gates as US1

### Tests for User Story 2 (REQUIRED - per Principle II) ⚠️

- [ ] T027 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T028 [P] [US2] Contract test for error cases in tests/contract/test_[name].py
- [ ] T029 [P] [US2] Integration test for [user journey] in tests/integration/test_[name].py
- [ ] T030 [P] [US2] Unit test for [Service] business logic in tests/unit/test_[service].py

### Implementation for User Story 2

- [ ] T031 [P] [US2] Create [Entity] model in src/models/[entity].py (with type hints, docstring)
- [ ] T032 [US2] Implement [Service] in src/services/[service].py (with logging)
- [ ] T033 [US2] Implement [endpoint/feature] in src/api/endpoints/[file].py; verify response matches contract
- [ ] T034 [US2] Integrate with User Story 1 components (if needed); verify no conflicts
- [ ] T035 [US2] Verify error handling and response consistency with Principle III
- [ ] T036 [US2] Run linting, type check, coverage gates before merge

**Checkpoint**: All user stories should now be independently functional and compliant

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

**Constitution Alignment**: All principles apply; same quality gates as US1 and US2

### Tests for User Story 3 (REQUIRED - per Principle II) ⚠️

- [ ] T037 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T038 [P] [US3] Contract test for error cases in tests/contract/test_[name].py
- [ ] T039 [P] [US3] Integration test for [user journey] in tests/integration/test_[name].py
- [ ] T040 [P] [US3] Unit test for [Service] business logic in tests/unit/test_[service].py

### Implementation for User Story 3

- [ ] T041 [P] [US3] Create [Entity] model in src/models/[entity].py (with type hints, docstring)
- [ ] T042 [US3] Implement [Service] in src/services/[service].py (with logging)
- [ ] T043 [US3] Implement [endpoint/feature] in src/api/endpoints/[file].py; verify response matches contract
- [ ] T044 [US3] Verify error handling and response consistency with Principle III
- [ ] T045 [US3] Run linting, type check, coverage gates before merge

**Checkpoint**: All user stories should now be independently functional and ready for production

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

**Constitution Alignment**: Principle I (Code Quality), Principle IV (Performance Optimization)

- [ ] TXXX [P] Documentation updates in docs/ and OpenAPI schema validation
- [ ] TXXX Code cleanup and refactoring; verify complexity ≤5 per function (Principle I)
- [ ] TXXX Performance optimization and benchmarking; verify p95 latencies (Principle IV)
- [ ] TXXX [P] Run full quality gate suite: pylint, mypy, black, coverage, security scan
- [ ] TXXX Security hardening and secrets audit; use environment variables everywhere
- [ ] TXXX Integration testing across all user stories; verify end-to-end workflows
- [ ] TXXX Run quickstart.md validation and smoke tests in staging environment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
