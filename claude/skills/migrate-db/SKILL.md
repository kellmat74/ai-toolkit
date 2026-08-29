---
name: migrate-db
description: Plan and execute a database schema or data migration safely: backup first, staged rollout, validation, and a tested rollback path. Use when asked to change a schema, add or drop columns, backfill data, or run a migration against a shared database.
---

# Migrate DB

## Trigger
`/migrate-db <schema change or migration>`. Single-session workflow: the main session
runs it, delegating focused passes via the Task tool where noted.

## Safety rule
Destructive or irreversible steps must be **confirmed with the user before execution,
never auto-run**: running the migration against production, dropping columns or tables,
data type changes, and data backfills that rewrite rows. Backup-first is non-negotiable:
no production migration runs without a verified backup.

## Workflow

### 1. Analyze scope
Identify the changes:
- New tables / columns
- Column modifications or removals
- Index changes
- Constraint additions
- Data type changes
- Data backfills

Assess impact: data volume, downtime implications, rollback complexity, application
compatibility (does deployed code tolerate both old and new schema during transition?).

Delegate design review for non-trivial changes:
- `database-architect` (Task tool): migration step design, ordering, downtime strategy.
- `database-optimizer` (Task tool): index/performance implications on large tables.

### 2. Design the migration plan
Break into ordered steps, each with an estimated time and its own rollback:

```
Step 1: Create new column with default value      (seconds, rollback: drop column)
Step 2: Backfill from existing data                (minutes, rollback: reverse update)
Step 3: Create index                               (minutes, rollback: DROP INDEX)
Step 4: Add constraint                             (minutes, rollback: drop constraint)
```

Downtime strategy:
- **Full downtime**: stop app, migrate, restart. Simple. Fine for small tables and
  low-impact changes.
- **Zero-downtime**: parallel table or expand/contract pattern, replicate with
  triggers, switch traffic, drop old. For large tables and high-traffic apps.

State the selected strategy and rationale.

### 3. Write the migration script
One file, transactional where the engine allows, with the rollback script alongside:

```sql
-- Migration: <date>_<seq>_<description>.sql
BEGIN;
-- forward steps
COMMIT;

-- Rollback (kept with the migration, tested on staging):
-- BEGIN; ...reverse steps in reverse order... COMMIT;
```

### 4. Test on staging
Delegate to `test-engineer` (Task tool) or run directly:
1. Pre-migration state capture (row counts, distinct keys)
2. Run the migration script on staging
3. Post-migration validation: data integrity counts, schema inspection (columns,
   indexes, constraints all present)
4. Performance check: EXPLAIN ANALYZE the queries the change targets; confirm index use
5. Application compatibility: run the app test suite against the migrated staging schema
6. **Test the rollback script too**, not just the forward path

### 5. Backup (before production, always)
Delegate to `database-admin` (Task tool) or run directly:
```bash
pg_dump prod_db > prod_db_backup_<date>.sql   # or engine equivalent
# verify the backup is readable, store a copy off-host
```

### 6. Execute against production (after user confirmation)
Follow the chosen strategy:

**Full downtime**: notify users, stop app, run migration, validate, restart, monitor.

**Zero-downtime**: create parallel structure, replicate, verify parity, switch the
application over, monitor, then drop the old structure (that drop is itself a
destructive step: confirm it separately).

### 7. Validate
1. Row counts match pre-migration
2. Schema verification (new column/index/constraint present)
3. Application functionality: affected features work (logins, sessions, whatever the
   change touches)
4. Performance within baseline, no constraint-violation errors
5. No spike in error rate or support signal

### 8. Monitor
Watch error rate, query performance, and constraint violations for 24 hours before
calling it done. Delegate to `monitoring-specialist` (Task tool) if alerting setup is
needed.

## Migration patterns and risk

| Change type | Est. time | Risk | Notes |
|------------|-----------|------|-------|
| Add nullable column | seconds | Low | |
| Add column with default | minutes | Low | Default covers existing rows |
| Add index | 5-15 min | Low | CONCURRENTLY on Postgres for large tables |
| Rename column | minutes | Moderate | Code must handle both names during transition |
| Remove column | 5-10 min | High | Irreversible; backup first; update dependent code first |
| Change data type | 10-30 min | High | Use temp-column approach: create, copy/convert, swap |
| Add constraint | minutes | Low-moderate | Verify data satisfies it first; may need cleanup |
| Large table migration | 30 min-hours | High | Break into steps; zero-downtime pattern |

## Rollback plan
If any step fails:
1. Stop immediately
2. Run the step's rollback (drop new column/index/constraint as applicable)
3. Restore from backup if state is inconsistent
4. Communicate the failure
5. Diagnose root cause before redesigning and retrying

## Persistence
If this surfaces something durable (a data model detail, an engine-specific gotcha, a
migration pattern for this project), propose saving it to the Obsidian vault via the
vault skill. Ask before writing.

## Output
Report: scope, migration plan with per-step rollback, staging test results, backup
confirmation, execution log, validation results, and 24-hour monitoring status.
