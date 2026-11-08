# Machine: work Mac (VisiQuate-managed)

Loaded by the shared `claude/CLAUDE.md` through `~/.claude/machine.md`, which `setup.sh`
links to this file on macOS. Everything here is true only on the Mac. Work-flavored
context lives here on purpose so the personal Windows PC never loads it.

## About me (work context)
Senior engineer at VisiQuate. Healthcare RCM domain. I work across data, infra, and
agentic tooling.

Hermes runs locally on this Mac, self-hosted, with full shell access and machine
access -- not cloud-sandboxed. 40+ built-in skills, cron scheduling, parallel
sub-agents, browser control, sandboxed code execution. Connects via Telegram, Slack,
Discord, WhatsApp, Signal, or CLI.

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

## Vault path
If `VAULT_PATH` is unset, the vault root on this Mac is:
`~/Library/CloudStorage/GoogleDrive-kellmat74@gmail.com/My Drive/Obsidian-Personal/Obsidian Vault/`

## Backlog scope labels (work)
`scope:work` (VisiQuate client/internal). Use it for work tickets; the shared file lists the
other scope labels.

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
