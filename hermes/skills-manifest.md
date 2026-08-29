# Hermes skills: what's versioned here vs reinstallable

Audited 2026-08-28. `~/.hermes/skills/` is not a plain folder: Hermes manages it with a
skill hub (`.hub/` - installs, taps, content hashes, quarantine) and a curator that
periodically consolidates per-skill dirs into class-level umbrella skills and prunes
stale ones into `.archive/`.

## Versioned in this repo (authored / curator-built)

The 21 umbrella skill dirs in `skills/` plus `backlog-protocol.md` and `seedream.md`.
These exist nowhere else and are the part that must survive the eject test. setup.sh
symlinks each into `~/.hermes/skills/`, so curator edits land in this repo's working
tree - review them with `git diff` and commit or revert deliberately.

## NOT versioned (reinstallable, runtime-managed)

- **Bundled skills**: ship with Hermes itself, tracked in `~/.hermes/skills/.bundled_manifest`
  (name:hash lines). `dogfood/` and `software-development/plan` were bundled at audit
  time; `plan` rides along inside the versioned software-development umbrella, which is
  harmless.
- **Hub-installed skills**: tracked in `~/.hermes/skills/.hub/lock.json`. At audit time:
  creative/creative-ideation, gaming/minecraft-modpack-server, gaming/pokemon-player,
  mlops/research/dspy. Note the curator has since consolidated some of these paths into
  umbrellas, so lock.json entries can be stale.
- **Runtime state**: `.usage.json`, `.curator_state`, `.bundled_manifest`, `.hub/`,
  `.archive/`, `.curator_backups/`. Never commit these.
- **Empty category stubs**: diagramming/, domain/, gifs/, inference-sh/ (DESCRIPTION.md
  only, no SKILL.md) - left live-only.

## Migration record (2026-08-28)

Live dirs were moved to `~/.hermes/skills/.pre-toolkit-backup/` (not deleted) and
replaced with symlinks into this repo. If Hermes misbehaves, restoring is
`rm <symlink> && mv .pre-toolkit-backup/<dir> <dir>`. Delete the backup folder once
Hermes has run cleanly for a while.

The old `kellmat74/hermes-skills` GitHub repo is a stale 2026-06-02 snapshot of the
pre-consolidation library (95 per-skill dirs plus runtime state files) and is
superseded by this repo.

## New machine checklist

1. `./setup.sh` (symlinks the versioned skills)
2. Install Hermes; bundled skills come with it
3. Reinstall hub skills per `.hub/lock.json` wants (or skip; they were barely used)
