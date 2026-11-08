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
codex/         # Codex skills and a non-overwriting skill-link installer
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

## Local commit secret scanning

The root [.pre-commit-config.yaml](.pre-commit-config.yaml) is a reusable blocking Gitleaks hook and is enabled for this repository after installation:

```sh
brew install gitleaks
pip install pre-commit
pre-commit install
pre-commit run gitleaks --all-files
```

This hook always scans staged changes, including when invoked with `--all-files`. Findings and scanner errors block commits; matched values are redacted. Copy the hook into another project's existing `repos` list without replacing its other checks. Install the hook in each checkout and keep CI history scanning enabled. Repository hooks do not automatically protect every repository on the machine.

The durable rationale, false-positive handling and verification recipe live in the vault at `Codex/ai-toolkit/Gitleaks Pre-Commit Pattern.md`; see [the vault pointer](notes/README.md). Contributor guidance is in [AGENTS.md](AGENTS.md).

## Development lessons across projects

The [development-lessons skill](codex/skills/development-lessons/SKILL.md) retrieves the vault playbook for new apps and substantial workflow/data changes. It selects applicable lessons instead of imposing one architecture on every project. The feedback register distinguishes current verified fixes from historical reports and includes source locators, prevention checks and coverage limits. See [the vault pointers](notes/README.md).

`./setup.sh` installs toolkit Codex skills and the existing Claude/Hermes skill links. For Codex-only setup, run `./codex/install-skills.sh`; its optional first argument chooses a destination directory. It leaves conflicting existing installations unchanged and returns a failure so they can be reviewed. The same canonical skill is shared with Claude and Hermes. Start a new session or refresh skill discovery if an already-running app has not picked it up. This adds knowledge retrieval, not an automatic exhaustive audit or a guarantee that an AI will load every lesson for every task.
