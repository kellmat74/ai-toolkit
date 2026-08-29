---
name: refactor
description: Safe incremental refactoring - verify test coverage first, change in small steps, run tests after every step, validate quality and performance at the end. Use when restructuring existing code without changing behavior, or when the user asks to refactor a file or component.
---

# Refactor: Safe Refactoring

## Trigger
`/refactor <file or component>`

Refactors safely: test coverage verified before starting, incremental changes
validated after each step, behavior preserved throughout.

## Purpose
- Existing test coverage is verified before starting
- Refactoring happens incrementally with test validation after each step
- No regression of functionality
- Code quality improvements without behavior changes
- Clear before/after comparisons

## Workflow

### Phase 1: Analyze Current State

1. Examine the code to refactor
   - Complexity metrics
   - Code smells
   - Duplication
   - Structure issues
2. Check test coverage
   ```bash
   pytest [component] --cov=[component] --cov-report=term
   ```
3. Identify refactoring needs
   - Extract functions
   - Remove duplication
   - Simplify logic
   - Improve naming
   - Better structure
4. Check for existing context: architecture decisions or prior refactoring
   notes in the repo's CLAUDE.md, docs, or the project's vault note. Respect
   documented constraints (performance targets, design patterns).

### Phase 2: Verify Test Coverage

1. Analyze existing tests: coverage report, test quality, gap analysis.
2. Ensure minimum 80% coverage on the code being refactored:
   ```
   If coverage < 80%:
   -> Write additional tests first (test-first, against current behavior)
   -> Reach target coverage
   -> Only then proceed
   ```
   For a large gap, the `test-engineer` subagent (Task tool) can do the gap
   analysis and write the missing tests as a fresh pass.
3. Record the coverage baseline (coverage %, test count, key scenarios) in the
   working notes for the final before/after comparison.
4. Run the full test suite. All tests must pass; no failures before starting.

### Phase 3: Design Refactoring Plan

1. Plan the steps
   - Order of changes
   - Dependency analysis
   - Risk assessment
2. Identify refactoring patterns to apply
   - Extract method
   - Extract class
   - Rename variables
   - Remove duplication
   - Simplify conditions
3. Write the plan down (steps, order, risks) before touching code.

### Phase 4: Execute Refactoring (Incremental)

**Key principle**: small changes, validate after each step.

1. Step 1: extract first function
   ```python
   # BEFORE
   def process_user_data(user):
       if user.age < 18:
           return "Minor"
       if user.status == "active":
           send_email(user.email)
       return user.name.upper()

   # AFTER - Extract validation
   def is_minor(user):
       return user.age < 18

   def process_user_data(user):
       if is_minor(user):
           return "Minor"
       if user.status == "active":
           send_email(user.email)
       return user.name.upper()
   ```

2. Run tests after each small change
   ```bash
   pytest tests/ -v
   # All tests pass? Continue.
   # Test fails? Revert change, try different approach.
   ```

3. Step 2: extract next function
   ```python
   def notify_active_user(user):
       if user.status == "active":
           send_email(user.email)

   def process_user_data(user):
       if is_minor(user):
           return "Minor"
       notify_active_user(user)
       return user.name.upper()
   ```

4. Run tests again.

5. Continue with remaining refactorings, and after each change:
   ```bash
   # 1. Run tests
   pytest tests/ -v

   # 2. Check coverage hasn't dropped
   pytest --cov=[component] --cov-report=term

   # 3. Verify behavior is unchanged (test results identical)
   ```
   Commit in small, logical increments rather than one large change.

### Phase 5: Validate After Each Batch

After every 2-3 changes:

1. Run the full test suite
   ```bash
   pytest tests/ -v --tb=short
   ```
2. Check code quality
   ```bash
   pylint [file]  # or language-specific linter
   ```
3. Measure complexity reduction
   ```
   Before refactoring: cyclomatic complexity 15
   After step 1: 12
   After step 2: 10
   Goal: < 10
   ```
4. Verify coverage maintained
   ```bash
   pytest --cov=[component]
   # Coverage before: 85%
   # Coverage after: 85% (or better)
   ```

### Phase 6: Code Review

When the refactoring is complete, spawn the `code-reviewer` subagent (Task
tool) on the diff for an independent pass. It should check:

- Code clarity improved?
- Naming is better?
- Duplication removed?
- Logic simplified?
- Architecture maintained: no unexpected coupling, design patterns respected,
  scalability preserved?

If the code touches auth, secrets, or external input, run `security-auditor`
in parallel with the same scope.

### Phase 7: Performance Validation

Refactoring shouldn't slow things down.

