# Global Claude Code instructions (personal)

This file is symlinked to ~/.claude/CLAUDE.md by setup.sh (macOS) and setup.ps1 (Windows),
so it applies to every Claude Code session on the machine (regardless of project). It is
the NEUTRAL part. Facts that are true only on one machine live in
`claude/machines/<machine>.md`, which the setup script links to `~/.claude/machine.md`
and this file imports at the bottom.

## About me
I work across data, infra, and agentic tooling. I use Claude Code and Hermes as parallel
agents - Claude Code for synchronous in-IDE work, Hermes for async/scheduled work.

Hermes is an open-source autonomous agent by Nous Research (hermes-agent.org),
self-hosted, with full shell access and machine access -- not cloud-sandboxed. 40+
built-in skills, cron scheduling, parallel sub-agents, browser control, sandboxed code
execution. Uses SKILL.md format (agentskills.io compatible). Does NOT natively support MCP.
Connects via Telegram, Slack, Discord, WhatsApp, Signal, or CLI. Where it is installed is
in the machine file.

## My Claude Code surface
I use the Claude Code desktop app (GUI) rather than the CLI terminal, on each machine. The
machine file says which app and how to phrase instructions.

Underlying mechanics (cwd, project CLAUDE.md, `~/.claude/`, symlinks from
ai-toolkit) are identical to CLI. Stdio MCP servers are also identical on both
surfaces: `claude/restore-mcp-config.py` renders them from one manifest
(`claude/mcp-servers-template.json`) into both surfaces' config files. The one
remaining difference: claude.ai connectors (Lucid, gws-mcp, Pulse, ...) need a
one-time interactive OAuth per surface and may be missing on a surface where that
hasn't been done. `claude mcp list` is ground truth.

## Memory and notes
Long-form notes live in my personal Obsidian vault. The root is the `VAULT_PATH`
environment variable (each machine sets its own). If it is unset, the machine file gives
the default path.

Per-project notes go under that vault's relevant folder.
Auto-memory (your `~/.claude/projects/*/memory/`) is fine for ephemeral conversational
context, but durable knowledge belongs in the Obsidian vault or as a committed skill.

### Vault backpointer rule
Whenever you create or update a vault note for a project, you MUST also add (or update)
a `## Vault Note` section in that project's CLAUDE.md pointing to it. Format:

```markdown
## Vault Note

Durable context for this project is in the Obsidian vault at `_ai/<folder>/<file>.md`.
Check it at the start of any new session for data model details, file locations, and prior decisions.
```

This ensures any future session opening that project directory finds the vault note immediately,
without having to reason about whether one might exist.

## Backlog
My AI Agent Team works from GitHub Issues at `kellmat74/agent-backlog`.
Routing labels: `agent:claude`, `agent:hermes`, `agent:any`.
Status labels: `status:ready`, `status:in-progress`, `status:blocked`, `status:needs-review`.
Scope labels: `scope:personal` (personal projects), `scope:ai-toolkit` (agent infrastructure, spans both). The machine file may list more.
Priority labels: `priority:p0` (drop everything), `priority:p1` (this week), `priority:p2` (whenever there's slack).
Always apply a scope label when filing an issue.
When you finish something tied to an issue, close it with a comment summarizing what changed.

## Conventions I prefer
- Be terse. Don't summarize work I can see in the diff.
- No emdashes in output, minimal emoji (organization policy).
- Don't add comments that just restate what the code does.
- For exploratory questions, give a recommendation + the main tradeoff, then wait.
- Before destructive ops (force push, hard reset, deleting branches), confirm.
- For ambiguous tasks, ask 1-2 sharp clarifying questions before diving in.

## New app-shaped personal projects
Start from the **buildermethods/build-new** template (Rails 8 + Inertia + React 19,
Postgres-for-everything). I don't review code; agents do all coding. That makes these
non-negotiable: run the review-code skill before any merge, security-audit before
anything touching auth or payments ships, green CI is the merge bar, managed hosting
(Render/Fly) over self-hosted. Full rationale and toolchain state:
`_ai/personal/greenfield-stack.md` in the vault. Does not apply to howlers-peak
(stays Supabase + Next.js) or data/infra work (stays Python).

## Reusable development feedback

For new apps or substantial data/workflow changes, use the `development-lessons` skill and read the relevant vault checklist before choosing the design. Apply only lessons that match the task; old client rules and old release choices do not become universal requirements. Preserve the user's stack, current repository rules and authorization boundaries. Confirmed findings should become scoped prevention checks rather than blanket approval flows.

## Local commit secret scanning

Before each local commit, use the repository's blocking Gitleaks staged scan. The reusable hook is `ai-toolkit/.pre-commit-config.yaml`; when setting up a repository, merge it into the existing configuration, preserve other checks, install Gitleaks on PATH and run `pre-commit install` in that checkout. Run `pre-commit run gitleaks --all-files` to check the staged index. Findings or a missing scanner must block the commit; redact matched values and fix the cause instead of bypassing the hook. Keep tests in Git and ignore generated outputs. Local hooks complement CI history scanning and can be bypassed, so they are not a replacement for CI.

Investigate false positives against actual source bytes before adding an exception. Prefer exact historical finding fingerprints and formats that distinguish checksums from credential assignments. Never exclude an entire document or test directory merely to silence a scan.

## Portability
Anything durable about how I work with agents should live in `~/git/personal/ai-toolkit`,
not in conversation memory. If you discover a generalizable skill, propose adding it as
a file in that repo. Machine-specific facts go in `claude/machines/<machine>.md`, not here.

## Vault Note

Durable context for this project is in the Obsidian vault at `_ai/ai-toolkit/agent-architecture.md`.
Check it at the start of any new session for agent roles, coordination patterns, GitHub access setup, and open design questions.

That note also covers how the setup works on each machine (macOS `setup.sh`, Windows
`setup.ps1`) and what does and does not carry across the two Claude Code surfaces.
It also flags an unresolved question about whether the Forge GCP project and a throwaway
OAuth project are the same project, which must be checked before deleting either. The
Windows procedure and results are in `AI Toolkit Personal PC Runbook.md` at the vault root.

Claude Code tooling config patterns: `_ai/workflow/claude-code-mcp-config.md` -- covers where MCP
config actually lives per surface (`~/.claude.json` and `claude_desktop_config.json`, **never**
`settings.json`), remote-server OAuth including the dynamic-client-registration failure and the
bring-your-own-client fix, Google Workspace access state for both accounts, and the Sheets API's
inability to touch uploaded `.xlsx` files.

**Read that note before touching any MCP or Google Sheets config.** Two separate multi-hour
detours (2026-06-07, 2026-08-09) came from config that looked correct but was in a file
Claude Code does not read. `claude mcp list` is the ground truth for whether a server exists.

Reusable local commit security pattern: `Codex/ai-toolkit/Gitleaks Pre-Commit Pattern.md` in the vault. Covers setup, staged-only semantics, redaction, missing-scanner failure and narrow false-positive handling. The portable hook lives in this repository's root `.pre-commit-config.yaml`.

Development playbook: `Codex/ai-toolkit/Development Lessons and Review Playbook.md` in the vault. Evidence and source coverage: `Development Feedback Register.md` and `Conversation Review Coverage.md` in the same folder. The skill's canonical source is `codex/skills/development-lessons/SKILL.md`; toolkit setup installs it for Codex and exposes the same skill through Claude/Hermes links. These files preserve reusable lessons with historical/current confidence labels; they do not claim complete access to every conversation.

## Machine-specific instructions
@~/.claude/machine.md
