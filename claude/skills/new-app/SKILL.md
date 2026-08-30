---
name: new-app
description: Start a new app-shaped personal project from the buildermethods/build-new template (Rails 8 + Inertia + React). Use when Matt says "new app", "new project", "start building X", or "spin up an app". Not for data pipelines, scrapers, or agent tooling (those stay Python), and not for howlers-peak.
---

# New App from build-new

Bootstraps a new app-shaped project from `buildermethods/build-new` with the
no-human-review guardrails wired in from commit one. Standing decision and rationale:
`_ai/personal/greenfield-stack.md` in the vault.

## 0. Confirm scope

App-shaped means a product with UI and users. If the request is a pipeline, scraper,
script, or agent tool, this skill does not apply; use Python and stop here.

Ask for (or confirm) the app name if not obvious. Derive: kebab-case repo/dir name,
CamelCase Rails module name, snake_case database prefix.

## 1. Clone and take ownership

```bash
gh repo clone buildermethods/build-new <app-name> -- --depth 1
cd <app-name>
rm -rf .git && git init -b main
```

The template is a snapshot: after cloning, the code is fully owned; no upstream
updates flow in.

Rename the app identity from BuildNew: `config/application.rb` (module name),
`config/database.yml` (db names), `package.json` name, and grep for remaining
`build_new`/`BuildNew`/`build-new` references and rename them all.

## 2. Setup and verify

```bash
bin/setup      # gems, db create/migrate/seed
npm install
```

Machine notes (Tirith):
- Ruby comes from mise (3.3.6 global). Postgres 16 runs as a Homebrew service.
- TLS interception: bundler is already configured globally against
  `~/.hermes/certs/combined_ca_bundle.pem`. If a plain `gem` command or Ruby
  net/http hits `CertificateFailureError`, set
  `SSL_CERT_FILE=~/.hermes/certs/combined_ca_bundle.pem`.

Verify before proceeding:

```bash
bin/rails runner 'puts "boot ok, users: #{User.count}"'
```

Then `bin/dev` (Rails :3000 + Vite :3036) if Matt wants to see it.

## 3. Wire the guardrails (before any feature work)

Matt does not review code. These substitute for review; wire them now, not later:

1. Edit the template's `AGENTS.md`: keep its conventions, add a "Merge bar" section:
   run the review-code skill (code-reviewer + security-auditor) before any merge;
   run the security-audit skill before anything touching auth or payments ships;
   green CI is the merge bar, no exceptions for "unrelated" failures.
2. Create the project `CLAUDE.md` pointing at `AGENTS.md` plus anything
   Claude-specific.
3. Confirm the template's CI workflows (tests, type-check, lint, security scan) are
   intact under `.github/workflows/`.

## 4. Repo and first commit

Ask before creating the GitHub repo (outward-facing):

```bash
gh repo create kellmat74/<app-name> --private --source . --push
```

First commit = pristine template + renames + guardrails, BEFORE any feature work,
so the diff of every later change is legible.

## 5. Vault note and backpointer

Create `_ai/<app-name>/project.md` in the vault (purpose, data model sketch, key
decisions) and add the `## Vault Note` backpointer section to the project CLAUDE.md
per the global rule. Add the note to `_ai/index.md`.

## 6. Backlog

If the app has known milestones, offer to decompose them into
`kellmat74/agent-backlog` issues via the plan-sprint skill (scope:personal).

## Deployment (when asked, not by default)

Managed hosting only: Render or Fly. Not self-hosted Kamal. Set it up when there is
something worth deploying, not at bootstrap.
