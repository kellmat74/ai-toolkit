# Global Claude Code instructions (personal)

This file is symlinked to ~/.claude/CLAUDE.md by setup.sh, so it applies to every
Claude Code session on this machine (regardless of project).

## About me
Senior engineer at VisiQuate. Healthcare RCM domain. I work across data, infra, and
agentic tooling. I use Claude Code and Hermes as parallel agents - Claude Code for
synchronous in-IDE work, Hermes for async/scheduled work.

Hermes is an open-source autonomous agent by Nous Research (hermes-agent.org),
self-hosted and running locally on this Mac. It has full shell access and machine
access -- not cloud-sandboxed. 40+ built-in skills, cron scheduling, parallel
sub-agents, browser control, sandboxed code execution. Uses SKILL.md format
(agentskills.io compatible). Does NOT natively support MCP. Connects via
Telegram, Slack, Discord, WhatsApp, Signal, or CLI.

## My Claude Code surface
**Primary: the Claude Code Mac app (GUI), not the CLI terminal.**
When giving me instructions, default to GUI-flavored guidance:
- "Start a new session" means File menu / Cmd+N / `+` button, not `claude` in a terminal
- "Switch projects" means picking a different working directory in the app, not `cd`
- Multiple parallel sessions are normal (one per tab/window)
- Push notifications work and are enabled (`agentPushNotifEnabled: true`)

Remote Control is enabled by default, so every session is also reachable from the
iOS/Android Claude app for on-the-go work. Treat the mobile surface as secondary:
good for review, comments, light prompts, and filing backlog tickets; not for
heavy tool-driven work. The Mac has to stay awake for the remote session to stay
live (10-minute network outage timeout).

Underlying mechanics (cwd, project CLAUDE.md, `~/.claude/`, symlinks from
ai-toolkit) are identical to CLI. Stdio MCP servers are also identical on both
surfaces: `claude/restore-mcp-config.py` renders them from one manifest
(`claude/mcp-servers-template.json`) into both surfaces' config files, and
setup.sh runs it. The one remaining difference: claude.ai connectors (Lucid,
gws-mcp, Pulse, ...) need a one-time interactive OAuth per surface and may be
missing on a surface where that hasn't been done. `claude mcp list` is ground
truth.

## Memory and notes
Long-form notes live in my personal Obsidian vault:
`~/Library/CloudStorage/GoogleDrive-kellmat74@gmail.com/My Drive/Obsidian-Personal/Obsidian Vault/`

Per-project notes go under that vault's relevant folder.
Auto-memory (your `~/.claude/projects/*/memory/`) is fine for ephemeral conversational
context, but durable knowledge belongs in the Obsidian vault or as a committed skill.

### Vault backpointer rule
Whenever you create or update a vault note for a project, you MUST also add (or update)
a `## Vault Note` section in that project's CLAUDE.md pointing to it. Format:

```markdown
## Vault Note

Durable context for this project is in the Obsidian vault at `_ai/<folder>/<file>.md`.
Check it at the start of any new session for data model details, file locations, and prior decisions.
```

This ensures any future session opening that project directory finds the vault note immediately,
without having to reason about whether one might exist.

