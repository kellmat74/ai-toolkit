---
name: backlog-protocol
description: Work the kellmat74/agent-backlog GitHub Issues queue - claim a ticket, work the backlog, pick the next backlog item, file a ticket, or close one out. Covers the label taxonomy, atomic claiming, the kanban board sync, and structured handoff comments.
---

# Agent Backlog Protocol

The AI Agent Team's shared task queue is GitHub Issues at `kellmat74/agent-backlog`,
worked via `gh` CLI (auth is already configured; never handle tokens). Claude Code and
Hermes coordinate purely through issue state - no direct agent-to-agent messaging.

## Label taxonomy

Every issue carries one label per applicable dimension. Scope is mandatory.

| Dimension | Labels |
|---|---|
| Routing | `agent:claude` (sync, IDE-bound), `agent:hermes` (async/scheduled), `agent:any` |
| Status | `status:ready` (groomed, claimable), `status:in-progress` (claimed), `status:blocked` (needs Matt/external input), `status:needs-review` (done, awaiting Matt) |
| Scope | `scope:work` (VisiQuate), `scope:personal`, `scope:ai-toolkit` |
| Priority | `priority:p0` (drop everything), `priority:p1` (this week), `priority:p2` (slack time) |

An issue with no status label is untriaged (shows in the board's Todo column). Don't
claim untriaged issues; ask Matt or triage first if directed.

## Picking work

List claimable issues for this agent, p0 first:

```bash
gh issue list --repo kellmat74/agent-backlog \
  --label "status:ready" --json number,title,labels,url \
  --jq '[.[] | select([.labels[].name] | any(. == "agent:claude" or . == "agent:any"))]
        | sort_by([.labels[].name] | if any(. == "priority:p0") then 0 elif any(. == "priority:p1") then 1 else 2 end)
        | .[] | "#\(.number)  \(.title)"'
```

## Claiming (atomic)

1. Swap the label - this is the claim; if it fails because another agent got there
   first, drop the ticket and pick another:

```bash
gh issue edit N --repo kellmat74/agent-backlog \
  --remove-label "status:ready" --add-label "status:in-progress"
```

2. Post `Claimed by claude at <ISO timestamp>.` as a comment. The kanban board
   follows label changes automatically (see below).

## While working

- Comment on substantial progress or direction changes, not chatter.
- If the issue's acceptance criteria turn out wrong or stale, say so in a comment
  before silently doing something different.

## Finishing

**Done:** close as completed with a handoff comment:

```bash
gh issue close N --repo kellmat74/agent-backlog --comment "## Handoff

**Status:** done
**What changed:**
- <bullet>

**State left behind:** <file paths, branches, commits, or 'none'>
**Next step (if any):** <follow-on work, or 'none'>"
```

**Needs review:** don't close. Swap `status:in-progress` for `status:needs-review`
and post the same handoff comment with `Status: needs-review`.

**Blocked:** don't close. Swap to `status:blocked`, comment what's blocking and who
or what can unblock, then move on to other work.

**Won't do:** no label for this. Close as not planned with a one-line reason:

```bash
gh issue close N --repo kellmat74/agent-backlog --reason "not planned" \
  --comment "Won't do: <reason>"
```

## Kanban board sync (automatic)

The board is GitHub Project 2 ("AI Agent Team", user kellmat74). The
`project-sync.yml` workflow in agent-backlog syncs the Status column automatically on
every label change, close, or reopen (via the PROJECT_SYNC_TOKEN repo secret), and
adds the issue to the board if auto-add missed it. You do NOT need to touch the board
when working issues - just manage labels and close reasons.

Manual fallback, only if the workflow is broken or a one-off resync is needed:

```bash
# find the item id for issue N, then set its Status column
ITEM=$(gh project item-list 2 --owner kellmat74 --format json \
  | jq -r '.items[] | select(.content.number == N) | .id')
gh project item-edit --id "$ITEM" \
  --project-id PVT_kwHOAYPyRc4BaAgL \
  --field-id PVTSSF_lAHOAYPyRc4BaAgLzhU7EvA \
  --single-select-option-id <OPTION_ID>
```

| Column | Option ID | When |
|---|---|---|
| Ready | d8c210fc | label `status:ready` |
| In Progress | 47fc9ee4 | label `status:in-progress` |
| Blocked | 7a340442 | label `status:blocked` |
| Needs Review | 79552a0f | label `status:needs-review` |
| Done | 98236657 | closed as completed |
| Won't Do | 6fb1e35c | closed as not planned |
| Todo | f75ad846 | untriaged (no status label) |

If these IDs stop working (field or project recreated), re-derive with
`gh project field-list 2 --owner kellmat74 --format json`.

## Filing new tickets

Required: context and acceptance criteria in the body, a scope label, and a routing
label. Add `status:ready` only if it's genuinely groomed; otherwise leave it
unlabeled for triage. Use the plan-sprint skill for decomposing epics into multiple
issues.
