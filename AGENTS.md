# ai-toolkit contributor guidance

This repository owns portable agent instructions, tools and configuration. Keep project-specific rules in their project repositories. Preserve unrelated local edits.

## Local commit security

Use the Gitleaks hook in `.pre-commit-config.yaml` before each local commit. Install Gitleaks on PATH and install the Git hook with `pre-commit install` in each checkout. It scans the staged Git index, redacts values and blocks on findings or scanner failure. Do not bypass a failing scan to complete a commit. Keep tests tracked; ignore generated artifacts instead.

When applying this pattern elsewhere, merge the hook into the existing pre-commit configuration and preserve existing hooks. Local hooks complement CI history scanning. Investigate findings before adding exceptions; use verified, narrowly scoped historical fingerprints rather than excluding whole documents or test directories.

## Vault Note

The reusable setup and verification procedure is in the Obsidian vault at `Codex/ai-toolkit/Gitleaks Pre-Commit Pattern.md`. The vault root and pointer are documented in `notes/README.md`.

Leave commits local unless Matt asks you to push. Do not include unrelated changes in a commit.
