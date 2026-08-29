---
name: deploy
description: Plan and execute a production deployment with readiness gates, a chosen rollout strategy (blue-green, canary, rolling), verification, and rollback. Use when asked to deploy, ship, release, or promote a version to staging or production.
---

# Deploy

## Trigger
`/deploy <version or component>`. Single-session workflow: the main session runs it,
delegating focused passes via the Task tool where noted.

## Safety rule
The production deploy itself, the traffic switch, and any database migration bundled
with it are irreversible-enough steps: **confirm with the user before executing each
one. Never auto-run them.** Everything before that (planning, staging validation,
checklist review) proceeds without confirmation.

## Workflow

### 1. Define scope
Identify what is deploying:
- Code version/commit
- Database migrations (if any, see the `migrate-db` skill; coordinate, don't duplicate)
- Infrastructure changes
- Configuration updates
- Dependencies

### 2. Readiness gates

```
PRE-DEPLOYMENT CHECKLIST
========================

Code Readiness:
[ ] All features merged to main branch
[ ] All code reviews completed and approved
[ ] All tests passing (unit, integration, E2E)
[ ] Code quality checks passing (lint, format)
[ ] No security vulnerabilities found
[ ] No performance regressions detected

Database Readiness (if migrations included):
[ ] Schema migration tested on staging
[ ] Rollback procedure documented
[ ] Data backup created
[ ] Migration duration estimated
[ ] Zero-downtime strategy planned if needed

Documentation:
[ ] Release notes prepared
[ ] Rollback procedure documented
[ ] Team notified of deployment window
[ ] Customer communication prepared (if user-visible)

Environment:
[ ] Staging environment matches production
[ ] All environment variables configured
[ ] Secrets properly managed (not in code)
[ ] Monitoring configured

Dependencies:
[ ] External services operational
[ ] API integrations tested
[ ] No known issues blocking deployment
```

Delegate verification of gates you can't check directly:
- `test-engineer` (Task tool): run/verify the test suite and staging smoke tests.
- `devops-engineer` (Task tool): verify infrastructure, env vars, secrets handling.

Any unchecked gate: report it and ask the user whether to proceed or fix first.

### 3. Validate on staging
Have `test-engineer` run, or run directly:
1. Smoke tests (health endpoint returns healthy + expected version)
2. Functional tests (full suite against staging)
3. Load test if the change is performance-sensitive (compare p95 and error rate to targets)
4. Dependency vulnerability scan

### 4. Pick a rollout strategy

| Strategy | Downtime | Rollback | Complexity | Risk |
|----------|----------|----------|-----------|------|
| Blue-Green | 0 | Instant | Low | Low |
| Canary | 0 | Fast (~5 min) | Medium | Low |
| Rolling | 0 | Gradual | High | Medium |
| Maintenance window | 10-30 min | Instant | Low | Medium |

**Blue-Green**: deploy to idle environment, test, warm up, switch traffic, keep old
environment running 2 hours as instant rollback.

**Canary**: route 5% of traffic to new version, monitor 30 min, then 25% -> 50% -> 100%
with monitoring between each step. Keep old version running for rollback.

**Rolling**: pull one server from the load balancer at a time, deploy, health-check,
re-add, monitor, repeat. Accepts mixed versions during rollout.

State the selected strategy and rationale, then **confirm with the user before
executing**.

### 5. Execute (after confirmation)
Staged sequence, verifying at each step:
1. Notify team of start, expected duration, ETA
2. Deploy artifact to target environment
3. Run migrations if bundled (confirm separately, see safety rule)
4. Health checks: endpoints, database connectivity, external integrations
5. Warm up / partial traffic per chosen strategy
6. Switch or ramp traffic
7. Keep the previous version available for rollback per strategy

### 6. Post-deploy verification
1. Smoke test production health endpoint (correct version reported)
2. Exercise key features (auth, core API calls, new functionality)
3. Compare metrics to baseline: error rate, response time, CPU, memory, DB connections

### 7. Monitor
Delegate to `monitoring-specialist` (Task tool) or run directly: watch error rate,
latency, resource usage, and alerts for the first 2 hours at 30-minute checkpoints.
Declare success only after the window is clean; then decommission the old version.

## Rollback procedure
If problems are detected at any point:
1. Switch traffic back to the previous version (blue-green: instant; canary: revert routing)
2. Notify team with the reason
3. Investigate root cause (logs, metrics, traces)
4. Fix, re-test, re-deploy; do not retry the same artifact without a diagnosis

## Persistence
If this surfaces something durable (a deployment gotcha for this stack, a strategy
decision worth keeping), propose saving it to the Obsidian vault via the vault skill.
Ask before writing.

## Output
Report: scope, gate results, chosen strategy and rationale, execution log, verification
results, monitoring status, and rollback readiness.
