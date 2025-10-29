# Phase 4 Plan: POST /api/v1/tabs Endpoint (Create Tab)

**Start Date:** October 27, 2025  
**Target Completion:** Same session  
**User Story:** US3 - Create a new music tab via POST request

## Objectives

1. Implement POST /api/v1/tabs endpoint with request validation
2. Achieve 80%+ test coverage with comprehensive error cases
3. Validate all quality gates (mypy, pylint, coverage)
4. Enable Phase 5: Additional features and refinements

## Architecture

### Endpoint Spec
- **Method**: POST
- **Path**: /api/v1/tabs
- **Request Model**: MusicTabCreate (title, artist, content - all required, min length 1)
- **Response Model**: MusicTab (with auto-assigned ID)
- **Status Codes**:
  - 201: Created (success)
  - 400: Bad Request (validation error)
  - 500: Internal Server Error (storage failure)

### Request Example
```json
POST /api/v1/tabs
{
  "title": "Stairway to Heaven",
  "artist": "Led Zeppelin",
  "content": "Em7 - A7sus4\n..."
}
```

### Response Example (201 Created)
```json
{
  "id": 3,
  "title": "Stairway to Heaven",
  "artist": "Led Zeppelin",
  "content": "Em7 - A7sus4\n..."
}
```

## Implementation Tasks

### T1: Write Unit Tests (RED phase)
- Test successful creation with valid data
- Test ID auto-increment (ID should be max_id + 1)
- Test file persistence to storage/tabs/
- Test in-memory cache update
- **File**: tests/unit/test_tab_service.py (add to existing)
- **Tests to Add**: 3-4 (already exist, verify they pass)

### T2: Write Contract Tests (RED phase)
- Test 201 response with valid payload
- Test response schema matches MusicTab
- Test validation error (missing field) → 400
- Test validation error (empty string) → 400
- Test validation error (extra fields) → 400
- **File**: tests/contract/test_tabs_create.py (NEW)
- **Tests to Create**: 5-6 contract tests

### T3: Write Integration Tests (RED phase)
- Test complete workflow: POST → GET /tabs → verify in list
- Test multiple creates with ID increment verification
- Test persistence across service restarts (restart tab_service, verify IDs persist)
- **File**: tests/integration/test_tabs_create_workflow.py (NEW)
- **Tests to Create**: 3 integration tests

### T4: Implement POST Endpoint (GREEN phase)
- Create POST handler in src/api/endpoints/tabs.py
- Use tab_service.create() method
- Return 201 status code
- Handle validation errors gracefully
- **File**: src/api/endpoints/tabs.py (update existing)
- **Code**: ~20 lines

### T5: Quality Gates (REFACTOR phase)
- Run mypy --strict (target: 0 errors)
- Run pylint (target: 8.0+)
- Run pytest with coverage (target: 80%+)
- Fix any issues found
- **Files**: src/api/endpoints/tabs.py

### T6: Documentation
- Update API documentation with POST endpoint spec
- Add request/response examples
- Document status codes and error scenarios
- **File**: README.md or separate API_SPEC.md

## Test Plan

### Unit Tests (Existing - verify pass)
- test_create_success ✓
- test_create_increments_id ✓
- test_create_persists_to_file ✓
- test_create_persists_to_cache ✓

### Contract Tests (NEW - 6 tests)
```
TestCreateTabsEndpoint::
  ✓ test_create_tab_success - Valid payload → 201 + response
  ✓ test_create_tab_response_schema - Validates MusicTab fields
  ✓ test_create_tab_auto_increment_id - ID increments correctly
  ✓ test_create_tab_missing_field_title - Missing title → 400
  ✓ test_create_tab_missing_field_artist - Missing artist → 400
  ✓ test_create_tab_invalid_empty_string - Empty string → 400
```

### Integration Tests (NEW - 3 tests)
```
TestCreateTabsWorkflow::
  ✓ test_create_and_retrieve_workflow - POST then GET
  ✓ test_create_multiple_tabs_id_sequence - Multiple creates increment correctly
  ✓ test_create_persists_across_restart - Tab persists after service restart
```

## Expected Coverage Impact

### Before (Phase 3)
- Total: 76.97%
- Missing: Exception handlers, error paths

### After (Phase 4 - estimated)
- Total: 82%+ (validation error paths now tested)
- New coverage areas: 400/500 error responses

## Files to Create/Modify

| File | Type | Action |
|------|------|--------|
| tests/contract/test_tabs_create.py | Test | CREATE |
| tests/integration/test_tabs_create_workflow.py | Test | CREATE |
| src/api/endpoints/tabs.py | Source | MODIFY |
| README.md | Docs | UPDATE |

## Success Criteria

- ✅ All unit tests pass (existing 4 + new 3-4)
- ✅ All contract tests pass (new 6)
- ✅ All integration tests pass (new 3)
- ✅ Total coverage ≥ 80%
- ✅ mypy --strict: 0 errors
- ✅ pylint: ≥ 8.0/10
- ✅ No regressions (GET endpoints still work)
- ✅ 400/500 error handling verified

## Timeline

1. **Write Tests (RED)**: 15 min
2. **Implement Endpoint (GREEN)**: 10 min
3. **Quality Gates (REFACTOR)**: 10 min
4. **Documentation**: 5 min
5. **Validation**: 5 min

**Total**: ~45 minutes

## Notes

- Reuse existing fixtures from conftest.py
- POST endpoint can use same error handlers as GET
- Validation is automatic via Pydantic (MusicTabCreate model)
- No database migration needed yet (Phase 6)
- Keep implementation simple - add dependency injection in Phase 5 if needed

## Next Phase (Phase 5)

After Phase 4 completion:
- Refactor to use dependency injection
- Add authentication/authorization skeleton
- Add PUT endpoint for updates
- Add DELETE endpoint for removal
- Expand error handling coverage

---

**Ready to start? Begin with T1: Write unit tests to verify existing create() implementation.**
