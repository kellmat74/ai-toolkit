# ai-toolkit contributor guidance

This repository owns portable agent instructions, tools and configuration. Keep project-specific rules in their project repositories. Preserve unrelated local edits.

## Local commit security

Use the Gitleaks hook in `.pre-commit-config.yaml` before each local commit. Install Gitleaks on PATH and install the Git hook with `pre-commit install` in each checkout. It scans the staged Git index, redacts values and blocks on findings or scanner failure. Do not bypass a failing scan to complete a commit. Keep tests tracked; ignore generated artifacts instead.

When applying this pattern elsewhere, merge the hook into the existing pre-commit configuration and preserve existing hooks. Local hooks complement CI history scanning. Investigate findings before adding exceptions; use verified, narrowly scoped historical fingerprints rather than excluding whole documents or test directories.

## Reusable development feedback

For new apps or substantial data/workflow changes, use the `development-lessons` skill and read the relevant vault checklist before choosing the design. Apply only lessons that match the task; old client rules and old release choices do not become universal requirements. Preserve the user's stack, current repository rules and authorization boundaries. Confirmed findings should become scoped prevention checks rather than blanket approval flows.

## Vault Note

The reusable setup and verification procedure is in the Obsidian vault at `Codex/ai-toolkit/Gitleaks Pre-Commit Pattern.md`. The vault root and pointer are documented in `notes/README.md`.

Leave commits local unless Matt asks you to push. Do not include unrelated changes in a commit.

Development playbook: `Codex/ai-toolkit/Development Lessons and Review Playbook.md` in the vault. Evidence and source coverage: `Development Feedback Register.md` and `Conversation Review Coverage.md` in the same folder. The skill's canonical source is `codex/skills/development-lessons/SKILL.md`; toolkit setup installs it for Codex and exposes the same skill through Claude/Hermes links. These files preserve reusable lessons with historical/current confidence labels; they do not claim complete access to every conversation.
