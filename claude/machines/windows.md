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

## Not installed here
Hermes (the `-Hermes` switch on `setup.ps1` links it when wanted). Codex skills are skipped.
Full setup history: `AI Toolkit Personal PC Runbook.md` at the vault root.
