---
name: backlog-protocol
description: Read and work the kellmat74/agent-backlog GitHub Issues queue. Covers claiming tasks, updating status labels, and closing with a structured handoff comment.
version: 1.2.0
author: kellmat74
platforms: [macos]
metadata:
  hermes:
    tags: [backlog, github, agent-coordination]
    related_skills: [github-issues]
---

# Agent Backlog Protocol

The shared task queue lives at `kellmat74/agent-backlog` on GitHub. All agents
(Claude Code and Hermes) read and write it using `gh` CLI. Authentication uses
the system keyring -- no token setup required.

## Label schema

**Routing** (who should do this):
- `agent:hermes` -- Hermes should handle (async, scheduled, channel-driven)
- `agent:claude` -- Claude Code should handle (sync, IDE-bound)
- `agent:any` -- either agent can claim

**Status:**
- `status:ready` -- claimable, no one is working it
- `status:in-progress` -- claimed, work is underway
- `status:blocked` -- waiting on something external
- `status:needs-review` -- done but needs a human or agent to verify

**Scope:**
- `scope:ai-toolkit` -- agent infrastructure (spans work and personal)
- `scope:work` -- VisiQuate client or internal
- `scope:personal` -- personal projects

**Priority:**
- `priority:p0` -- drop everything
- `priority:p1` -- this week
- `priority:p2` -- whenever there is slack

---

## Discovering your work queue

List open issues assigned to Hermes, highest priority first:

```bash
gh issue list \
  --repo kellmat74/agent-backlog \
  --label "agent:hermes" \
  --label "status:ready" \
  --json number,title,labels,url \
  --jq 'sort_by(.labels | map(.name) | index("priority:p0") // (index("priority:p1") // (index("priority:p2") // 99))) | .[] | "#\(.number)  \(.title)  \(.url)"'
```

Also check `agent:any` for unclaimed tasks:

```bash
gh issue list \
  --repo kellmat74/agent-backlog \
  --label "agent:any" \
  --label "status:ready" \
  --json number,title,url \
  --jq '.[] | "#\(.number)  \(.title)  \(.url)"'
```

---

## Claiming a task

When you start work on an issue, move it from `status:ready` to `status:in-progress`:

```bash
ISSUE=42
gh issue edit $ISSUE \
  --repo kellmat74/agent-backlog \
  --remove-label "status:ready" \
  --add-label "status:in-progress"
```

---

## Closing with a handoff comment

When you finish (or get blocked), close the issue with this structured comment
so the next agent or human can pick up without a summary from you:

```bash
ISSUE=42
gh issue close $ISSUE \
  --repo kellmat74/agent-backlog \
  --comment "## Handoff

**Status:** done | blocked | needs-review
**What changed:**
- <bullet>
- <bullet>

**State left behind:** <file paths, branch names, output locations, or 'none'>
**Next step (if any):** <what a follow-on agent or human should do, or 'none'>"
```

For a blocked issue, don't close it -- just update the label and comment:

```bash
gh issue edit $ISSUE \
  --repo kellmat74/agent-backlog \
  --remove-label "status:in-progress" \
  --add-label "status:blocked"

gh issue comment $ISSUE \
  --repo kellmat74/agent-backlog \
  --body "## Handoff

**Status:** blocked
**What changed:** <what was done so far>
**Blocked on:** <what is needed to continue>
**Next step:** <who or what can unblock this>"
```

---

## Won't do

There is no `status:wont-do` label. Close the issue as not planned with a one-line
reason; the kanban board shows these in its Won't Do column:

```bash
gh issue close $ISSUE --repo kellmat74/agent-backlog \
  --reason "not planned" --comment "Won't do: <reason>"
```

---

## Kanban board sync (automatic)

The queue also renders as GitHub Project 2 ("AI Agent Team", owner kellmat74).
The `project-sync.yml` workflow in agent-backlog syncs the board's Status column
automatically on every label change, close, or reopen. Do not touch the board when
working issues - manage labels and close reasons only.

Manual fallback, only if the workflow is broken or a one-off resync is needed:

```bash
ITEM=$(gh project item-list 2 --owner kellmat74 --format json \
  | jq -r '.items[] | select(.content.number == '$ISSUE') | .id')
gh project item-edit --id "$ITEM" \
  --project-id PVT_kwHOAYPyRc4BaAgL \
  --field-id PVTSSF_lAHOAYPyRc4BaAgLzhU7EvA \
  --single-select-option-id <OPTION_ID>
```

Option IDs: Ready `d8c210fc`, In Progress `47fc9ee4`, Blocked `7a340442`,
Needs Review `79552a0f`, Done `98236657`, Won't Do `6fb1e35c`, Todo `f75ad846`.
Re-derive with `gh project field-list 2 --owner kellmat74 --format json` if stale.

---

## Quick reference

| Action | Command |
|--------|---------|
| List my queue | `gh issue list --repo kellmat74/agent-backlog --label "agent:hermes" --label "status:ready"` |
| View an issue | `gh issue view N --repo kellmat74/agent-backlog` |
| Claim | edit: remove `status:ready`, add `status:in-progress` |
| Done | `gh issue close N --repo kellmat74/agent-backlog --comment "## Handoff ..."` |
| Blocked | edit: remove `status:in-progress`, add `status:blocked` + comment |
| Won't do | `gh issue close N --reason "not planned" --comment "Won't do: <reason>"` |
| Board sync | automatic via project-sync.yml workflow; manual fallback above |
