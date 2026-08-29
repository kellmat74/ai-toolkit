---
name: research
description: Umbrella skill for research-related tools and workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---
# Research Skills Umbrella

This skill serves as an umbrella for various research-related tools and workflows, including arXiv search, blog monitoring, LLM wiki, Polymarket data, and research paper writing.

## Subskills

- **arxiv**: Search arXiv papers by keyword, author, category, or ID.
- **blogwatcher**: Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool.
- **llm-wiki**: Karpathy's LLM Wiki: build/query interlinked markdown KB.
- **polymarket**: Query Polymarket: markets, prices, orderbooks, history.
- **research-paper-writing**: Write ML papers for NeurIPS/ICML/ICLR: design→submit.

Each subskill has its own detailed documentation. Use `skill_view(<subskill-name>)` to see specific instructions.

## Usage

When working with research tasks, load this skill to access the relevant subskills. The umbrella skill provides guidance on choosing the right subskill for your research workflow.