## Backlog
My AI Agent Team works from GitHub Issues at `kellmat74/agent-backlog`.
Routing labels: `agent:claude`, `agent:hermes`, `agent:any`.
Status labels: `status:ready`, `status:in-progress`, `status:blocked`, `status:needs-review`.
Scope labels: `scope:work` (VisiQuate client/internal), `scope:personal` (personal projects), `scope:ai-toolkit` (agent infrastructure, spans both).
Priority labels: `priority:p0` (drop everything), `priority:p1` (this week), `priority:p2` (whenever there's slack).
Always apply a scope label when filing an issue.
When you finish something tied to an issue, close it with a comment summarizing what changed.

## Conventions I prefer
- Be terse. Don't summarize work I can see in the diff.
- No emdashes in output, minimal emoji (organization policy).
- Don't add comments that just restate what the code does.
- For exploratory questions, give a recommendation + the main tradeoff, then wait.
- Before destructive ops (force push, hard reset, deleting branches), confirm.
- For ambiguous tasks, ask 1-2 sharp clarifying questions before diving in.

## Before automating a new login/scraping target
When a new project needs to log into or scrape an unfamiliar site (payer
portal, vendor dashboard, etc.), do a quick recon pass before writing any
scraper code:
- Check response headers/cookies on the login page for known bot-detection
  signatures: a `CF-RAY` header means Cloudflare, `_abck` cookie means Akamai,
  a bare 429 with no body means Kasada. Also scan the page source for inline
  fingerprinting script calls (e.g. a subdomain like `rba.*` or `fp.*` loaded
  on page load) -- a giveaway even without a matching header/cookie pattern.
- If bot detection shows up, don't spend a session iterating on selectors to
  fight it -- stealth patches only fix fingerprint-level signals
  (`navigator.webdriver`, missing plugins), not IP reputation, TLS
  fingerprinting, or behavioral analysis. Plan up front for a one-time manual
  login (real browser, real human timing) that saves a reusable session
  (Playwright `storage_state` or equivalent) instead of scripting login itself.
- If nothing shows up, proceed with normal scripted login, but still expect
  the first real attempt to reveal surprises -- 2FA variance between
  otherwise-identical accounts, MFA methods that differ per account, lazy-
  rendered content that beats `networkidle`. Budget time for it; don't assume
  the first mapped flow generalizes to every account.

Learned the hard way on `portal-access-verification` (SURG UHC scraper,
2026-08-06): several rounds of otherwise-correct selector fixes went by
before recognizing the real blocker was fraud detection, not a wrong
selector. A five-minute header check up front would have caught it immediately.

**Whenever a human is going to interact with the target live anyway (real
credentials, MFA, a manual login step), use `playwright codegen` instead of
writing selectors by hand and iterating on tracebacks.** It opens a real
browser, and every click/fill the human does gets turned into working code
automatically:
```
playwright codegen --target python -o /tmp/recording.py <url>
```
Have them do the whole thing in that one recording -- login, MFA, navigating
to whatever needs to be scraped -- then read the generated file directly for
real selectors instead of a debug-dump-and-patch loop. Still worth
sanity-checking anything flaky (elements needing dismissal, hidden duplicate
buttons, etc.) against what codegen recorded rather than copying it blindly,
but it replaces nearly all of the trial-and-error.

Learned the hard way on the same project's Cigna scraper (2026-08-08): spent
a full session iterating selectors through login/MFA one traceback at a time
before the user pointed out codegen would have recorded the entire flow in
one pass. Reach for it from the start whenever a live human walkthrough is
already required, not just as a fallback after manual debugging stalls.

## Portability
Anything durable about how I work with agents should live in `~/git/personal/ai-toolkit`,
not in conversation memory. If you discover a generalizable skill, propose adding it as
a file in that repo.

## Vault Note

Durable context for this project is in the Obsidian vault at `_ai/ai-toolkit/agent-architecture.md`.
Check it at the start of any new session for agent roles, coordination patterns, GitHub access setup, and open design questions.

That note also covers **what does and does not carry across the two Claude Code surfaces**
(Mac app vs CLI). Short version: CLAUDE.md, settings.json, and skills are shared via
symlink; **MCP servers are not**, and the CLI currently has none. A skill that calls an
MCP tool may work in the app and silently fail in the CLI. It also flags an unresolved
question about whether the Forge GCP project and a throwaway OAuth project are the same
project, which must be checked before deleting either.

Claude Code tooling config patterns: `_ai/workflow/claude-code-mcp-config.md` -- covers where MCP
config actually lives per surface (`~/.claude.json` and `claude_desktop_config.json`, **never**
`settings.json`), remote-server OAuth including the dynamic-client-registration failure and the
bring-your-own-client fix, Google Workspace access state for both accounts, and the Sheets API's
inability to touch uploaded `.xlsx` files.

**Read that note before touching any MCP or Google Sheets config.** Two separate multi-hour
detours (2026-06-07, 2026-08-09) came from config that looked correct but was in a file
Claude Code does not read. `claude mcp list` is the ground truth for whether a server exists.