1. Compare performance metrics before/after
   ```
   Metric: Response time for /api/users
   - Before refactoring: 250ms
   - After refactoring: 245ms
   - Improvement: 2% (acceptable)

   Metric: Memory usage
   - Before: 120MB
   - After: 120MB
   - Regression: none (good)
   ```
2. Run performance tests if the project has them
   ```bash
   pytest tests/performance/ -v
   ```
3. Benchmark critical paths
   ```bash
   python -m cProfile -s cumulative main.py
   ```

For performance-critical components, the `performance-engineer` subagent can
do this comparison as an independent pass.

### Phase 8: Final Validation

1. All tests pass
2. Coverage maintained
3. Code quality improved
4. Performance maintained or improved
5. Architecture respected
6. Review findings addressed

Summarize before/after: coverage, complexity, lines of code, test results.

## Refactoring Patterns

### Extract Method
```python
# BEFORE
def calculate_total(items):
    subtotal = sum(item.price for item in items)
    tax = subtotal * 0.08
    shipping = 10 if subtotal < 50 else 0
    return subtotal + tax + shipping

# AFTER
def calculate_tax(subtotal):
    return subtotal * 0.08

def calculate_shipping(subtotal):
    return 10 if subtotal < 50 else 0

def calculate_total(items):
    subtotal = sum(item.price for item in items)
    return subtotal + calculate_tax(subtotal) + calculate_shipping(subtotal)
```

### Remove Duplication
```python
# BEFORE
def get_active_users():
    users = db.query(User).filter(User.status == "active").all()
    return [u.to_dict() for u in users]

def get_premium_users():
    users = db.query(User).filter(User.status == "premium").all()
    return [u.to_dict() for u in users]

# AFTER
def get_users_by_status(status):
    users = db.query(User).filter(User.status == status).all()
    return [u.to_dict() for u in users]

def get_active_users():
    return get_users_by_status("active")

def get_premium_users():
    return get_users_by_status("premium")
```

### Simplify Conditional Logic
```python
# BEFORE
def is_eligible_for_discount(user):
    if user.is_premium:
        if user.spent_amount > 1000:
            if user.days_member > 365:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# AFTER
def is_eligible_for_discount(user):
    return (user.is_premium and
            user.spent_amount > 1000 and
            user.days_member > 365)
```

### Extract Class
```python
# BEFORE
class User:
    def __init__(self, name, email, street, city, zip):
        self.name = name
        self.email = email
        self.street = street
        self.city = city
        self.zip = zip

    def format_address(self):
        return f"{self.street}, {self.city} {self.zip}"

# AFTER
class Address:
    def __init__(self, street, city, zip):
        self.street = street
        self.city = city
        self.zip = zip

    def format(self):
        return f"{self.street}, {self.city} {self.zip}"

class User:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address
```

## Metrics to Track

| Metric | Goal | Tool |
|--------|------|------|
| Cyclomatic Complexity | < 10 per function | radon, pylint |
| Lines per Function | < 30 lines | wc, radon |
| Duplication | < 3% | pylint, radon |
| Test Coverage | Maintain 85%+ | pytest-cov |
| Performance | No regression | cProfile, benchmarks |

## Risk Mitigation

### Before Starting
- [ ] All tests passing
- [ ] Coverage baseline documented
- [ ] Refactoring plan documented
- [ ] Architecture constraints reviewed
- [ ] Performance baseline measured

### During Refactoring
- [ ] Tests run after each small change
- [ ] No large unvalidated changes
- [ ] Incremental commits (not one large change)

### After Completion
- [ ] All tests pass
- [ ] Coverage maintained or improved
- [ ] Code review done
- [ ] Performance validated

## Best Practices

1. **Small incremental changes** - 1-2 refactorings per commit
2. **Test after each change** - validate before proceeding
3. **Measure complexity** - know what you're improving
4. **Document decisions** - why this refactoring?
5. **Preserve behavior** - code should work identically
6. **Review thoroughly** - different eyes catch issues
7. **Performance validate** - refactoring shouldn't slow things down
8. **Architecture check** - don't violate design patterns
9. **Git branching** - isolated feature branch for refactoring
10. **Clear commits** - logical, reviewable commit messages

## Persistence

If this surfaces something durable (a recurring pattern, a convention, a
lesson), propose saving it to the Obsidian vault via the vault skill - ask
before writing.

## Output Format

Report with:
- Baseline metrics (before) and final metrics (after)
- Changes made, by category (extract, remove duplication, simplify, etc.)
- Test results (all passing)
- Coverage analysis (maintained or improved)
- Review findings, if any
- Performance impact
- Lessons learned
