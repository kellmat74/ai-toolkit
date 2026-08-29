---
name: review-code
description: Multi-perspective code review combining code-quality and security passes. Use when asked to review a diff, PR, branch, or specific files - especially before a merge or when the change touches auth, data handling, or external input.
---

# Review Code

## Trigger
`/review-code [diff | PR | branch | file/path]`. With no argument, review the current
diff (`git diff` against the merge base, or staged changes if nothing is unstaged).

## Scope

1. Determine what's under review: `git diff`, a PR (`gh pr diff <n>`), a branch, or
   explicit paths.
2. Decide review depth from what changed:
   - Touches auth, secrets, external input, data storage, or PHI-adjacent code (this is
     healthcare RCM work - assume patient/claims data is sensitive by default) -> run
     both passes below.
   - Everything else (docs, tests, small internal refactors) -> code-reviewer pass only.

## Workflow

1. Spawn `code-reviewer` (Task tool) with the diff/files in scope. It reads only -
   quality, readability, duplication, error handling, test coverage.
2. If security-relevant (see above), spawn `security-auditor` in parallel with the same
   scope. Independent passes, not sequential - they're not supposed to see each other's
   findings before reporting.
3. Wait for both, then merge into one report.

Don't do the review yourself in the main context - delegate to the subagents even for a
small diff. They're read-only and cheap; the point is the fresh, focused pass, not
saving a tool call.

## Merging findings

Combine both agents' output into one severity-ordered report:

```
CODE REVIEW: <scope>

CRITICAL (must fix before merge)
- [security-auditor] file:line - vulnerability, impact, fix
- [code-reviewer] file:line - issue, why it matters, fix

WARNING / HIGH
...

SUGGESTION / MEDIUM+LOW
...

ASSESSMENT: pass | pass with warnings | blocked on critical findings
```

Dedup if both agents flag the same line - keep the more specific finding, note both
perspectives caught it.

## Persistence

This is a stateless review by default - don't invent a knowledge-base call, there isn't
one. If the review surfaces something durable (a recurring anti-pattern in this repo, a
convention worth writing down, a lesson that would save time next time), say so and
propose saving it - either as feedback/project memory (auto-memory, this conversation)
or, if it's cross-project and durable, via the `vault` skill into the Obsidian vault.
Don't write to the vault automatically; ask first, per normal vault-skill behavior.

## Notes

- `code-reviewer` and `security-auditor` (`claude/agents/`) are both read-only
  (Glob/Grep/Read only, no Edit/Write) on purpose - a reviewer that can rewrite the code
  it's critiquing isn't a review. If a finding needs fixing, that's a separate step the
  user or main session does after reading the report.
- Keep the two passes independent. If you're tempted to have code-reviewer also do
  security, or vice versa, don't - overlapping scope produces overlapping, shallower
  findings instead of two real perspectives.
