---
name: media
description: Umbrella skill for media-related tools and workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---
# Media Skills Umbrella

This skill serves as an umbrella for various media-related tools and workflows, including GIF search, audio generation, spectrogram analysis, Spotify integration, and YouTube content processing.

## Subskills

- **gif-search**: Search/download GIFs from Tenor via curl + jq.
- **heartmula**: HeartMuLa: Suno-like song generation from lyrics + tags.
- **songsee**: Audio spectrograms/features (mel, chroma, MFCC) via CLI.
- **spotify**: Spotify: play, search, queue, manage playlists and devices.
- **youtube-content**: YouTube transcripts to summaries, threads, blogs.

Each subskill has its own detailed documentation. Use `skill_view(<subskill-name>)` to see specific instructions.

## Usage

When working with media tasks, load this skill to access the relevant subskills. The umbrella skill provides guidance on choosing the right subskill for your media workflow.