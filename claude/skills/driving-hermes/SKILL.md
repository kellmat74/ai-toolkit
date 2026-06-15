---
name: driving-hermes
description: How Claude Code invokes and directs the local Hermes agent from the shell. Use when asked to run something through Hermes, test a Hermes skill, send Hermes a task, inspect a Hermes session, or hand work off to Hermes for async/scheduled execution.
---

# Driving Hermes from Claude Code

Hermes is a self-hosted autonomous agent running locally on this Mac (see global
CLAUDE.md). Claude Code drives it through the `hermes` CLI. This skill captures the
non-obvious mechanics so you don't rediscover them.

## Mental model

- The **gateway** runs as a long-lived background process (`hermes gateway run`),
  connected to Discord. It handles inbound messages and cron. Don't kill it.
- A `hermes -z "..."` invocation spins up a **separate one-shot agent process**.
  It does NOT talk to the running gateway; it's its own session.
- Config is symlinked: `~/.hermes/config.yaml -> <repo>/hermes/config.yaml`.
- The OpenRouter API key lives in `~/.hermes/.env`, NOT in the shell environment.
  `hermes auth list` shows `env:OPENROUTER_API_KEY`; `hermes auth status openrouter`
  may say "logged out" because the shell var is unset. That's expected.

## One-shot invocation (the common case)

```bash
hermes --cli --skills <repo>/hermes/skills -z "your instruction here"
```

- `--cli` forces CLI mode instead of the TUI.
- `--skills <dir>` loads skills from a path. Point it at `hermes/skills` in the
  repo so Hermes can see project skills (e.g. `seedream`, `backlog-protocol`).
- `-z "..."` is the one-shot prompt.

**Output behavior (important):** Hermes buffers its output and only flushes when
the run COMPLETES. You will NOT see streaming progress. So:
- Run it as a **background task** (`run_in_background: true`) and read the result
  when you get the completion notification. Don't poll an empty log and assume it
  hung; a real agentic run can take several minutes.
- Capture with `... 2>&1 | tee /tmp/hermes_run.log` so the final transcript lands
  in a file you can read.

## Approval gates

- Hermes config has `approvals.mode: manual`. Most actions need approval.
- `shell command via -c/-lc flag` and `script execution via -e/-c flag` are on the
  `command_allowlist`, so skills that run shell/Python proceed without prompting.
- **Do NOT reach for `--yolo`.** It disables Hermes's approval gates entirely, and
  Claude Code's auto-mode classifier will block launching a non-sandboxed agent
  that way unless the user has explicitly authorized bypass mode. Run without it;
  the allowlist usually covers what a skill needs.

## Inspecting what Hermes did

```bash
hermes sessions list                 # recent sessions with IDs + previews
hermes sessions export <SESSION_ID>  # (note: dumps into cwd; clean up after)
tail -f ~/.hermes/logs/gateway.log   # live gateway activity (Discord, cron)
hermes auth list                     # configured provider credentials
hermes status                        # component health
```

## Pushing a message to a Hermes channel

To send into a configured platform (Discord, etc.) rather than spawn an agent:

```bash
hermes send <platform> "message"     # e.g. for scripts / cron / CI
```

## Direct API calls on this machine (TLS gotcha)

If you (or a Hermes skill) call an HTTPS API directly, TLS is intercepted on this
Mac (Tirith). Plain urllib/curl with default certs fails the handshake and can
return misleading errors (including spurious 404s). Verify against the Hermes CA
bundle:

```
~/.hermes/certs/combined_ca_bundle.pem
```

Python: `ssl.create_default_context(cafile=...)`. curl: `--cacert <bundle>`.

## Don't confuse the two skill systems

- **Hermes skills** live in `hermes/skills/*.md` (single-file, with a `metadata.hermes`
  frontmatter block). They teach *Hermes* how to do something.
- **Claude Code skills** (like this one) live in `claude/skills/<name>/SKILL.md` and
  teach *Claude Code*. setup.sh symlinks each into `~/.claude/skills/`.

## Asking Hermes to remember something

There's no CLI to inject a memory directly. Drive a session and tell it to save the
note: `hermes --cli -z "Save a durable memory note: <text>. Confirm you saved it."`
Note Hermes has a security filter that redacts certain literal strings (e.g. the
literal `~/.hermes/.env` path) from memory; phrase durable notes descriptively
("the Hermes config directory") rather than with blocked literals.
