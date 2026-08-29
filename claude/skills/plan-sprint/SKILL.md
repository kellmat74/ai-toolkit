---
name: plan-sprint
description: Decompose an epic or large requirement into stories and tasks with acceptance criteria, sizing, and dependency ordering, then file them as GitHub issues in kellmat74/agent-backlog. Use when asked to plan a sprint, break down an epic, or turn a big feature request into backlog issues.
---

# Plan Sprint

## Trigger
`/plan-sprint <epic or requirement>`. With no argument, ask what to plan.

## What it does
Turns one epic-sized requirement into a dependency-ordered set of backlog issues.
Two phases: decompose and show the plan, then (only after confirmation) create
issues via `gh issue create`.

## Phase 1: Decompose

1. Parse the epic: goal, acceptance criteria, constraints, tech stack, risks.
   If acceptance criteria are missing or ambiguous, ask 1-2 sharp questions
   before decomposing.
2. Break the epic into user stories. Each story gets:
   - Title and 2-5 concrete acceptance criteria
   - Effort points (see sizing table)
   - Dependencies on other stories
3. Break stories into tasks where a story spans distinct work types
   (implementation, tests, docs, review). Small stories can stay one issue.
4. Order by dependency: design before implementation, tests alongside or
   before code, integration after components, docs can start early. Call out
   what can run in parallel.

### Sizing

| Points | Effort | Duration | Typical |
|--------|--------|----------|---------|
| 3 | Trivial | under 1 hour | Doc update, small fix |
| 5 | Small | 1-2 hours | Simple feature, utility |
| 8 | Medium | 2-4 hours | Feature with tests |
| 13 | Large | 4-8 hours | Complex feature, integration |
| 21 | Too big | 8+ hours | Break it down further |

No story over 13 points. Leave 10-15% buffer for unknowns.

### Present the plan

Show the user the full breakdown before creating anything:
- Stories with acceptance criteria, points, dependencies
- Proposed labels per issue (routing, scope, priority)
- Sequential vs parallel ordering
- Total points and risk notes

Wait for explicit confirmation. Issue creation is outward-facing; do not
create issues from the plan alone.

## Phase 2: Create issues

After confirmation, create one issue per story (or per task for split
stories) in `kellmat74/agent-backlog`:

```bash
gh issue create --repo kellmat74/agent-backlog \
  --title "<story title>" \
  --body "<acceptance criteria, points, dependencies as 'Blocked by #N', context>" \
  --label "agent:claude,status:ready,scope:personal,priority:p2"
```

Label rules (one per dimension, scope is mandatory):
- Routing: `agent:claude` (synchronous, in-IDE), `agent:hermes` (async,
  scheduled, browser/scraping), `agent:any` (either)
- Status: `status:ready` for unblocked issues, `status:blocked` for issues
  with unmet dependencies
- Scope: `scope:work` (VisiQuate), `scope:personal`, `scope:ai-toolkit`
- Priority: `priority:p0` / `priority:p1` / `priority:p2`

Create issues in dependency order so `Blocked by #N` references resolve to
real issue numbers. After creating, list the issue URLs back to the user.

## Notes

- Routing is the `agent:*` label, nothing else. Do not invent agent
  assignment tables or spawn planning subagents; the decomposition happens
  in the main session.
- If the epic itself deserves a tracking issue, create it first and
  reference it from each story body.
