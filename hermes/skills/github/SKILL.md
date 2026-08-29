---
name: github
description: "GitHub workflow tools and utilities"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# GitHub Workflow Umbrella

This skill provides a collection of tools and workflows for interacting with GitHub, including repository management, pull request workflows, issue tracking, and authentication.

## Subskills

- **github-auth**: GitHub authentication setup (HTTPS tokens, SSH keys, gh CLI login)
- **github-code-review**: Review pull requests: diffs, inline comments via gh or REST
- **github-issues**: Create, triage, label, assign GitHub issues via gh or REST
- **github-pr-workflow**: GitHub PR lifecycle: branch, commit, open, CI, merge
- **github-repo-management**: Clone/create/fork repos; manage remotes, releases
- **codebase-inspection**: Inspect codebases with pygount: LOC, languages, ratios

Each subskill retains its own documentation and usage instructions. Refer to the individual skill details for specific commands and workflows.