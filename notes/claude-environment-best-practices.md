# Claude Environment Best Practices

Captured from working session 2026-06-06. Reference before setting up new projects or auditing existing ones.

## The three-layer memory model

| Layer | File | Scope | When read |
|-------|------|-------|-----------|
| Behavioral instructions | `CLAUDE.md` (global + project) | Always active | Every turn |
| Durable knowledge | Obsidian vault `_ai/` | Cross-project | On demand |
| Ephemeral context | `~/.claude/projects/*/memory/` | Per-project | On demand |

Never conflate these. Don't put facts Claude can read from code into CLAUDE.md. Don't put behavioral rules into the vault.

## CLAUDE.md hierarchy

- **Global** (`~/.claude/CLAUDE.md`): identity, surface preferences, behavioral rules, cross-project conventions
- **Project** (`<repo>/CLAUDE.md`): what this project IS, decisions already made, what never to do here, vault backpointer
- **Subdir** (optional): specialized context for a subsystem (e.g., frontend vs backend)

Each layer should add something the others don't. No duplication. Project CLAUDEs should answer:
1. What is this project trying to accomplish?
2. What architectural/design decisions are already settled?
3. What should Claude never do in this codebase?
4. Where is durable context stored (vault backpointer)?

Keep global CLAUDE.md under ~150 lines -- everything past that is read less reliably.

## Vault backpointer rule

Whenever a vault note is created or updated for a project, add or update a `## Vault Note` section in that project's `CLAUDE.md`:

```markdown
## Vault Note

Durable context for this project is in the Obsidian vault at `_ai/<folder>/<file>.md`.
Check it at the start of any new session for data model details, file locations, and prior decisions.
```

This is baked into the vault skill (step 5) and the global CLAUDE.md.

## Skill design principles

- Skills encode **judgment + steps**, not just steps. Explain the *why* behind each step so Claude can adapt.
- The **description field IS the trigger** -- invest in it. Run the skill-creator description optimizer on every skill you care about.
- **Bundle scripts** that subagents keep reinventing. If 3 eval runs all wrote the same helper script, it belongs in `scripts/` inside the skill.
- Skills should handle multi-step workflows. One-liners don't need skills.

## Hooks for automation

Memory and CLAUDE.md instructions rely on Claude reading and applying them. Hooks execute deterministically. Use `update-config` skill to wire up:

- **Stop hook**: push notification summarizing what changed (already have push notifs enabled -- just needs the hook)
- **Pre-session hook**: check vault/memory at start of known project sessions

## Feedback capture habit

The memory system is only as good as what gets written into it. At the end of any non-trivial task, ask:

> "What was non-obvious here?"

That surfaces: unexpected behavior, decisions that required reasoning, patterns that will recur. These become feedback memories. Run `consolidate-memory` monthly to merge duplicates and prune stale entries.

## Hermes vs Claude Code routing criteria

| Factor | Claude Code | Hermes |
|--------|-------------|--------|
| Timing | Synchronous, right now | Async, can wait |
| Human in loop | Yes, interactive | No, fire-and-forget |
| File/IDE access needed | Yes | No (or via MCP) |
| Recurring/scheduled | No | Yes |
| Heavy tool use | Yes | Light preferred |

Document routing criteria explicitly so neither agent picks up the wrong work.

## Eval loop for skills

Iterating skills based on feel only works at small scale. The skill-creator eval loop gives quantitative signal:
1. Write 2-3 realistic test prompts
2. Run with-skill vs baseline in parallel
3. Grade assertions, view in browser reviewer
4. Improve skill, repeat

Run description optimizer *after* the skill content is stable.

## Checklist for new project setup

- [ ] Create `<client>/CLAUDE.md` with purpose, decisions, vault backpointer section
- [ ] Create vault note at `_ai/clients/<code>.md` with data model, file locations, quirks
- [ ] Confirm vault backpointer in CLAUDE.md points to correct vault path
- [ ] Add project to vault `_ai/index.md`

## Checklist for skill audit

- [ ] Run description optimizer on every active skill
- [ ] Check that skills bundle any scripts subagents kept reinventing
- [ ] Verify skill descriptions include both "what" and "when" context
