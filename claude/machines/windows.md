# Machine: personal Windows PC

Loaded by the shared `claude/CLAUDE.md` through `~/.claude/machine.md`, which `setup.ps1`
links to this file. Everything here is true only on this PC.

## Scope of this machine
Personal projects and the ai-toolkit only. No VisiQuate client data, no patient data, no
PHI, and nothing copied from work accounts or work drives ever belongs here. If a file
looks like client or patient data, stop and tell me.

## My Claude Code surface
**Primary: the Claude desktop app for Windows (Code tab), not a terminal CLI.**
Default to GUI-flavored guidance:
- "Start a new session" means the new-session control in the app, not `claude` in a terminal
- "Switch projects" means picking a different working directory in the app, not `cd`
- Underlying mechanics (`%USERPROFILE%\.claude`, symlinks from ai-toolkit) match the Mac

Shell notes:
- Run `setup.ps1` with PowerShell 7 (`pwsh`). Windows PowerShell 5.1 cannot create
  unprivileged symlinks even with Developer Mode on.
- Git Bash is installed but not on PATH. Claude Code finds it itself.
- Keep the toolkit repo under `%USERPROFILE%`, not on the Google Drive path.
- Clone with `core.symlinks=true`, or tracked symlinks land as plain text files.

## Vault path
`VAULT_PATH` is set as a user environment variable to
`G:\My Drive\Obsidian-Personal\Obsidian Vault`. The vault agents (Glob, Grep, Read only)
cannot read environment variables, so pass the vault root in their prompt.

## MCP on this PC
Only `github` is rendered here. Re-render with the Claude app closed:
`python claude\restore-mcp-config.py --only github`. The script is strict: it refuses to
write anything if a selected server cannot resolve. claude.ai connectors need their own
one-time sign-in on this machine. Check with the app's connector status, or `claude mcp
list` if a CLI is installed.

## Hermes on this PC
Installed (v0.23.0 stable) at `%LOCALAPPDATA%\hermes`, with `hermes` on the User PATH. It runs
on its own config and skills: `setup.ps1 -Hermes` has NOT been run, because the repo's Hermes
config comes from an older Hermes (the Mac runs v0.16.0) and some skill names collide with the
installer's own. API keys are added by hand to `%LOCALAPPDATA%\hermes\.env`. Do not link
the repo's Hermes config here without a plan.

Provider: OpenRouter, on FREE models by choice (set with `hermes config set`, the Windows
config is not linked to the repo): main `nvidia/nemotron-3-ultra-550b-a55b:free`, auxiliary
`openrouter/free`, `auxiliary.free_only: true`. Free slugs get retired (the Nemotron Super
free slug was); when a 404 "unavailable for free" appears, pick a new one from
`https://openrouter.ai/api/v1/models` (pricing 0, supports tools). Free routes may log
prompts, so no private data. Backup of the earlier config: `config.yaml.bak-before-free-models`.
Discord is connected (own bot, gateway log shows it connecting). The
gateway auto-starts at login through a Startup folder login item
(`Startup\Hermes_Gateway.vbs`), NOT a Scheduled Task: `hermes gateway install` fell back
to it because the UAC prompt was skipped. Remove it with `hermes gateway uninstall`. The
Mac is not running Hermes at the moment, so this PC is the only Discord host.

## Not installed here
Codex skills are skipped.
Full setup history: `AI Toolkit Personal PC Runbook.md` at the vault root.
