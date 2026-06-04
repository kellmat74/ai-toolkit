# ai-toolkit

Personal, portable AI agent toolchain. Owns the durable parts of my "AI Agent Team":
custom skills, agents, slash commands, MCP configs, prompts, and a backlog system that
multiple agents (Claude Code, Hermes) can work from.

This repo is the source of truth. `~/.claude/` and `~/.hermes/` on any machine are just
symlinks into this repo plus per-machine secrets in `.env` files (never committed).

## Eject test
On any new machine:
```bash
git clone git@github.com:kellmat74/ai-toolkit.git ~/git/personal/ai-toolkit
cd ~/git/personal/ai-toolkit
./setup.sh
# then populate ~/.claude/.env and ~/.hermes/.env from .env.example
```
Should be enough to bring the full team back online.

## Layout
```
claude/        # Claude Code: CLAUDE.md, settings.json, skills/, agents/, commands/
hermes/        # Hermes Agent: config.yaml, skills/
backlog/       # markdown-based backlog (fallback; GitHub Issues is primary - see backlog/README.md)
prompts/       # reusable personas and system prompts
notes/         # pointers to the Obsidian vault (don't duplicate notes here)
```

## What's NOT in this repo (by design)
- API keys, tokens, secrets - those live in `~/.claude/.env` and `~/.hermes/.env`
- Auto-memory files from `~/.claude/projects/*/memory/` - conversational scratchpad, machine-local
- Work-specific project CLAUDE.md files - those belong in the work repos themselves

## Backlog
The team works from `kellmat74/agent-backlog` (GitHub Issues). See `backlog/README.md`
for the routing/labeling conventions.
