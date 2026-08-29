---
name: tdd
description: Test-driven development workflow - write failing tests first, implement the minimum to pass, then refactor with tests as the safety net. Use when building a new feature or fixing a bug where tests should drive the design, or when the user asks for TDD explicitly.
---

# TDD: Test-Driven Development

## Trigger
`/tdd <requirement>`

Implements a feature or fix test-first: tests written before code, implementation
focused on passing them, refactoring done only under green tests.

## Purpose
- Tests are written BEFORE code
- Implementation is focused on passing tests
- High test coverage from the start
- Refactoring safety through a comprehensive suite
- Clear requirements expressed as test cases

## Workflow

### Phase 1: Analyze Requirements

1. Parse the requirement
   - Identify acceptance criteria
   - Extract edge cases
   - Note performance/security constraints
2. If the requirement is ambiguous, ask 1-2 sharp clarifying questions before
   writing anything. Document the acceptance criteria and assumptions.

### Phase 2: Design Test Suite

1. Identify test categories:
   - Unit tests (functions, methods)
   - Integration tests (component interactions)
   - Edge case tests (boundaries, error conditions)
   - Performance tests (if applicable)
   - Security tests (if applicable)

2. Lay out test file structure (adapt to the project's existing conventions):
   ```
   tests/
   ├── unit/
   │   ├── test_core_logic.py
   │   ├── test_utils.py
   │   └── test_validators.py
   ├── integration/
   │   ├── test_api_endpoints.py
   │   └── test_database_integration.py
   ├── edge_cases/
   │   └── test_boundary_conditions.py
   └── conftest.py (fixtures)
   ```

3. Design test cases
   - Input: acceptance criteria
   - Output: named test cases
   - Pattern: test_[feature]_[scenario]_[expected_result]

### Phase 3: Write Tests FIRST

**Key principle**: no implementation code until tests are written.

1. Unit tests
   ```python
   def test_jwt_token_creation_with_valid_payload():
       token = create_jwt_token({"user_id": 123})
       assert token is not None
       assert isinstance(token, str)

   def test_jwt_token_expires_in_24_hours():
       token = create_jwt_token({"user_id": 123})
       decoded = decode_jwt_token(token)
       assert decoded["exp"] - decoded["iat"] == 86400  # 24 hours

   def test_jwt_token_validation_fails_with_invalid_signature():
       token = "invalid.jwt.token"
       with pytest.raises(JWTInvalidSignatureError):
           decode_jwt_token(token)
   ```

2. Integration tests
   ```python
   def test_login_endpoint_returns_jwt_token():
       response = client.post("/auth/login",
           json={"email": "user@example.com", "password": "secret"})
       assert response.status_code == 200
       assert "token" in response.json()

   def test_protected_endpoint_requires_valid_jwt():
       response = client.get("/api/profile",
           headers={"Authorization": "Bearer invalid"})
       assert response.status_code == 401
   ```

3. Edge case tests
   ```python
   def test_jwt_token_rejects_expired_token():
       # Create token that expired 1 second ago
       past_time = int(time.time()) - 1
       token = create_jwt_token({"user_id": 123, "exp": past_time})
       with pytest.raises(JWTExpiredError):
           decode_jwt_token(token)

   def test_jwt_handles_empty_payload():
       with pytest.raises(InvalidPayloadError):
           create_jwt_token({})
   ```

4. State the coverage goal for this feature up front (see targets below).

### Phase 4: Run Tests (Should Fail)

**Red phase**: tests fail because the code doesn't exist yet.

```bash
pytest tests/ -v

# All tests FAIL (expected)
FAILED tests/test_auth.py::test_jwt_token_creation_with_valid_payload
FAILED tests/test_auth.py::test_jwt_token_expires_in_24_hours
...
```

If a new test passes before any implementation exists, it isn't testing the new
behavior. Fix the test.

### Phase 5: Implement Code

**Green phase**: implement the minimum code to pass tests. Don't over-engineer.

```python
import jwt
import time

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_jwt_token(payload):
    if not payload:
        raise InvalidPayloadError("Payload cannot be empty")

    payload["iat"] = int(time.time())
    payload["exp"] = payload["iat"] + 86400  # 24 hours

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise JWTExpiredError("Token has expired")
    except jwt.InvalidSignatureError:
        raise JWTInvalidSignatureError("Invalid token signature")
```

Then run the suite; all tests should pass before moving on.

### Phase 6: Refactor

**Refactor phase**: improve code quality while keeping tests green.

1. Check for code smells, duplication, missing type hints, weak error handling.
   For a nontrivial implementation, a fresh review pass helps: spawn the
   `code-reviewer` subagent (Task tool) on the new code - it reads only and
   reports issues without fixing them.
2. Apply refactorings one at a time.
3. Run tests after EACH refactoring. Tests validate refactoring safety; any
   failure means revert or fix before continuing.

### Phase 7: Test Coverage Analysis

1. Run coverage:
   ```bash
   pytest tests/ --cov=src --cov-report=term
   ```
2. Identify gaps: missing edge cases, untested error paths, low-coverage areas.
3. Write additional tests as needed
   - Target: minimum 85% coverage
   - Ideally 90%+ for critical paths

If the project has a `test-engineer` subagent available, delegating the gap
analysis to it as an independent pass can catch cases the implementing context
is blind to.

### Phase 8: Integration & Validation

1. Run the full suite, including integration tests against real dependencies.
2. Run performance tests if applicable (load, stress, benchmarks).
3. Final validation:
   - All tests pass
   - Coverage meets target
   - No performance regressions

## Test Design Patterns

### Arrange-Act-Assert
```python
def test_login_with_valid_credentials():
    # ARRANGE - Set up test data
    user = create_test_user(email="test@example.com", password="secret")

    # ACT - Perform action
    response = client.post("/login",
        json={"email": "test@example.com", "password": "secret"})

    # ASSERT - Verify results
    assert response.status_code == 200
    assert "token" in response.json()
```

### Given-When-Then
```python
def test_expired_token_rejected():
    # GIVEN - An expired JWT token
    token = create_expired_token()

    # WHEN - Requesting a protected endpoint
    response = client.get("/api/profile",
        headers={"Authorization": f"Bearer {token}"})

    # THEN - Request is rejected
    assert response.status_code == 401
    assert response.json()["error"] == "Token expired"
```

### Parametrized Tests
```python
@pytest.mark.parametrize("invalid_token,expected_error", [
    ("malformed.token", "Invalid format"),
    ("expired_token_data", "Token expired"),
    ("invalid_signature", "Invalid signature"),
    ("", "Missing token"),
])
def test_various_invalid_tokens(invalid_token, expected_error):
    with pytest.raises(AuthenticationError) as exc_info:
        verify_token(invalid_token)
    assert expected_error in str(exc_info.value)
```

## Best Practices

1. **Test FIRST** - write tests before implementation
2. **One assertion focus** - each test validates one behavior
3. **Clear test names** - name describes what is being tested
4. **DRY tests** - use fixtures for common setup
5. **Isolated tests** - no dependencies between tests
6. **Fast tests** - unit tests < 100ms, integration tests < 1s
7. **Deterministic** - tests always pass/fail consistently
8. **No test-only code** - keep implementation clean
9. **Document why** - comments explain non-obvious tests
10. **Coverage goals** - aim for 85%+

## Test Categories

- **Unit**: individual functions/methods, external deps mocked, fast and
  focused. Largest category (~70% of tests).
- **Integration**: component interactions with real dependencies (DB, API).
  Slower but comprehensive. Critical workflows (~20%).
- **End-to-end**: complete user workflows, no mocks. Slowest, most realistic.
  Happy path coverage (~10%).
- **Edge cases**: boundary conditions, error conditions, invalid inputs,
  performance limits. Cuts across the above.

## Metrics to Track

| Metric | Target | Tool |
|--------|--------|------|
| Line Coverage | 85%+ | pytest-cov |
| Branch Coverage | 80%+ | pytest-cov |
| Test Pass Rate | 100% | pytest |
| Test Speed | < 30s total | pytest -v |
| Critical Path Coverage | 95%+ | Manual review |

## Refactoring Safety

1. **Red-Green-Refactor cycle**
   - Red: tests fail (intentional)
   - Green: tests pass (implementation)
   - Refactor: improve code (tests stay green)
2. **Regression prevention**: change code, run tests; if tests fail you broke
   something - fix and re-run.
3. **Refactoring confidence**: with 85%+ coverage you can refactor without
   fear; tests catch regressions.

## Example Workflows

### Feature with TDD
```
1. Design tests for JWT auth
2. Write test suite (all fail)
3. Implement JWT code
4. Run tests -> all pass
5. Review pass suggests refactoring
6. Refactor (tests still pass)
7. Analyze coverage, add missing edge case tests
8. Final validation: 90% coverage, all tests pass
```

### Bug Fix with TDD
```
1. Find root cause (delegate to the debugger subagent if it's not obvious)
2. Write a regression test that reproduces the bug
3. Test runs -> fails (reproduces bug)
4. Fix the code
5. Test runs -> passes
6. Run full suite -> no regressions

Result: bug fixed, regression test prevents recurrence
```

## Persistence

If this surfaces something durable (a recurring pattern, a convention, a
lesson), propose saving it to the Obsidian vault via the vault skill - ask
before writing.

## Output Format

Report with:
- Test suite overview and design rationale
- Coverage analysis
- Test execution results
- Refactoring notes
- Outstanding items
