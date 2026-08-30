#!/usr/bin/env python3
"""
Render MCP server config for BOTH Claude Code surfaces from one manifest.

Source of truth: claude/mcp-servers-template.json (this repo). Placeholders are
resolved at render time, so no secret ever lives in the repo:
  __GH_TOKEN__               <- `gh auth token` (system keyring)
  __NOTION_PERSONAL_TOKEN__  <- ~/.claude/secrets.json
  __NOTION_WORK_TOKEN__      <- ~/.claude/secrets.json
Leading `~` in commands/args/env values expands to the local home directory.

Targets (both machine-local, never committed):
  Mac app: ~/Library/Application Support/Claude/claude_desktop_config.json
           (app updates wipe mcpServers; rerun this after any update)
  CLI:     ~/.claude.json (user scope; only the mcpServers key is touched,
           everything else in that file is preserved)

claude.ai connectors (Lucid, gws-mcp, Pulse, ...) are NOT covered: those are
OAuth'd interactively per surface and cannot be scripted.

Verify with: claude mcp list  (ground truth, per the vault note)

Usage:
  python3 claude/restore-mcp-config.py            # both targets
  python3 claude/restore-mcp-config.py --app-only
  python3 claude/restore-mcp-config.py --cli-only
"""

import json
import os
import shutil
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(REPO_DIR, "mcp-servers-template.json")
APP_CONFIG_PATH = os.path.expanduser(
    "~/Library/Application Support/Claude/claude_desktop_config.json"
)
CLI_CONFIG_PATH = os.path.expanduser("~/.claude.json")
SECRETS_PATH = os.path.expanduser("~/.claude/secrets.json")


def load_secrets():
    if not os.path.exists(SECRETS_PATH):
        print(f"ERROR: secrets file not found at {SECRETS_PATH}")
        print("Create it with:")
        print('  {"notion_personal": "ntn_...", "notion_work": "ntn_..."}')
        sys.exit(1)
    with open(SECRETS_PATH) as f:
        return json.load(f)


def get_gh_token():
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception as e:
        print(f"ERROR: could not get GitHub token from gh CLI: {e}")
        sys.exit(1)


def resolve(value, replacements):
    if isinstance(value, str):
        for k, v in replacements.items():
            value = value.replace(k, v)
        if value.startswith("~/"):
            value = os.path.expanduser(value)
        return value
    if isinstance(value, list):
        return [resolve(v, replacements) for v in value]
    if isinstance(value, dict):
        return {k: resolve(v, replacements) for k, v in value.items()}
    return value


def render_servers():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    replacements = {"__GH_TOKEN__": get_gh_token()}
    secrets = load_secrets()
    replacements["__NOTION_PERSONAL_TOKEN__"] = secrets["notion_personal"]
    replacements["__NOTION_WORK_TOKEN__"] = secrets["notion_work"]
    return resolve(manifest, replacements)


def update_json_file(path, servers, label):
    """Replace only the mcpServers key, preserving everything else."""
    config = {}
    if os.path.exists(path):
        shutil.copy2(path, path + ".bak")
        with open(path) as f:
            config = json.load(f)
    config["mcpServers"] = servers
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(config, f, indent=2)
    os.replace(tmp, path)
    print(f"{label}: wrote {len(servers)} servers -> {path}")


def main():
    args = set(sys.argv[1:])
    do_app = "--cli-only" not in args
    do_cli = "--app-only" not in args

    servers = render_servers()

    if do_app:
        os.makedirs(os.path.dirname(APP_CONFIG_PATH), exist_ok=True)
        update_json_file(APP_CONFIG_PATH, servers, "Mac app")
    if do_cli:
        update_json_file(CLI_CONFIG_PATH, servers, "CLI")

    print("\nServers: " + ", ".join(servers))
    if do_app:
        print("Restart the Claude Code app to reconnect.")
    if do_cli:
        print("Verify CLI with: claude mcp list")


if __name__ == "__main__":
    main()
