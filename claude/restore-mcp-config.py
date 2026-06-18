#!/usr/bin/env python3
"""
Restore mcpServers in claude_desktop_config.json after a Claude Code app update wipes it.

App updates delete the mcpServers block but preserve preferences. Run this after any update,
then restart the Claude Code app.

Tokens:
  - GitHub: pulled live from `gh auth token` (system keyring, no hardcoded value)
  - Notion: stored in ~/.claude/secrets.json (not committed to repo)

Usage:
  python3 claude/restore-mcp-config.py
"""

import json
import os
import subprocess
import sys

CONFIG_PATH = os.path.expanduser(
    "~/Library/Application Support/Claude/claude_desktop_config.json"
)
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


def main():
    secrets = load_secrets()
    gh_token = get_gh_token()

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    if "mcpServers" in config:
        print("mcpServers already present -- overwriting anyway.")

    config["mcpServers"] = {
        "drawio": {
            "command": "npx",
            "args": ["-y", "@drawio/mcp"]
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": gh_token
            }
        },
        "notion-personal": {
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {
                "NOTION_TOKEN": secrets["notion_personal"]
            }
        },
        "notion-work": {
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {
                "NOTION_TOKEN": secrets["notion_work"]
            }
        },
        "analytics-mcp": {
            "command": "/Users/matt.kelley/.local/bin/uvx",
            "args": ["analytics-mcp"],
            "env": {
                "GOOGLE_APPLICATION_CREDENTIALS": "/Users/matt.kelley/Documents/keys/ga4-mcp.json",
                "GOOGLE_PROJECT_ID": "the-forge-498316"
            }
        }
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print("Restored mcpServers:")
    for name in config["mcpServers"]:
        print(f"  - {name}")
    print("\nRestart the Claude Code app to reconnect.")


if __name__ == "__main__":
    main()
