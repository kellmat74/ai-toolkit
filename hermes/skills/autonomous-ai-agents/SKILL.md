---
name: autonomous-ai-agents
description: "Umbrella skill for autonomous AI agent tools and workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Autonomous AI Agents Umbrella

This skill consolidates various autonomous AI agent tools into a single class-level umbrella.

## Subskills

- **codex**: Delegate coding to OpenAI Codex CLI (features, PRs)
- **hermes-agent**: Configure, extend, or contribute to Hermes Agent
- **kanban-codex-lane**: Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementation lane while Hermes keeps ownership of task lifecycle, reconciliation, testing, and handoff
- **opencode**: Delegate coding to OpenCode CLI (features, PR review)

Each subskill retains its own documentation and usage instructions. Refer to the individual skill details for specific commands and workflows.