#!/usr/bin/env python3
"""
Render MCP server config for BOTH Claude Code surfaces from one manifest.

Source of truth: claude/mcp-servers-template.json (this repo). Placeholders are
resolved at render time, so no secret ever lives in the repo:
  __GH_TOKEN__               <- `gh auth token` (system keyring)
  __NOTION_PERSONAL_TOKEN__  <- ~/.claude/secrets.json  ("notion_personal")
  __NOTION_WORK_TOKEN__      <- ~/.claude/secrets.json  ("notion_work")
Leading `~` in commands/args/env values expands to the local home directory.

A server whose placeholders cannot be resolved (for example no notion_work key
on a personal machine) is SKIPPED with a printed note, not a crash.

Targets (both machine-local, never committed):
  macOS app:   ~/Library/Application Support/Claude/claude_desktop_config.json
  Windows app: %APPDATA%\\Claude\\claude_desktop_config.json
               (app updates can wipe mcpServers; rerun this after any update)
  CLI:         ~/.claude.json (user scope; only the mcpServers key is touched,
               everything else in that file is preserved)

Windows notes: `npx` is a .cmd shim that desktop apps often fail to spawn
directly, so npx servers are written as `cmd /c npx ...` (use --no-cmd-wrap to
disable). A Unix-only `~/.local/bin/<tool>` command is rewritten to the bare
tool name so it resolves from PATH.

claude.ai connectors (Lucid, gws-mcp, Pulse, ...) are NOT covered: those are
OAuth'd interactively per surface and cannot be scripted.

Close the Claude app before running this: a running app can overwrite
~/.claude.json with its in-memory copy and drop the new mcpServers block.

Usage:
  python restore-mcp-config.py                    # both targets, all servers
  python restore-mcp-config.py --app-only
  python restore-mcp-config.py --cli-only
  python restore-mcp-config.py --only github,drawio
  python restore-mcp-config.py --skip notion-work
  python restore-mcp-config.py --dry-run          # show plan, write nothing
"""

import json
import os
import re
import shutil
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(REPO_DIR, "mcp-servers-template.json")
CLI_CONFIG_PATH = os.path.expanduser("~/.claude.json")
SECRETS_PATH = os.path.expanduser("~/.claude/secrets.json")
PLACEHOLDER_RE = re.compile(r"__[A-Z0-9_]+__")
IS_WINDOWS = sys.platform == "win32"


def app_config_path():
    if sys.platform == "darwin":
        return os.path.expanduser(
            "~/Library/Application Support/Claude/claude_desktop_config.json"
        )
    if IS_WINDOWS:
        appdata = os.environ.get("APPDATA") or os.path.expanduser("~/AppData/Roaming")
        return os.path.join(appdata, "Claude", "claude_desktop_config.json")
    return os.path.expanduser("~/.config/Claude/claude_desktop_config.json")


APP_CONFIG_PATH = app_config_path()


def load_secrets():
    """Return the secrets dict, or {} if the file is absent."""
    if not os.path.exists(SECRETS_PATH):
        print(f"note: no secrets file at {SECRETS_PATH}; servers needing secrets are skipped")
        return {}
    with open(SECRETS_PATH) as f:
        return json.load(f)


def get_gh_token():
    """Return the gh token, or None if gh is missing or not logged in."""
    try:
        token = subprocess.check_output(
            ["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        return token or None
    except Exception:
        return None


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


def placeholders_in(value):
    if isinstance(value, str):
        return set(PLACEHOLDER_RE.findall(value))
    if isinstance(value, list):
        return set().union(*[placeholders_in(v) for v in value]) if value else set()
    if isinstance(value, dict):
        return set().union(*[placeholders_in(v) for v in value.values()]) if value else set()
    return set()


def adapt_for_platform(server, wrap_npx):
    """Apply Windows-only command fixes. macOS/Linux entries pass through unchanged."""
    if not IS_WINDOWS:
        return server
    server = dict(server)
    cmd = server.get("command", "")
    base = os.path.basename(cmd.replace("\\", "/"))
    if cmd.startswith("~/.local/bin/") or cmd.replace("\\", "/").startswith(
        os.path.expanduser("~").replace("\\", "/") + "/.local/bin/"
    ):
        cmd = base
        server["command"] = cmd
    if wrap_npx and cmd == "npx":
        server["command"] = "cmd"
        server["args"] = ["/c", "npx"] + list(server.get("args", []))
    return server


def parse_list_flag(argv, flag):
    for i, a in enumerate(argv):
        if a == flag and i + 1 < len(argv):
            return {s.strip() for s in argv[i + 1].split(",") if s.strip()}
        if a.startswith(flag + "="):
            return {s.strip() for s in a.split("=", 1)[1].split(",") if s.strip()}
    return None


def render_servers(argv):
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    only = parse_list_flag(argv, "--only")
    skip = parse_list_flag(argv, "--skip") or set()
    wrap_npx = "--no-cmd-wrap" not in argv

    secrets = load_secrets()
    available = {}
    gh = get_gh_token()
    if gh:
        available["__GH_TOKEN__"] = gh
    if secrets.get("notion_personal"):
        available["__NOTION_PERSONAL_TOKEN__"] = secrets["notion_personal"]
    if secrets.get("notion_work"):
        available["__NOTION_WORK_TOKEN__"] = secrets["notion_work"]

    servers, skipped = {}, []
    for name, entry in manifest.items():
        if only is not None and name not in only:
            continue
        if name in skip:
            skipped.append((name, "excluded by --skip"))
            continue
        missing = placeholders_in(entry) - set(available)
        if missing:
            skipped.append((name, "missing " + ", ".join(sorted(missing))))
            continue
        servers[name] = adapt_for_platform(resolve(entry, available), wrap_npx)

    if only is not None:
        unknown = only - set(manifest)
        for name in sorted(unknown):
            skipped.append((name, "not in manifest"))

    return servers, skipped


def update_json_file(path, servers, label, dry_run):
    """Replace only the mcpServers key, preserving everything else."""
    if dry_run:
        print(f"{label}: would write {len(servers)} servers -> {path}")
        return
    config = {}
    if os.path.exists(path):
        shutil.copy2(path, path + ".bak")
        with open(path) as f:
            config = json.load(f)
    config["mcpServers"] = servers
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(config, f, indent=2)
    os.replace(tmp, path)
    print(f"{label}: wrote {len(servers)} servers -> {path}")


def main():
    argv = sys.argv[1:]
    args = set(argv)
    do_app = "--cli-only" not in args
    do_cli = "--app-only" not in args
    dry_run = "--dry-run" in args

    servers, skipped = render_servers(argv)

    if not servers:
        print("ERROR: no servers to write (everything skipped or filtered out).")
        for name, why in skipped:
            print(f"  skipped {name}: {why}")
        sys.exit(1)

    app_label = {"darwin": "Mac app", "win32": "Windows app"}.get(sys.platform, "App")
    if do_app:
        update_json_file(APP_CONFIG_PATH, servers, app_label, dry_run)
    if do_cli:
        update_json_file(CLI_CONFIG_PATH, servers, "CLI", dry_run)

    print("\nServers: " + ", ".join(servers))
    for name, why in skipped:
        print(f"Skipped {name}: {why}")
    if dry_run:
        print("\n(dry run: nothing was written; secrets are never printed)")
        return
    if do_app:
        print("Restart the Claude app to reconnect.")
    if do_cli:
        print("Verify CLI with: claude mcp list")


if __name__ == "__main__":
    main()
