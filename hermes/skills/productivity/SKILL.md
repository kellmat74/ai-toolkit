---
name: productivity
description: Umbrella skill for productivity tools and workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---
# Productivity Skills Umbrella

This skill serves as an umbrella for various productivity tools and workflows, including Airtable, Google Workspace, Linear, Maps, PDF editing, Notion, OCR, PowerPoint, and Teams meeting pipeline.

## Subskills

- **airtable**: Airtable REST API via curl. Records CRUD, filters, upserts.
- **google-workspace**: Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python.
- **linear**: Linear: manage issues, projects, teams via GraphQL + curl.
- **maps**: Geocode, POIs, routes, timezones via OpenStreetMap/OSRM.
- **nano-pdf**: Edit PDF text/typos/titles via nano-pdf CLI (NL prompts).
- **notion**: Notion API + ntn CLI: pages, databases, markdown, Workers.
- **ocr-and-documents**: Extract text from PDFs/scans (pymupdf, marker-pdf).
- **powerpoint**: Create, read, edit .pptx decks, slides, notes, templates.
- **teams-meeting-pipeline**: Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions.

Each subskill has its own detailed documentation. Use `skill_view(<subskill-name>)` to see specific instructions.

## Usage

When working with productivity tasks, load this skill to access the relevant subskills. The umbrella skill provides guidance on choosing the right subskill for your productivity workflow.