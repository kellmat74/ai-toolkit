# Notes

Durable notes live in the personal Obsidian vault, not here:
```
~/Library/CloudStorage/GoogleDrive-kellmat74@gmail.com/My Drive/Obsidian-Personal/Obsidian Vault/
```

This directory is intentionally near-empty. Anything written here should be either:
- A pointer to a vault note (with the path)
- Toolkit-internal docs that don't belong in the vault (e.g. `notes/decisions/` for
  agent-architecture decisions worth committing alongside the code)

## Gitleaks pre-commit pattern

Vault note: `Codex/ai-toolkit/Gitleaks Pre-Commit Pattern.md` beneath the vault root above.

Reusable implementation: [root pre-commit configuration](../.pre-commit-config.yaml). This repository retains the implementation and agent guidance; the explanatory note lives in the vault.

## Reusable development lessons

Vault notes under `Codex/ai-toolkit/`:

- `Development Lessons and Review Playbook.md`: applicability-aware checklist for new apps and substantial changes.
- `Development Feedback Register.md`: stable lesson IDs, evidence, prevention checks and historical/current confidence.
- `Conversation Review Coverage.md`: sources, paging, deduplication and unreviewed-history limits.

Portable entry point: [development-lessons skill](../codex/skills/development-lessons/SKILL.md). The notes remain in the vault; they are not duplicated here.
