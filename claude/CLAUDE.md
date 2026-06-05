# Global Claude Code instructions (personal)

This file is symlinked to ~/.claude/CLAUDE.md by setup.sh, so it applies to every
Claude Code session on this machine (regardless of project).

## About me
Senior engineer at VisiQuate. Healthcare RCM domain. I work across data, infra, and
agentic tooling. I use Claude Code and Hermes as parallel agents - Claude Code for
synchronous in-IDE work, Hermes for async/scheduled work.

## My Claude Code surface
**Primary: the Claude Code Mac app (GUI), not the CLI terminal.**
When giving me instructions, default to GUI-flavored guidance:
- "Start a new session" means File menu / Cmd+N / `+` button, not `claude` in a terminal
- "Switch projects" means picking a different working directory in the app, not `cd`
- Multiple parallel sessions are normal (one per tab/window)
- Push notifications work and are enabled (`agentPushNotifEnabled: true`)

Remote Control is enabled by default, so every session is also reachable from the
iOS/Android Claude app for on-the-go work. Treat the mobile surface as secondary:
good for review, comments, light prompts, and filing backlog tickets; not for
heavy tool-driven work. The Mac has to stay awake for the remote session to stay
live (10-minute network outage timeout).

Underlying mechanics (cwd, project CLAUDE.md, `~/.claude/`, symlinks from
ai-toolkit) are identical to CLI. Only the UI differs.

## Memory and notes
Long-form notes live in my personal Obsidian vault:
`~/Library/CloudStorage/GoogleDrive-kellmat74@gmail.com/My Drive/Obsidian-Personal/Obsidian Vault/`

Per-project notes go under that vault's relevant folder.
Auto-memory (your `~/.claude/projects/*/memory/`) is fine for ephemeral conversational
context, but durable knowledge belongs in the Obsidian vault or as a committed skill.

## Backlog
My AI Agent Team works from GitHub Issues at `kellmat74/agent-backlog`.
Routing labels: `agent:claude`, `agent:hermes`, `agent:any`.
Status labels: `status:ready`, `status:in-progress`, `status:blocked`, `status:needs-review`.
When you finish something tied to an issue, close it with a comment summarizing what changed.

## Conventions I prefer
- Be terse. Don't summarize work I can see in the diff.
- No emdashes in output, minimal emoji (organization policy).
- Don't add comments that just restate what the code does.
- For exploratory questions, give a recommendation + the main tradeoff, then wait.
- Before destructive ops (force push, hard reset, deleting branches), confirm.
- For ambiguous tasks, ask 1-2 sharp clarifying questions before diving in.

## Portability
Anything durable about how I work with agents should live in `~/git/personal/ai-toolkit`,
not in conversation memory. If you discover a generalizable skill, propose adding it as
a file in that repo.
