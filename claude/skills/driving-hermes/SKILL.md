---
name: driving-hermes
description: How Claude Code invokes and directs the local Hermes agent from the shell (macOS and Windows). Use when asked to run something through Hermes, test a Hermes skill, send Hermes a task, inspect a Hermes session, or hand work off to Hermes for async/scheduled execution.
---

# Driving Hermes from Claude Code

Hermes is a self-hosted autonomous agent running locally (see global CLAUDE.md).
Claude Code drives it through the `hermes` CLI. Check which machine you are on first:
the machine file (`~/.claude/machine.md`) says, and the per-OS sections below differ.

## Mental model (both machines)

- The **gateway** (`hermes gateway run`) is a long-lived background process that
  handles inbound platform messages and cron. A `hermes -z "..."` invocation spins up a
  **separate one-shot agent process**; it does NOT talk to the running gateway.
- Provider API keys live in the Hermes `.env`, NOT in the shell environment.
  `hermes auth list` shows them; `hermes auth status <provider>` may say "logged out"
  because the shell var is unset. That is expected.
- With no provider key configured, `hermes -z` cannot run an agent turn.
  `hermes status` shows "Providers: none connected" in that case. Check it first.

## Where things live

| | macOS (v0.16) | Windows (v0.23) |
|---|---|---|
| Hermes home | `~/.hermes` | `%LOCALAPPDATA%\hermes` |
| Config | symlink to `<repo>/hermes/config.yaml` | its own `config.yaml`, NOT linked to the repo |
| Keys | `~/.hermes/.env` | `%LOCALAPPDATA%\hermes\.env` |
| Logs | `~/.hermes/logs` | `%LOCALAPPDATA%\hermes\logs` (`agent.log`, `errors.log`, `gateway.log`, `gui.log`) |
| Repo skills via `--skills <dir>` | works | does NOT work (see below) |
| TLS interception (Tirith) | yes, needs CA bundle | no, no bundle exists |

## One-shot invocation

```bash
hermes --cli -z "your instruction here"
```

- `--cli` forces the classic REPL instead of the TUI. `-z "..."` is the one-shot prompt.
- **`--skills` changed between versions.** On v0.16 (Mac) it takes a directory:
  `--skills <repo>/hermes/skills`. On v0.23 (Windows) it takes skill NAMES to preload
  (`-s name1,name2`) and a directory fails immediately with `Error: unknown_skill`
  (verified). To make repo skills visible on Windows, add the repo directory to
  `skills.external_dirs` in the Windows `config.yaml` (read-only external dirs, local
  skills win on name collisions). This is untested, and repo skills that declare
  `platforms: [macos]` (for example `seedream`) will likely be filtered out on Windows.
- Do not link the repo's Hermes config on Windows: it comes from the older Hermes and
  some skill names collide with the installer's own.

**Output behavior (important):** Hermes buffers its output and only flushes when the
run COMPLETES. You will NOT see streaming progress. So run it as a **background task**
(`run_in_background: true`), read the result on the completion notification, and do not
poll an empty log and assume it hung. A real agentic run can take several minutes.

Capture the transcript to a file:
- macOS (bash): `hermes --cli -z "..." 2>&1 | tee /tmp/hermes_run.log`
- Windows (PowerShell tool): `hermes --cli -z "..." 2>&1 | Tee-Object -FilePath "$env:TEMP\hermes_run.log"`
  (or a path in the session scratchpad). Do not use `/tmp` on Windows.

## Windows shell notes

- `hermes` lives in `%LOCALAPPDATA%\hermes\bin` on the User PATH. A Claude app session
  that started before the install does not see it. Refresh PATH per call:
  `$env:Path = [Environment]::GetEnvironmentVariable('Path','User') + ';' + [Environment]::GetEnvironmentVariable('Path','Machine')`
  or restart the app once.
- Use the PowerShell tool for `hermes` commands. Git Bash is not on PATH.
- Python-based Hermes tooling here runs on its own bundled interpreter (3.14), so do not
  assume the system `python`.

## Gateway and dashboard on Windows

- The gateway can start itself: opening the dashboard's chat/TUI auto-starts it as
  `gateway run --quiet --idle-exit` (log: "Auto-started gateway: exits after 600s with
  no clients, adapters, cron/kanban work"). It shows as "manual run", not a service.
  That is expected and not a stray process. No Scheduled Task is created.
- Check: `hermes gateway status`. `hermes gateway stop` is documented as stopping the
  *service*; whether it also stops a manual or auto-started run is UNVERIFIED on
  Windows. After running it, confirm with `hermes gateway status` and, if needed, stop
  the process by PID (`gateway-exit-diag.log` in the logs dir records it).
- Dashboard (port 9119): `hermes dashboard --no-open`, `hermes dashboard --status`,
  `hermes dashboard --stop`.
- If you do want it persistent, `hermes gateway install` would add a service. Do not
  run that without the user asking.

## Approval gates

- Hermes config has `approvals.mode: manual` on the Mac. Most actions need approval.
  `shell command via -c/-lc flag` and `script execution via -e/-c flag` are on the
  `command_allowlist`, so skills that run shell/Python proceed without prompting.
  Verify the Windows `config.yaml` before assuming the same allowlist exists there.
- **Do NOT reach for `--yolo`.** It disables Hermes's approval gates entirely, and
  Claude Code's auto-mode classifier will block launching a non-sandboxed agent that way
  unless the user has explicitly authorized bypass mode.

## Inspecting what Hermes did

```bash
hermes sessions list                 # recent sessions with IDs + previews
hermes sessions export <SESSION_ID>  # dumps into cwd; clean up after
hermes auth list                     # configured provider credentials
hermes status                        # component health (providers, platforms, jobs, gateway)
hermes doctor                        # config and dependency check
```

Live logs: macOS `tail -f ~/.hermes/logs/gateway.log`. Windows
`Get-Content "$env:LOCALAPPDATA\hermes\logs\gateway.log" -Wait -Tail 20`.

## Pushing a message to a Hermes channel

To send into a configured platform (Discord, etc.) rather than spawn an agent:

```bash
hermes send <platform> "message"     # e.g. for scripts / cron / CI
```

Needs a configured platform. None is configured on the Windows PC yet.

## Direct API calls (macOS TLS gotcha)

On the Mac, TLS is intercepted (Tirith). Plain urllib/curl with default certs fails the
handshake and can return misleading errors (including spurious 404s). Verify against the
Hermes CA bundle `~/.hermes/certs/combined_ca_bundle.pem`. Python:
`ssl.create_default_context(cafile=...)`. curl: `--cacert <bundle>`. This does not apply
on the Windows PC.

## Don't confuse the two skill systems

- **Hermes skills** live in `hermes/skills/*.md` in the repo (single-file, with a
  `metadata.hermes` frontmatter block). They teach *Hermes* how to do something. Hermes
  v0.23 installs its own skills as `<category>/<name>/SKILL.md` directories.
- **Claude Code skills** (like this one) live in `claude/skills/<name>/SKILL.md` and
  teach *Claude Code*. `setup.sh` / `setup.ps1` symlink each into `~/.claude/skills/`.

## Asking Hermes to remember something

There's no CLI to inject a memory directly. Drive a session and tell it to save the
note: `hermes --cli -z "Save a durable memory note: <text>. Confirm you saved it."`
Hermes has a security filter that redacts certain literal strings (for example the
literal path of its `.env` file) from memory; phrase durable notes descriptively ("the
Hermes config directory") rather than with blocked literals.
