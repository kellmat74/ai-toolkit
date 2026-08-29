---
name: handoff
description: Capture the current session's state as a handoff note in the Obsidian vault so the next session (Claude or Hermes) can pick up without re-deriving context. Use when wrapping up a work session, switching agents, or when asked to hand off, write up where we are, or preserve session state.
---

# Handoff

## Trigger
`/handoff [project or current work]`. With no argument, hand off whatever this
session has been working on.

## What it does
Writes a markdown handoff note to the Obsidian vault, adds or updates the
`## Vault Note` backpointer in the project's CLAUDE.md, and optionally files a
backlog issue if follow-up work should be routed to another agent or session.

## What the note must capture

Work through this checklist; skip sections only when genuinely empty:

- **State of work**: what's done (committed? pushed? tested?), what's
  in progress and how far along, what hasn't started
- **Decisions made**: architecture and technology choices with rationale
  and constraints, so they don't get relitigated
- **Next steps**: concrete immediate actions, in order, with enough detail
  to start cold
- **Blockers**: what's stuck, why, and any known mitigation or owner
- **Gotchas**: anything non-obvious learned this session (flaky behavior,
  misleading errors, config that lives somewhere unexpected)
- **File locations**: paths to the files that matter, including anything
  half-modified or awaiting review

Before writing, verify the working tree honestly: uncommitted changes,
failing tests, and unpushed commits belong in the note, not glossed over.

## Where it goes

Vault root (quote it, the path has spaces):

```
~/Library/CloudStorage/GoogleDrive-kellmat74@gmail.com/My Drive/Obsidian-Personal/Obsidian Vault/
```

Write the note under `_ai/<project-folder>/`, e.g.
`_ai/ai-toolkit/handoff-2026-08-28.md`. If the project already has a vault
note, prefer updating it (or adding a dated handoff section) over scattering
new files; use a separate dated handoff file when the state is genuinely
session-specific. Date the note and name the project in the first line.

## Backpointer (mandatory)

Per the vault backpointer rule, add or update a `## Vault Note` section in the
project's CLAUDE.md pointing at the note:

```markdown
## Vault Note

Durable context for this project is in the Obsidian vault at `_ai/<folder>/<file>.md`.
Check it at the start of any new session for data model details, file locations, and prior decisions.
```

If the section already exists and points at the right file, leave it alone.

## Routing follow-up work (optional)

If the next steps should be picked up by a specific agent rather than
whichever session opens the project next, file an issue in
`kellmat74/agent-backlog`:

```bash
gh issue create --repo kellmat74/agent-backlog \
  --title "<follow-up title>" \
  --body "<next steps from the note, plus a pointer to the vault note path>" \
  --label "agent:hermes,status:ready,scope:personal,priority:p2"
```

- `agent:hermes` for async/scheduled/browser work, `agent:claude` for the
  next Claude Code session, `agent:any` if either can take it
- A scope label (`scope:work` / `scope:personal` / `scope:ai-toolkit`) is
  mandatory
- `status:blocked` if the follow-up is waiting on something; say what

## Notes

- The vault note is the handoff artifact. Do not rely on auto-memory or
  conversation context to carry state to the next session; auto-memory is
  for ephemeral context only.
- Terse and factual beats comprehensive. A note the next session actually
  reads is worth more than an exhaustive report.
