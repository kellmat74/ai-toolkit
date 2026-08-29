---
name: software-development
description: Umbrella skill for software-development tools and workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---
# Software Development Skills Umbrella

This skill serves as an umbrella for various software-development tools and workflows, including debugging, planning, code review, and more.

## Subskills

- **computer-use-vision-adaptation**: Adapt computer use techniques based on whether the model supports vision input.
- **debugging-hermes-tui-commands**: Debug Hermes TUI slash commands: Python, gateway, Ink UI.
- **hermes-agent-skill-authoring**: Author in-repo SKILL.md: frontmatter, validator, structure.
- **hermes-s6-container-supervision**: Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
- **macos-network-troubleshooting**: Diagnose network connectivity issues on macOS — DNS, VPN, proxy, and firewall problems. Especially relevant when corporate MDM-managed VPN clients (Cloudflare WARP, Zscaler, etc.) interfere with API access.
- **node-inspect-debugger**: Debug Node.js via --inspect + Chrome DevTools Protocol CLI.
- **plan**: Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. Bite-sized tasks, exact paths, complete code.
- **python-debugpy**: Debug Python: pdb REPL + debugpy remote (DAP).
- **requesting-code-review**: Pre-commit review: security scan, quality gates, auto-fix.
- **simplify-code**: Parallel 3-agent cleanup of recent code changes.
- **spike**: Throwaway experiments to validate an idea before build.
- **subagent-driven-development**: Execute plans via delegate_task subagents (2-stage review).
- **systematic-debugging**: 4-phase root cause debugging: understand bugs before fixing.
- **test-driven-development**: TDD: enforce RED-GREEN-REFACTOR, tests before code.
- **writing-plans**: Write implementation plans: bite-sized tasks, paths, code.

Each subskill has its own detailed documentation. Use `skill_view(<subskill-name>)` to see specific instructions.

## Usage

When working with software-development tasks, load this skill to access the relevant subskills. The umbrella skill provides guidance on choosing the right subskill for your software-development workflow.