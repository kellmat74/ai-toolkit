# Prompts

Reusable personas and system prompts. Each `.md` file is one prompt with frontmatter
describing when to use it.

Example:
```markdown
---
name: pr-reviewer
description: Code review focused on correctness, security, simplicity
intended_for: [claude-code, hermes]
---

You are reviewing a pull request. ...
```

Both Claude Code and Hermes can read these directly. Skills are the preferred long-term
home for repeatable behavior; prompts here are for ad-hoc reuse before something gets
promoted to a skill.
